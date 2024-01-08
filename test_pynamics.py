import pynamics
import time
import random

ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)



bob1 = pynamics.GameObject(ctx, 10, 10, 10, 10)
thisTime = time.time()
bob = pynamics.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                           from_points=(((0, 0), (0, 100)),
                                        ((0, 100), (100, 100)),
                                        ((100, 100), (100, 50)),
                                        ((100, 50), (50, 50)),
                                        ((50, 50), (50, 0)),
                                        ((50, 0), (0, 0))
                                        ))
nooo= pynamics.PhysicsBody(ctx, 100, 300, 100, 100, 2,
                           from_points=(((0, 0), (0, 100)),
                                        ((0, 100), (100, 100)),
                                        ((100, 100), (100, 50)),
                                        ((100, 50), (50, 50)),
                                        ((50, 50), (50, 0)),
                                        ((50, 0), (0, 0))
                                        ), use_gravity=False,
                                        use_mass=False)

#

bob2 = pynamics.PhysicsBody(ctx, 500, 750, 1000, 1000, 2, use_gravity=False,use_mass=False
                           )
bob.rectitude = 0.5
nooo.rectitude = 0.5

def condition():
    global thisTime
    if time.time() - thisTime >= 3:
        return True
    else:
        return False


@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_UP))
def listen(self):
    # bob.apply_force(pynamics.Vector2d(90, 1),ctx._epoch_tps)
    bob.add_force(pynamics.Vector2d(90, 1))


@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_DOWN))
def listen(self):
    # bob.apply_force(pynamics.Vector2d(270, 1),ctx._epoch_tps)
    bob.add_force(pynamics.Vector2d(270, 1))


@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_LEFT))
def listen(self):
    # bob.apply_force(pynamics.Vector2d(180, 1),ctx._epoch_tps)
    bob.add_force(pynamics.Vector2d(180, 1))


@ctx.add_event_listener(event=pynamics.EventType.KEYHOLD, condition=pynamics.KeyEvaulator(pynamics.K_RIGHT))
def listen(self):
    # bob.apply_force(pynamics.Vector2d(0, 1),10)
    bob.add_force(pynamics.Vector2d(0, 1))


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_r))
def listen(self):
    camera.position = camera.position.add(0, 10)



print(ctx.children)
ctx.start()
print("killed")
