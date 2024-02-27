import pynamics as pn
import random
import winsound

import time

MIN_VERSION = "1.0.0"

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)
view = pn.ProjectWindow(ctx, size=pn.Dim(960, 540), title="Suberb Game")

winsound.PlaySound("effect1.wav", winsound.SND_ASYNC)
log = pn.Image(ctx, path="resource1.png", ratio=3, x=388, y=202)

@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(self):
    time.sleep(4.5)

    winsound.PlaySound("swsh.wav", winsound.SND_ASYNC)
    ani = pn.Animation(pn.CubicBezier(.55,-0.9,.57,.93), duration=128, fields=["y"])
    ani.play(log.position, [1000])

    time.sleep(3)
    ani = pn.Animation(pn.CubicBezier(0, 0, 0.58, 1), duration=32, fields=["r", "g", "b"])
    ani.play(view.color, [0, 0, 0])

    time.sleep(0.8)

    tit = pn.Image(ctx, path="title.png", ratio=3, x=392, y=-100)
    tit2 = pn.Image(ctx, path="playbtn.png", ratio=0.1, x=420, y=600)
    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=32, fields=["y"]).play(tit.position, [80])
    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=32, fields=["y"]).play(tit2.position, [190])

    time.sleep(0.5)
    winsound.PlaySound("opening.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

    ctx.aa = 0
    ctx.b = 0

    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=64 * 5, fields=["r", "g", "b"]).play(view.color, [3, 0, 46])

    @ctx.add_event_listener(event=pn.EventType.TICK)
    def t(self):
        ctx.aa += 1

        if ctx.aa == 64 * 5:

            if ctx.b == 1:
                pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=64 * 5, fields=["r", "g", "b"]).play(view.color,
                                                                                                           [3, 0, 46])
                ctx.b = 0
            else:
                pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=64 * 5, fields=["r", "g", "b"]).play(view.color,
                                                                                                           [0, 0, 0])
                ctx.b = 1

            ctx.aa = 0


ctx.start()
