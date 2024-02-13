from .styling import StyleLoader
from .events import EventType, EventHolder
import uuid as ulib




class PyNamical(EventHolder):

    LINKER = {}
    linkedNetworkingDispatcher = None
    P_whitelisted = set()

    def __init__(self, parent, no_parent=False, uuid=None):
        super().__init__()
        self.Replicated = False
        self.style = StyleLoader()
        self.parent = parent
        self.uuid = uuid

        if self.uuid is None:
            self.uuid = ulib.uuid4()
        PyNamical.LINKER[self.uuid] = self

        if not no_parent:
            self.parent.children.append(self)
        self.children = []

    def __setattr__(self, key, value):
        try:
            object.__setattr__(self, key, value)
        except:
            return
        if PyNamical.linkedNetworkingDispatcher is not None and key in self.P_whitelisted:
            PyNamical.linkedNetworkingDispatcher.network_edit(self, key, value)

    def debug_unhighlight(self):
        pass

    def debug_highlight(self):
        pass

    def edit_uuid(self, new):
        del PyNamical.LINKER[self.uuid]
        PyNamical.LINKER[new] = self
        self.uuid = new

    def delete(self):
        pass

