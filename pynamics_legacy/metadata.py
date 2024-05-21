from .logger import Logger

import os


class FileStruct:

    def __init__(self, stream):
        self.io = stream

    def read_header(self):
        self.io.read(2)
        version = int.from_bytes(self.io.read(2), "little")

        v = int(os.environ["PN_PROTOCOL_VERSION"])


        if version != v:

            Logger.warn(
                f"Metadata file {self.io.name} is compiled in version {version} but current PyNamics version is {v}. Issues may occur while reading.")

    def read_uint4(self):
        return int.from_bytes(self.io.read(4), "little", signed=False)

    def read_uint2(self):
        return int.from_bytes(self.io.read(2), "little", signed=False)

    def read_int4(self):
        return int.from_bytes(self.io.read(4), "little", signed=True)


class PyNamicsTexture(FileStruct):

    def __init__(self, stream):
        super().__init__(stream)
        self.read_header()

        self.frames = self.read_uint2()
        self.current = 0

    def hasnext(self):
        return self.current < self.frames

    def frame(self):
        hashed = self.read_uint4()
        x, y, a, b = self.read_uint2(), self.read_uint2(), self.read_uint2(), self.read_uint2()
        self.current += 1

        return hashed, (x, y, a, b)
