import fcntl
import os
import struct


class _File_Lock:
    def __init__(self, len=0, start=0, whence=os.SEEK_SET):
        self.flock = (self.type, whence, start, len, 0)

    def can_lock(self, fd):
        status = self.status(fd)
        return status["type"] == fcntl.F_UNLCK

    def lock(self, fd):
        lockdata = struct.pack("hhQQi", *self.flock)
        fcntl.fcntl(fd, fcntl.F_SETLK, lockdata)

    def lockw(self, fd):
        lockdata = struct.pack("hhQQi", *self.flock)
        fcntl.fcntl(fd, fcntl.F_SETLKW, lockdata)

    def status(self, fd):
        # see F_GETLK in https://www.man7.org/linux/man-pages/man2/fcntl.2.html
        lockdata = struct.pack("hhQQi", *self.flock)
        res = fcntl.fcntl(fd, fcntl.F_GETLK, lockdata)
        res = struct.unpack("hhQQi", res)
        return dict(zip(("type", "whence", "start", "len", "pid"), res))

    def unlock(self, fd):
        lockdata = struct.pack("hhQQi", fcntl.F_UNLCK, *(self.flock[1:]))
        fcntl.fcntl(fd, fcntl.F_SETLK, lockdata)

    def unlockw(self, fd):
        lockdata = struct.pack("hhQQi", fcntl.F_UNLCK, *(self.flock[1:]))
        fcntl.fcntl(fd, fcntl.F_SETLKW, lockdata)


class Read_File_Lock(_File_Lock):
    type = fcntl.F_RDLCK


class Write_File_Lock(_File_Lock):
    type = fcntl.F_WRLCK
