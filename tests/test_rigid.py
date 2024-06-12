import pynamics_legacy as pn
import random

ctx = pn.GameManager(pn.Dim(700, 700), tps=32, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(700, 700))

body = pn.RigidBody(ctx, x=20, y=20, points=[(-10, -10), (10, -10), (10, 10), (-10, 10), (-10, -10)])

ctx.start()