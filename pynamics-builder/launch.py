
import tkinter as tk
from tkinter import ttk

def load_workspace():
    pass


def process(root, id=0):

    [child.destroy() for child in root.winfo_children()]

    if id ==0:
        tk.Label(root, text="Select what to create.").pack()
        d = tk.Listbox(root)
        d.insert(tk.END, 
                                "FramedTexture", "GameLevel" )
        d.bind("<Double-1>", )
        d.pack(expand=True, fill=tk.BOTH)


    elif id == 1:
        pass

def ask_open_option(root):
    selectmenu = tk.Toplevel(root)
    selectmenu.geometry("300x200")
    selectmenu.title("New or Open Projects")

    new = tk.Button(selectmenu, text="Create New", command=lambda: process(selectmenu, 0))
    new.pack()

    op = tk.Button(selectmenu, text="Open Project", command=lambda: process(selectmenu, 1))
    op.pack()





def mainloop(root):

    tree = ttk.Treeview(root)
    tree.heading("File Structure")
    tree.pack(anchor=tk.W, expand=True, fill="y")

    ask_open_option(root)