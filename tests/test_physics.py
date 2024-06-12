import pynamics_legacy as pn
import random

ctx = pn.GameManager(pn.Dim(700, 700), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(700, 700))

rigid = pn.RigidBody(ctx, 50, 50, points=[(0, 10), (10, 0), (0, -10), (-10, 0)])

ctx.start()
