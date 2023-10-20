import pynamics
import time
import random

ctx = pynamics.GameManager(pynamics.Dim(1000, 1000), tps=128)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)

bob = pynamics.GameObject(ctx, 10, 10, 10, 10)
thisTime = time.time()


def condition():
    global thisTime
    if time.time() - thisTime >= 3:
        return True
    else:
        return False





@ctx.add_event_listener(eventtype=pynamics.EventType.APRESSED)
def listen():
    bob.position.x-=1


print(ctx.children)

ctx.start()
print("killed")
