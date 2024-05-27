import tkinter as tk
from launch import mainloop

import os
os.environ["PN_PROTOCOL_VERSION"] = "144"

root = tk.Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry(f"800x450")

root.after(100, lambda: mainloop(root))
root.mainloop()

