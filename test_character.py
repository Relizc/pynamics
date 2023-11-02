import pynamics as pn

game = pn.GameManager(dimensions=pn.Dimension(100, 100))
window = pn.ProjectWindow(game, size=pn.Dimension(1000, 700))
cam = pn.ViewPort(window)

back1 = pn.Image(game, 0, 0, 100, 100, "world.jpeg")

bob1 = pn.TopViewPhysicsBody(game, 10, 10, 10, 10, 1)
bob1.init_movement()
#bob1.establish_movement()

# @game.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_UP))
# def move_up(ctx):
#     bob1.position.y -= 1

game.start()