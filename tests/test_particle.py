import pynamics_legacy as pn
import time

import pickle

ctx = pn.GameManager(pn.Dim(800, 800), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(800, 800))

circle61 = pn.Particle(ctx, 80, 10, 200, use_gravity=True, rectitude=0.5, clear_blit=True, mass=10, color="green transparent")
circle61.init_movement(10)

circle62 = pn.Particle(ctx, 100, 10, 10, use_gravity=True, rectitude=0.8, clear_blit=True, mass=10)

# @circle61.add_event_listener(event=pn.EventType.PHYSICS_COLLIDE)
# def hit(self):
#     self.r += 1

title = pn.Text(ctx, x=400, y=50)

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_r))
def listen(self, key):
    circle61.position.set(10, 10)
    circle61.clear()
    

print(pickle.dumps(listen))

ctx.start()