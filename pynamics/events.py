
import enum

def commit(e, s, a):
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


    CLIENT_CONNECTED = 0x100

    

class Executable:

    def __init__(self, function, condition):
        self.function = function
        self.condition = condition # lambda

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)

class KeyEvaulator:

    def __init__(self, key):
        self.key = key

    def __call__(self, inp, *args, **kwargs):
        return inp == self.key

class EventPriority:
    HIGHEST = 0
    LOWEST = 2147483647


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
            EventType.STARTUP: []
        }

    def add_event_listener(self, event: EventType = EventType.NONE, priority: EventPriority=EventPriority.LOWEST, condition=lambda i: True, tick_delay=0, replicated=False):
        """

        :param replicated: `Boolean` **ONLY USE THIS WHEN THERE IS AN AVALIABLE SERVER** A replicated event that will run on the client side.
        :param event: `EventType` The event type of this event listener
        :param priority: `EventPriority` Determines the order that the listener should run. If a listener has high priority, it will be run last, and vice versa.
        :param condition: `Function` A lambda or a function that takes a specific input based on the EventType, and returns a boolean to tell whether the event should run or not.
        :param tick_delay: `Integer` How many ticks it takes to execute this event.
        :return:
        """

        def inner(function):
            self.events[event].insert(2147483647 - priority, Executable(function, condition))

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
                DebugAttacher(event, self, func)
                func(self, *args, **kwargs)
