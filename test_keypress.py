import pygamepro
import random

pygamepro.Logger.print("&eKeypress Test Demo using pygamepro &a1.0.0")
pygamepro.Logger.print("&bThis is an example with listeners in the game context listening for keypresses, \nwhich moves the rectangle in the middle around the screen \n\nUse your arrow keys to control the rectangle.")

ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(500, 500), styles = {
    "background-color": "white"
}, maxfps = 144)

test = ctx.create_rect(pygamepro.Dimension(240, 240), pygamepro.Dimension2d(0, 10, 0, 10))

@ctx.addEventListener("keyhold", target=pygamepro.K_DOWN)
def hold(self):
    test.y += 1

@ctx.addEventListener("keyhold", target=pygamepro.K_UP)
def hold(self):
    test.y -= 1

@ctx.addEventListener("keyhold", target=pygamepro.K_LEFT)
def hold(self):
    test.x -= 1

@ctx.addEventListener("keyhold", target=pygamepro.K_RIGHT)
def hold(self):
    test.x += 1

ctx.start_main()