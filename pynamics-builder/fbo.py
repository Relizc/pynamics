
import os
import json
os.environ["PN_PROTOCOL_VERSION"] = "144"

from PIL import ImageTk
from PIL import Image as ImageUtils

from screen import *
from filing import *
import screen as temp

import random
import tkinter.ttk as ttk
import tkinter as tk

TREEVIEW_TK: ttk.Treeview = None
NAMES: set = set()
PRESSED: set = set()



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

    def __init__(self, parent, treeview_id: int = None, name: str = "untitled", file: File = None):
        global TREEVIEW_TK, NAMES, DICT_ID_TO_OBJ

        self.children = []
        self.file = file

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

    def create_info(self):
        pass


    def attach_file(self, buffer):
        self.file = buffer

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}"

class Workspace(Property):

    def __init__(self):
        super().__init__(parent=None)
        self.directory = None


class Folder(Property):

    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)
        self.directory = self.parent.directory + "/" + name

    def create_info(self):
        os.mkdir(self.directory)



class Script(Property):

    def __init__(self, parent, name="Script"):
        super().__init__(parent, name=name)
        self.path = self.parent.directory + f"/{name}.py"


    def write_example(self):
        k = os.environ["PN_PROTOCOL_VERSION"]
        self.buffer.writelines([
            "# PyNamics Furnace Auto Created\n",
            f"# PyNamics Version: {k}\n",
            f"# File Name: {self.name}.py\n",
            "\n"
        ])


    def create_info(self):


        if os.path.exists(self.path):
            self.buffer = open(self.path, "r")
        else:

            self.buffer = open(self.path, "w")
            self.write_example()

            self.buffer.close()

            self.buffer = open(self.path, "r")

    def selected(self, root):
        for child in root.winfo_children():
            child.destroy()

        x = tk.Button(root, text="Open in Visual Studio Code", command=lambda: os.system(f"code \"{self.path}\""))
        x.pack()

class MainScript(Script):

    def __init__(self, parent):
        super().__init__(parent, name="__main__")

    def write_example(self):
        k = os.environ["PN_PROTOCOL_VERSION"]
        self.buffer.writelines([
            "# PyNamics Furnace Auto Created\n",
            f"# PyNamics Version: {k}\n",
            f"# File Name: {self.name}.py\n",
            "\n"
        ])

        self.buffer.writelines([
            "\nimport pynamics as pn\n\n",
            "ctx = pn.GameManager(pn.Dim(500, 500))\n",
            "window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))\n",
            "\n",
            "ctx.start()"
        ])

class PropertySettings(Property):

    def __init__(self, parent):
        super().__init__(parent, name="settings")

    def create_info(self):
        self.attach_file(WorkspaceFile(dir=self.parent.directory, name=self.name))



import shutil


class Image(Property):

    def __init__(self, parent, path, name):
        super().__init__(parent, name=name)

        self.path = path


    def selected(self, root):
        for child in root.winfo_children():
            child.destroy()

        self._browser = ImageBrowser(root, path=self.path)

    def create_info(self):
        shutil.copy2(self.path, self.parent.directory + f"/{self.name}.png")
        self.path = self.parent.directory + f"/{self.name}.png"


class FramedTexture(Property):

    def __init__(self, parent):
        super().__init__(parent)


class FrameGroup(Property):

    def __init__(self, parent):
        super().__init__(parent)


    def create_info(self):
        self.attach_file(TextureFile(dir=self.parent.directory, name=self.name))

class Frame(Property):

    def __init__(self, parent, point_0, point_1):
        super().__init__(parent)
        self.point_0 = point_0
        self.point_1 = point_1

temp.ALL_OBJECTS = {
    "Image": Image,
    "FrameGroup": FrameGroup,
    "Frame": Frame,
    "Folder": Folder,
    "Script": Script
}

temp.OBJECT_TYPING_HINTS = {
    "Image": ("object", "path"),
    "FrameGroup": ("object",),
    "Frame": ("object", "iterable int", "iterable int"),
    "Folder": ("object", "str"),
    "Script": ("object", "str")
}

temp.DICT_ID_TO_OBJ = DICT_ID_TO_OBJ





