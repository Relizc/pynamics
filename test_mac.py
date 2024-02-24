import pynamics as pn
import matplotlib.pyplot as plot
import numpy as np

ctx = pn.GameManager(dimensions=pn.Dim(500, 500), event_tracker=False)
view = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))

circle = pn.Particle(ctx, 250, 250, use_gravity=False)

k = pn.Animation(pn.CubicBezier(
    0, 1, 1, 0
), fields=("x",))
# n = 0

# a = []
# b = []

# for i in range(0, 100):
#     x, y = bei(n)
#     a.append(x)
#     b.append(y)
#     n += 0.01

# print(a, b)

# plot.plot(np.array(a), np.array(b))
# plot.show()
@ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_a))
def press_a(self, key):
    circle.position.x = 250
    k.play(circle.position, (449,))

ctx.start()