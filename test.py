import pygamepro
import random

x = pygamepro.GameObject()
ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(600, 800), styles = {
    "background-color": "white"
})

n = 0

@ctx.addEventListener("post-update", run_delay=pygamepro.ClockResizer(0.1, pygamepro.SECOND))
def update():
    ctx.updateStyles({
        "background-color": (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    })

@ctx.addEventListener("post-update", run_delay=pygamepro.ClockResizer(1, pygamepro.SECOND))
def update():
    print("1 secon tick")

    

ctx.start()

