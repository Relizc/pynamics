import tkinter as tk
from pygame import K_BACKQUOTE
import threading

from .interface import PygameProObject
from .text import Text

class Debugger(PygameProObject):

    def _toggle(self):
        self.enabled = not self.enabled
        self.text.enabled = self.enabled


    
    def __init__(self, parent):
        super().__init__(self)
        self.parent = parent
        self.enabled = False
        self.text = Text(self.parent, Text.str("Debug Menu (1/10) <Change with arrow keys or F+N>"), size=12)
        self.text.enabled = False
        
        @self.parent.addEventListener("keydown", target=K_BACKQUOTE)
        def press(ctx):
            self._toggle()
