import pynamics
import math

p = pynamics.Vector2d(15, 17)
n = pynamics.Vector2d(-12, 21)
print(p.cart())
print(n.cart())
print(p + n)

print(math.atan(0.03/36.96))

print(pynamics.Vector2d.from_xy(-128, -310))