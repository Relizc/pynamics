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


@ctx.add_tick_update
def q():
    pynamics.GameObject(ctx, random.randint(0, 100), random.randint(0, 100), 10, 10)


@ctx.add_event_listener(eventtype=pynamics.EventType.APRESSED)
def listen():
    print("i did stuff")


print(ctx.children)

ctx.start()
print("killed")
