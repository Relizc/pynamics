
import enum
import threading
import random

import traceback

from .logger import Logger

def commit(e, s, a, kill=False, special=None):
    None
DebugAttacher = commit
def change_debug_attacher(func):
    global DebugAttacher
    DebugAttacher = func

class EventType():

    NONE = 0x00

    KEYDOWN = 0x01
    KEYHOLD = 0x02
    KEYUP = 0x03
    STARTUP = 0x04

    FRAME = 0x00
    TICK = 0x10

    KEYDOWN_FRAMEBIND = 0x12
    KEYUP_FRAMEBIND = 0x13
    KEYHOLD_FRAMEBIND = 0x14
    KEYPRESSED = 0x15
    APRESSED = 0x16

    HOVER = 0x20
    NO_HOVER = 0x21

    ONCLICK = 0x22

    COLLIDE = 0x23


    CLIENT_CONNECTED = 0x100

event_name_linker = {
    EventType.NONE: "NullEvent",
    EventType.KEYDOWN: "KeyboardListenerPress",
    EventType.KEYUP: "KeyboardListenerUnpress",
    EventType.KEYHOLD: "KeyboardListenerHold",
    EventType.TICK: "GamemanagerTick",
    EventType.STARTUP: "GamemanagerStartup",
    EventType.ONCLICK: "UserInterfaceClick",
    EventType.CLIENT_CONNECTED: "NetworkClientConnected",
    EventType.COLLIDE: "PhysicsBodyCollideEvent"
}
events_first = list(EventType.__dict__.keys())
events_second = list(EventType.__dict__.values())

class Executable:

    def __init__(self, function, condition, killafter = 0, threaded=True, name="GenericEvent", belong_group = "Event"):
        self.function = function
        self.runs = 0
        self.killafter = killafter
        self.condition = condition # lambda
        self.type = name
        self.belong_group = belong_group
        self.event_id = random.randint(-2147483648, 2147483647)
        self.debug_del = None
        self.threaded = threaded

    def __call__(self, *args, **kwargs):
        self.runs += 1
        try:
            self.function(self, *args, **kwargs)
        except Exception as e:
            Logger.print(f"Event {self.type} (ID={self.event_id}) threw an exception: {traceback.format_exc()}", channel=4)
        if self.runs == self.killafter:
            self.function = None

    def terminate(self):
        self.function = None

    def stop(self):
        self.terminate()

class KeyEvaulator:

    def __init__(self, key):
        self.key = key

    def __call__(self, inp, *args, **kwargs):
        return inp == self.key

class EventPriority:
    HIGHEST = 0
    LOWEST = 2147483647

registered_events = set()
def get_registered_events():
    return len(registered_events)

def event_registered(exe):
    global registered_events
    registered_events.add(exe)
    DebugAttacher(exe, exe, exe, special=0)

def event_unregistered(exe):
    global registered_events
    try:
        registered_events.remove(exe)
        DebugAttacher(exe, exe, exe, special=1)
    except:
        pass
    

class EventHolder:

    def __init__(self):
        self.events = {
            EventType.NONE: [],
            EventType.KEYDOWN: [],
            EventType.KEYHOLD: [],
            EventType.KEYUP: [],
            EventType.TICK: [],
            EventType.HOVER: [],
            EventType.NO_HOVER: [],
            EventType.STARTUP: [],
        }

        self.event_linker = {}

    def add_event_listener(self, event: EventType = EventType.NONE, priority: EventPriority=EventPriority.LOWEST, condition=lambda i: True, tick_delay=0, replicated=False, killafter:int = 0, id:int = None,
                           name: str = None, threaded=True):
        """

        :param replicated: `Boolean` **ONLY USE THIS WHEN THERE IS AN AVALIABLE SERVER** A replicated event that will run on the client side.
        :param event: `EventType` The event type of this event listener
        :param priority: `EventPriority` Determines the order that the listener should run. If a listener has high priority, it will be run last, and vice versa.
        :param condition: `Function` A lambda or a function that takes a specific input based on the EventType, and returns a boolean to tell whether the event should run or not.
        :param tick_delay: `Integer` How many ticks it takes to execute this event.
        :return:
        """

        if name is None:
            name = event_name_linker.get(event, "GenericEvent")

        if id is None:
            id = random.randint(-2147483648, 2147483647)


        def inner(function):
            func = Executable(function, condition, killafter=killafter, name=name, 
                              threaded=threaded, belong_group=events_first[events_second.index(event)])
            func.event = event

            event_registered(func)
            self.events[event].insert(2147483647 - priority, func)
            func.id = id
            self.event_linker[id] = func

        return inner


    def call_event_listeners(self, event: EventType = EventType.NONE, condition=None, *args, **kwargs):
        """
        Call all event listeners with optional condition that will be passed into a function's condition lambda event
        :param event: The event name, EventType
        :param condition: The value that will be passed into the lambda function's i value and asserted.
        :return: None, call events with lambda functions that returns true
        """

        for func in self.events[event]:
            if func.condition(condition):
                if func.function is None:
                    DebugAttacher(event, self, func, kill=True)
                    self.events[event].remove(func)
                    event_unregistered(func)
                    del self.event_linker[func.id]
                else:
                    DebugAttacher(event, self, func)
                    #func(self, *args, **kwargs)
                    if func.threaded:
                        n = threading.Thread(target=lambda: func(*args, **kwargs))
                        n.start()
                        #print("thread")
                    else:
                        func(*args, **kwargs)
                        #print("no thread")

    def kill_event(self, event_id: int):
        try:
            func = self.event_linker[event_id]
        except KeyError:
            raise KeyError(
                "Event ID Not Found"
            )
        DebugAttacher(func.event, self, func, kill=True)
        self.events[func.event].remove(func)
        event_unregistered(func)
        del self.event_linker[event_id]
