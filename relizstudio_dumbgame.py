import pynamics as pn
import random

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
camera = pn.ViewPort(window)

shield = pn.Image(ctx, 200, 200, path="shield.jpeg", width=100, height=100)

side = 0

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_RIGHT))
def press_a(self, key):
    global side
    k = pn.Animation(pn.CubicBezier(0.25, 0.1, 0.25, 1.0), fields=("rotation",), duration=16)
    shield.rotation = -90 * side
    side = 1
    k.play(shield, (-90,))

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_UP))
def press_a(self, key):
    global side
    k = pn.Animation(pn.CubicBezier(0.25, 0.1, 0.25, 1.0), fields=("rotation",), duration=16)
    shield.rotation = -90 * side
    side = 0
    k.play(shield, (0,))

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_LEFT))
def press_a(self, key):
    global side
    k = pn.Animation(pn.CubicBezier(0.25, 0.1, 0.25, 1.0), fields=("rotation",), duration=16)
    shield.rotation = -90 * side
    side = 3
    k.play(shield, (-270,))

@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_DOWN))
def press_a(self, key):
    global side
    k = pn.Animation(pn.CubicBezier(0.25, 0.1, 0.25, 1.0), fields=("rotation",), duration=16)
    shield.rotation = -90 * side
    side = 2
    k.play(shield, (-180,))

blocks = []

@ctx.add_event_listener(event=pn.EventType.TICK)
def tick(self):
    global blocks
    k = random.randint(1, 1024)

    x = list(blocks)

    for i in blocks:
        if i.dead:
            i.dead_age += 1
            if i.dead_age > 10:
                x.remove(i)
                i.delete()

        if 200 <= i.position.x <= 300 and 200 <= i.position.y <= 300:
            
            i.velocity = pn.Vector(0, 0)
            i.position.x = -2147483648
            i.position.y = -2147483648
            i.dead = True

    blocks = x


    if 4 <= k <= 7:
        p = pn.Particle(ctx, -100, -100, use_gravity=False, use_collide=False)
        p.dead = False
        p.dead_age = 0

        if k == 4:
            p.movement = "right"
            p.position.x = 30
            p.position.y = 250
            p.velocity = pn.Vector(0, 1)
        if k == 5:
            p.movement = "left"
            p.position.x = 480
            p.position.y = 250
            p.velocity = pn.Vector(180, 1)
        if k == 6:
            p.movement = "up"
            p.position.x = 250
            p.position.y = 480
            p.velocity = pn.Vector(90, 1)
        if k == 7:
            p.movement = "down"
            p.position.x = 250
            p.position.y = 30
            p.velocity = pn.Vector(270, 1)
    
        blocks.append(p)

ctx.start()