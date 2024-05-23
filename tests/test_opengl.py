import pynamics_legacy as pn

ctx = pn.GameManager(pn.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pn.OpenGLWindow(ctx)

bob1 = pn.GameObject(ctx, 10, 10, 10, 10)

ctx.start()
