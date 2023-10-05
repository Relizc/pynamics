from .interface import PygameProObject
from .dimensions import Dimension

class MassBody(PygameProObject):

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.massbody = self
        self.mass = kwargs.get("mass", 1)
        self.gravity = kwargs.get("gravity", 10) / parent.parent.tickspeed
        self.velocity = Dimension(0, 0)

        self.acceleration = Dimension(0, 0)
        self.netforce = Dimension(0, 0)

        self.air_resistance_coefficient = 0.1

        @self.parent.addEventListener("update")
        def gravity(ctx):

            self.add_force(Dimension(
                -self.velocity.x * self.air_resistance_coefficient,
                -self.velocity.y * self.air_resistance_coefficient
            )) # Air Res

            self.acceleration.set(
                self.netforce.x / self.mass,
                self.netforce.y / self.mass
            )

            self.velocity.add_dim(self.acceleration)
            self.velocity.add(0, self.gravity)

            ctx.x += self.velocity.x
            ctx.y += self.velocity.y
            #print(self.velocity, self.acceleration, self.netforce)
            self.netforce.set(0, 0)

        

    def clear(self):
        self.velocity = Dimension(0, 0)
        self.acceleration = Dimension(0, 0)
        self.netforce = Dimension(0, 0)

    def add_force(self, dim: Dimension):
        self.netforce.add_dim(dim)


