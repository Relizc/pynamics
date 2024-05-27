
import json

from pynamics_legacy import metadata
import os


class File(metadata.FileStruct):

    def __init__(self, path, filetype=metadata.FileType.CUSTOM):

        self.path = path

        print("create", path)

        if os.path.exists(path):
            super().__init__(open(path, "rb"), filetype=filetype)
            self.read_header()
        else:

            super().__init__(open(path, "wb"), filetype=filetype)
            self.write_header()
            self.close()

            super().__init__(open(path, "rb"), filetype=filetype)
            self.read_header()


class WorkspaceFile(File):

    def __init__(self, dir=None, name="Untitled", attribute="pndef"):
        super().__init__(path=f"{dir}/{name}.{attribute}", filetype=metadata.FileType.WORKSPACE)

        self.name = name
        self.attribute = attribute

class TextureFile(File):

    def __init__(self, dir=None, name="Untitled", attribute="pntexture", filetype=metadata.FileType.STATIC_TEXTURE):
        super().__init__(path=f"{dir}/{name}.{attribute}", filetype=filetype)

        self.name = name
        self.attribute = attribute


