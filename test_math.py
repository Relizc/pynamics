import pynamics_legacy as pn
import time

ctx = pn.GameManager(pn.Dim(800, 400), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dimension(800, 400))
camera = pn.ViewPort(window, position=pn.Dimension(0, 0))

bob = pn.Particle(ctx, 20, 380, use_gravity=False, gravity=-0.08)

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_RIGHT))
def push(self, key):
    bob.use_gravity = True
    bob.add_velocity(pn.Vector(60, 10))
    time.sleep(1)
    bob.delete()
    

@bob.add_event_listener(event=pn.EventType.COLLIDE)
def kill():
    pass

ctx.start()

