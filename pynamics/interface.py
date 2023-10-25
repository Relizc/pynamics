from .styling import StyleLoader
from .events import EventType, EventHolder



class PyNamical(EventHolder):

    def __init__(self, parent, no_parent=False):
        super().__init__()
        self.style = StyleLoader()
        self.parent = parent

        if not no_parent:
            self.parent.children.append(self)
        self.children = []



    def delete(self):
        pass
