import pynamics, time

ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)
bob1 = pynamics.GameObject(ctx, 10, 10, 10, 10,from_points=pynamics.load_object_from_binary("output/object.obj"))
curTime = time.time()
count = 1


@ctx.add_event_listener(event=pynamics.EventType.TICK)
def checkfordel(self):
    global curTime, count
    if time.time() - curTime > 1:
        if count == 1:
            bob1.hide()
        else:
            bob1.unhide()
        curTime = time.time()
        count *= -1


ctx.start()
