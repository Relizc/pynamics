import pynamics as pn
import sys

ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
#window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
#camera = pn.ViewPort(window)
vcam = pn.DedicatedServer(ctx)
vcam.DOWNSTREAM_PING_TIMEOUT = 30
vcam.UPSTREAM_PACKET_WAIT_TIME = 15

circle61 = pn.Particle(ctx, 80, 10, 10, use_gravity=True, rectitude=0.5, clear_blit=True, mass=10)

large = pn.ExampleLargeBinaryObject(ctx)
print(large.uuid)
print(sys.getsizeof(large))

ctx.start()