import pynamics as pn
import time
import random
import threading

ctx = pn.GameManager(pn.Dim(800, 400), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dimension(800, 400))

#bob = pn.Particle(ctx, 20, 380, use_gravity=False, gravity=-0.08)

n = 0

@ctx.add_event_listener(event=pn.EventType.TICK)
def push(self):
    global n
    n += 1
    if n == 4:
        x = pn.Particle(ctx, 10, 10, 3, use_gravity=True, rectitude=0.1)
        x.velocity = pn.Vector(-30 + random.random() * 10, 5)

        def k(n):
            time.sleep(0.5)
            n.delete()

        threading.Thread(target=lambda: k(x)).start()


        

        n = 0



    
ctx.start()
