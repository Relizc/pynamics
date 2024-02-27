import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
from .logger import Logger
from .dimensions import Dimension, Vector
from .events import EventType, get_registered_events
from .socket import DedicatedClient
import datetime
import time
import traceback
import inspect
import random
import enum

def change(s, a, b, c):
    print(c)
    a.__dict__[b[0]] = c
    s.parent._workspace_select(None)
    s.tk.destroy()

class Console:

    def __init__(self, parent, root, output):
        self.parent = parent
        self.output = output

        self.output.insert(tk.END, "Console is now enabled.\nUse \"main\" to access root GameManager.\n")
        self.root = root

    def log(self, text):
        self.output.insert(tk.END, str(text) + "\n")
        self.output.see(tk.END)

    def execute(self, query):

        main = self.root



        try:
            exec(f"self.log({query})")
        except:
            try:
                exec(f"{query}")
            except:
                self.log(traceback.format_exc())


class DebugPropertyEditor:

    SUPPORTED_TYPES = {
        "int": int,
        "str": str,
        "float": float,
        "Dimension": Dimension.format_space_str,
        "Dim": Dimension.format_space_str,
        "Vector": Vector.format_space_str,
        "Vector2d": Vector.format_space_str,
        "bool": bool
    }

    def __init__(self, parent, fro, path):
        property = fro.__dict__[path[0]]

        self.parent = parent
        self.tk = tk.Toplevel()
        self.tk.title(f"Property Editor of {property.__class__.__name__}")
        self.tk.geometry("300x200")



        self.property = property

        self.tk.columnconfigure(0, weight=1)

        tk.Label(self.tk, text=f"Changing property of", pady=0).grid(row=0)
        tk.Label(self.tk, text=f"<{property.__class__.__name__}> {property}", pady=0).grid(row=1)

        print(property.__class__.__name__)

        self.ok = tk.StringVar(value=property.__class__.__name__)
        gg = []
        for i in self.SUPPORTED_TYPES:
            gg.append(i)
        self.option = tk.OptionMenu(self.tk, self.ok, *gg)
        self.option.grid(row=2)

        if isinstance(property, (str, int, float)):
            self.e = tk.StringVar(value=str(property))
        elif isinstance(property, (Dimension)):
            self.e = tk.StringVar(value=str(property.x) + ", " + str(property.y))
        elif isinstance(property, (Vector)):
            self.e = tk.StringVar(value=str(property.r) + ", " + str(property.f))

        self.entry = tk.Entry(self.tk, textvariable=self.e)
        self.entry.grid(row=3)

        self.sure = tk.Button(self.tk, text="Change Property", command=lambda: change(self, fro, path, self.SUPPORTED_TYPES[self.ok.get()](self.e.get())))
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
        self._ekps = 0

        self.tk.geometry("800x500")
        self.tk.title("Debug Tools")

        self.nb = ttk.Notebook(self.tk)
        self.nb.pack(fill='both', expand=True)
        self.editor = None

        ### General ###

        self.general = tk.Frame(self.nb)
        self.general.pack(fill='both', expand=True)
        self.nb.add(self.general, text="General Information")

        self._fps = tk.Label(self.general, text=f"FPS: ? (Set: {self.parent.fps})")
        self._fps.grid(row=0, column=0, sticky="w")

        self._tps = tk.Label(self.general, text=f"TPS: ? (Set: {self.parent.tps})")
        self._tps.grid(row=1, column=0, sticky="w")

        self._network = tk.Label(self.general, text=f"Loading Networking...")
        self._network.grid(row=2, column=0, sticky="w")

        self._obj_guide = tk.Label(self.general, text=f"E: ? / R: ?")
        self._obj_guide.grid(row=3, column=0, sticky="w")

        self._event_monitor = tk.Label(self.general, text=f"Events: ? / Suspended: ? / KPS: ?")
        self._event_monitor.grid(row=4, column=0, sticky="w")

        ### Console ###

        self.console = tk.Frame(self.nb)
        self.console.pack(fill="both", expand=True)
        self.nb.add(self.console, text="Console")

        self.consoletext = tk.Text(self.console, height=0)
        self.consoletext.pack(fill="both", expand=True)

        self.consoleinput = tk.Entry(self.console, width=0, font=("Consolas", 11))
        self.consoleinput.pack(fill="both", expand=True, side="left")
        self.consoleinput.bind("<Return>", lambda i: self._console_execute())

        self.consolesend = tk.Button(self.console, text="Execute", command=self._console_execute)
        self.consolesend.pack(side="left")

        self.consoleobj = Console(self, self.parent, self.consoletext)

        ### Event Tracker ###
        self.events = ttk.Frame(self.nb)
        self.events.pack(fill='both', expand=True)
        self.nb.add(self.events, text="Event Tracker")

        if self.event_update:

            self.event = ttk.Treeview(self.events, columns=("epoch", "name", "type", "source", "threaded", "eventid"), show='headings')

            self.event.column("epoch", anchor=tk.W, width=100)
            self.event.heading("epoch", text="Last Called", anchor=tk.W)

            self.event.column("name", anchor=tk.W, width=200)
            self.event.heading("name", text="Event Name", anchor=tk.W)

            self.event.column("type", anchor=tk.W, width=100)
            self.event.heading("type", text="Event Type", anchor=tk.W)

            self.event.column("source", anchor=tk.W, width=200)
            self.event.heading("source", text="Function Source", anchor=tk.W)

            self.event.column("threaded", anchor=tk.W, width=200)
            self.event.heading("threaded", text="Is Threaded", anchor=tk.W)

            self.event.column("eventid", anchor=tk.W, width=100)
            self.event.heading("eventid", text="Event ID", anchor=tk.W)

            self.event.grid(row=2, column=0, sticky="ewns")

            self.events.columnconfigure(0, weight=1)
            self.events.rowconfigure(2, weight=1)

            self.event_iid = 0
            self.await_push = []

            self.log = 0
        else:
            tk.Label(self.events, text="Event Tracker is currently disabled due to resource optimization.\nYou can enable Event Tracker by creating a pynamics.debug.Debugger class with enable_event_listener = True.").pack()






        ### Workspace ###

        self.lastLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL = None
        self.wspath = {}

        self.exp = tk.Frame(self.nb)
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

        # Tick Manager

        self.tickman = tk.Frame(self.nb)
        self.tickman.pack(fill="both", expand=True)
        self.nb.add(self.tickman, text="Tick Manager")

        self.tickinfo = tk.Label(self.tickman, text=f"Tick Epoch: {self.parent.ticks}\nUptime: {self.parent.starttime}", font=("Courier", 14))
        self.tickinfo.pack()

        self.insttps = tk.Label(self.tickman, text=f"Instantaneous TPS: ?", font=("Courier", 14))
        self.insttps.pack()

        self.statusgraph = tk.Canvas(self.tickman, width=700,height=100,bg="green")
        self.statusgraph.pack()

        self.pp = tk.Button(self.tickman, text="Pause Tick", command=self._tickman_pause)
        self.pp.pack()

        self.ticknext = tk.Button(self.tickman, text="Tick Step", command=self._tickman_stepnext)
        self.ticknext.pack()

        tk.Label(self.tickman, text="Change game tick:")

        self._tickinput = tk.IntVar()
        self._tickinput.set(self.parent.tps)

        self.tickinput = tk.Entry(self.tickman, textvariable=self._tickinput)
        self.tickinput.pack()

        self.submittickinput = tk.Button(self.tickman, command=self._tickman_change_tps, text="Change TPS")
        self.submittickinput.pack()

        self.tickchanger_paused = False
        self.tickchanger_stepping = 0

        self.points = [0]
        self.fps_points = [0]
        self.graph_x = 0
        self.graph_x_factor = 2
        self.last = 0
        self.graph_measure = 0

        self.parent.pressed["quoteleft"] = False

    def _console_execute(self):
        q = self.consoleinput.get()
        self.consoleinput.delete(0, tk.END)
        self.consoleobj.execute(q)

    def _tickman_change_tps(self):
        f = self._tickinput.get()
        #print(f)
        self.parent.tps = f
        self.parent._epoch_tps = 1 / self.parent.tps
        Logger.print(f"Changed TPS to {f} (DeltaTime:{self.parent._epoch_tps})", channel=5)

    def await_tickchanger_continue(self):
        if self.tickchanger_stepping:
            self.tickchanger_paused = False
        time.sleep(0.01)
        pass

    def _tickman_stepnext(self):
        self.tickchanger_stepping = self.parent.ticksteplisteners

    def _tickman_unpause(self):
        self.pp.config(text="Pause Tick", command=self._tickman_pause)
        self.tickchanger_paused = False

    def _tickman_pause(self):
        self.pp.config(text="Resume Tick", command=self._tickman_unpause)
        self.tickchanger_paused = True



    def _tickman_update(self):
        #print(f"update {random.randint(1, 1000)}")
        t = max(time.time() - self.parent.starttime, 1)
        c = "%.2f" % (self.parent.ticks / t)
        self.tickinfo.config(text=f"""Tick Epoch: {self.parent.ticks}
Uptime: {int(t * 1000)}ms since startup
Avg TPS: {c} (Target: {self.parent.tps})
Tick DeltaTime: {self.parent.deltatime}""", font=("Courier", 14))
        self.tk.after(1, self._tickman_update)

    def _tickman_graph_update(self):
        self.graph_x += self.graph_x_factor
        #self.statusgraph.create_line(self.graph_x, 10, self.graph_x + 1, 10, fill="red")

        asdf = round(((1 / self.parent.deltatime) / (self.parent.tps + int(self.parent.tps * 0.5))) * 100)
        self.points.append(asdf)

        p = int((self.parent.fps_deltatime / self.parent._epoch_fps) * 30)
        self.fps_points.append(p)

        if self.graph_x > 700: 
            self.points.pop(0)
            self.fps_points.pop(0)

        self.statusgraph.delete("all")

        color = ["red", "blue"]
        n = 0

        for x in range(1, len(self.points)):
            n = 0
            for pt in [self.points, self.fps_points]:
                point_a = 100 - pt[x - 1]
                point_b = 100 - pt[x]

                self.statusgraph.create_line((x - 1) * self.graph_x_factor, point_a, x * self.graph_x_factor, point_b, fill=color[n])

                n += 1

        self.last = asdf
        self.tk.after(10, self._tickman_graph_update)

        

    def _workspace_property_dfs(self, start, fr, path):
        #print(start)

        if not isinstance(start, (dict, list)):
            return

        ind = 0
        r = list(path)

        for i in start:
            self._ws_prop_iid += 1

            if isinstance(start, list):
                bb = f"ListIndex({ind})<{i.__class__.__name__}> = {i}"
                item = i
                ind += 1
                r.append(ind)

            elif isinstance(start, dict):
                if isinstance(start[i], list):
                    bb = f"{i}<{start[i].__class__.__name__}> = [Iterable List({len(start[i])})]"
                elif isinstance(start[i], dict):
                    bb = f"{i}<{start[i].__class__.__name__}> = [Iterable Dict({len(start[i])})]"
                else:
                    bb = f"{i}<{start[i].__class__.__name__}> = {start[i]}"
                item = start[i]
                nam = start[i].__class__.__name__
                r.append(i)

            self.m[self._ws_prop_iid] = item
            self.wspath[self._ws_prop_iid] = r

            # if isinstance(item, (dict, list)):
            #     bb = "..."
            self.info.insert('', tk.END, text=bb, open=False, iid=self._ws_prop_iid)
            self.info.move(self._ws_prop_iid, fr, 2147483647)
            self._workspace_property_dfs(item, self._ws_prop_iid, r)

    def _workspace_property_change(self, e):
        stuff = self.m[int(self.info.focus())]

        if not isinstance(stuff, (int, float, str, Dimension, Vector)):
            tkmsg.showinfo(f"Unable to edit property", f"The debugger cannot edit the property because the type {stuff.__class__.__name__} is not supported.")
            return

        self.editor = DebugPropertyEditor(self, self.q[int(self.explorer.focus())], self.wspath[int(self.info.focus())])

    def _workspace_select(self, e):
        self.info.pack_forget()

        stuff = self.q[int(self.explorer.focus())]
        if self.lastLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL != None:
            self.lastLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.debug_unhighlight()
        stuff.debug_highlight()
        self.lastLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL = stuff


        self.info = ttk.Treeview(self.data_viewer)
        self.info.heading("#0", text=f"Browsing properties for element {stuff.__class__.__name__}")
        self.info.grid(row=0, column=0, sticky="nesw")
        self.data_viewer.rowconfigure(0, weight=1)
        self.data_viewer.columnconfigure(0, weight=1)

        self.info.bind("<Double-1>", self._workspace_property_change)

        self._ws_prop_iid = 0

        self.m = {}

        for i in sorted(stuff.__dict__):
            thing = stuff.__dict__[i]
            if isinstance(thing, list):
                bb = f"[Iterable List({len(thing)})]"
            elif isinstance(thing, dict):
                bb = f"[Iterable Dict({len(thing)})]"
            else:
                bb = str(thing)
            self.info.insert('', tk.END, text=f"{i}<{thing.__class__.__name__}> = {bb}", open=False, iid=self._ws_prop_iid)
            self.m[self._ws_prop_iid] = thing
            self.wspath[self._ws_prop_iid] = [i]
            self._workspace_property_dfs(thing, self._ws_prop_iid, [i])
            self._ws_prop_iid += 1


    def _workspace_dfs(self, next, fr):

        self._workspace_iid += 1
        c = int(self._workspace_iid)

        self.explorer.insert('', tk.END, text=next.__class__.__name__, open=False, iid=self._workspace_iid)
        self.q[self._workspace_iid] = next
        self.explorer.move(self._workspace_iid, fr, 2147483647)



        for i in next.children:
            self._workspace_dfs(i, c)




    def _call_callevent(self, event, obj, func, kill=False, special=None):
        
        if kill:
            self._ekps += 1
            return

        if special is None:
            if func.debug_del is None: return
            self.await_push.append(func)

        if special == 0: # register

            event.debug_del = self.event.insert("", 'end', values=(
                datetime.datetime.now().strftime("%H:%m:%S.%f"),
                event.type,
                event.belong_group,
                f"{func.function.__module__}:{inspect.findsource(func.function)[1]}",
                True,
                event.event_id
            ))
            return
        elif special == 1: #unregister
            if event.debug_del is not None:
                self.event.delete(event.debug_del)
            return






        # if self.event_update:
        #     e = list(EventType.__dict__)[list(EventType.__dict__.values()).index(event)]
        #     self.await_push.append([
        #         datetime.datetime.now().strftime("%H:%m:%S.%f"),
        #         e,
        #         f"{func.function.__module__}:{inspect.findsource(func.function)[1]}"
        #     ])
        #     self.event_iid += 1


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
        self.insttps.config(text=f"Instantaneous TPS: {self.parent.t}")
        self.parent.t = 0
        
        self._obj_guide.config(text=f"C: {len(self.parent.children)} / E: {len(self.parent.objects)} / R: {self.parent.window._blits}")
        self.parent.window._blits = 0

        self._event_monitor.config(text=f"Events: {get_registered_events()} / Suspended: ? / EPS: {self._eps} / KPS: {self._ekps}")
        self._ekps = 0

        self.tk.after(1000, self._tick_tps_op)

    def _tick_packeting_op(self):
        if isinstance(self.parent.client, DedicatedClient):
            if self.parent.client.connected:
                self._network.config(text=f"rx: {self.parent.client._rx}, tx: {self.parent.client._tx}, loss: {self.parent.client._loss} ({round((self.parent.client._loss / max(1, self.parent.client._tx)) * 100, 2)}%) / {int(self.parent.client.latency * 1000)}ms")
                self.parent.client._rx = 0
                self.parent.client._tx = 0
                self.parent.client._loss = 0
            else:
                self._network.config(text=f"Networking: Not connected to server")
        else:
            self._network.config(text=f"Networking: No connection established")

        self.tk.after(1000, self._tick_packeting_op)

    def _tick_event_update(self):
        for i in self.await_push:
            if i.type is None or i.belong_group is None or i.function is None or i.event_id is None: continue
            self.event.item(i.debug_del, values=(
                datetime.datetime.now().strftime("%H:%m:%S.%f"),
                i.type,
                i.belong_group,
                f"{i.function.__module__}:{inspect.findsource(i.function)[1]}",
                True,
                i.event_id
            ))
        self.await_push = []

        self.tk.after(100, self._tick_event_update)

    def _tick_event_update_sec(self):
        self.eps = self._eps
        self._eps = 0


    def _run(self):
        self.tk.focus_force()

        if not self.opened:
            self.tk.after(1000, self._tick_fps_op)
            self.tk.after(1000, self._tick_tps_op)
            self.tk.after(1000, self._tick_packeting_op)
            self.tk.after(1, self._tick_event_update)
            self.tk.after(1000, self._tick_event_update_sec)
            self.tk.after(1, self._tickman_update)
            self.tk.after(100, self._tickman_graph_update)
                

            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.opened = True

        if not self.display:
            self.display = True
            self.tk.deiconify()

    def run(self):
        self.run_thread = threading.Thread(target=self._run)
        self.run_thread.start()

            