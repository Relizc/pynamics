import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
from .logger import Logger
from .events import EventType
import datetime
import inspect

def change(a, b):
    print(id(a.property), id(a.parent.parent.tps))
    a.property = b
    a.parent.parent.tps = b
    print(id(a.property), id(a.parent.parent.tps))

class DebugPropertyEditor:

    SUPPORTED_TYPES = {
        "int": int,
        "str": str,
        "float": float
    }

    def __init__(self, parent, property):
        self.parent = parent
        self.tk = tk.Toplevel()
        self.tk.title(f"Property Editor of {property.__class__.__name__}")
        self.tk.geometry("300x200")
        self.property = property

        self.tk.columnconfigure(0, weight=1)

        tk.Label(self.tk, text=f"Changing property of", pady=0).grid(row=0)
        tk.Label(self.tk, text=f"<{property.__class__.__name__}> {property}", pady=0).grid(row=1)

        self.ok = tk.StringVar(value=property.__class__.__name__)
        gg = []
        for i in self.SUPPORTED_TYPES:
            gg.append(i)
        self.option = tk.OptionMenu(self.tk, self.ok, *gg)
        self.option.grid(row=2)

        self.e = tk.StringVar(value=str(property))

        self.entry = tk.Entry(self.tk, textvariable=self.e)
        self.entry.grid(row=3)

        print(id(self.property), id(self.parent.parent.tps))

        self.sure = tk.Button(self.tk, text="Change Property", command=lambda: change(self, self.SUPPORTED_TYPES[self.ok.get()](self.e.get())))
        self.sure.grid(row=5, columnspan=2)




class Debugger:

    def __init__(self, parent, enable_event_listener: bool=False, allow_edits: bool=False):
        self.event_update = enable_event_listener
        self.tk = tk.Toplevel()
        self.opened = False
        self.display = True
        self.parent = parent

        self._eps = 0
        self.eps = 0

        self.tk.geometry("800x500")
        self.tk.title("Debug Tools")

        self.nb = ttk.Notebook(self.tk)
        self.nb.pack(fill='both', expand=True)
        self.editor = None

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

        if self.event_update:


            self.l = tk.Label(self.events, text="4700 Events Called. EPS: 370")
            self.l.grid(row=1, column=0, sticky="ew")

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

            self.log = 0
        else:
            tk.Label(self.events, text="Event Tracker is currently disabled due to resource optimization.\nYou can enable Event Tracker by creating a pynamics.debug.Debugger class with enable_event_listener = True.").pack()






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

        

    def _workspace_property_dfs(self, start, fr):
        #print(start)

        if not isinstance(start, (dict, list)):
            return

        ind = 0

        for i in start:
            self._ws_prop_iid += 1
            if isinstance(start, list):
                bb = f"ListIndex({ind})<{i.__class__.__name__}> = {i}"
                item = i
                ind += 1
            elif isinstance(start, dict):
                if isinstance(start[i], list):
                    bb = f"{i}<{start[i].__class__.__name__}> = [Iterable List({len(start[i])})]"
                elif isinstance(start[i], dict):
                    bb = f"{i}<{start[i].__class__.__name__}> = [Iterable Dict({len(start[i])})]"
                else:
                    bb = f"{i}<{start[i].__class__.__name__}> = {start[i]}"
                item = start[i]
            self.m[self._ws_prop_iid] = item

            # if isinstance(item, (dict, list)):
            #     bb = "..."
            self.info.insert('', tk.END, text=bb, open=False, iid=self._ws_prop_iid)
            self.info.move(self._ws_prop_iid, fr, 2147483647)
            self._workspace_property_dfs(item, self._ws_prop_iid)

    def _workspace_property_change(self, e):
        stuff = self.m[int(self.info.focus())]

        if not isinstance(stuff, (int, float, str)):
            tkmsg.showinfo(f"Unable to edit property", f"The debugger cannot edit the property because the type {stuff.__class__.__name__} is not supported.")
            return

        self.editor = DebugPropertyEditor(self, stuff)

    def _workspace_select(self, e):
        self.info.pack_forget()

        stuff = self.q[int(self.explorer.focus())]


        self.info = ttk.Treeview(self.data_viewer)
        self.info.heading("#0", text=f"Browsing properties for element {stuff.__class__.__name__}")
        self.info.grid(row=0, column=0, sticky="nesw")
        self.data_viewer.rowconfigure(0, weight=1)
        self.data_viewer.columnconfigure(0, weight=1)

        self._ws_prop_iid = 0

        self.m = {}

        for i in stuff.__dict__:
            thing = stuff.__dict__[i]
            if isinstance(thing, list):
                bb = f"[Iterable List({len(thing)})]"
            elif isinstance(thing, dict):
                bb = f"[Iterable Dict({len(thing)})]"
            else:
                bb = str(thing)
            self.info.insert('', tk.END, text=f"{i}<{thing.__class__.__name__}> = {bb}", open=False, iid=self._ws_prop_iid)
            self.m[self._ws_prop_iid] = thing
            self._workspace_property_dfs(thing, self._ws_prop_iid)
            self._ws_prop_iid += 1


    def _workspace_dfs(self, next, fr):

        self._workspace_iid += 1
        c = int(self._workspace_iid)

        self.explorer.insert('', tk.END, text=next.__class__.__name__, open=False, iid=self._workspace_iid)
        self.q[self._workspace_iid] = next
        self.explorer.move(self._workspace_iid, fr, 2147483647)

        for i in next.children:
            self._workspace_dfs(i, c)




    def _call_callevent(self, event, obj, func):
        if self.event_update:
            self.await_push.append([
                datetime.datetime.now().strftime("%H:%m:%S.%f"),
                EventType(event).name,
                f"{func.function.__module__}:{inspect.findsource(func.function)[1]}"
            ])
            self.event_iid += 1


    def close(self):
        self.tk.withdraw()
        self.display = False
        if self.editor != None:
            self.editor.tk.destroy()

    def _tick_fps_op(self):
        self._fps.config(text=f"FPS: {self.parent.f} (Set: {self.parent.fps})")
        self.parent.f = 0

        self.tk.after(1000, self._tick_fps_op)

    def _tick_tps_op(self):
        self._tps.config(text=f"TPS: {self.parent.t} (Set: {self.parent.tps})")
        self.parent.t = 0

        self.tk.after(1000, self._tick_tps_op)

    def _tick_event_update(self):
        if not self.event_update: return

        for i in self.await_push:
            self.event.insert(parent='',index='end',text='', values=i)
        self.log += len(self.await_push)
        self._eps += len(self.await_push)
        self.event.yview_moveto(1)
        self.await_push = []

        self.l.config(text=f"{self.log} events called. EPS: {self.eps}")

        self.tk.after(1, self._tick_event_update)

    def _tick_event_update_sec(self):
        self.eps = self._eps
        self._eps = 0
        self.l.config(text=f"{self.log} events called. EPS: {self.eps}")

        self.tk.after(1000, self._tick_event_update_sec)

    def run(self):
        self.tk.focus_force()

        if not self.opened:
            self.tk.after(1000, self._tick_fps_op)
            self.tk.after(1000, self._tick_tps_op)
            self.tk.after(1, self._tick_event_update)
            self.tk.after(1000, self._tick_event_update_sec)
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.opened = True

        if not self.display:
            self.display = True
            self.tk.deiconify()

            