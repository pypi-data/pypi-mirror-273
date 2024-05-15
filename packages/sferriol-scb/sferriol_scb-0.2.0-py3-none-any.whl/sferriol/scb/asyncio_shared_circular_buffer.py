import asyncio

from asyncinotify import Inotify, Mask

from .shared_circular_buffer import *


class Async_Reader(Reader):
    """Asynchronous reader

    Parameters
    ----------
    name -- name of circular buffer
    timeout -- limit amount of time waiting notify event from writer
    counter -- begin with counter value. If None, writer's counter is taken

    """

    def __init__(
        self, name: str, timeout: float | None = None, counter: int | None = None
    ):
        ret = Reader.__init__(self, name, counter)
        self.timeout = timeout
        self._inotify = Inotify()
        fpath = f"/dev/shm/{self._shm.name}"
        self._inotify.add_watch(fpath, Mask.ATTRIB)
        return ret

    async def get(self):
        """
        Return a copy of an array from the buffer or None if no array available.
        """
        put_counter = self.put_counter
        while self.put_counter == self.get_counter:
            async with asyncio.timeout(self.timeout):
                await self._inotify.get()

        self._check_next_put_counter()
        array = self._get()
        self._check_next_put_counter()

        self.get_counter += 1

        return array

    def close(self):
        if self._inotify:
            self._inotify.close()
            self._inotify = None
        return Reader.close(self)
