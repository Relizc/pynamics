
import json
import importlib.util

import os
<<<<<<< HEAD
import sys


# class File(metadata.FileStruct):

#     def __init__(self, path):
#         if not os.path.exists(path):
#             json.dump()
#         self.content = json.load(open(path, "r"))
=======


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
>>>>>>> 56da336628102faffa2a97d392f3054adb35c9d7


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


