
from .gameobject import GameObject, Point, doIntersect, LimitedArray
from ..interface import PyNamical
from ..dimensions import Vector, Vector2d, Dimension, Dimension2d
from ..events import EventType, KeyEvaulator

import time
import threading
import copy
import numpy as np
import math

class PhysicsBody(GameObject):
    def __init__(self, parent: PyNamical, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 mass: int = 1,
                 contents: str = None, from_points: tuple = None, row=1.225, rectitude=1, use_mass=True,
                 use_collide=True,
                 collision_type=1, use_gravity=True, use_airres=False, gravity=-0.1, **kwargs):
        super().__init__(parent, x, y, width, height, contents, from_points, **kwargs)

        self.events[EventType.COLLIDE] = []

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
        self.coefficient = 0.5
        self.rectitude = rectitude
        self.row = row
        self.use_mass = use_mass

        self.collision_type = int(collision_type)
        self.use_collide = use_collide
        self.force = Vector2d(0, 0)
        self.gravity = gravity
        self.past_positions = LimitedArray(PyNamical.MAIN_GAMEMANAGER.tps)

        # self.timeB = time.time()
        # self.timeA = time.tokl;,
        if self.use_gravity: self.force = Vector2d(90, self.gravity * self.mass)
        if self.use_mass:
            self.attach_movement_thread()

    def init_movement(self, force: int = 1):
        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Up"))
        def m(ctx, key):
            self.force.add_self(Vector2d(90, force))

        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Down"))
        def m(ctx, key):
            self.force.add_self(Vector2d(270, force))

        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Left"))
        def m(ctx, key):
            self.force.add_self(Vector2d(180, force))

        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Right"))
        def m(ctx, key):
            self.force.add_self(Vector2d(0, force))

    def attach_movement_thread(self):
        self.parent.ticksteplisteners += 1

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
        self.past_positions.push_add(copy.deepcopy(self.position))
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
            if isinstance(i, PhysicsBody) and i.uuid != self.uuid:

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


                self.position = self.past_positions.arr[-1]
                vixself = self.velocity.cart()[0]
                viyself = self.velocity.cart()[1]
                vixi = i.velocity.cart()[0]
                viyi = i.velocity.cart()[1]
                xmomentuminitial = vixself * self.mass + vixi * i.mass
                ymomentuminitial = viyself * self.mass + viyi * i.mass

                # print(vixself, viyself, vixi, viyi, i.mass, self.mass)

                vfxself = -(((self.mass - i.mass) / (self.mass + i.mass)) * vixself + (
                        (2 * i.mass) / (self.mass + i.mass)) * vixi) * min(self.rectitude, i.rectitude)
                vfyself = (((self.mass - i.mass) / (self.mass + i.mass)) * viyself + (
                        (2 * i.mass) / (self.mass + i.mass)) * viyi) * min(self.rectitude, i.rectitude)
                vfxi = (xmomentuminitial - self.mass * vfxself) / i.mass
                vfyi = (ymomentuminitial - self.mass * vfyself) / i.mass

                rho = np.sqrt(vfxself ** 2 + vfyself ** 2)
                phi = np.arctan2(vfyself, vfxself) * 180 / np.pi

                self.velocity.r = phi
                self.velocity.f = rho

                rho2 = np.sqrt(vfxi ** 2 + vfyi ** 2)
                phi2 = np.arctan2(vfyi, vfxi) * 180 / np.pi

                i.velocity.r = phi2
                i.velocity.f = rho2


class TopViewPhysicsBody(PhysicsBody):

    def __init__(self, parent: GameObject, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 mass: int = 1,
                 contents: str = None, from_points: tuple = None, use_airress=True,
                 floor_friction: float = 0.1, *args, **kwargs):
        self.coefficient = floor_friction
        super().__init__(parent, x, y, width, height, mass, contents, from_points, use_gravity=False,
                         use_airres=use_airress, *args, **kwargs)

    def update(self):
        self.acceleration = Vector2d(self.force.r, self.force.f / self.mass)
        self.force.clear()
        self.velocity.add_self(self.acceleration)
        self.acceleration.clear()
        self.position.add_vector(self.velocity)

        if self.use_airres:
            v = Vector2d(self.velocity.r + 180, self.velocity.f * self.coefficient)

            self.velocity.add_self(v)

        if self.velocity.f < 0.1:
            self.velocity.f = 0

    def init_movement(self, force: int = 1):
        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Up"),
                                        name="PhysicsBodyMovement")
        def m(ctx, key):
            self.force.add_self(Vector2d(90, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Down"),
                                        name="PhysicsBodyMovement")
        def m(ctx, key):
            self.force.add_self(Vector2d(270, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Left"),
                                        name="PhysicsBodyMovement")
        def m(ctx, key):
            self.force.add_self(Vector2d(180, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Right"),
                                        name="PhysicsBodyMovement")
        def m(ctx, key):
            self.force.add_self(Vector2d(0, force))


class Particle(PhysicsBody):

    def __init__(self, parent, x=0, y=0, r=10, circle_steps=64, **kwargs):

        self.radius = r
        self.r = self.radius  # Alias
        super().__init__(parent, x, y, r * 2, r * 2, **kwargs)

        self.circle_steps = circle_steps

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

class RigidBody(PhysicsBody):

    def __init__(self, parent, x, y, points=[]):

        self.rotation = 0

        super().__init__(parent, x, y)

        self.geometry = points

        self.points = list(points)


        self.angular_velocity = 0
        self.torque = 0

        self.attach_update_thread()

    def update(self):

        if self.rotation is None:
            self.rotation = 0
            return

        self.points = []
        for i in self.geometry:
            x, y = np.cos(self.rotation) * i[0] + np.sin(self.rotation) * i[1], -np.sin(self.rotation) * i[0] + np.cos(self.rotation) * i[1]
            self.points.append((x, y))

        self.angular_velocity += self.torque
        self.torque = 0
        self.rotation += self.angular_velocity