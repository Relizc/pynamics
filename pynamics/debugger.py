
import tkinter as tk
from tkinter import ttk
from .logger import Logger

class Debugger:

    def __init__(self):
        self.tk = tk.Tk()
        self.opened = False
        self.display = False

        self.tk.geometry("800x500")

        self.explorer = ttk.Treeview(self.tk)
        self.explorer.heading("#0", text="Workspace")

        self.explorer.insert('', tk.END, text="Object1", open=False)

        self.explorer.grid(row=0, column=0)


    def close(self):
        self.tk.withdraw()
        self.display = False

    def run(self):
        if not self.opened:
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.opened = True

        if not self.display:
            self.display = True
            self.tk.deiconify()

        if not self.opened: self.tk.mainloop()