from .display import ProjectWindow, ViewPort
from .gameobject import GameObject, TopViewPhysicsBody, Image
from .gamemanager import GameManager,PhysicsBody,Vector2d
from .dimensions import Dimension, Dimension2d
from .events import EventHolder, EventType, KeyEvaulator
from .logger import Logger
from . import utils

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

K_r = "r"

K_backquote = 'quoteleft'

VERSION = "1.0.0"

Logger.print("&bInitialization completed.")
Logger.print(f"&ePy&aNamics &bVersion {VERSION}")