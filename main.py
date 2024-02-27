import pynamics as pn
import random
import winsound

import time

MIN_VERSION = "1.0.0"

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)
view = pn.ProjectWindow(ctx, size=pn.Dim(960, 540), title="Suberb Game")

winsound.PlaySound("effect1.wav", winsound.SND_ASYNC)
log = pn.Image(ctx, path="resource1.png", ratio=3, x=388, y=202)

x = pn.Particle(ctx, rectitude=0.91, x=480, y=270, no_display=True)
x.velocity.r = random.randint(0, 180)
x.velocity.f = random.randint(0, 20)

@ctx.add_event_listener(event=pn.EventType.STARTUP)
def move(this):
    @ctx.add_event_listener(event=pn.EventType.TICK, killafter=100*2)
    def c(a):
        log.position.x = x.x
        log.position.y = x.y
    time.sleep(2)

    ani = pn.Animation(pn.CubicBezier(.17,.67,.62,.97), duration=100, fields=["x", "y"])
    ani.play(log.position, [388, 202])


@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(self):
    time.sleep(4.5)

    winsound.PlaySound("swsh.wav", winsound.SND_ASYNC)
    ani = pn.Animation(pn.CubicBezier(.55,-0.9,.57,.93), duration=128, fields=["y"])
    ani.play(log.position, [1000])

    time.sleep(3)
    ani = pn.Animation(pn.CubicBezier(0, 0, 0.58, 1), duration=32, fields=["r", "g", "b"])
    ani.play(view.color, [135, 206, 235])

    time.sleep(0.8)

    font = pn.TextFont("Courier", color="black", size=8)

    tit = pn.Image(ctx, path="title.png", ratio=3, x=392, y=-100)
    tit2 = pn.Image(ctx, path="playbtn.png", ratio=0.1, x=420, y=600)

    tex = pn.Text(ctx, text="Copyright 2024 DumbAbra Studio", x=480, y=910,
                  font=font, zindex=99)

    ctx.make_scroll = True

    @tit2.add_event_listener(event=pn.EventType.ONCLICK)
    def click(self):
        backbtn = pn.Image(ctx, path="backbtn.png", ratio=2, x=1000, y=10)

        serv = pn.Image(ctx, path="btn.png", width=400, height=80, x=1000, y=100)
        servtxt = pn.Text(ctx, text="Singleplayer (Demo)", font=pn.TextFont("Courier", color="white", size=16), zindex=99, x=1200, y=140)

        @serv.add_event_listener(event=pn.EventType.ONCLICK)
        def c(self):
            for i in ctx.kk:
                if i.y < 100:
                    pn.Animation(pn.CubicBezier(.44,-0.51,.63,.79), duration=64, fields=["y"]).play(i.position, [-100])
                else:
                    pn.Animation(pn.CubicBezier(.44, -0.51, .63, .79), duration=64, fields=["y"]).play(i.position,
                                                                                                       [600])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(backbtn.position, [-600])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv.position, [-400])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(servtxt.position, [-200])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2.position, [-400])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2txt.position, [-200])
            ctx.make_scroll = False
            time.sleep(1.5)
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=128, fields=["r", "g", "b"]).play(view.color, [0, 0, 0])
            backbtn.delete()
            serv.delete()
            servtxt.delete()
            serv2.delete()
            serv2txt.delete()
            for i in ctx.kk:
                i.delete()
            game()

        serv2 = pn.Image(ctx, path="btn.png", width=400, height=80, x=1000, y=260)
        serv2txt = pn.Text(ctx, text="Multiplayer (Demo)", font=pn.TextFont("Courier", color="white", size=16), zindex=99, x=1200, y=300)

        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(backbtn.position, [10])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv.position, [280])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(servtxt.position, [480])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2.position, [280])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2txt.position, [480])
        @backbtn.add_event_listener(event=pn.EventType.ONCLICK)
        def back(self):
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(backbtn.position, [1000])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv.position, [1000])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(servtxt.position, [1200])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2.position, [1000])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2txt.position, [1200])



            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(tit.position, [392])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(tit2.position, [420])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(tex.position, [480])

            time.sleep(1.5)
            backbtn.delete()
            serv.delete()
            servtxt.delete()
            serv2.delete()
            serv2txt.delete()

        pn.Animation(pn.CubicBezier(.13,.7,.5,.93), duration=64, fields=["x"]).play(tit.position, [-300])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(tit2.position, [-300])
        pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(tex.position, [-300])



    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=32, fields=["y"]).play(tit.position, [80])
    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=32, fields=["y"]).play(tit2.position, [190])
    pn.Animation(pn.CubicBezier(.0, 0, 0.58, 1), duration=32, fields=["y"]).play(tex.position, [500])

    time.sleep(0.5)
    winsound.PlaySound("opening.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

    ctx.aa = 0
    ctx.b = 0

    ctx.kk = []

    @ctx.add_event_listener(event=pn.EventType.TICK)
    def t(self):

        if not ctx.make_scroll:
            self.terminate()
        k = random.randint(0, 256)
        if k == 256:
            i = pn.Image(ctx, path="building0.png", ratio=3, x=1000, y=450, zindex=-1)
            pn.Animation(pn.CubicBezier(0, 0, 1, 1), duration=128*3, fields=["x"]).play(i.position, [-200])
            ctx.kk.append(i)
        if k == 147:
            i = pn.Image(ctx, path="building1.png", ratio=5, x=1000, y=400, zindex=-1)
            pn.Animation(pn.CubicBezier(0, 0, 1, 1), duration=128 * 3, fields=["x"]).play(i.position, [-200])
            ctx.kk.append(i)
        if k == 15:
            i = pn.Image(ctx, path="building2.png", ratio=4, x=1000, y=420, zindex=-1)
            pn.Animation(pn.CubicBezier(0, 0, 1, 1), duration=128 * 3, fields=["x"]).play(i.position, [-200])
            ctx.kk.append(i)
        cc = random.randint(0, 400)
        if cc == 231:
            i = pn.Image(ctx, path=f"building{random.randint(3, 4)}.png", ratio=4, x=1000, y=20 + random.randint(-10, 50), zindex=-1)
            pn.Animation(pn.CubicBezier(0, 0, 1, 1), duration=128 * 8, fields=["x"]).play(i.position, [-200])
            ctx.kk.append(i)

    @ctx.add_event_listener(event=pn.EventType.TICK)
    def check(self):
        if not ctx.make_scroll:
            self.terminate()
        n = list(ctx.kk)
        for i in ctx.kk:
            if i.x < -100:
                i.delete()
                n.remove(i)
        ctx.kk = n

def game():
    print("game start")

ctx.start()
