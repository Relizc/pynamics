import pynamics_legacy as pn
import random

ctx = pn.GameManager(pn.Dim(700, 700), tps=64, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(700, 700))

body = pn.RigidBody(ctx, x=200, y=200, points=[(-10, -10), (10, -50), (65, 10), (-10, 10), (-10, -10)], angular_velocity=0.01, use_gravity=True,
                    rectitude=0.8)
body.init_movement(5)

ctx.start()