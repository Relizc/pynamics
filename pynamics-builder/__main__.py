import tkinter as tk

root = tk.Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry(f"{w}x{h}")

root.mainloop()