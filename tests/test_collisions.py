import pynamics
import time
import random

ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ewPort(window)

bob1 = pynamics.GameObject(ctx, 10, 10, 10, 10)
thisTime = time.time()
bob = pynamics.PhysicsBody(ctx, 100, 100, 100, 100, 2,
                           from_points=(((0, 0), (100, 100))
                                        , ((100, 100), (50, 100))
                                        , ((50, 100), (0, 0))
                                        ), use_graty= False)

bob2 = pynamics.PhysicsBody(ctx, 100, 500, 100, 100, 5, use_mass=False, from_points=(
    ((0,0),(10000,0)),
    ((0,0),(0,10000)),
))
bob.velocity.add(pynamics.dimensions.Vector2d(-45, 1))
ctx.start()