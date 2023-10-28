
import tkinter as tk
from tkinter import ttk
from .logger import Logger

class Debugger:

    def __init__(self, parent):
        self.tk = tk.Tk()
        self.opened = False
        self.display = False
        self.parent = parent

        self.tk.geometry("800x500")

        self.nb = ttk.Notebook(self.tk)
        self.nb.pack(fill='both', expand=True)

        self.general = ttk.Frame(self.nb)
        self.general.pack(fill='both', expand=True)
        self.nb.add(self.general, text="General Information")

        self._fps = tk.Label(self.general, text=f"FPS: ? (Set: {self.parent.fps})")
        self._fps.grid(row=0, column=0)

        self._tps = tk.Label(self.general, text=f"TPS: ? (Set: {self.parent.tps})")
        self._tps.grid(row=1, column=0)

        self.exp = ttk.Frame(self.nb)
        self.exp.pack(fill='both', expand=True)
        self.nb.add(self.exp, text="Workspace")

        self.explorer = ttk.Treeview(self.exp)
        self.explorer.heading("#0", text="Workspace")

        self.explorer.insert('', tk.END, text="Object1", open=False)

        self.explorer.grid(row=0, column=0)


    def close(self):
        self.tk.withdraw()
        self.display = False

    def _tick_fps_op(self):
        self._fps.config(text=f"FPS: {self.parent.f} (Set: {self.parent.fps})")
        self.parent.f = 0

        self.tk.after(1000, self._tick_fps_op)

    def _tick_tps_op(self):
        self._tps.config(text=f"TPS: {self.parent.t} (Set: {self.parent.tps})")
        self.parent.t = 0

        self.tk.after(1000, self._tick_tps_op)

    def run(self):
        if not self.opened:
            self.tk.after(1000, self._tick_fps_op)
            self.tk.after(1000, self._tick_tps_op)
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.opened = True

        if not self.display:
            self.display = True
            self.tk.deiconify()