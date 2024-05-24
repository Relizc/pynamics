
import os
import json
os.environ["PN_PROTOCOL_VERSION"] = "144"

from PIL import ImageTk
from PIL import Image as ImageUtils

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
        self.buffer = ImageUtils.open(path)
        self.tkbuffer = ImageTk.PhotoImage(self.buffer)

        self._tk_pressed = set()

    def selected(self, root):
        for child in root.winfo_children():
            child.destroy()

        self._browser = tk.Canvas(root, background="white")
        self._container = self._browser.create_image(0, 0, anchor=tk.NW, image=self.tkbuffer)
        self._browser.pack(expand=True, fill="both")
        self._browser.bind_all("<MouseWheel>", self._on_mousewheel)
        self.delta = 0.3
        self.imscale = 0

    def _on_mousewheel(self, event):
        print(PRESSED)

        if "Control_L" in PRESSED or "Control_R" in PRESSED:

            if self.imscale <= -5 or self.imscale >= 5:
                self.imscale -= 1
                return

            x = self._browser.canvasx(event.x)
            y = self._browser.canvasy(event.y)

            if event.delta > 0:
                m = self.delta
                self.imscale += 1
            else:
                m = -self.delta
                self.imscale -= 1



            self._browser.delete(self._container)
            self.buffer = ImageUtils.open(self.path).resize((int(self.buffer.width + (self.buffer.width * m)), int(self.buffer.height + (self.buffer.height * m))), resample=ImageUtils.BOX)
            self.tkbuffer = ImageTk.PhotoImage(self.buffer)
            self._container = self._browser.create_image(0, 0, anchor=tk.NW, image=self.tkbuffer)


        else:
            if "Shift_L" in PRESSED or "Shift_R" in PRESSED:
                self._browser.xview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                self._browser.yview_scroll(int(-1 * (event.delta / 120)), "units")





