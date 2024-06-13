import pynamics
import time
import random

<<<<<<< HEAD
ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ewPort(window)

bob1 = pynamics.GameObject(ctx, 10, 10, 10, 10)
thisTime = time.time()
bob = pynamics.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                           from_points=(((0, 0), (100, 100))
=======
ctx = pynamics_legacy.GameManager(pynamics_legacy.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics_legacy.ProjectWindow(ctx)

bob = pynamics_legacy.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                                  from_points=(((0, 0), (100, 100))
>>>>>>> d3fa84cf6eb02090645329182a3e30720bff79a0
                                        , ((100, 100), (50, 100))
                                        , ((50, 100), (0, 0))
                                        ), use_gravity= False)

bob2 = pynamics.PhysicsBody(ctx, 100, 500, 100, 100, 5, use_mass=False, from_points=(
    ((0,0),(10000,0)),
    ((0,0),(0,10000)),
))
bob.velocity.add(pynamics.dimensions.Vector2d(-45, 1))
ctx.start()