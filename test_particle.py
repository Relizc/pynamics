import pynamics as pn

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(800, 450))
camera = pn.ViewPort(window)

ctx.set_title("Clicker")

middle = pn.Image(ctx, 400, 225, path="image.png")
@middle.add_event_listener(event=pn.EventType.HOVER)
def move(self):
    pass

ctx.start()