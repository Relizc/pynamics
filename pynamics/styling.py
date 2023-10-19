
class DisplayEnum:
    AUTO = 0

class StyleLoader:

    def __init__(self):
        self.display = DisplayEnum.AUTO

    def set_style(self, name, value):
        setattr(self, name, value)