from .interface import PyNamical
import tkinter as tk
from tkinter import ttk
import threading
import random


class Profile:

    def __init__(self, parent=None, cpanel=None, menu: ttk.Treeview = None, name: str = "Profile"):

        self.parent = parent

        if self.parent is not None:
            self.parent.children.append(self)

        self.children = []
        self.name = name

        self.menu = menu
        self.cpanel = cpanel

        print(self.parent)

        if self.parent is None:
            self._tk_id = self.menu.insert('', tk.END, text=name)
        else:

            self._tk_id = self.menu.insert(self.parent._tk_id, tk.END, text=name)

    def focus(self):
        pass


class ProfileNative(Profile):
    class TickOptions(Profile):
        def __init__(self, parent=None, cpanel=None, menu: ttk.Treeview = None):
            super().__init__(parent, cpanel, menu, name="TickOptions")

    class FrameOptions(Profile):
        def __init__(self, parent=None, cpanel=None, menu: ttk.Treeview = None):
            super().__init__(parent, cpanel, menu, name="FrameOptions")

    def __init__(self, parent=None, cpanel=None, menu: ttk.Treeview = None):
        super().__init__(parent, cpanel, menu, name="Pynamics")

        self.TickOptions(self, self.cpanel, self.menu)
        self.FrameOptions(self, self.cpanel, self.menu)


class Crane2(PyNamical, tk.Toplevel):

    def __init__(self, parent):
        PyNamical.__init__(self, parent)
        tk.Toplevel.__init__(self, parent.window._tk.master)

        self._tk_id_counter = 0

        self.geometry(
            f"{int(self.winfo_screenwidth() / 2)}x{int(self.winfo_screenheight() / 2)}+{int(self.winfo_screenwidth() / 4)}+{int(self.winfo_screenheight() / 4)}")
        self.title("Pynamics Crane DevTools")

        self._frame1 = tk.Frame(self)

        self.content_browser = ttk.Treeview(self._frame1)
        self.content_browser.pack(expand=True, anchor="nw", fill="y")

        self.content_browser.heading("#0", text="Profiles")

        self._frame1.pack(expand=True, anchor="w", fill="both")

        self.status = tk.Label(self, text="Pynamics 14.1.47 (Python 3.8.9)", justify="left", anchor="w", height=1)
        self.status.pack(expand=False, anchor="w")

        self.opened = False
        self.display = False
        self.editor = None

        self.tickchanger_paused = False

        self.profiles = []

        self._create_default_profiles()

    def _create_default_profiles(self):
        ProfileNative(None, self, self.content_browser)

    def _call_callevent(self, *args, **kwargs):
        pass

    def run(self):
        self.run_thread = threading.Thread(target=self._run)
        self.run_thread.start()

    def close(self):
        self.withdraw()
        self.display = False
        if self.editor != None:
            self.editor.tk.destroy()

    def _run(self):
        self.focus_force()

        if not self.opened:
            self.protocol("WM_DELETE_WINDOW", self.close)

        if not self.display:
            self.display = True
            self.deiconify()
