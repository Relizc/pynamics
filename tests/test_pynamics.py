import pynamics_legacy
import time
import random

ctx = pynamics_legacy.GameManager(pynamics_legacy.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics_legacy.ProjectWindow(ctx)


bob = pynamics_legacy.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                                  from_points=(((0, 0), (0, 100)),
                                        ((0, 100), (100, 100)),
                                        ((100, 100), (100, 50)),
                                        ((100, 50), (50, 50)),
                                        ((50, 50), (50, 0)),
                                        ((50, 0), (0, 0))
                                        ))
nooo= pynamics_legacy.PhysicsBody(ctx, 300, 100, 100, 100, 2,
                                  from_points=(((0, 0), (0, 100)),
                                        ((0, 100), (100, 100)),
                                        ((100, 100), (100, 50)),
                                        ((100, 50), (50, 50)),
                                        ((50, 50), (50, 0)),
                                        ((50, 0), (0, 0))
                                        ))

nooo.bugid = 1
bob.bugid = 2
#hi = pynamics_legacy.Text(ctx, 100, 100, "Loser")

#

bob2 = pynamics_legacy.PhysicsBody(ctx, 500, 750, 1000, 1000, 2, use_gravity=False, use_mass=False
                                   )
bob.rectitude = 1
nooo.rectitude = 1

def condition():
    global thisTime
    if time.time() - thisTime >= 3:
        return True
    else:
        return False


@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_UP))
def listen(self, key):
    # bob.apply_force(pynamics_legacy.Vector2d(90, 1),ctx._epoch_tps)
    bob.add_force(pynamics_legacy.Vector2d(90, 1))


@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_DOWN))
def listen(self, key):
    # bob.apply_force(pynamics_legacy.Vector2d(270, 1),ctx._epoch_tps)
    bob.add_force(pynamics_legacy.Vector2d(270, 1))


@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_LEFT))
def listen(self, key):
    # bob.apply_force(pynamics_legacy.Vector2d(180, 1),ctx._epoch_tps)

    bob.add_force(pynamics_legacy.Vector2d(180, 1))


@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_RIGHT))
def listen(self, key):
    # bob.apply_force(pynamics_legacy.Vector2d(0, 1),10)
    bob.add_force(pynamics_legacy.Vector2d(0, 1))


@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYDOWN, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_r))
def listen(self, key):
    bob.position.set(10, 10)
    bob.velocity.clear()



print(ctx.children)
ctx.start()
print("killed")
