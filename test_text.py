import pygamepro

ctx = pygamepro.GameContext.from_dim(pygamepro.Dimension(500, 500), styles = {
    "background-color": "white"
}, tick = 128, maxfps = 144)

text = pygamepro.Text(ctx, "Hello World")

ctx.start()