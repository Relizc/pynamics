
from .gameobject import GameObject
from ..dimensions import Vector, Dimension

import time
import threading
import math

class RigidBody(GameObject):

    def __init__(self, parent, x=0, y=0, points=[], *args, **kwargs):
        super().__init__(parent, x, y, *args, **kwargs)

        self.points = points
        self.momentum_points = list(points)

        self.acceleration = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.force = Vector(0, 0)

        self.torque = 0
        self.angular_acceleration = 0
        self.angular_velocity = 0
        self.rotation = 0


        self.attach_update_thread()

    def _recalc_position(self):
        self.momentum_points = []
        for i in self.points:
            x = math.cos(self.rotation) * i[0] - math.sin(self.rotation) * i[1]
            y = math.sin(self.rotation) * i[0] + math.cos(self.rotation) * i[1]
            self.momentum_points.append((x, y))

    def update(self):
        self._recalc_position()



