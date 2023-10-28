import threading
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

        self.query = tk.Entry(self.events)
        self.query.grid(row=1, column = 0, sticky="ew")

        self.event = ttk.Treeview(self.events, columns=("epoch", "type", "source"), show='headings')

        self.event.column("epoch", anchor=tk.W, width=100)
        self.event.heading("epoch", text="Time", anchor=tk.W)

        self.event.column("type", anchor=tk.W, width=100)
        self.event.heading("type", text="Event Type", anchor=tk.W)

        self.event.column("source", anchor=tk.W, width=200)
        self.event.heading("source", text="Called By", anchor=tk.W)

        self.event.grid(row=2, column=0, sticky="ewns")

        self.events.columnconfigure(0, weight=1)
        self.events.rowconfigure(2, weight=1)

        self.event_iid = 0
        self.await_push = []






        ### Workspace ###

        self.exp = ttk.Frame(self.nb)
        self.exp.pack(fill='both', expand=True)
        self.nb.add(self.exp, text="Workspace")
        self.q = {}

        self.explorer = ttk.Treeview(self.exp)
        self.explorer.heading("#0", text="Workspace")

        self.explorer.insert('', tk.END, text="GameManager", open=False, iid=0)
        self._workspace_iid = 0
        self.q[self._workspace_iid] = self.parent
        for i in self.parent.children:
            self._workspace_dfs(i, 0)

        self.explorer.grid(row=0, column=0, sticky="ns")

        self.data_viewer = ttk.Frame(self.exp)
        self.info = tk.Label(self.data_viewer, text="Select an item to view its properties")
        self.info.pack(anchor="w")
        self.data_viewer.grid(row=0, column=1, sticky="nesw")

        self.explorer.bind('<ButtonRelease-1>', self._workspace_select)

        self.exp.rowconfigure(0, weight=1)
        self.exp.columnconfigure(0, weight=0)
        self.exp.columnconfigure(1, weight=1)



    def _workspace_select(self, e):
        self.info.pack_forget()

        stuff = self.q[int(self.explorer.focus())]

        self.info = ttk.Treeview(self.data_viewer)
        self.info.heading("#0", text=f"Browsing properties for element {stuff}")
        self.info.grid(row=0, column=0, sticky="nesw")
        self.data_viewer.rowconfigure(0, weight=1)
        self.data_viewer.columnconfigure(0, weight=2)
        self.data_viewer.columnconfigure(1, weight=1)



        disp = ""
        f = stuff.__dict__
        for i in f:
            cd = str(f[i])[:128]
            disp += f"{i} = {cd}\n"
        self.info.config(text=disp, anchor="w")


    def _workspace_dfs(self, next, fr):

        print(next, fr, self._workspace_iid)

        self._workspace_iid += 1
        c = int(self._workspace_iid)

        self.explorer.insert('', tk.END, text=next.__class__.__name__, open=False, iid=self._workspace_iid)
        self.q[self._workspace_iid] = next
        self.explorer.move(self._workspace_iid, fr, 1)

        for i in next.children:
            self._workspace_dfs(i, c)




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

            