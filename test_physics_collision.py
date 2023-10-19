import pygamepro
import random

FORCE = 1 # Change this to what force you want
MASS = 20

pygamepro.Logger.print("&ePhysics Test 2")
pygamepro.Logger.print("&bIn this demo, physics is enabled as usual, with another rigid object at the bottom of the screen")
pygamepro.Logger.print("&bThe rectangle in the middle will fall due to gravity, and collide with the table.")
pygamepro.Logger.print(f"&bPress &eArrow Keys &bto apply {FORCE}N of force to the object with {MASS}kg mass.")
pygamepro.Logger.print("&bPress &eR &bto reset the object to the center.")

ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(500, 1000), styles = {
    "background-color": (0, 255, 255)
}, tick = 128, maxfps = 500000)

test = ctx.create_rect(pygamepro.Dimension(240, 0), pygamepro.Dimension2d(0, 10, 0, 10), smooth_blit=True)
phy = pygamepro.MassBody(test, mass=MASS) # Adds mass to the object
col = pygamepro.CollisionBody(phy)

test2 = ctx.create_rect(pygamepro.Dimension(10, 480), pygamepro.Dimension2d(1, -20, 0, 10))
pygamepro.MassBody(test2, mass=1, anchored=True)

@ctx.addEventListener("keydown", target=pygamepro.K_r)
def hold(self):
    test.set_position(pygamepro.Dimension(240, 0))
    test.massbody.clear()

@ctx.addEventListener("keyhold.framebind", target=pygamepro.K_RIGHT)
def hold(self):
    test.massbody.netforce.x += FORCE

@ctx.addEventListener("keyhold.framebind", target=pygamepro.K_LEFT)
def hold(self):
    test.massbody.netforce.x += -FORCE

@ctx.addEventListener("keyhold.framebind", target=pygamepro.K_UP)
def hold(self):
    test.massbody.netforce.y += -FORCE

@ctx.addEventListener("keyhold.framebind", target=pygamepro.K_DOWN)
def hold(self):
    test.massbody.netforce.y += FORCE

@ctx.addEventListener("update")
def update(self):
    self.set_title("velocity: " + str(test.massbody.velocity))



ctx.start()