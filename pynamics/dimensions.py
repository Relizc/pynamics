import math

class ClockResizer:

    def __init__(self, value, timescale):
        self.value = value
        self.tick = int(round(value * 60 * timescale, 0))

    def __int__(self):
        return self.tick


class Dimension:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def format_space_str(target):
        a = list(map(float, target.split(",")))
        return Dimension(a[0], a[1])

    def set(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, x: float, y: float):
        return Dimension(self.x + x, self.y + y)

    def add_dim(self, dim):
        return Dimension(self.x + dim.x, self.y + dim.y)

    def add_self(self, x:float, y: float):
        self.x += x
        self.y += y

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def add_dim_self(self, dim):
        self.x += dim.x
        self.y += dim.y

    def add_vector(self, vector):
        v = Vector2d(vector.r, vector.f)

        x3, y3 = v.cart()
        # print(x3,y3)
        self.x += x3
        self.y -= y3

    def __repr__(self):
        return f"Dimension({self.x}, {self.y})"

    def __tuple__(self):
        return (self.x, self.y)
    
    def __eq__(self, other):
        if not isinstance(other, Dimension):
            return NotImplemented
        return self.x == other.x and self.y == other.y

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

class Vector():
    def __init__(self, r, f):
        """

        :param r: the rotation of the object from the origin.
            |
            O
        ----|----           =90 degrees
            |
            |
            |
            |
        --O-|----           =180 degrees
            |
            |
            etc.
        :param f: the value of the vector
        """
        self.r = r
        self.f = f

    def format_space_str(target):
        a = list(map(float, target.split(",")))
        return Vector(a[0], a[1])

    def from_xy(x, y):
        value = math.sqrt(x ** 2 + y ** 2)
        angle = math.degrees(math.atan2(y, x))
        return Vector2d(angle, value)

    def add_self(self, vector):
        q = self.add(vector)
        self.r = q.r
        self.f = q.f

    def add(self, b):
        x = self.f * math.cos(math.radians(self.r))
        y = self.f * math.sin(math.radians(self.r))

        x1 = b.f * math.cos(math.radians(b.r))
        y1 = b.f * math.sin(math.radians(b.r))

        xf = x + x1
        yf = y + y1

        r = (xf ** 2 + yf ** 2) ** .5
        theta = math.degrees(math.atan2(yf, xf))
        p = Vector2d(theta, r)
        self.r = theta
        self.f = r
        return p

    def subtract(self, b1):
        rb = (b1.r + 180) % 360
        fb = b1.f
        b = Vector2d(rb, fb)

        x = self.f * math.cos(math.radians(self.r))
        y = self.f * math.sin(math.radians(self.r))

        x1 = b.f * math.cos(math.radians(b.r))
        y1 = b.f * math.sin(math.radians(b.r))

        xf = x + x1
        yf = y + y1

        r = (xf ** 2 + yf ** 2) ** .5
        theta = math.degrees(math.atan2(yf, xf))
        self.r = theta
        self.f = r
        return Vector2d(theta, r)

    def cart(self) -> tuple:
        x = self.f * math.cos(math.radians(self.r))
        y = self.f * math.sin(math.radians(self.r))

        return x, y

    def equation(self) -> tuple:
        x, y = self.cart()
        x1, y1 = Vector2d(self.r, self.f / 2).cart()
        if x1 - x == 0:
            return "X", x, 0
        m = (y1 - y) / (x1 - x)
        if m == 0:
            return "Y", y, 0
        b = y - (m * x)
        return "Y", m, b

    def clear(self):
        self.r = 0
        self.f = 0

    def __repr__(self):
        return f"Vector(Angle: {self.r}, Value: {self.f})"
    
    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return self.r == other.r and self.f == other.f
    
    def __add__(self, other):
        return self.add(other)

class Vector2d(Vector): pass