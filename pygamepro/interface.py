class Runnable:

    def __init__(self, function, kwargs):
        self.function = function
        self.run_delay = kwargs.get("run_delay", 0)
        self.tick = 0

    def __call__(self):
        if self.tick == self.run_delay:
            self.tick = 0
            self.function()
        self.tick += 1

class PygameProObject:

    def __init__(self, *args, **kwargs):

        self.styles = kwargs.get("styles", None)
        
        self.listeners = {}

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def addEventListener(self, event, *args, **kwargs):

        def inner(func):
            
            self.listeners[event] = Runnable(func, kwargs)
        
        return inner

    def updateStyles(self, styles):
        self.styles = {**self.styles, **styles}
        