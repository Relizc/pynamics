import tkinter as tk
from pygame import K_BACKQUOTE
import threading

class Debugger:

    def _loop(self):
        self.window = tk.Tk()
        self.window.mainloop()
    
    def __init__(self, parent):
        self.parent = parent
        
        # @self.parent.addEventListener("keydown", target=K_BACKQUOTE)
        # def press(ctx):
        #     self.x = threading.Thread(target = self._loop)
        #     self.x.start()
