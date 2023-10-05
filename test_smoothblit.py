import pygamepro
import random

x = pygamepro.GameObject()
ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(600, 800), styles = {
    "background-color": "white"
}, tick = 2, maxfps=144)

n = 0

test = ctx.create_rect(pygamepro.Dimension(300, 400), pygamepro.Dimension2d(0, 10, 0, 10), smooth_blit = True)
test2 = ctx.create_rect(pygamepro.Dimension(300, 400), pygamepro.Dimension2d(0, 10, 0, 10), smooth_blit = False, styles = {
    "background-color": (255, 0, 0)
})

@test.addEventListener("update")
def onrender(self):
    self.x = random.randint(0, 590)
    self.y = random.randint(0, 590)

    test2.x = self.x
    test2.y = self.y

ctx.start()

