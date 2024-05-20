from .logger import Logger

class DisplayEnum:
    AUTO = 0

class StyleLoader:

    def __init__(self):
        self.display = DisplayEnum.AUTO
        self.property = None

    def load_styles(self, property):
        self.property = property
        if property is None: return
        for i in property:
            self.set_style(i, property[i])

    def get_style(self, name):
        if hasattr(self, name):
            return getattr(self, name)

    def set_style(self, name, value):
        setattr(self, name, value)

_COLORMAP = {
    "black": [0, 0, 0, 1],
    "white": [1, 1, 1, 1],
    "red": [1, 0, 0, 1],
    "green": [0, 1, 0, 1],
    "blue": [0, 0, 1, 1]
}

def color_alias(color: str):

    if isinstance(color, tuple): return color

    args = color.lower().split(" ")
    if _COLORMAP.get(args[0], None) is None:
        raise ValueError(
            f"Color data not found with the specific name \"{color}\". Using white instead"
        )
    base = _COLORMAP[args[0]]
    for i in range(1, len(args)):
        if args[i] == "transparent":
            base[3] = 0.5
        if args[i] == "tint":
            for i in range(4):
                base[i] = base[i] + (1 - base[i]) * 0.5
    return tuple(base)

