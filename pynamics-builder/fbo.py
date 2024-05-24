
import os
import json
os.environ["PN_PROTOCOL_VERSION"] = "144"

class WorkspaceFile:

    type = "PyNamicsObject"

    def __init__(self, name="Untitled", attribute="pnobj", op=False):
        self.name = name
        self.attribute = attribute

        if op:
            self.content = json.load(open(f"{name}.{attribute}", "r"))
        else:
            self.content = {"version": int(os.environ["PN_PROTOCOL_VERSION"]), "filetype": self.type, "attribute": attribute, "contents": {}}

        self.save()



    def save(self):
        json.dump(self.content, open(f"{self.name}.{self.attribute}", "w"))

    def write_uint32(self, val: int):
        self.stream.write(val.to_bytes(4, "little"))

    def write_uint16(self, val: int):
        self.stream.write(val.to_bytes(2, "little"))


class FramedTextureFile(WorkspaceFile):

    type = "FramedTexture"

    def __init__(self, name="UntitledFramedTexture", attribute="pntexture"):
        super().__init__(name, attribute)

