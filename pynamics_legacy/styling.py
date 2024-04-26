
class DisplayEnum:
    AUTO = 0

class StyleLoader:

    def __init__(self):
        self.display = DisplayEnum.AUTO
        self.property = None

    def load_styles(self, property):
        self.property = property
        if property is None: return
        for i in property:
            self.set_style(i, property[i])

    def set_style(self, name, value):
        setattr(self, name, value)