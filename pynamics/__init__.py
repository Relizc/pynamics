import os
os.environ["PN_PROTOCOL_VERSION"] = "144"


from .display import OpenGLProjectWindow, LegacyProjectWindow, USE_OPENGL, ImageTexture
from .gameobject.gameobject import GameObject, Image, Text, TextFont, FramedTexture, AnimatedSprite
from .gameobject.physics import RigidBody, PhysicsBody, TopViewPhysicsBody, Particle
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d, Vector2d, Vector, Color
from .events import EventHolder, EventType, KeyEvaulator
from .logger import Logger
from .socket import DedicatedServer, DedicatedClient
from .socket import *
from .utils import ExampleLargeBinaryObject
from .interface import PyNamical, find_object_by_id, build_class_tree
from .animation import *
from .sound import *
from . import utils
import pickle

Logger.init()


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

# Typing Hint implementation
class ProjectWindow:
    
    def __init__(self) -> None:
        pass

if os.environ.get("PN_WINDOW_MODE", "opengl") == "legacy":
    ProjectWindow = LegacyProjectWindow
    Logger.print("Forced Using Legacy Tkinter Window", channel=3)
else:
    ProjectWindow = OpenGLProjectWindow

Logger.print("&bInitialization completed.")
Logger.print(f"&ePy&aNamics &bVersion {VERSION}")
def load_object_from_binary(path:str):
    f = open(path,"rb")

    obj = pickle.load(f)
    return obj

build_class_tree()