

class EventType:

    NONE = 0x00

    KEYDOWN = 0x01
    KEYHOLD = 0x02
    KEYUP = 0x03

    FRAME = 0x00
    TICK = 0x01

    KEYDOWN_FRAMEBIND = 0x12
    KEYUP_FRAMEBIND = 0x13
    KEYHOLD_FRAMEBIND = 0x14
    KEYPRESSED = 0x15
    APRESSED = 0x16

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

class EventHolder:

    def __init__(self):
        self.events = {
            EventType.NONE: [],
            EventType.KEYDOWN: [],
            EventType.KEYHOLD: [],
            EventType.KEYUP: [],
        }

    def add_event_listener(self, event: EventType = EventType.NONE, condition=lambda i: True, tick_delay=0):

        def inner(function):
            self.events[event].append(Executable(function, condition))

        return inner

    def call_event_listeners(self, event: EventType = EventType.NONE, condition=None):
        """
        Call all event listeners with optional condition that will be passed into a function's condition lambda event
        :param event: The event name, EventType
        :param condition: The value that will be passed into the lambda function's i value and asserted.
        :return: None, call events with lambda functions that returns true
        """
        for func in self.events[event]:
            if func.condition(condition):
                func(self)
