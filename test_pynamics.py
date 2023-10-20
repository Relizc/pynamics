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


@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_UP))
def listen(self):
    bob.position.y -= 1

@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_DOWN))
def listen(self):
    bob.position.y += 1

@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_LEFT))
def listen(self):
    bob.position.x -= 10

@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_RIGHT))
def listen(self):
    bob.position.x += 10

@ctx.add_event_listener(event=pynamics.EventType.FRAME)
def frame(self):
    print(f"Welcome to frame {self}")

@ctx.add_event_listener(event=pynamics.EventType.TICK)
def frame(self):
    print(f"Welcome to tick {self}")


print(ctx.children)

ctx.start()
print("killed")
