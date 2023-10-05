import pygame
import threading

from .dimensions import Dimension, Dimension2d
from .interface import PygameProObject
from .gameobject import GameObjectCreator

class GameContext(PygameProObject, GameObjectCreator):

    def __init__(self, size_x: int, size_y: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.clock = pygame.time.Clock()
        self.maxfps = kwargs.get("maxfps", 0)

        self.sprites = pygame.sprite.Group()

    def update(self):
        self.sprites.update()
        print("update")
        

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
        
        self.main.fill(c)

    def _thread_frame_update(self):

        self.callEventListeners("pre-update")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.gametick.kill()

        self._thread_update_styles()

        self.callEventListeners("update")

        self.sprites.draw(self.main)

        pygame.display.update()
        self.set_title("fps: " + str(self.clock.get_fps()))

        self.callEventListeners("post-update")

        

    def _thread_self_tick(self):
        self.main = pygame.display.set_mode((self.size_x, self.size_y), vsync=1)

        while True:
            self._thread_frame_update()
            self.clock.tick(self.maxfps)

    def _thread_self_game_tick(self):
        self.game_tick_clock = pygame.time.Clock()
        while True:
            print("game tick")
            self.game_tick_clock.tick(128)

    def start(self):
        self.tick = threading.Thread(target=self._thread_self_tick)
        self.tick.start()

        self.gametick = threading.Thread(target=self._thread_self_game_tick)
        self.gametick.start()

        print("GameContext is running in thread " + str(self.tick))