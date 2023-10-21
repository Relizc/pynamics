import tkinter

from .gameobject import *
from .interface import PyNamical
from .events import EventType

import threading
import time


class Event:
    def __init__(self, func, typeC=None, condition=None, ):
        self.func = func
        self.type = typeC
        self.condition = condition

    def type_down(self) -> str:
        # theType = self.type
        # if theType == EventType.KEYPRESSED:
        #     return keyboard.read_key()
        pass

    def type_bool_down(self) -> bool:
        # theKey = self.type
        # if theKey == EventType.APRESSED:
        #     return keyboard.is_pressed("a")
        pass


class GameManager(PyNamical):
    def __init__(self, dimensions: Dimension, tps: int = 128):
        super().__init__(None, no_parent=True)
        self.dimensions = dimensions
        self.width = dimensions.x
        self.length = dimensions.y
        self.objects = []
        self.updates = []
        self.listeners = []
        self.tpu = 1
        self.ticks = 0
        self.tpl = 1
        self.tps = tps
        self._epoch_tps = 1 / self.tps
        self.listenthread = threading.Thread(target=self.listen)
        self.framethread = threading.Thread(target=self.frame)
        self.fps=144
        self.updatethread = threading.Thread(target=self.update)
        self.terminated = False
        self.f = 0
        self._epoch_fps = 1/self.fps
        self.parent = None
        self.children = []

        self.pressed = {}

    def _key(self, e):
        eventCode = int(e.type)
        if eventCode == 2: # KeyPress
            self.pressed[e.keysym] = True
            self.call_event_listeners(EventType.KEYDOWN, str(e.keysym))
        elif eventCode == 3: # KeyUp
            self.pressed[e.keysym] = False
            self.call_event_listeners(EventType.KEYUP, str(e.keysym))
        pass

    def start(self):
        self.updatethread.start()
        self.listenthread.start()
        self.framethread.start()



        self.window._tk.after(100, self.frame)
        self.window._tk.bind("<KeyPress>", self._key)
        self.window._tk.bind("<KeyRelease>", self._key)
        self.window.start()


    def update(self):

        while True:

            if self.terminated: break

            self.call_event_listeners(EventType.TICK)

            for i in self.pressed:
                if self.pressed[i]:
                    self.call_event_listeners(EventType.KEYHOLD, i)

            self.ticks += 1

            for i in self.updates:
                i()

            time.sleep(self._epoch_tps)

    def listen(self):
        while True:

            if self.terminated: break

            for i in self.listeners:
                if isinstance(i, Event):
                    if i.condition is not None and i.condition():
                        i.func()
                    elif i.condition is None:
                        if i.type_bool_down():
                            i.func()
            time.sleep(self._epoch_tps)

    def frame(self):
        self.call_event_listeners(EventType.FRAME)
        self.f += 1
        self.window.blit()
        self.window.surface.after(int(self._epoch_fps*1000), self.frame)




    def set_ticks_per_update(self, tick: int):
        self.tpu = tick

    def set_ticks_per_listener(self, tick: int):
        self.tpl = tick

    def add_object(self, object: GameObject):
        self.objects.append(object)

