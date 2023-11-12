import pynamics as pn

game = pn.GameManager(dimensions=pn.Dimension(100, 100), fps=300, event_tracker=False)
window = pn.ProjectWindow(game, size=pn.Dimension(1000, 700))
cam = pn.ViewPort(window)

back1 = pn.Image(game, 0, 0, 1000, 700, "world.jpeg")

bob1 = pn.TopViewPhysicsBody(game, 10, 10, 10, 10, 60)
bob1.init_movement(30)
#bob1.establish_movement()]]]]]]]]]]]

# @game.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_UP))
# def move_up(ctx):
#     bob1.position.y -= 1

game.start()