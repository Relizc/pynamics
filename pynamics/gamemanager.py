import tkinter

from .gameobject import *
import threading
from enum import Enum
import time
import keyboard


class EventType(Enum):
    FRAME = 0x00
    TICK = 0x01
    KEYDOWN = 0x02
    KEYUP = 0x03
    KEYHOLD = 0x04

    KEYDOWN_FRAMEBIND = 0x12
    KEYUP_FRAMEBIND = 0x13
    KEYHOLD_FRAMEBIND = 0x14
    KEYPRESSED = 0x15
    APRESSED = 0x16


class Event:
    def __init__(self, func, typeC=None, condition=None, ):
        self.func = func
        self.type = typeC
        self.condition = condition

    def type_down(self) -> str:
        theKey = self.type
        if theKey == EventType.KEYPRESSED:
            return keyboard.read_key()

    def type_bool_down(self) -> bool:
        theKey = self.type
        if theKey == EventType.APRESSED:
            return keyboard.is_pressed("a")


class GameManager:
    def __init__(self, dimensions: Dimension, tps: int = 128):
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
        self.framethread = threading.Thread(target=self.update_frame)
        self.fps=60
        self.updatethread = threading.Thread(target=self.update)
        self.terminated = False
        self.f = 0
        self._epoch_fps = 1/self.fps
        self.parent = None
        self.children = []

    def start(self):
        self.updatethread.start()
        self.listenthread.start()
        self.framethread.start()



        self.window._tk.after(100, self.frame)
        self.window.start()
    def update_frame(self):
        while True:
            self.frame()
            time.sleep(self._epoch_fps)
    def update(self):

        while True:

            if self.terminated: break

            self.ticks += 1

            if self.ticks % self.tpu == 0:
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
        self.f += 1
        self.window.blit()




    def set_ticks_per_update(self, tick: int):
        self.tpu = tick

    def set_ticks_per_listener(self, tick: int):
        self.tpl = tick

    def add_object(self, object: GameObject):
        self.objects.append(object)

    def add_tick_update(self, function):

        self.updates.append(function)

        print(self.updates)

    def add_event_listener(self, eventtype=None, condition=None):

        if eventtype is None:
            def inner(func):
                self.listeners.append(Event(func, condition=condition))

            return inner
        elif condition is None:
            def inner(func):
                self.listeners.append(Event(func, typeC=eventtype))

            return inner
