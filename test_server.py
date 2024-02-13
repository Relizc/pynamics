import pynamics as pn
import sys

import random

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
#window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
#camera = pn.ViewPort(window)
vcam = pn.DedicatedServer(ctx)
vcam.DOWNSTREAM_PING_TIMEOUT = 30
vcam.UPSTREAM_PACKET_WAIT_TIME = 15

circle61 = pn.Particle(ctx, 80, 10, 10, use_gravity=True, rectitude=0.5, clear_blit=True, mass=20)

# large = pn.ExampleLargeBinaryObject(ctx)
# print(large.uuid)
# print(sys.getsizeof(large))

q = 0
@ctx.add_event_listener(event=pn.EventType.TICK)
def ccccc(this):
    global q
    q += 1
    if q == 20:
        q = 0
        circle61.position = pn.Dim(random.randint(1, 100), random.randint(1, 100))

ctx.start()