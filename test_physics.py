import pygamepro
import random

FORCE = 2 # Change this to what force you want
MASS = 10

pygamepro.Logger.print("&ePhysics Test")
pygamepro.Logger.print("&bIn this demo, physics is enabled for the default &aGameContext ctx.")
pygamepro.Logger.print("&bThe rectangle in the middle will fall due to gravity.")
pygamepro.Logger.print(f"&bPress &eArrow Keys &bto apply {FORCE}N of force to the object with {MASS}kg mass.")
pygamepro.Logger.print("&bPress &eR &bto reset the object to the center.")

ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(500, 500), styles = {
    "background-color": "white"
}, tick = 128, maxfps = 144)

test = ctx.create_rect(pygamepro.Dimension(240, 0), pygamepro.Dimension2d(0, 20, 0, 20))
phy = pygamepro.MassBody(test, mass=MASS, gravity=0) # Adds mass to the object

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