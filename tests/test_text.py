import pynamics
import random
import uuid

ctx = pynamics.GameManager(pynamics.Dim(100, 100), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)

hi = pynamics.Text(ctx, 100, 100, "Loser")

@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_r))
def d(ctx):
    hi.text = str(uuid.uuid4())
    print(hi.text)

ctx.start()