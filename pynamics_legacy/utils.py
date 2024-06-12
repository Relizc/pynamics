from pynamics_legacy.gameobject.gameobject import GameObject
from .gamemanager import GameManager
from .interface import PyNamical
from .events import EventType, KeyEvaulator

import os
import uuid
import random


def establish_basic_movement(manager: GameManager, parent: GameObject):
    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Up"))
    def m(ctx):
        parent.position.y -= 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Down"))
    def m(ctx):
        parent.position.y += 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Left"))
    def m(ctx):
        parent.position.x -= 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Right"))
    def m(ctx):
        parent.position.x += 1


def establish_basic_movement_wasd(manager: GameManager, parent: GameObject):
    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("w"))
    def m(ctx):
        parent.position.y -= 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("s"))
    def m(ctx):
        parent.position.y += 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("a"))
    def m(ctx):
        parent.position.x -= 1

    @manager.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("d"))
    def m(ctx):
        parent.position.x += 1


class ExampleLargeBinaryObject(PyNamical):

    def __init__(self, parent):
        super().__init__(parent)

        for i in range(random.randint(1, 10)):
            self.__setattr__(str(uuid.uuid4()), os.urandom(random.randint(0, 1 << 8)))


