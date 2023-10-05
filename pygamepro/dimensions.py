class ClockResizer:

    def __init__(self, value, timescale):
        self.value = value
        self.tick = int(round(value * 60 * timescale, 0))

    def __int__(self):
        return self.tick

class Dimension:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def add_dim(self, dim):
        self.x += dim.x
        self.y += dim.y

    def __repr__(self):
        return f"Dimension({self.x}, {self.y})"

    def __tuple__(self):
        return (self.x, self.y)

    @property
    def scale_x(self):
        return self.x

    @property
    def offset_x(self):
        return self.y

class Dimension2d:

    def __init__(self, scale_x, offset_x, scale_y, offset_y):
        self.x = Dimension(scale_x, offset_x)
        self.y = Dimension(scale_y, offset_y)

    @property
    def scale_x(self):
        return self.x.scale_x

    @property
    def offset_x(self):
        return self.x.offset_x

    @property
    def scale_y(self):
        return self.y.scale_x
    
    @property
    def offset_y(self):
        return self.y.offset_x
