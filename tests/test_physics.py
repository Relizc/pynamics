import pynamics_legacy as pn
import random

ctx = pn.GameManager(pn.Dim(700, 700), tps=32, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(700, 700))

# rigid = pn.RigidBody(ctx, 50, 50, points=[(0, 10), (10, 0), (0, -10), (-10, 0)])
a = pn.PhysicsBody(ctx, x=50, y=50, use_gravity=False, width=100, height=100)
b = pn.PhysicsBody(ctx, x=400, y=50, use_gravity=False, width=100, height=100, mass=1)

wall = pn.PhysicsBody(ctx, x=650, y=-10, use_gravity=False, width=100, height=1000, mass=1)


a.init_movement(3)

ctx.start()
