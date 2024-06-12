import pynamics_legacy
import random
import uuid

ctx = pynamics_legacy.GameManager(pynamics_legacy.Dim(100, 100), tps=128, fps=0, event_tracker=True)
window = pynamics_legacy.ProjectWindow(ctx)
camera = pynamics_legacy.ViewPort(window)

hi = pynamics_legacy.Text(ctx, 100, 100, "Loser")

@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYDOWN, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_r))
def d(ctx):
    hi.text = str(uuid.uuid4())
    print(hi.text)

ctx.start()