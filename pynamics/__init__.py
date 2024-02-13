from .display import ProjectWindow, ViewPort
from .gameobject import GameObject, TopViewPhysicsBody, Image, Text, Particle
from .gamemanager import GameManager,PhysicsBody
from .dimensions import Dimension, Dimension2d, Vector2d, Vector
from .events import EventHolder, EventType, KeyEvaulator
from .logger import Logger
from .socket import DedicatedServer, DedicatedClient
from .socket import *
from .utils import ExampleLargeBinaryObject
from . import utils
import pickle
# Aliases
Dim = Dimension
Dim2d = Dimension2d

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
def load_object_from_binary(path:str):
    f = open(path,"rb")

    obj = pickle.load(f)
    return obj