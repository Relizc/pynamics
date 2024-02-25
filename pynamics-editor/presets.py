

MAIN = """import pynamics_1_0_0 as pn

MIN_VERSION = "1.0.0"

ctx = pn.GameManager(dimensions=pn.Dim(500, 500), event_tracker=False)
view = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))

ctx.start()
"""