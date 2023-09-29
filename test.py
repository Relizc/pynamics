import pygamepro
import random

x = pygamepro.GameObject()
ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(600, 800), styles = {
    "background-color": "white"
})

n = 0

@ctx.addEventListener("update", run_delay = 60)
def update():
    ctx.updateStyles({
        "background-color": (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    })
    

ctx.start()

