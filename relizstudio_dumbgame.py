import pynamics as pn

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
camera = pn.ViewPort(window)

shield = pn.Image(ctx, 250, 250, path="shield.jpeg", width=100, height=100, rotation=10)

@ctx.add_event_listener(event=pn.EventType.TICK)
def tick(self):
    shield.rotation += 5
    print(shield.rotation)

ctx.start()