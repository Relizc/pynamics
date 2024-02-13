from .styling import StyleLoader
from .events import EventType, EventHolder
import uuid as ulib

LINKER = {}


class PyNamical(EventHolder):

    def __init__(self, parent, no_parent=False, uuid=None):
        super().__init__()
        self.style = StyleLoader()
        self.parent = parent
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = ulib.uuid4()
        LINKER[self.uuid] = self

        if not no_parent:
            self.parent.children.append(self)
        self.children = []

    def debug_unhighlight(self):
        pass

    def debug_highlight(self):
        pass

    def delete(self):
        pass

