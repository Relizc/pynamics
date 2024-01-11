
class DisplayEnum:
    AUTO = 0

class StyleLoader:

    def __init__(self):
        self.display = DisplayEnum.AUTO

    def load_styles(self, property):
        if property is None: return
        for i in property:
            self.set_style(i, property[i])

    def set_style(self, name, value):
        setattr(self, name, value)