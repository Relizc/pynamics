import pynamics as pn
import time

ctx = pn.GameManager(pn.Dim(500, 500), tps=4, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
camera = pn.ViewPort(window)

circle61 = pn.Particle(ctx, 80, 10, 10, use_gravity=False, rectitude=1, clear_blit=True, styles={"fill": "green"})
circle61.init_movement()

circle62 = pn.Particle(ctx, 100, 10, 10, use_gravity=False, rectitude=1, clear_blit=True)

# @circle61.add_event_listener(event=pn.EventType.PHYSICS_COLLIDE)
# def hit(self):
#     self.r += 1

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_r))
def listen(self):
    circle61.position.set(10, 10)
    circle61.clear()

ctx.start()