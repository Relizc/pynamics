import threading
import time

import numpy as np

from .events import EventPriority, EventType, KeyEvaulator
from .interface import PyNamical, network_transferrable
from .dimensions import Dimension, Vector2d
import math
import cmath
import tkinter as tk
import ctypes
from PIL import Image as ImageUtils
from PIL import ImageTk



import random


class Point(Dimension):
    pass

    # Given three collinear points p, q, r, the function checks if


def socket_whitelisted_attributes(*args, **kwargs):
    def add_fields(obj):
        obj.P_whitelisted = args
        return obj

    return add_fields

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

@socket_whitelisted_attributes("position", "velocity")
@network_transferrable
class GameObject(PyNamical):
    def __init__(self, parent: PyNamical, x: float = 0, y: float = 0, width: float = 10, height: float = 10, contents: str = None,
                 rotation = 0,
                 from_points: tuple = None,
                 clear_blit: bool = True,
                 anchor: str = "nw"):
        """
        :param x: The position of the GameObject, on X-Axis
        :param y: The position of the GameObject, on Y-Axis
        :param width: The width of the GameObject
        :param height: The height of the GameObject
        """
        super().__init__(parent)

        self.position = Dimension(x, y)
        self.this_position = Dimension(x, y)

        self.this_display_position = Dimension(self.this_position.x, self.position.y)
        self.last_display_position = None
        self.size = Dimension(width, height)
        if contents != None:
            self.content = ImageTk.PhotoImage(ImageUtils.open(contents))
        else:
            self.content = None
        self.hidden = False
        self.absolute = Dimension(x, y)
        self.blit_id = None
        self.force_update = 0
        self.start_debug_highlight_tracking = False
        self.rotation = rotation
        self.last_display_rotation = None
        self.this_display_position = rotation
        self.points = [
            ((self.position.x, self.position.y), (self.position.x - self.size.x, self.position.y)),
            ((self.position.x - self.size.x, self.position.y),
             (self.position.x - self.size.x, self.position.y - self.size.y)),
            ((self.position.x - self.size.x, self.position.y - self.size.y),
             (self.position.x, self.position.y - self.size.y)),
            ((self.position.x, self.position.y - self.size.y), (self.position.x, self.position.y)),

        ]
        self.clear_blit = clear_blit
        if from_points is not None:
            self.points = []
            for i in from_points:
                self.points.append(i)
        self.id = id(self)

        self.parent.add_object(self)

        self.anchor = anchor

    def delete(self):
        if isinstance(self.parent.objects, list):
            self.parent.objects.remove(self)
            self.parent.ghosts.append(self)
            self.parent.frame(recursion=False)
            self.parent.ghosts.remove(self)
            self.unbind()
            del self
    

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

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def hide(self):
        self.hidden = True
        self.parent.frame()

    def unhide(self):
        self.hidden = False
        self.forcedisplay = True
        self.parent.frame()
        self.forcedisplay = False

    def _debug_blit_once(self):
        self.parent.delete_draws(f"DEBUG@{self._debughighlight}")
        self._debughighlight = random.randint(-2**64, 2**64)
        self.parent.create_rectangle(self.position.x, self.position.y, self.position.x + self.size.x, self.position.y + self.size.y,
                                     outline="green",
                                     width=2,
                                     tags=f"DEBUG@{self._debughighlight}")

    def debug_highlight(self):
        self._debughighlight = random.randint(-2**64, 2**64)
        self.parent.create_rectangle(self.position.x, self.position.y, self.position.x + self.size.x, self.position.y + self.size.y,
                                     outline="green",
                                     width=2,
                                     tags=f"DEBUG@{self._debughighlight}")
        self.start_debug_highlight_tracking = True

    def debug_unhighlight(self):
        self.start_debug_highlight_tracking = False
        self.parent.delete_draws(f"DEBUG@{self._debughighlight}")




class Image(GameObject):

    def __init__(self, parent: GameObject, x: float = 0, y: float = 0, width: float = -1, height: float = -1,
                 path: str = None,
                 resize_keep_ratio: bool = False,
                 **kwargs):
        
        self.image_path = path
        self.image = ImageUtils.open(self.image_path).convert("RGBA")

        super().__init__(parent, x, y, self.image.size[0], self.image.size[1], contents=None, **kwargs)

        if width != -1 or height != -1:
            if resize_keep_ratio:
                self.image.thumbnail((width, height), ImageUtils.ANTIALIAS)
            else:
                self.image = self.image.resize((width, height))

        self.content = ImageTk.PhotoImage(self.image.rotate(self.rotation))

    def __repr__(self):
        return f"Image(file={self.image_path})"

class TopViewPhysicsBody(GameObject):

    def __init__(self, parent: GameObject, x: float = 0, y: float = 0, width: float = 10, height: float = 10, mass: int = 1,
                 contents: str = None, from_points: tuple = None,
                 floor_friction: float = 0.1):
        super().__init__(parent, x, y, width, height, contents, from_points)

        self.mass = mass
        self.force = Vector2d(0, 0)
        self.velocity = Vector2d(0, 0)
        self.acceleration = Vector2d(0, 0)
        self.coefficient = floor_friction

        self.finish_creating()

    def update(self):
        self.acceleration = Vector2d(self.force.r, self.force.f / self.mass)
        self.force.clear()
        self.velocity.add_self(self.acceleration)
        self.acceleration.clear()
        self.position.add_vector(self.velocity)

        v = Vector2d(self.velocity.r + 180, self.velocity.f * self.coefficient)

        self.velocity.add_self(v)

class PhysicsBody(GameObject):
    def __init__(self, parent: PyNamical, x: float = 0, y: float = 0, width: float = 10, height: float = 10, mass: int = 1,
                 contents: str = None, from_points: tuple = None, row=1.225, rectitude=1, use_mass=True, use_collide=True,
                 collision_type=1, use_gravity=True, use_airres=False, **kwargs):
        super().__init__(parent, x, y, width, height, contents, from_points, **kwargs)

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
        if use_mass == False:
            self.mass = 10e18
        else:
            self.mass = mass
        self.velocity = Vector2d(0, 0)
        self.use_airres = use_airres
        self.use_gravity = use_gravity
        self.acceleration = Vector2d(0, 0)
        self.coeff = 0.5
        self.rectitude = rectitude
        self.row = row
        self.use_mass = use_mass
        self.collision_type = int(collision_type)
        self.use_collide = use_collide
        self.force = Vector2d(0, 0)
        self.gravity = -0.1
        

        # self.timeB = time.time()
        # self.timeA = time.time()

        if self.use_gravity: self.force = Vector2d(90, self.gravity * self.mass)
        if self.use_mass:
            self.attach_movement_thread()

    def init_movement(self, force: int = 1):
        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Up"))
        def m(ctx):
            self.force.add_self(Vector2d(90, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Down"))
        def m(ctx):
            self.force.add_self(Vector2d(270, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Left"))
        def m(ctx):
            self.force.add_self(Vector2d(180, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Right"))
        def m(ctx):
            self.force.add_self(Vector2d(0, force))

    def attach_movement_thread(self):
        self.parent.ticksteplisteners+= 1

        def update_self():
            while self.parent.terminated == False:

                while self.parent.debug != None and self.parent.debug.tickchanger_paused:
                    time.sleep(0.01)
                    if self.parent.debug.tickchanger_stepping:
                        self.parent.debug.tickchanger_stepping = 0
                        break
                    continue

                self.update()
                time.sleep(self.parent._epoch_tps)

        threading.Thread(target=update_self).start()
                    
    def collide(self, other):
        collision = False
        if isinstance(other, GameObject):
            for j in other.points:
                for k in self.points:
                    p1 = (j[0][0] + other.position.x, (j[0][1] + other.position.y) * -1)
                    p2 = (j[1][0] + other.position.x, (j[1][1] + other.position.y) * -1)
                    q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                    q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                    p1 = Point(p1[0], p1[1])
                    p2 = Point(p2[0], p2[1])
                    q1 = Point(q1[0], q1[1])
                    q2 = Point(q2[0], q2[1])
                    if doIntersect(p1, p2, q1, q2):
                        collision = True
                        break
                if collision:
                    break
        return collision

    def collide_side(self, other):
        collision = False
        if isinstance(other, GameObject):
            for j in other.points:
                for k in self.points:
                    p1 = (j[0][0] + other.position.x, (j[0][1] + other.position.y) * -1)
                    p2 = (j[1][0] + other.position.x, (j[1][1] + other.position.y) * -1)
                    q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                    q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                    p1 = Point(p1[0], p1[1])
                    p2 = Point(p2[0], p2[1])
                    q1 = Point(q1[0], q1[1])
                    q2 = Point(q2[0], q2[1])
                    if doIntersect(p1, p2, q1, q2):
                        collision = True
                        break
                if collision:
                    break
        return collision
    
    # Added to avoid repeated code.
    # Since there are a lot of objects extending PhysicsBody and we dont want the update code to be repeatedly
    # coded again.
    def handle_forces(self):
        """Handles the object's delta-x based on velocity and calculates the delta-v due to gravity"""

        if self.use_gravity: 
            self.force.add_self(Vector2d(90, self.gravity * self.mass))

        self.acceleration.r = self.force.r
        self.acceleration.f = self.force.f / self.mass

        self.velocity.add_self(Vector2d(self.acceleration.r, self.acceleration.f))

        x3, y3 = self.velocity.cart()

        self.position.x += x3
        self.position.y -= y3

        self.force.clear()

    def update(self):

        self.handle_forces()

        if self.use_collide and self.use_mass and self.collision_type == 1:
            self.handle_collisions()
        elif self.use_collide and self.use_mass and self.collision_type == 2:
            pass

    def add_force(self, force):
        self.force.add_self(force)

    def add_velocity(self, velocity):
        self.velocity.add_self(velocity)

    def apply_force(self, force, duration):
        def add_force():
            self.force = self.force.add(force)
            start_time = time.time()
            while True:
                if time.time() - start_time >= duration:
                    break
                time.sleep(self.parent._epoch_tps)
            self.force = self.force.subtract(force)

        thread_add_force = threading.Thread(target=add_force)
        thread_add_force.start()

    def clear(self):
        self.force.clear()
        self.velocity.clear()
        self.acceleration.clear()

    def handle_collisions(self):
        objects = self.parent.objects
        # while True:
        collision = False
        # if self.parent.terminated: break
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
                    if collision:
                        break
            if collision:
                x, y = self.velocity.cart()
                x += self.position.x
                y -= self.position.y
                pointx, pointy = self.position.x, self.position.y
                if pointx - x == 0:
                    num = pointx
                    collisions = []
                    collDist = 0

                    for k in self.points:
                        q11 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                        q22 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                        if min(q11[0], q22[0]) <= num <= max(q11[0], q22[0]):
                            if q11[0] == q22[0]:

                                collDist = max(abs(-self.position.y - min(q11[1], q22[1])), collDist)


                            else:
                                q1x, q1y = (q11[0], q11[1])
                                q2x, q2y = (q22[0], q22[1])
                                m = (q1y - q2y) / (q1x - q2x)
                                b = q2y - m * q2x

                                # intersection
                                yd = m * num + b
                                intersection = (num, yd)
                                if min(q11[0], q22[0]) <= intersection[0] <= max(q11[0], q22[0]) and min(q11[1],
                                                                                                         q22[1]) <= \
                                        intersection[1] <= max(q11[1], q22[1]):
                                    collDist = max(collDist, abs(-self.position.y - intersection[1]))

                vixself = self.velocity.cart()[0]
                viyself = self.velocity.cart()[1]

                vixi = i.velocity.cart()[0]
                viyi = i.velocity.cart()[1]
                # print(vixself, viyself, vixi, viyi, i.mass, self.mass)

                vfxself = -(((self.mass - i.mass) / (self.mass + i.mass)) * vixself + (
                        (2 * i.mass) / (self.mass + i.mass)) * vixi) * min(self.rectitude, i.rectitude)
                vfyself = (((self.mass - i.mass) / (self.mass + i.mass)) * viyself + (
                        (2 * i.mass) / (self.mass + i.mass)) * viyi) * min(self.rectitude, i.rectitude)

                rho = np.sqrt(vfxself ** 2 + vfyself ** 2)
                phi = np.arctan2(vfyself, vfxself) * 180 / np.pi

                self.velocity.r = phi
                self.velocity.f = rho

                # time.sleep(self.parent._epoch_tps)

class Particle(PhysicsBody):

    def __init__(self, parent, x = 0, y = 0, r = 10, **kwargs):
        
        self.radius = r
        self.r = self.radius # Alias
        super().__init__(parent, x, y, r*2, r*2, **kwargs)
        

    def reflect_vector(self):
        vixself = self.velocity.cart()[0]
        viyself = self.velocity.cart()[1]

        vixi = 0
        viyi = 0
        # print(vixself, viyself, vixi, viyi, i.mass, self.mass)

        

        vfxself = -(((self.mass - 10e19) / (self.mass + 10e19)) * vixself + (
                (2 * 10e19) / (self.mass + 10e19)) * vixi) * self.rectitude
        vfyself = (((self.mass - 10e19) / (self.mass + 10e19)) * viyself + (
                (2 * 10e19) / (self.mass + 10e19)) * viyi) * self.rectitude

        rho = np.sqrt(vfxself ** 2 + vfyself ** 2)
        phi = np.arctan2(vfyself, vfxself) * 180 / np.pi

        self.velocity.r = phi
        self.velocity.f = rho

    def reflect_vector_yaxis(self):
        r = self.velocity

        vixself = r.cart()[0]
        viyself = r.cart()[1]

        vixi = 0
        viyi = 0
        # print(vixself, viyself, vixi, viyi, i.mass, self.mass)

        vfxself = (((self.mass - 10e19) / (self.mass + 10e19)) * vixself + (
                (2 * 10e19) / (self.mass + 10e19)) * vixi)
        vfyself = -(((self.mass - 10e19) / (self.mass + 10e19)) * viyself + (
                (2 * 10e19) / (self.mass + 10e19)) * viyi)

        rho = np.sqrt(vfxself ** 2 + vfyself ** 2)
        phi = np.arctan2(vfyself, vfxself) * 180 / np.pi

        self.velocity.r = phi
        self.velocity.f = rho

    def handle_wall_collisions(self):
        # Collided to bottom wall
        if self.y + self.r > self.parent.height:
            self.position.set(self.x, self.parent.height - self.r - 1)
            self.reflect_vector()
        # Collided to top wall
        if self.y - self.r < 0:
            self.position.set(self.x, self.r + 1)
            self.reflect_vector()
        # Collide to right wall
        if self.x + self.r > self.parent.width:
            self.position.set(self.parent.width - self.r - 1, self.y)
            self.reflect_vector_yaxis()
        # Collide to left wall
        if self.x - self.r < 0:
            self.position.set(self.r + 1, self.y)
            self.reflect_vector_yaxis()

    def handle_air_res(self):
        self.velocity.f *= 0.8
        if self.velocity.f < 0.1:
            self.velocity.f = 0
            

    def update(self):
        if self.use_collide:
            self.handle_wall_collisions()
        self.handle_forces()
        if self.use_airres:
            self.handle_air_res()

    

class TextFont:

    def __init__(self, name: str = "Helvetica", size: int = 15, type: str = "", color: str = "black"):
        self.name = name
        self.size = size
        self.type = type
        self.color = color
    
    def __str__(self):
        return f"{self.name} {self.size} {self.type}"

class Text(GameObject):

    def __init__(self, parent, x = 0, y = 0, text = "Hello PyNamics World!", font=TextFont("Helvetica", 15), **kwargs):

        w, h = 10, 10
        super().__init__(parent, x, y, w, h)
        self.collision = False
        self.style.load_styles(kwargs.get("styles"))
        self.text = text
        self.font = font
        self.i=0

        #self.__setattr__ = self._silent__setattr__

    # This overrides the set attribute function when user does sometext.text = "anotherstring"
    # Therefore no need to do self.old == self.new
    def __setattr__(self, key, value):
        if key == "text":
            self.force_update += 1
        super(Text, self).__setattr__(key, value)

    def update(self):
        print(self.i)
        self.i+=1