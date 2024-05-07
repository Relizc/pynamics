import pynamics_legacy as pn
import time

ctx = pn.GameManager(pn.Dim(800, 400), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dimension(800, 400))
camera = pn.ViewPort(window, position=pn.Dimension(0, 0))

#bob = pn.Particle(ctx, 20, 380, use_gravity=False, gravity=-0.08)

n = 0

@ctx.add_event_listener(event=pn.EventType.TICK)
def push(self):
    global n
    n += 1
    if n == 32:
        x = pn.Particle(ctx, 10, 10, use_gravity=True)
        x.velocity = pn.Vector(-30, 5)
        pass

    
ctx.start()
