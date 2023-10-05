from .gameobject import GameObject
from .context import GameContext
from .dimensions import Dimension, Dimension2d, ClockResizer
from .logger import Logger
from .physics import MassBody

# ClockResizer Units
MILISECOND  = 0.001
MILISECONDS = 0.001
SECOND      = 1
SECONDS     = 1
MINUTE      = 60
MINUTES     = 60

# Max FPS Units
UNLIMITED   = 0
VSYNC       = -1

# Initialize Logger
Logger.init()

# Logger Channels
CLIENT      = 0
SERVER      = 1
INFO        = 2
WARNING     = 3
ERROR       = 4
DEBUG       = 5

from pygame.constants import *