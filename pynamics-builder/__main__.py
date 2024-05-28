import tkinter as tk

import os

from launch import mainloop

root = tk.Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry(f"800x450")

root.after(100, lambda: mainloop(root))
root.mainloop()

