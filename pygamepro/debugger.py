import tkinter as tk
from pygame import K_BACKQUOTE
import threading

class Debugger:

    def _toggle(self):
        pass
    
    def __init__(self, parent):
        self.parent = parent
        
        @self.parent.addEventListener("keydown", target=K_BACKQUOTE)
        def press(ctx):
            self.x = threading.Thread(target = self._toggle)
            self.x.start()
