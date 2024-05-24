
import tkinter as tk
from tkinter import ttk
from fbo import *

FBO = None
TOP = None

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

    global FBO

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

    selectmenu = tk.Toplevel(root)
    selectmenu.geometry("300x200")
    selectmenu.title("New or Open Projects")

    new = tk.Button(selectmenu, text="Create New", command=lambda: process(selectmenu, 0))
    new.pack()

    op = tk.Button(selectmenu, text="Open Project", command=lambda: process(selectmenu, 1))
    op.pack()





def mainloop(root):

    global TOP
    TOP = root

    tree = ttk.Treeview(root)
    tree.heading("#0", text="File Structure")
    tree.pack(anchor=tk.W, expand=True, fill="y")

    ask_open_option(root)