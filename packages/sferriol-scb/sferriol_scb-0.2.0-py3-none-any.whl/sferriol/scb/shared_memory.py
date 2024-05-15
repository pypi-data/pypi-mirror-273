import mmap
import os
import pickle

import numpy as np

# from multiprocessing import shared_memory # KO
import posix_ipc

_O_CREX = os.O_CREAT | os.O_EXCL


class PosixSharedMemory:
    """ """

    # Defaults; enables close() and unlink() to run without errors.
    _name = None
    _mmap = None
    _buf = None
    _flags = 0
    _mode = 0o600
    _shm = None

    def __init__(self, name, create=False, size=0, read_only=False):
        if not (size >= 0):
            raise ValueError("'size' must be a positive integer")
        if create:
            #            self._flags = os.O_CREAT | os.O_EXCL
            self._flags = os.O_CREAT

            if size == 0:
                raise ValueError("'size' must be a positive number different from zero")
        try:
            self._shm = posix_ipc.SharedMemory(
                flags=self._flags, name="/" + name, read_only=read_only, size=size
            )
        except posix_ipc.ExistentialError as e:
            raise OSError(f"Shared memory ({name}): {e}") from None
        _fd = self._shm.fd
        self._name = name
        try:
            stats = os.fstat(_fd)
            size = stats.st_size
            self._mmap = mmap.mmap(
                fileno=_fd,
                length=size,
                access=mmap.ACCESS_READ if read_only else mmap.ACCESS_DEFAULT,
            )
        except OSError:
            self.unlink()
            raise
        self._size = size
        self._buf = memoryview(self._mmap)

    def __del__(self):
        try:
            self.close()
        except OSError:
            pass

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.name,
                False,
                self.size,
            ),
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, size={self.size})"

    def _exists(self):
        return self.exists(self.name)

    @property
    def buf(self):
        "A memoryview of contents of the shared memory block."
        return self._buf

    @property
    def fd(self):
        return self._shm.fd

    @property
    def name(self):
        "Unique name that identifies the shared memory block."
        reported_name = self._name
        return reported_name

    @property
    def size(self):
        "Size in bytes."
        return self._size

    def close(self):
        """Closes access to the shared memory from this instance but does
        not destroy the shared memory block."""
        if self._buf is not None:
            self._buf.release()
            self._buf = None
        if self._mmap is not None:
            self._mmap.close()
            self._mmap = None
        if self._shm:
            self._shm.close_fd()

    @classmethod
    def exists(cls, name):
        try:
            shm = cls(name=name, read_only=True)
            ret = True
        except OSError as e:
            ret = False
        except posix_ipc.ExistentialError:
            ret = False
        else:
            shm.close()
        return ret

    def unlink(self):
        """Requests that the underlying shared memory block be destroyed.

        In order to ensure proper cleanup of resources, unlink should be
        called once (and only once) across all processes which have access
        to the shared memory block."""
        if self._shm:
            self._shm.unlink()
            self._shm = None
