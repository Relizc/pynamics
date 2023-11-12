import threading
import time
from .events import EventType, EventPriority
from .interface import PyNamical
from .dimensions import Dimension
import math
import cmath


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Given three collinear points p, q, r, the function checks if


# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False


class GameObject(PyNamical):
    def __init__(self, parent: PyNamical, x: float, y: float, width: float, height: float, contents: str = None,
                 from_points: tuple = None):
        """
        :param x: The position of the GameObject, on X-Axis
        :param y: The position of the GameObject, on Y-Axis
        :param width: The width of the GameObject
        :param height: The height of the GameObject
        """
        super().__init__(parent)
        self.position = Dimension(x, y)
        self.size = Dimension(width, height)
        self.content = contents
        self.absolute = Dimension(x, y)
        self.points = [
            ((self.position.x, self.position.y), (self.position.x - self.size.x, self.position.y)),
            ((self.position.x - self.size.x, self.position.y),
             (self.position.x - self.size.x, self.position.y - self.size.y)),
            ((self.position.x - self.size.x, self.position.y - self.size.y),
             (self.position.x, self.position.y - self.size.y)),
            ((self.position.x, self.position.y - self.size.y), (self.position.x, self.position.y)),

        ]
        if from_points is not None:
            self.points = []
            for i in from_points:
                self.points.append(i)

        self.parent.add_object(self)

    def __repr__(self):
        return f"GameObject()"

    @property
    def topleft(self):
        return self.position

    @property
    def topright(self):
        return self.position.add(self.size.x, 0)

    @property
    def bottomleft(self):
        return self.position.add(0, self.size.y)

    @property
    def bottomright(self):
        return self.position.add_dim(self.size)

    @property
    def center(self):
        return self.position.add(self.size.x / 2, self.size.y / 2)


class PhysicsBody(GameObject):
    def __init__(self, parent: PyNamical, x: float, y: float, width: float, height: float, mass: int,
                 contents: str = None, from_points: tuple = None, row=1.225, use_mass=True, use_collide=True):
        super().__init__(parent, x, y, width, height, contents, from_points)

        # @self.parent.add_tick_update
        # def applyAirResistance():
        #     airResistance = (1 / 2) * self.row * (self.v_inst.f**2) * self.coeff
        #     print("AIRO",airResistance)
        #     r = (self.fnet.r + 180) % 360
        #
        #
        #     airVector = Vector2d(r,airResistance)
        #
        #     self.fnet = self.fnet.add(airVector)

        self.mass = mass
        self.velocity = Vector2d(0, 0)
        self.acceleration = Vector2d(0, 0)
        self.coeff = 0.5
        self.rectitude = 0.6
        self.row = row
        self.use_mass = use_mass
        self.use_collide = use_collide
        self.fnet = Vector2d(0, 0)
        self.gravity = -0.1
        self.zeroed = False
        # self.timeB = time.time()
        # self.timeA = time.time()
        self.fa = False
        self.fnet = Vector2d(90, self.gravity * self.mass)
        if self.use_mass:
            @self.parent.add_event_listener(event=EventType.TICK,priority=EventPriority.LOWEST)
            def update_self(e):
                    if not self.zeroed:
                        self.acceleration.r = self.fnet.r
                        self.acceleration.f = self.fnet.f / self.mass

                        self.velocity = self.velocity.add(
                            Vector2d(self.acceleration.r, self.acceleration.f))

                        v = Vector2d(self.velocity.r, self.velocity.f)
                        v.f *= self.parent._epoch_tps

                        x3, y3 = self.velocity.cart()
                        # print(x3,y3)
                        self.position.x += x3
                        self.position.y -= y3

                        self.fnet = Vector2d(90, self.gravity * self.mass)
        if self.use_collide:
            @self.parent.add_event_listener(event=EventType.TICK,priority=EventPriority.LOWEST)

            def handle_collisions(e):
                objects = self.parent.objects


                collision = False
                coeff = 0
                for i in objects:
                    if isinstance(i, PhysicsBody) and i != self:
                        for j in i.points:
                            for k in self.points:
                                p1 = (j[0][0] + i.position.x, (j[0][1] + i.position.y) * -1)
                                p2 = (j[1][0] + i.position.x, (j[1][1] + i.position.y) * -1)
                                q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                                q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                                p1 = Point(p1[0], p1[1])
                                p2 = Point(p2[0], p2[1])
                                q1 = Point(q1[0], q1[1])
                                q2 = Point(q2[0], q2[1])
                                if doIntersect(p1, p2, q1, q2):
                                    collision = True
                                    coeff = i.rectitude
                                    break

                                # if (p1[0] - p2[0]) == 0:
                                #     if (q1[0] - q2[0]) == 0:
                                #         print("this is true")
                                #         collision = True
                                #         coeff = i.rectitude
                                #         break
                                #     else:
                                #
                                #         m2 = (q1[1] - q2[1]) / (q1[0] - q2[0])
                                #         if m2 == 0:
                                #             b2 = q1[1]
                                #         elif q1[0] == 0:
                                #             b2 = q1[1]
                                #         else:
                                #             b2 = q1[1] / (m2 * q1[0])
                                #         x = p1[0]
                                #         y = m2 * x + b2
                                #         intersect = False
                                #         pointMore = (x, y)
                                #         if min(p1[0], p2[0]) <= pointMore[0] <= max(p1[0], p2[0]):
                                #             if min(q1[0], q2[0]) <= pointMore[0] <= max(q1[0], q2[0]):
                                #                 if min(p1[1], p2[1]) <= pointMore[1] <= max(p1[1], p2[1]):
                                #                     if min(q1[1], q2[1]) <= pointMore[1] <= max(q1[1], q2[1]):
                                #                         intersect = True
                                #         if intersect:
                                #             collision = True
                                #             coeff = i.rectitude
                                #             break
                                # elif (q1[0] - q2[0]) == 0:
                                #
                                #     m = (p1[1] - p2[1]) / (p1[0] - p2[0])
                                #     if m == 0:
                                #         b = p1[1]
                                #     elif p1[0] == 0:
                                #         b = p1[1]
                                #     else:
                                #         b = p1[1] / (m * p1[0])
                                #     x = q1[0]
                                #     y = m * x + b
                                #
                                #     intersect = False
                                #     pointMore = (x, y)
                                #     if min(p1[0], p2[0]) <= pointMore[0] <= max(p1[0], p2[0]):
                                #         if min(q1[0], q2[0]) <= pointMore[0] <= max(q1[0], q2[0]):
                                #             if min(p1[1], p2[1]) <= pointMore[1] <= max(p1[1], p2[1]):
                                #                 if min(q1[1], q2[1]) <= pointMore[1] <= max(q1[1], q2[1]):
                                #                     intersect = True
                                #
                                #     if intersect:
                                #         collision = True
                                #         coeff = i.rectitude
                                #         break
                                # else:
                                #
                                #     m = (p1[1] - p2[1]) / (p1[0] - p2[0])
                                #
                                #     m2 = (q1[1] - q2[1]) / (q1[0] - q2[0])
                                #
                                #     if m == 0:
                                #         b = p1[1]
                                #     elif p1[0] == 0:
                                #         b = p1[1]
                                #     else:
                                #         b = p1[1] / (m * p1[0])
                                #     if m2 == 0:
                                #         b2 = q1[1]
                                #     elif q1[0] == 0:
                                #         b2 = q1[1]
                                #     else:
                                #         b2 = q1[1] / (m2 * q1[0])
                                #     if (m2 - m) == 0:
                                #         if b == b2:
                                #             intersect = True
                                #     else:
                                #         x = (b - b2) / (m2 - m)
                                #         y = m * x + b
                                #         intersect = False
                                #         pointMore = (x, y)
                                #         if min(p1[0], p2[0]) <= pointMore[0] <= max(p1[0], p2[0]):
                                #             if min(q1[0], q2[0]) <= pointMore[0] <= max(q1[0], q2[0]):
                                #                 if min(p1[1], p2[1]) <= pointMore[1] <= max(p1[1], p2[1]):
                                #                     if min(q1[1], q2[1]) <= pointMore[1] <= max(q1[1], q2[1]):
                                #                         intersect = True
                                #
                                #     if intersect:
                                #         collision = True
                                #         coeff = i.rectitude
                                #         break
                            if collision:
                                break
                    if collision:
                        # if not self.fa: self.zeroed = True
                        # selfMomentum = Vector2d(self.velocity.r, self.velocity.f * self.mass)
                        # otherMomentum = Vector2d(i.velocity.r, i.velocity.f * i.mass)
                        finalVelocity = ((self.velocity.f * (self.mass - i.mass) + 2 * (i.mass * i.velocity.f)) / (
                                self.mass + i.mass)) * self.rectitude
                        finalVelocity2 = ((i.velocity.f * (i.mass - self.mass) + 2 * (
                                    self.mass * self.velocity.f)) / (
                                                 i.mass + self.mass)) * self.rectitude

                        self.velocity.f = finalVelocity
                        i.velocity.f = finalVelocity2
                        break
                    else:
                        pass
                        # self.zeroed = False


    def add_force(self, force):
        self.fnet = self.fnet.add(force)
        def d():
            da = time.time()
            while time.time() - da <= self.parent._epoch_tps:

                self.fa = True
                time.sleep(self.parent._epoch_tps*0.8)
            self.fa = False
        threading.Thread(target=d).start()

        self.zeroed = False

    def apply_force(self, force, duration):
        def add_force():
            self.fnet = self.fnet.add(force)
            start_time = time.time()
            while True:
                if time.time() - start_time >= duration:
                    break
                time.sleep(self.parent._epoch_tps)
            self.fnet = self.fnet.subtract(force)

        thread_add_force = threading.Thread(target=add_force)
        thread_add_force.start()

    def clear(self):
        self.fnet.clear()
        self.velocity.clear()
        self.acceleration.clear()



    # def use_advanced_collision(self):`r
    #     rotation = self.acceleration.r
    #     xoffset = self.position.x
    #     yoffset = -self.position.y
    #     ray = Vector2d(rotation,2)
    #     rayCart = ray.cart()
    #     rayX = rayCart[0]+xoffset
    #     rayY = rayCart[1]+yoffset
    #     predictionTimes = []
    #     if rayX - self.position.x == 0:
    #         for i in self.parent.objects:
    #             if isinstance(i,PhysicsBody):
    #                 for j in i.points:
    #                     p1 = (j[0][0] + i.position.x, (j[0][1] + i.position.y) * -1)
    #                     p2 = (j[1][0] + i.position.x, (j[1][1] + i.position.y) * -1)
    #
    #                     minX = min(p1[0],p2[0])
    #                     maxX = max(p1[0],p2[0])
    #
    #                     if minX <= rayX <= maxX:
    #                         if p1[0]-p2[0] == 0:
    #                             predictionTimes.append(0)
    #                         else:
    #                             m = (p1[1]-p2[1])/(p1[0]-p2[0])
    #                             b = p1[1] - (m*p1[0])
    #                             distance = m*rayX + b
    #                             predicted =


class Vector2d():
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

    def add(self, b):
        x = self.f * math.cos(math.radians(self.r))
        y = self.f * math.sin(math.radians(self.r))

        x1 = b.f * math.cos(math.radians(b.r))
        y1 = b.f * math.sin(math.radians(b.r))

        xf = x + x1
        yf = y + y1

        r = (xf ** 2 + yf ** 2) ** .5
        theta = math.degrees(math.atan2(yf, xf))
        return Vector2d(theta, r)

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
        return f"Vector2d(Angle: {self.r}, Value: {self.f})"
