import pynamics
import time
import random

ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128)
window = pynamics.ProjectWindow(ctx, size=pynamics.Dim(1000, 1000))
camera = pynamics.ViewPort(window)

bob1 = pynamics.GameObject(ctx, 10, 10, 10, 10)
thisTime = time.time()
bob = pynamics.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                           from_points=(((0, 0), (100, 100))
                                        , ((100, 100), (50, 100))
                                        , ((50, 100), (0, 0))
                                        ))

def condition():
    global thisTime
    if time.time() - thisTime >= 3:
        return True
    else:
        return False


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_UP))
def listen(self):
    bob.apply_force(pynamics.Vector2d(90, 1), 0.1)


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_DOWN))
def listen(self):
    bob.apply_force(pynamics.Vector2d(270, 1), 0.1)


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_LEFT))
def listen(self):
    bob.apply_force(pynamics.Vector2d(180, 1), 0.1)


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_RIGHT))
def listen(self):
    bob.apply_force(pynamics.Vector2d(0, 1), 0.1)

@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_r))
def listen(self):
    bob.position.set(10, 10)
    bob.clear()

@ctx.add_event_listener(event=pynamics.EventType.TICK)
def a(self):
    #print(bob.velocity)
    pass


print(ctx.children)

ctx.start()
print("killed")
