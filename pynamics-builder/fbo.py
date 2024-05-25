
import os
import json
os.environ["PN_PROTOCOL_VERSION"] = "144"

from PIL import ImageTk
from PIL import Image as ImageUtils

from screen import AutoScrollbar, ImageBrowser, ObjectSelectButton, PathSelectButton, CreationPrompt
import screen as temp

import random
import tkinter.ttk as ttk
import tkinter as tk

TREEVIEW_TK: ttk.Treeview = None
NAMES: set = set()
PRESSED: set = set()

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

DICT_ID_TO_OBJ = {

}

PROTECTED_ATTRIBUTES = (
    "children",
    "tkbuffer"
)

def get_obj_id(id: int):
    global DICT_ID_TO_OBJ
    return DICT_ID_TO_OBJ[str(id)]

class Property:

    def __init__(self, parent, treeview_id: int = None, name: str = "untitled"):
        global TREEVIEW_TK, NAMES, DICT_ID_TO_OBJ

        self.children = []

        while name in NAMES:
            name += "1"
        self.name = name
        NAMES.add(self.name)

        if treeview_id is None:

            self._treeview_id = random.randint(0, 2**32-1)

        else:

            self._treeview_id = treeview_id

        self._treeview_tag = TREEVIEW_TK.insert('', tk.END, text=self.__repr__(), open=False, iid=self._treeview_id)
        DICT_ID_TO_OBJ[str(self._treeview_id)] = self

        self.parent = None
        self.set_parent(parent)
    def remove_children(self, obj):
        self.children.remove(obj)

    def add_children(self, obj):
        self.children.append(obj)

    def set_parent(self, parent):

        if self.parent is not None:
            self.parent.remove_children(self)

        self.parent = parent



        if parent is not None:

            self.parent = parent
            self.parent.add_children(self)
            TREEVIEW_TK.move(self._treeview_id, self.parent._treeview_id, 2147483647)

    def delete(self):
        self.parent.remove_children(self)
        TREEVIEW_TK.delete(self._treeview_tag)
        del DICT_ID_TO_OBJ[str(self._treeview_id)]

    def selected(self, root):
        for child in root.winfo_children():
            child.destroy()
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}"

class Workspace(Property):

    def __init__(self):
        super().__init__(parent=None)





class Image(Property):

    def __init__(self, parent, path):
        super().__init__(parent)

        self.path = path


    def selected(self, root):
        for child in root.winfo_children():
            child.destroy()

        self._browser = ImageBrowser(root, path=self.path)

class FramedTexture(Property):

    def __init__(self, parent):
        super().__init__(parent)

    @staticmethod
    def prompt_creation():
        pass

class FrameGroup(Property):

    def __init__(self, parent):
        super().__init__(parent)

    @staticmethod
    def prompt_creation():
        pass

class Frame(Property):

    def __init__(self, parent, point_0, point_1):
        super().__init__(parent)

temp.ALL_OBJECTS = {
    "Image": Image,
    "FrameGroup": FrameGroup,
    "Frame": Frame
}

temp.OBJECT_TYPING_HINTS = {
    "Image": ("object", "path"),
    "FrameGroup": ("object",),
    "Frame": ("object", "iterable int", "iterable int")
}

temp.DICT_ID_TO_OBJ = DICT_ID_TO_OBJ





