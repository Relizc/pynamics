import pynamics
import time
ctx = pynamics.GameManager(pynamics.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx, color="black")

obj = pynamics.RigidBody(ctx, x=50, y=50, points=[(0, 10), (10, 0), (0, -10), (-10, 0)])

ctx.start()

