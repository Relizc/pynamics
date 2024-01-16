from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import threading
import shutil
import os

class Project:

    def __init__():
        pass

def create_empty_project(dir: str):
    os.mkdir(dir)



#s = ttk.Style()

root = tk.Tk()
root.geometry("640x360")
root.title("PyNamics Workstation - New")

greeting0 = tk.Label(root, font=("Segoe UI", 24), text="PyNamics Workstation (v1.0)")
greeting0.pack()

greeting1 = tk.Label(root, font=("Segoe UI", 12), text="Gonna frick some games")
greeting1.pack()

def ask_open_dir(entry):
    p = filedialog.askdirectory()
    entry.set(p)

def popen():
    pass
    

def main():
    op = tk.Toplevel(root, padx=8,pady=8)
    op.geometry("480x80")

    nt = tk.StringVar(value=os.getcwd())

    tk.Label(op, text="File Directory").grid(row=0, column=0, sticky="E")
    L = tk.Entry(op, textvariable=nt, width=32)
    L.grid(row=0, column=1, sticky="W")

    tk.Button(op, text="Browse", width=12, command=lambda: ask_open_dir(nt)).grid(row=2, column=0, sticky="E")
    tk.Button(op, text="Create", width=12).grid(row=2, column=1, sticky="W")
    tk.Button(op, text="Open", width=12, default="active").grid(row=2, column=1, sticky="E", command=popen)


    op.mainloop()

# root.after(100, main)
# root.mainloop()

p = filedialog.askdirectory() + "/Bozo"
if p != '':
    print(p)
    create_empty_project(p)

