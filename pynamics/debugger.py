
import tkinter as tk
from tkinter import ttk
from .logger import Logger
from .events import EventType
import datetime
import inspect



class Debugger:

    def __init__(self, parent):
        self.tk = tk.Tk()
        self.opened = False
        self.display = True
        self.parent = parent

        self.tk.geometry("800x500")
        self.tk.title("Debug Tools")

        self.nb = ttk.Notebook(self.tk)
        self.nb.pack(fill='both', expand=True)

        ### General ###

        self.general = ttk.Frame(self.nb)
        self.general.pack(fill='both', expand=True)
        self.nb.add(self.general, text="General Information")

        self._fps = tk.Label(self.general, text=f"FPS: ? (Set: {self.parent.fps})")
        self._fps.grid(row=0, column=0, sticky="w")

        self._tps = tk.Label(self.general, text=f"TPS: ? (Set: {self.parent.tps})")
        self._tps.grid(row=1, column=0, sticky="w")

        ### Event Tracker ###
        self.events = ttk.Frame(self.nb)
        self.events.pack(fill='both', expand=True)
        self.nb.add(self.events, text="Event Tracker")

        self.event = ttk.Treeview(self.events, columns=("epoch", "type", "source"), show='headings')



        self.event.column("epoch", anchor=tk.W, width=100)
        self.event.heading("epoch", text="Time", anchor=tk.W)

        self.event.column("type", anchor=tk.W, width=100)
        self.event.heading("type", text="Event Type", anchor=tk.W)

        self.event.column("source", anchor=tk.W, width=200)
        self.event.heading("source", text="Called By", anchor=tk.W)

        self.event.pack(fill="both", expand=True)

        self.event_iid = 0
        self.await_push = []

        ### Workspace ###

        self.exp = ttk.Frame(self.nb)
        self.exp.pack(fill='both', expand=True)
        self.nb.add(self.exp, text="Workspace")

        self.explorer = ttk.Treeview(self.exp)
        self.explorer.heading("#0", text="Workspace")

        self.explorer.insert('', tk.END, text="Object1", open=False)

        self.explorer.grid(row=0, column=0)


    def _call_callevent(self, event, obj, func):
        self.await_push.append([
            datetime.datetime.now().strftime("%H:%m:%S.%f"),
            EventType(event).name,
            f"{func.function.__module__}:{inspect.findsource(func.function)[1]}"
        ])
        self.event_iid += 1


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

    def _tick_event_update(self):
        for i in self.await_push:
            self.event.insert(parent='',index='end',text='', values=i)
        self.event.yview_moveto(1)
        self.await_push = []
        self.tk.after(1, self._tick_event_update)

    def run(self):
        if not self.opened:
            self.tk.after(1000, self._tick_fps_op)
            self.tk.after(1000, self._tick_tps_op)
            self.tk.after(1, self._tick_event_update)
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.opened = True

        if not self.display:
            self.display = True
            self.tk.deiconify()

            