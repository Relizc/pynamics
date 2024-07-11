from .interface import PyNamical
import tkinter as tk
import threading

class Crane2(PyNamical, tk.Toplevel):

    def __init__(self, parent):
        PyNamical.__init__(self, parent)
        tk.Toplevel.__init__(self, parent.window._tk.master)

    def run(self):
        self.run_thread = threading.Thread(target=self._run)
        self.run_thread.start()
