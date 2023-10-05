import pygamepro
import random

x = pygamepro.GameObject()
ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(600, 800), styles = {
    "background-color": "white"
})

n = 0

test = ctx.create_rect(pygamepro.Dimension(10, 10), pygamepro.Dimension2d(0, 10, 0, 10))

@test.addEventListener("update")
def onrender(self):
    print("update")
    self.rect.x += random.randint(-1, 1)
    self.rect.y += random.randint(-1, 1)


print(test)

ctx.start()

