from .display import ProjectWindow, ViewPort
from .gameobject import GameObject
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d
from .events import EventHolder, EventType, KeyEvaulator

# Aliases
class Dim(Dimension): pass
class Dim2d(Dimension2d): pass

K_UP = "Up"
K_DOWN = "Down"
K_RIGHT = "Right"
K_LEFT = "Left"
K_a = "a"
K_b = "b"
K_c = "c"
K_d = "d"