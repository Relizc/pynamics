import pynamics as pn
import os

os.environ["PN_WINDOW_MODE"] = "legacy"

import mainloop
ctx = pn.GameManager(dimensions=pn.Dim(256, 240), event_tracker=True, tps=128)
view = pn.ProjectWindow(ctx, size=pn.Dim(512, 480), title="Megaman 2", color="black", scale=2)

@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(e):
    mainloop.mainloop(ctx, view)



ctx.start()