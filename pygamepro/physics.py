from .interface import PygameProObject
from .dimensions import Dimension
import pygame

MASSBODIES = []


class CollisionHandler:

    def __init__(self, parent):
        self.parent = parent
        self.masses = []

    def handle(self, obj):
        self.masses.append(obj)
        pass

    def test(self):
        for i in range(len(self.masses) - 1):
            for j in range(i + 1, len(self.masses)):
                a = self.masses[i]
                b = self.masses[j]
                
                self.predict_step_collison(a, b)

                # collide = a.parent.rect.colliderect(b.parent.rect)

                # if collide:
                #     a.clear()
                #     b.clear()

    def predict_step_collison(self, a, b):
        # print(a.parent.x, a.parent.y)
        # print(a.velocity, b.velocity)
        collide = False
        
        #if a.parent.x + a.velocity.x > b.parent.x + b.velocity.x or a.parent.y + a.velocity.y > b.parent.y + b.velocity.y:
            #collide = True
        self.future_movement(a, b)

    def future_movement(self, a, b):
        # Positions in Next Tick
        a_tl, b_tl = self.predict(a.parent.topleft, b.parent.topleft, a.velocity, b.velocity)
        a_tr, b_tr = self.predict(a.parent.topright, b.parent.topright, a.velocity, b.velocity)
        a_bl, b_bl = self.predict(a.parent.bottomleft, b.parent.bottomleft, a.velocity, b.velocity)
        a_br, b_br = self.predict(a.parent.bottomright, b.parent.bottomright, a.velocity, b.velocity)
        
        #print(a.parent.topleft, a_tl)
        self.move_cross((a.parent.topleft, a_tl), (b.parent.topleft, b.parent.topright))
        #print(b_tl, b_tr, b_bl, b_br)

    def move_cross(self, point: tuple, b: tuple):
        print(point, b)

    def predict(self, a, b, vela, velb) -> bool:
        cur_a, cur_b = a, b
        next_a, next_b = (cur_a[0] + vela.x, cur_a[1] + vela.y), (cur_b[0] + velb.x, cur_b[1] + velb.y)
        return next_a, next_b
        # inbound_x = rect.topleft[0] < point[0] < rect.bottomright[0]
        # inbound_y = rect.topleft[1] < point[1] < rect.bottomright[1]
        # print(inbound_x, inbound_y)


class MassBody(PygameProObject):

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.parent.massbody = self
        self.parent.parent.collision.handle(self)
        self.mass = kwargs.get("mass", 1)
        self.gravity = kwargs.get("gravity", 10) / parent.parent.tickspeed
        self.velocity = Dimension(0, 0)
        self.anchored = kwargs.get("anchored", False)

        self.acceleration = Dimension(0, 0)
        self.netforce = Dimension(0, 0)

        self.air_resistance_coefficient = 0.1

        self.show_force_lines = True

        if self.show_force_lines:
            @self.parent.addEventListener("draw")
            def drawforce(self):
                pygame.draw.line(self.parent.main, (255, 0, 0), self.rect.center, (self.rect.center[0] + self.massbody.netforce.x * 10, self.rect.center[1] + self.massbody.netforce.y * 20))
                pygame.draw.line(self.parent.main, (255, 0, 255), self.rect.center, (self.rect.center[0] + self.massbody.velocity.x * 10, self.rect.center[1] + self.massbody.velocity.y * 20))

        @self.parent.addEventListener("update")
        def gravity(ctx):

            self.add_force(Dimension(
                -self.velocity.x * self.air_resistance_coefficient,
                -self.velocity.y * self.air_resistance_coefficient
            )) # Air Res

            self.add_force(Dimension(
                0, self.mass * self.gravity
            ))

            self.acceleration.set(
                self.netforce.x / self.mass,
                self.netforce.y / self.mass
            )

            if self.anchored:
                self.acceleration.set(0, 0)

            self.velocity.add_dim(self.acceleration)

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


