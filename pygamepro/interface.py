class Runnable:

    def __init__(self, function, kwargs, parent):
        self.function = function
        self.run_delay = int(kwargs.get("run_delay", 0))
        self.tick = 0

        self.parent = parent

    def __call__(self):
        if self.tick == self.run_delay:
            self.tick = 0
            self.function(self.parent)
        else:
            self.tick += 1

class PygameProObject:

    def __init__(self, *args, **kwargs):

        self.styles = kwargs.get("styles", None)
        
        self.listeners = {
            "pre-update": set(),
            "update": set(),
            "post-update": set(),
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def addEventListener(self, event, *args, **kwargs):

        def inner(func):
            
            self.listeners[event].add(Runnable(func, kwargs, self))
        
        return inner

    def callEventListeners(self, event):

        for i in self.listeners[event]:
            i()

        return

    def updateStyles(self, styles):
        self.styles = {**self.styles, **styles}
        