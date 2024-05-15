"""
Shared memory is composed by: trailer_nbytes(64bits) + put_counter(64bits) + next_put_counter(64bits) + circular_data + trailer(pickled)

We put pickled infos in a trailer instead of a header, because the size of pickled bytes can not be multiple of 64 bits. In this case, we have to add padding between header and counter.
If we put pickled header at the end, no paddin is needed because all others data (header_size, counter, circular_data) are multiple of 64 bits and then memory aligned.
"""

import os
import pickle

import numpy as np
from sferriol.python.dictionary import adict

from .file_lock import Write_File_Lock
from .shared_memory import PosixSharedMemory as SharedMemory

_NAME_PREFIX = "scb."

# Infos of all header items (position slice, size in bytes) stored inside the shared memory
shm_header_struct = adict(
    trailer_nbytes=adict(slice=slice(0, 8), nbytes=8),
    put_counter=adict(slice=slice(8, 16), nbytes=8),
    next_put_counter=adict(slice=slice(16, 24), nbytes=8),
)
shm_header_struct_nbytes = sum([d.nbytes for d in shm_header_struct.values()])


def _to_shape(s):
    return (s,) if isinstance(s, int) else s


def exists(name):
    return SharedMemory.exists(_NAME_PREFIX + name)


def list_buffers(prefix):
    """Return 'running' shared circular buffers whose name starts with prefix"""
    ret = list()
    for fname in os.listdir("/dev/shm"):
        if fname.startswith(_NAME_PREFIX + prefix):
            ret.append(fname.split(_NAME_PREFIX)[1])
    return ret


def np_size(capacity, shape, dtype):
    """Returns the size in bytes used in buffer by the numpy data
    capacity: Buffer length = number of numpy arrays
    shape: Shape of the numpy array
    dtype: Data type the numpy array
    """
    return capacity * shape_size(shape) * np.dtype(dtype).itemsize


def shape_size(shape):
    """Returns the number of elements in a array according to its shape"""
    shape = _to_shape(shape)
    size = 1
    for i in shape:
        size = size * i
    return size


def unlink_buffer(name):
    try:
        fpath = os.path.join("/dev/shm", _NAME_PREFIX + name)
        os.remove(fpath)
    except FileNotFoundError:
        pass


class _Common:

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.close()

    def _exists(self):
        return SharedMemory.exists(self.shm_name)

    def _build_shm_np(self):
        header = shm_header_struct
        header_nbytes = shm_header_struct_nbytes
        np_nbytes = np_size(self.capacity, self.shape, self.dtype)
        np_slice = slice(header_nbytes, header_nbytes + np_nbytes)
        return np.ndarray(
            _to_shape(self.capacity) + _to_shape(self.shape),
            dtype=self.dtype,
            buffer=self._shm.buf[np_slice],
        )

    @property
    def next_put_counter(self):
        return int.from_bytes(
            self._shm.buf[shm_header_struct.next_put_counter.slice], byteorder="big"
        )

    @property
    def put_counter(self):
        return int.from_bytes(
            self._shm.buf[shm_header_struct.put_counter.slice], byteorder="big"
        )

    @property
    def shm_name(self):
        return _NAME_PREFIX + self.name


class Reader(_Common):
    def __init__(self, name: str, counter: int = None):
        self.name = name

        # test if it exists
        if not self._exists():
            raise OSError(f"Circular buffer ({name}): not found")

        self._shm = self._build_shm()
        self._init_from_shm()
        self.shm_np = self._build_shm_np()

        self.get_counter = counter if counter is not None else self.put_counter

    def _build_shm(self):
        return SharedMemory(name=_NAME_PREFIX + self.name, create=False, read_only=True)

    def _check_next_put_counter(self):
        # read next_put_counter only once (like a snapshot)
        next_put_counter = self.next_put_counter

        # check writer has not reseted the circular buffer
        if next_put_counter < self.get_counter:
            raise ValueError("Circular buffer has been reseted")

        # check writer has not loop the circular buffer and overwritten reader data
        if next_put_counter >= (self.get_counter + self.capacity):
            raise OverflowError("Overwrited data by writer, reader is too slow")

    def _get(self):
        array = self.shm_np[self.get_counter % self.capacity]
        return np.copy(array)

    def _init_from_shm(self):
        header = shm_header_struct
        trailer_nbytes = int.from_bytes(
            self._shm.buf[header.trailer_nbytes.slice], byteorder="big"
        )
        trailer = pickle.loads(self._shm.buf[-trailer_nbytes:])
        self.capacity = trailer["capacity"]
        self.dtype = trailer["dtype"]
        self.shape = trailer["shape"]

    def close(self):
        del self.shm_np
        self._shm.close()
        del self._shm

    def get(self):
        """
        Return a copy of an array from the buffer or None if no array available.
        """
        put_counter = self.put_counter
        if put_counter == self.get_counter:
            return None

        # checks if writer has not overwritten the data read
        self._check_next_put_counter()
        array = self._get()
        self._check_next_put_counter()

        self.get_counter += 1

        return array

    def get_all(self):
        """
        Return a copy of remaining arrays from the buffer or None if no arrays available .
        """
        put_counter = self.put_counter
        if put_counter == self.get_counter:
            return None

        self._check_next_put_counter()
        put_pos = put_counter % self.capacity
        get_pos = self.get_counter % self.capacity
        if put_pos < get_pos:
            array = np.concatenate((self.shm_np[get_pos:], self.shm_np[:put_pos]))
        else:
            array = np.copy(self.shm_np[get_pos:put_pos])
        self._check_next_put_counter()

        self.get_counter = put_counter

        return array

    def get_last(self):
        self.get_counter = self.put_counter - 1
        return self.get()

    def reset(self):
        self.get_counter = self.put_counter


class Writer(_Common):
    """
    There is only one Writer
    """

    flock = Write_File_Lock(start=0, len=1)
    singleton_id = dict()

    def __init__(self, name: str, capacity: int, shape: tuple, dtype: np.dtype):
        """
        name: Name of the circular buffer
        capacity: Buffer length = number of numpy arrays
        shape: Shape of the numpy array
        dtype: Data type the numpy array
        """
        self.name = name
        self.capacity = capacity
        self.shape = shape
        self.dtype = dtype

        # test if shm already exists
        # if no , we create one
        # if (yes and there is no lock on it) then we can use it
        self._shm = self._build_shm()

        # only one writer per shared memory
        self._lock()

        self.shm_np = self._build_shm_np()

        self.reset()

    def __del__(self):
        if Writer.singleton_id[self.name] == id(self):
            del Writer.singleton_id[self.name]

    def _build_shm(self):
        header = shm_header_struct
        header_nbytes = shm_header_struct_nbytes
        np_nbytes = np_size(self.capacity, self.shape, self.dtype)
        trailer = dict(capacity=self.capacity, shape=self.shape, dtype=self.dtype)
        trailer_bytes = pickle.dumps(trailer)
        trailer_nbytes = len(trailer_bytes)
        trailer_slice = slice(
            header_nbytes + np_nbytes, header_nbytes + np_nbytes + trailer_nbytes
        )

        shm_nbytes = header_nbytes + np_nbytes + trailer_nbytes
        fname = _NAME_PREFIX + self.name
        shm = SharedMemory(name=fname, create=True, size=shm_nbytes)

        shm.buf[header.trailer_nbytes.slice] = int.to_bytes(
            trailer_nbytes, header.trailer_nbytes.nbytes, "big"
        )
        shm.buf[trailer_slice] = trailer_bytes

        return shm

    def _lock(self):
        # test if circular buffer is already used by another object in the same process
        if (self.name in Writer.singleton_id) and (
            sid := Writer.singleton_id[self.name]
        ) is not None:
            raise BlockingIOError(
                f"Circular buffer {self.name} is already used by object id {sid}"
            )
        Writer.singleton_id[self.name] = id(self)

        # test if circular buffer is already used by another process
        try:
            Writer.flock.lock(self._shm.fd)
        except BlockingIOError:
            self.singleton_id = None
            pid = Writer.flock.status(self._shm.fd)["pid"]
            msg = f"Circular buffer {self.name} is already used by process {pid}"
            raise BlockingIOError(msg) from None

    def close(self):
        del self.shm_np
        self._shm.close()
        self._shm.unlink()

    @_Common.next_put_counter.setter
    def next_put_counter(self, value):
        struct = shm_header_struct.next_put_counter
        self._shm.buf[struct.slice] = int.to_bytes(value, struct.nbytes, "big")

    @_Common.put_counter.setter
    def put_counter(self, value):
        struct = shm_header_struct.put_counter
        self._shm.buf[struct.slice] = int.to_bytes(value, struct.nbytes, "big")

    def put(self, array):
        put_counter = self.put_counter
        next_put_counter = put_counter + 1

        # notify readers that buffer will change
        self.next_put_counter = next_put_counter

        # modify the buffer
        self.shm_np[put_counter % self.capacity] = array

        # notify readers that buffer has changed
        self.put_counter = next_put_counter
        # update the timestamps of a the shared memory file
        # in order to force ATTRIB inotify event, used by async_reader
        os.utime(self._shm.fd)

    def reset(self):
        self.put_counter = 0
        self.next_put_counter = 0
