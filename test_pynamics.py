import pynamics
import time
import random

ctx = pynamics.GameManager(pynamics.Dim(1000, 1000), tps=128, fps=1)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)

bob = pynamics.GameObject(ctx, 10, 10, 10, 10)

@ctx.add_tick_update
def q():
    pynamics.GameObject(ctx, random.randint(0, 100), random.randint(0, 100), 10, 10)

print(ctx.children)

ctx.start()

# time.sleep(2)
#
# ctx.kill()
print("killed")
