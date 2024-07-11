import winsound
import pynamics as pn

ctx = pn.GameManager(dimensions=pn.Dim(256, 240), event_tracker=True, tps=128)
view = pn.ProjectWindow(ctx, size=pn.Dim(512, 480), title="Music Test", color="black", scale=2)

winsound.PlaySound("ruruskaado.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

ctx.start()