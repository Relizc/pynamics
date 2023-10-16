import pygame
import threading
import time

from .dimensions import Dimension, Dimension2d
from .interface import PygameProObject
from .gameobject import GameObjectCreator
from .debugger import Debugger
from .physics import CollisionHandler

class GameContext(PygameProObject, GameObjectCreator):

    def __init__(self, size_x: int, size_y: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.clock = pygame.time.Clock()
        self.maxfps = kwargs.get("maxfps", 0)
        self.tickspeed = kwargs.get("tick", 128)
        self.terminate = False
        self.sprites = pygame.sprite.Group()
        self.collision = CollisionHandler(self)

        self.debugger = Debugger(self)

        self.smoothblit = kwargs.get("smoothdrawing", False)

        self.fpt = self.maxfps / self.tickspeed
        self._fpt = self.maxfps / self.tickspeed
        if self.fpt == 0: self._fpt_cl = -1
        else: self._fpt_cl = 0

        self.f = [0, 0]

    def update(self):
        self.sprites.update()
        

    def from_dim(scale: Dimension, *args, **kwargs):
        return GameContext(scale.x, scale.y, *args, **kwargs)

    def set_title(self, caption: str):
        pygame.display.set_caption(caption)

    def _thread_update_styles(self):
        # Color Update
        color = self.styles.get("background-color", None)
        c = (0, 0, 0)
        
        if isinstance(color, tuple):
            c = color
        elif isinstance(color, str):
            if color == "white":
                c = (255, 255, 255)
            if color == "red":
                c = (255, 0, 0)
        
        self.main.fill(c)

    def _thread_frame_update(self):

        self.callEventListeners("pre-update")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                self.callEventListeners("keydown", lambda i: i == event.key)
            if event.type == pygame.KEYUP:
                self.callEventListeners("keyup", lambda i: i == event.key)
        
        pressed = pygame.key.get_pressed()
        self.callEventListeners("keyhold.framebind", lambda i: pressed[i])

        self._thread_update_styles()

        self.callEventListeners("update")

        for i in self.sprites:
            i.draw(self, self.main)

        

        self.f[0] += 1
        self._fpt += 1
        pygame.display.update()

        self.callEventListeners("post-update")

        

    def _thread_self_tick(self):
        self.main = pygame.display.set_mode((self.size_x, self.size_y), vsync=1)

        self.gametick = threading.Thread(target=self._thread_self_game_tick)
        self.gametick.start()

        while True:
            self._thread_frame_update()
            self.clock.tick(self.maxfps)
            if self._fpt_cl == -1:
                self.fpt = self.clock.get_fps() / self.tickspeed

    def _thread_self_game_tick(self):
        self.game_tick_clock = pygame.time.Clock()
        while True:
            if self.terminate: break

            pressed = pygame.key.get_pressed()
            self.callEventListeners("keyhold", lambda i: pressed[i])

            self.collision.test()

            self.f[1] += 1
            self.fpt = int(self._fpt)
            self._fpt = 0
            
            self.update()
            self.game_tick_clock.tick(self.tickspeed)

    def start(self):
        self.tick = threading.Thread(target=self._thread_self_tick)
        self.tick.start()

        

        print("GameContext is running in thread " + str(self.tick))