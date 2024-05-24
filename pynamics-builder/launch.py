
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from fbo import *

FBO = None
TOP = None
WORKSPACE = None
PROPERTY = None
FRAME = None

import fbo as temp


def ask_open_file():
    return filedialog.askopenfilename(filetypes=[("Images", [".png", ".jpg", ".jpeg", ".bmp", ".gif"])], title="Import Image...")

def import_image():
    global WORKSPACE
    path = ask_open_file()

    img = Image(WORKSPACE, path)
    print(img)



def load_workspace(content, root):

    global FBO, TOP

    target = content.selection_get()
    root.destroy()

    if target == "FramedTexture":
        FBO = FramedTextureFile()

    TOP.title(f"PyNamics Furnace - {FBO.name}.{FBO.attribute}")





def process(root, id=0):

    [child.destroy() for child in root.winfo_children()]

    if id ==0:
        tk.Label(root, text="Select what to create.").pack()
        d = tk.Listbox(root)
        d.insert(tk.END, 
                                "FramedTexture", "GameLevel" )
        d.bind("<Double-1>", lambda e: load_workspace(d, root))
        d.pack(expand=True, fill=tk.BOTH)


    elif id == 1:
        pass

def ask_open_option(root):

    global FBO, WORKSPACE, TREEVIEW_TK

    WORKSPACE = Workspace()

    topmenu = tk.Menu(root)
    root.config(menu=topmenu)

    file = tk.Menu(topmenu, tearoff="off")
    file.add_command(label="Open")
    file.add_command(label="Save", command=lambda: FBO.save())
    topmenu.add_cascade(label="File", menu=file)

    file = tk.Menu(topmenu, tearoff="off")
    file.add_command(label="...")
    topmenu.add_cascade(label="Edit", menu=file)

    file = tk.Menu(topmenu, tearoff="off")

    t = tk.Menu(file, tearoff="off")
    t.add_command(label="Recent properties will show here", state="disabled")
    file.add_cascade(label="Recent", menu=t)
    file.add_separator()

    t = tk.Menu(file, tearoff="off")
    t.add_command(label="FrameGroup")
    t.add_command(label="Frame")
    t.add_separator()
    t.add_command(label="TextureGroup")
    t.add_command(label="Texture")
    t.add_separator()
    t.add_command(label="TileMap")
    t.add_command(label="Tile")
    file.add_cascade(label="Texture", menu=t)
    file.add_separator()

    t = tk.Menu(file, tearoff="off")
    t.add_command(label="GameLevel")
    t.add_separator()
    t.add_command(label="TileArrangement")
    t.add_command(label="HitboxArrangement")
    file.add_cascade(label="World", menu=t)

    topmenu.add_cascade(label="New Property", menu=file)

    imports = tk.Menu(topmenu, tearoff="off")
    imports.add_command(label="Image", command=lambda: import_image())
    topmenu.add_cascade(label="Import", menu=imports)

    selectmenu = tk.Toplevel(root)
    selectmenu.geometry("300x200")
    selectmenu.title("New or Open Projects")

    new = tk.Button(selectmenu, text="Create New", command=lambda: process(selectmenu, 0))
    new.pack()

    op = tk.Button(selectmenu, text="Open Project", command=lambda: process(selectmenu, 1))
    op.pack()


def update_attribute(tree):
    for c in PROPERTY.get_children():
        PROPERTY.delete(c)

    id = tree.focus()
    obj = get_obj_id(id)
    obj.selected(FRAME)

    r = obj.__dict__

    for k in r:

        if k[0] != "_" and k not in PROTECTED_ATTRIBUTES:

            code = PROPERTY.insert('', tk.END, values=(
                f"{k}: {r[k].__class__.__name__}", r[k]
            ))




def add_key(event):
    temp.PRESSED.add(event.keysym)

def no_key(event):
    try:
        temp.PRESSED.remove(event.keysym)
    except KeyError:
        pass


def mainloop(root):

    global TOP, PROPERTY, FRAME
    TOP = root

    TOP.columnconfigure(0, weight=1)
    TOP.columnconfigure(1, weight=8)
    TOP.columnconfigure(2, weight=1)
    TOP.rowconfigure(0, weight=1)

    tree = ttk.Treeview(root)
    tree.heading("#0", text="File Structure")
    tree.grid(column=0, row=0, sticky="news", rowspan=2)

    FRAME = tk.Frame(root)
    FRAME.grid(column=1, row=0, sticky="news", rowspan=1)

    FRAME.bind_all("<KeyPress>", add_key)
    FRAME.bind_all("<KeyRelease>", no_key)

    PROPERTY = ttk.Treeview(root,
                            columns=["attr", "value"], show="headings")

    PROPERTY.column("attr", anchor=tk.W, width=100)
    PROPERTY.heading("attr", text="Attribute", anchor=tk.W)

    PROPERTY.column("value", anchor=tk.W, width=100)
    PROPERTY.heading("value", text="Value", anchor=tk.W)

    PROPERTY.heading("#0", text="Attribute Viewer")
    PROPERTY.grid(column=2, row=0, sticky="news", rowspan=2)

    PROPERTY.tag_configure("dis", foreground="green")

    temp.TREEVIEW_TK = tree
    tree.bind("<<TreeviewSelect>>", lambda e: update_attribute(tree))

    ask_open_option(root)