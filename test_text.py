import pygamepro
import random

ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(500, 500), styles = {
    "background-color": "white"
}, tick = 128, maxfps = 144)

text = pygamepro.Text.create(ctx, pygamepro.Text.str("Hello World\nLMFAO"))

@ctx.addEventListener("keydown", target = pygamepro.K_q)
def q(self):
    text.x = random.randint(0, 300)
    text.y = random.randint(0, 300)

ctx.start()