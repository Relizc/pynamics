import pynamics as pn
import random
import winsound
import math

import time

MIN_VERSION = "1.0.0"

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)

ctx.ADDRESS = "127.0.0.1"
ctx.PORT = 11027

view = pn.ProjectWindow(ctx, size=pn.Dim(960, 540), title="Suberb Game")

# winsound.PlaySound("effect1.wav", winsound.SND_ASYNC)
# log = pn.Image(ctx, path="resource1.png", ratio=3, x=388, y=202)

# x = pn.Particle(ctx, rectitude=0.91, x=480, y=270, no_display=True)
# x.velocity.r = random.randint(0, 180)
# x.velocity.f = random.randint(0, 20)

# @ctx.add_event_listener(event=pn.EventType.STARTUP)
# def move(this):
#     @ctx.add_event_listener(event=pn.EventType.TICK, killafter=100*2)
#     def c(a):
#         log.position.x = x.x
#         log.position.y = x.y
#     time.sleep(2)
#
#     ani = pn.Animation(pn.CubicBezier(.17,.67,.62,.97), duration=100, fields=["x", "y"])
#     ani.play(log.position, [388, 202])


@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(self):
    # time.sleep(4.5)

    # winsound.PlaySound("swsh.wav", winsound.SND_ASYNC)
    # ani = pn.Animation(pn.CubicBezier(.55,-0.9,.57,.93), duration=128, fields=["y"])
    # ani.play(log.position, [1000])
    #
    # time.sleep(3)
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

        @serv2.add_event_listener(event=pn.EventType.ONCLICK)
        def r(self):

            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(backbtn.position, [-600])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv.position, [-400])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(servtxt.position, [-200])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2.position, [-400])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(serv2txt.position, [-200])


            con = pn.Image(ctx, path="btn.png", width=500, height=300, x=1000, y=120)
            conne = pn.Text(ctx, text=f"Connecting to {ctx.ADDRESS}:{ctx.PORT}", font=pn.TextFont("Courier", color="white", size=12), zindex=99, x=1250, y=200)
            conne.dots = 0
            conne.age = 0
            @ctx.add_event_listener(event=pn.EventType.TICK)
            def momom(self):
                conne.age += 1
                if conne.age == 64:
                    conne.age = 0
                    conne.text = f"Connecting to {ctx.ADDRESS}:{ctx.PORT}" + (conne.dots % 4) * "."
                    conne.dots += 1
            time.sleep(1)
            winsound.PlaySound(None, winsound.SND_PURGE)
            time.sleep(0.5)
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(con.position, [230])
            pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(conne.position, [480])

            ctx.CLIENT = pn.DedicatedClient(ctx, address=ctx.ADDRESS, port=ctx.PORT)
            @ctx.CLIENT.add_event_listener(event=pn.EventType.CLIENT_CONNECTED)
            def done(event):
                time.sleep(2)
                ctx.make_scroll = False
                for i in ctx.kk:
                    if i.y < 100:
                        pn.Animation(pn.CubicBezier(.44, -0.51, .63, .79), duration=64, fields=["y"]).play(i.position,
                                                                                                           [-100])
                    else:
                        pn.Animation(pn.CubicBezier(.44, -0.51, .63, .79), duration=64, fields=["y"]).play(i.position,
                                                                                                           [600])
                pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(con.position, [-500])
                pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=64, fields=["x"]).play(conne.position, [-250])
                time.sleep(1.5)
                pn.Animation(pn.CubicBezier(.13, .7, .5, .93), duration=128, fields=["r", "g", "b"]).play(view.color,
                                                                                                          [0, 0, 0])
                winsound.PlaySound(None, winsound.SND_PURGE)
                backbtn.delete()
                serv.delete()
                servtxt.delete()
                serv2.delete()
                serv2txt.delete()
                for i in ctx.kk:
                    i.delete()
                game(True)

            ctx.CLIENT.join_server()


            winsound.PlaySound("connecting_fromsonic.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

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
        cc = random.randint(0, 200)
        if cc == 100:
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

PLAYER = None

def load_level():
    mid = pn.Text(ctx, x=480, y=270, text=f"Superb Universe {ctx.CODE}-{ctx.NUM}", font=pn.TextFont("Courier", size=12, color="white"))
    mid2 = pn.Text(ctx, x=480, y=290, text="\"I'VE BEEN THIS PLACE A THOUSAND TIMES\" - Dr.Waddy", font=pn.TextFont("Courier", size=8, color="white"))
    time.sleep(0.5)
    winsound.PlaySound("ingame.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
    time.sleep(1)

    pn.Animation(pn.CubicBezier(.17,.67,.46,.9), duration=128, fields=["y"]).play(mid.position, [530])
    pn.Animation(pn.CubicBezier(.17,.67,.46,.9), duration=128, fields=["y"]).play(mid2.position, [550])
    time.sleep(1.5)
    mid2.delete()
    time.sleep(0.5)

    heart = pn.Image(ctx, x=20, y=-110, width=50, height=50, path="heart.png")
    health = mid = pn.Text(ctx, x=100, y=-110, text="100", font=pn.TextFont("Courier", size=24, color="white"))
    pn.Animation(pn.CubicBezier(.17,.67,.46,.9), duration=128, fields=["y"]).play(heart.position, [20])
    pn.Animation(pn.CubicBezier(.17,.67,.46,.9), duration=128, fields=["y"]).play(health.position, [45])

    global PLAYER
    PLAYER = pn.TopViewPhysicsBody(ctx, x=100, y=270, width=50, height=50, mass=5, color="white")
    PLAYER.init_movement()

    for i in OTHER_PLAYERS:
        OTHER_PLAYERS[i].hidden = False


    @ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator("space"))
    def shoot(self, key):
        dx, dy = ctx.mouse.x - PLAYER.position.x - 25, ctx.mouse.y - PLAYER.position.y - 25
        angle = -math.degrees(math.atan2(dy, dx))
        for i in range(1):
            x = pn.TopViewPhysicsBody(ctx, x=PLAYER.position.x + 25, y=PLAYER.position.y + 25, color="white",
                                      use_airress=False)
            x.velocity = pn.Vector(angle, 2)
            x.velocity.add_self(PLAYER.velocity)
            x.destroy_outside_boundary = True

        winsound.PlaySound("shoot.wav", winsound.SND_ASYNC)


@pn.PacketId(0x70)
class SendUniverseData(pn.Packet):

    def handle(self, parent, connection, ip):
        code = self.read_string()
        num = self.read_varint()
        ctx.CODE = code
        ctx.NUM = num

@pn.PacketId(0x71)
class SendMovementData(pn.Packet):

    def handle(self, parent, connection, ip):
        usr = self.read_UUID()
        dir = self.read_varint()
        mode = self.read_bool()
        print(usr, mode, dir, parent.uuid)
import uuid

OTHER_PLAYERS = {}
@pn.PacketId(0x72)
@pn.PacketFields(uuid.UUID, str)
class SendUserJoined(pn.Packet):

    def handle(self, parent, connection, ip):
        global OTHER_PLAYERS
        usr = self.read_UUID()
        nam = self.read_string()


        p = pn.TopViewPhysicsBody(ctx, x=100, y=270, width=50, height=50, mass=5, color="white")
        p.hidden = True
        p.init_movement()
        p.name = nam

        OTHER_PLAYERS[usr] = p
        print(p)



def game(server=False):
    if not server:
        ctx.CODE = "SD"
        ctx.NUM = 114514
    print("game start")
    time.sleep(3)
    winsound.PlaySound("null", winsound.SND_PURGE)
    time.sleep(1)

    

    load_level()

    



    

ctx.start()
