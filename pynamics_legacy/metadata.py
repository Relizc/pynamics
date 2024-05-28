from .logger import Logger

import os


class FileType:

    CUSTOM = 0

    STATIC_TEXTURE = 0x01
    FRAMED_TEXTURE = 0x02


    WORKSPACE = 0x10


class FileStruct:

    def __init__(self, stream, filetype=FileType.CUSTOM):
        self.io = stream
        self.filetype = filetype

    def close(self):
        self.io.close()

    def write_header(self):
        self.io.write(b"PN")
        self.write_uint32(int(os.environ["PN_PROTOCOL_VERSION"]))
        self.write_uint16(self.filetype)

    def write_uint32(self, value: int):
        self.io.write(value.to_bytes(4, byteorder="little"))

    def write_uint16(self, value: int):
        self.io.write(value.to_bytes(2, byteorder="little"))

    def write_uint8(self, value: int):
        self.io.write(value.to_bytes(1, byteorder="little"))

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
