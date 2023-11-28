import pynamics as pn
import random

game = pn.GameManager(dimensions=pn.Dimension(100, 100), fps=300, event_tracker=True)
window = pn.ProjectWindow(game, size=pn.Dimension(1000, 700))
cam = pn.ViewPort(window, position=pn.Dimension(100, 100))

back1 = pn.Image(game, 0, 0, 1000, 700, "world.jpeg")

bob1 = pn.TopViewPhysicsBody(game, 10, 10, 10, 10, 60)
bob1.init_movement(30)
@game.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator(pn.K_LEFT))
def c(ctx):
    pn.TopViewPhysicsBody(game, random.randint(1, 100), random.randint(1, 100), 10, 10, 60).init_movement(10)

game.start()