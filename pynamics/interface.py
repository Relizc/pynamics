from .styling import StyleLoader
from .events import EventType, EventHolder
from .logger import Logger
import uuid as ulib

def network_transferrable(clazz):

    PyNamical.P_can_io_classes += (clazz,)
    clazz.network_transferrable = True

    return clazz


def build_class_tree():
    points = {}
    init_functions = {}

    indegree_zero = []
    
    def dfs(fro):
        Logger.print(f"Class Tree Builder DFS passing node {fro}", channel=5)
        fro.__real_init__ = fro.__init__
        points[fro] = fro.__base__
        if len(fro.__subclasses__()) == 0:
            indegree_zero.append(fro)
            return
        for i in fro.__subclasses__():
            dfs(i)

    dfs(PyNamical)

    for element in indegree_zero:

        if issubclass(element, PyNamical.P_can_io_classes):
            def __init__wrapper(self, *args, **kwargs):
                self.__real_init__(*args, **kwargs)
                self.finish_creating()
            element.__init__ = __init__wrapper

class PyNamical(EventHolder):

    LINKER = {}
    linkedNetworkingDispatcher = None
    P_whitelisted = set()
    P_can_io_classes = ()
    MAIN_GAMEMANAGER = None

    def __init__(self, parent, no_parent=False, uuid=None):
        super().__init__()
        self.children = []
        self.Replicated = False
        self.style = StyleLoader()
        self.parent = parent
        self.uuid = uuid

        if self.uuid is None:
            self.uuid = ulib.uuid4()
        
        PyNamical.LINKER[self.uuid] = self

        if not no_parent:
            self.parent.children.append(self)


    def unbind(self):
        self.parent.children.remove(self)

    def finish_creating(self):
        # Making sure PN doesnt crash when creating a ConnectedClient PyNamical class when connecting
        if PyNamical.linkedNetworkingDispatcher is not None: 
            
            PyNamical.linkedNetworkingDispatcher.network_newly_created(self)

    def __setattr__(self, key, value):
        try:
            object.__setattr__(self, key, value)
        except:
            return
        
        if PyNamical.linkedNetworkingDispatcher is not None and key in self.P_whitelisted:
            PyNamical.linkedNetworkingDispatcher.network_edit(self, key, value)

    def add_children(self, obj):
        self.children.append(obj)
        obj.parent = self

    def set_parent(self, obj):
        obj.children.append(self)
        self.parent = obj



    def debug_unhighlight(self):
        pass

    def debug_highlight(self):
        pass

    def update(self):
        pass

    def attach_update_thread(self):
        PyNamical.MAIN_GAMEMANAGER.attach_thread(self, self.update)

    def edit_uuid(self, new):
        del PyNamical.LINKER[self.uuid]
        PyNamical.LINKER[new] = self
        self.uuid = new

    def delete(self):
        pass

def find_object_by_id(uid):
    return PyNamical.LINKER[uid]

