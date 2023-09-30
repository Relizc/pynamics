import pygame
import threading

from .dimensions import Dimension, Dimension2d
from .interface import PygameProObject

class GameContext(PygameProObject):

    def __init__(self, size_x: int, size_y: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.clock = pygame.time.Clock()

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

        self._thread_update_styles()

        self.callEventListeners("update")

        pygame.display.update()

        self.callEventListeners("post-update")

        

    def _thread_self_tick(self):
        self.main = pygame.display.set_mode((self.size_x, self.size_y))

        while True:
            self._thread_frame_update()
            self.clock.tick(60)

    def start(self):
        self.tick = threading.Thread(target=self._thread_self_tick)
        self.tick.start()
        print("GameContext is running in thread " + str(self.tick))