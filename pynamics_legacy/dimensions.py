import math


class ClockResizer:

    def __init__(self, value, timescale):
        self.value = value
        self.tick = int(round(value * 60 * timescale, 0))

    def __int__(self):
        return self.tick


class Dimension:

    def __init__(self, x: float, y: float):
        self.x = round(x, 2)
        self.y = round(y, 2)

    def format_space_str(target):
        a = list(map(float, target.split(",")))
        return Dimension(a[0], a[1])

    def set(self, x: float, y: float):
        self.x = round(x, 2)
        self.y = round(y, 2)

    def add(self, x: float, y: float):
        return Dimension(self.x + x, self.y + y)

    def add_dim(self, dim):
        return Dimension(self.x + dim.x, self.y + dim.y)

    def add_self(self, x: float, y: float):
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

    def __getitem__(self, i):
        if i:
            return self.y
        return self.x

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


class Color(object):

    def __init__(self, r = 255, g = 255, b = 255, a = 0):
        if isinstance(r, str):
            if r.lower() == "white":
                self.r, self.g, self.b = 255, 255, 255
            return

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return "#%02x%02x%02x" % (int(self.r), int(self.g), int(self.b))

    def __iter__(self):
        return (self.r, self.g, self.b)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def tuple(self):
        r, g, b, a = self.r + 1, self.g + 1, self.b + 1, self.a + 1
        return (r/256, g/256, b/256, a/256)

    @staticmethod
    def from_float(r, g, b, a):
        return Color(r * 256 - 1, g * 256 - 1, b * 256 - 1, a * 256 - 1)


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
        self.r = round(r, 2)
        self.f = round(f, 2)

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

    def __mul__(self, other):
        return Vector2d(self.r, self.f * other)


Vector2d = Vector