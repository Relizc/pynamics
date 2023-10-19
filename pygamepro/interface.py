class Runnable:

    def __init__(self, function, kwargs, parent):
        self.function = function
        self.target = kwargs.get("target", None)
        self.run_delay = int(kwargs.get("run_delay", 0))
        self.tick = 0

        self.parent = parent

    def __call__(self, *args, **kwargs):
        if self.tick == self.run_delay:
            self.tick = 0
            self.function(self.parent, *args, **kwargs)
        else:
            self.tick += 1

class RenderableObject:

    def __init__(self, *args, **kwargs):
        pass

class PygameProObject:

    def __init__(self, *args, **kwargs):

        self.styles = kwargs.get("styles", {})
        
        self.listeners = {
            "pre-update": set(),
            "update": set(),
            "post-update": set(),
            "keyhold": set(),
            "keyhold.framebind": set(),
            "keydown": set(),
            "keydown.framebind": set(),
            "keyup": set(),
            "draw": set()
        }

        self.enabled = True

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def addEventListener(self, event, *args, **kwargs):

        def inner(func):
            
            self.listeners[event].add(Runnable(func, kwargs, self))
        
        return inner

    def callEventListeners(self, event, limit = lambda c: True, *args, **kwargs):

        for i in self.listeners[event]:
            if limit(i.target):
                i(*args, **kwargs)

        return

    def updateStyles(self, styles):
        self.styles = {**self.styles, **styles}
        