import pynamics as pn

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
camera = pn.ViewPort(window)

circle61 = pn.Particle(ctx, 10, 10, 5, use_gravity=False)
circle61.init_movement(0.1)

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_r))
def listen(self):
    circle61.position.set(10, 10)
    circle61.clear()

ctx.start()