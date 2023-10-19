from .gameobject import *
import threading
from enum import Enum
import time


class EventType(Enum):
    FRAME = 0x00
    TICK = 0x01
    KEYDOWN = 0x02
    KEYUP = 0x03
    KEYHOLD = 0x04

    KEYDOWN_FRAMEBIND = 0x12
    KEYUP_FRAMEBIND = 0x13
    KEYHOLD_FRAMEBIND = 0x14


class Event:
    def __init__(self, func, type: EventType = None, condition=None, ):
        self.func = func
        self.type = type
        self.condition = condition


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
        self.updatethread = threading.Thread(target=self.update)
        self.terminated = False
        self.f = 0

        self.parent = None
        self.children = []

    def start(self):
        self.updatethread.start()
        self.listenthread.start()

        self.window._tk.after(100, self.frame)
        self.window.start()

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

            time.sleep(self._epoch_tps)

    def frame(self):
        self.f += 1
        print(f"This is frame {self.f}")
        self.window._tk.after(0, self.frame)

    def kill(self):
        self.updatethread.daemon = True
        self.listenthread.daemon = True

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
                self.listeners.append(Event(func, type=eventtype))

            return inner
