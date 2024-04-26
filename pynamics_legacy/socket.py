import sys
import uuid
from .interface import PyNamical
import socket
import threading
import time
from .logger import Logger
from .events import EventType
import pickle
import struct
import traceback
from numpy import float32, float64
from .dimensions import Dimension, Vector
from .events import *
import tkinter.messagebox as tkmsg

# Helper Object (Byte)
class u_int8(int): pass

# Helper Object (Short)
class u_int16(int): pass

# Helper Object (Integer)
class u_int32(int): pass

# Helper Object (Long)
class u_int64(int): pass

# Helper Object (Byte)
class int8(int): pass

# Helper Object (Short)
class int16(int): pass

# Helper Object (Integer)
class int32(int): pass

# Helper Object (Long)
class int64(int): pass

# Helper Object (Byte Array)
class bytesArray(bytes): pass

# Helper Object (Regular Int)
class VarInt(int): pass

# Helper Object (Extended Float)
class double(float64): pass

T_TypeToInt = {
    int: 0x08,
    str: 0x09,
    bytes: 0x0b,
    bool: 0x0c,
    float: 0x0d,
    double: 0x0e,
    float32: 0x0d,
    float64: 0x0e,
    Dimension: 0x10,
    Vector: 0x12
}

T_IntToType = {
    0x00: u_int8,
    0x01: u_int16,
    0x02: u_int32,
    0x03: u_int64,
    0x04: int8,
    0x05: int16,
    0x06: int32,
    0x07: int64,
    0x08: VarInt,
    0x09: str,
    0x0a: uuid.UUID,
    0x0b: bytes,
    0x0c: bool,
    0x0d: float,
    0x0e: double,
    0x10: Dimension,
    0x12: Vector
}

class Packet:

    fields = []

    def __init__(self, *args, buffer=b"", write_packetid=True):
        self.buffer = b""
        self.read_pointer = 1

        if write_packetid:
            self.write_uint8(self.packetid)

        self.buffer += buffer
        self.objects = []

        self.T_PacketCorrespondingTypeWriter = {
            int: self.write_varint,
            u_int8: self.write_uint8,
            u_int16: self.write_uint16,
            u_int32: self.write_uint32,
            u_int64: self.write_uint64,
            int8: self.write_int8,
            int16: self.write_int16,
            int32: self.write_int32,
            int64: self.write_int64,
            str: self.write_string,
            uuid.UUID: self.write_UUID,
            bytes: self.write_bytes,
            VarInt: self.write_varint,
            bool: self.write_bool,
            float: self.write_float,
            double: self.write_double,
            float64: self.write_double,
            Dimension: self.write_dimension,
            Vector: self.write_vector
        }
        self.T_PacketCorrespondingTypeReader = {
            int: self.read_varint,
            u_int8: self.read_uint8,
            u_int16: self.read_uint16,
            u_int32: self.read_uint32,
            u_int64: self.read_uint64,
            int8: None,
            int16: None,
            int32: None,
            int64: None,
            str: self.read_string,
            uuid.UUID: self.read_UUID, 
            bytes: self.read_bytes,
            VarInt: self.read_varint,
            bool: self.read_bool,
            float: self.read_float,
            double: self.read_double,
            float64: self.read_double,
            Dimension: self.read_dimension,
            Vector: self.read_vector
        }

        if len(args) != 0:
            for kw in range(len(self.fields)):
                f = self.fields[kw]
                a = args[kw]
                if isinstance(a, f):
                    self.type_write(a, f)
                else:
                    raise TypeError(
                        f"Field {kw} requires {f.__name__}, got {a} ({a.__class__.__name__}) instead.")


    def write(self, var):
        pass

    def write_bool(self, var):
        if var:
            self.write_uint8(1)
        else:
            self.write_uint8(0)

    def write_float(self, var):
        x = struct.pack("f", var)
        self.buffer += x


    def write_with_type(self, var):
        typeint = T_TypeToInt[var.__class__]
        self.write_varint(typeint)
        self.T_PacketCorrespondingTypeWriter[var.__class__](var)

    def type_write(self, var, type):
        self.T_PacketCorrespondingTypeWriter[type](var)
        self.objects.append(var)

    def write_uint8(self, var): 
        self.buffer += bytes([var % 0x100])

    def write_uint16(self, var):
        op = 1 << 8
        self.write_uint8(var)
        self.write_uint8((var // op) % op)
    
    def write_uint32(self, var):
        op = 1 << 16
        self.write_uint16(var % op)
        self.write_uint16((var // op) % op)

    def write_uint64(self, var):
        op = 1 << 32
        self.write_uint32(var % op)
        self.write_uint32((var // op) % op)

    # https://github.com/fmoo/python-varint/blob/master/varint.py also for readvarint
    def write_varint(self, var):
        while True:
            towrite = var & 0x7f
            var >>= 7
            if var:
                self.buffer += bytes([towrite | 0x80])
            else:
                self.buffer += bytes([towrite])
                break

    def write_string(self, var):
        encoded = var.encode()
        self.write_varint(len(encoded))
        self.buffer += encoded

    def write_int8(self, var):
        self.write_uint8(var + 0x80)
    
    def write_int16(self, var):
        self.write_uint16(var + 0x8000)

    def write_int32(self, var):
        self.write_uint32(var + 0x800000)

    def write_int64(self, var):
        self.write_uint64(var + 0x80000000)

    def write_UUID(self, var: uuid.UUID):
        self.buffer += var.bytes

    def write_bytes(self, var):
        self.write_varint(len(var))
        self.buffer += var

    def read_varint(self):
        shift = 0
        result = 0
        while True:
            i = self.buffer[self.read_pointer]
            self.read_pointer += 1
            result |= (i & 0x7f) << shift
            shift += 7
            
            if not (i & 0x80):
                break
            
        return result
    
    def read_bool(self):
        return bool(self.read_uint8())
    
    def read_string(self):
        length = self.read_varint()
        p = self.buffer[self.read_pointer : self.read_pointer + length]
        self.read_pointer += length
        return p.decode()
    
    def read_uint8(self):
        c = self.buffer[self.read_pointer]
        self.read_pointer += 1
        return c
    
    def read_uint16(self):
        return self.read_uint8() + self.read_uint8() * 0x100
    
    def read_uint32(self):
        return self.read_uint16() + self.read_uint16() * 0x10000
    
    def read_uint64(self):
        return self.read_uint16() + self.read_uint16() * 0x1000000
    
    def read_UUID(self):
        b = self.buffer[self.read_pointer : self.read_pointer + 16]
        self.read_pointer += 16
        return uuid.UUID(bytes=b)
    
    def read_bytes(self):
        l = self.read_varint()
        b = self.buffer[self.read_pointer : self.read_pointer + l]
        self.read_pointer += l
        return b

    def read_with_type(self):
        typeint = self.read_varint()
        readed = self.T_PacketCorrespondingTypeReader[T_IntToType[typeint]]()
        return readed

    def read_float(self):
        x = struct.unpack("f", self.buffer[self.read_pointer : self.read_pointer + 4])[0]
        self.read_pointer += 4
        return x
    
    def read_all(self):
        for i in self.fields:
            self.objects += self.T_PacketCorrespondingTypeReader[i]()

    def size(self):
        """Gets the packet size, in number of bytes"""
        return len(self.buffer)

    def write_double(self, var):
        c = struct.pack("d", var)
        self.buffer += c

    def read_double(self):
        x = struct.unpack("d", self.buffer[self.read_pointer : self.read_pointer + 8])[0]
        self.read_pointer += 8
        return x

    def write_dimension(self, var: Dimension):
        self.write_double(var.x)
        self.write_double(var.y)

    def read_dimension(self):
        x = self.read_double()
        y = self.read_double()
        return Dimension(x, y)

    def write_vector(self, var: Vector):
        self.write_double(var.r)
        self.write_double(var.f)

    def read_vector(self):
        return Vector(self.read_double(), self.read_double())
    
    def __repr__(self):
        n = ", ".join(map(lambda i: i.__name__, self.fields))
        return f"{self.__class__.__name__}[{n}]"
        
    def handle(self, parent, connection, ip):
        pass

P_PacketIdFinder = {}

def PacketFields(*args, **kwargs):

    def add_fields(packet):

        packet.fields = args
        return packet
    
    return add_fields

def PacketId(num: int):

    def set_id(packet):
        P_PacketIdFinder[num] = packet
        packet.packetid = num
        return packet
    
    return set_id


def obj_to_bytes(obj: PyNamical):

    stream = Packet(write_packetid=False)

    if obj.parent is None or obj.parent.parent is None:
        stream.write_uint8(0)
    else:
        stream.write_uint8(1)
        stream.write_UUID(obj.parent.uuid)

    stream.write_UUID(obj.uuid)

    stream.write_bytes(pickle.dumps(obj.__class__))

    for i in dir(obj):
        try:
            if isinstance(obj.__getattribute__(i), tuple(T_TypeToInt.keys())):
                stream.write_string(i)
                stream.write_with_type(obj.__getattribute__(i))
        except Exception as e:
            Logger.print(f"Error while writing property {i} of {obj}: {e}", channel=4, prefix="[DedicatedServer]")


    return stream

@PacketId(0x00)
class P_DownstreamSayNothing(Packet):
    """0x00 Say Nothing: Server has nothing to say to client. Usually a response when client pings and there are no packets to send to client
    """
    pass

@PacketFields(uuid.UUID, str)
@PacketId(0x01)
class P_UpstreamHandshake(Packet):
    """UUID[0]: User ID - The User ID for login.
    0x01 Handshake: Tells the server that you are here.
    """
    def handle(self, parent, connection, ip):
        x = self.read_UUID()
        pas = self.read_string()

        ad = False
        if pas == parent.password:
            ad = True

        parent.users[x] = ConnectedClient(parent, x, ad)

        Logger.print(f"User {parent.users[x]} has logged on!", prefix="[DedicatedServer]")

        # Sending Resources to User
        for i in parent.parent.children:
            if isinstance(i, (DedicatedServer, DedicatedServerV2)):
                continue
            k = obj_to_bytes(i).buffer
            packet = P_DownstreamResource()
            packet.write_uint8(0) # General PyNamics Object
            packet.buffer += k
            parent.send(x, packet)

        parent.call_event_listeners(event=EventType.CLIENT_CONNECTED, client=parent.users[x])

@PacketId(0x02)
@PacketFields(uuid.UUID)
class P_UpstreamStayAlive(Packet):
    """UUID[0]: User ID - The username
    0x02 U StayAlive: Tells the server that you are still online to prevent from disconnecting
    """
    def handle(self, parent, connection, ip):
        x = self.read_UUID()
        user = parent.users[x]
        user.last_renewed = time.time()
        n = time.time()

        while True:

            if len(user.packets) > 0:
                pack = user.packets.pop(0)
                if not isinstance(pack, Packet):
                    continue

                Logger.print(f"&eUpstream   &b-> {ip[0]}:{ip[1]} : {pack} ({H_FormatBytes(pack.size())})",
                             prefix="[DedicatedServer]")
                # print(f"Sth to esnd, packet size: {pack.buffer}")
                connection.send(pack.buffer)
                break
            # if time.time() - n > parent.UPSTREAM_PACKET_WAIT_TIME:
            #     pack = P_DownstreamSayNothing()
            #     Logger.print(f"&eUpstream   &b-> {ip[0]}:{ip[1]} : {pack} ({H_FormatBytes(pack.size())})",
            #                  prefix="[DedicatedServer]")
            #     connection.send(pack.buffer)
            #     break


            time.sleep(0.01)

@PacketId(0x03)
@PacketFields()
class P_DownstreamStayAlive(Packet):
    """0x03 D StayAlive: Tells Client that you acknowledge their ping
    """
    def handle(self, parent, connection, ip):
        pass


    

@PacketId(0x04)
@PacketFields(bytes)
class P_DownstreamResource(Packet):

    """bytes[0]: Object path - Picked Object Path
    0x04 Resource: Tells the client to spawn or create a specific resource
    """
    def handle(self, parent, connection, ip):
        type = self.read_uint8()

        hasparent = self.read_bool()
        if hasparent:
            pp = self.read_UUID()
            p = PyNamical.LINKER[pp]
        else:
            p = parent.parent

        id = self.read_UUID()
        if PyNamical.LINKER.get(id, None) is not None:
            Logger.print(f"Not replicating resource becuase {id} already exists!", channel=2)
            return

        if type == 0x00:
            clazz = pickle.loads(self.read_bytes())
            loaded = clazz(p)
            setattr(loaded, "Replicated", True)
            loaded.edit_uuid(id)

            while self.read_pointer < self.size():
                key = self.read_string()
                if key == "Replicated":
                    continue

                value = self.read_with_type()
                setattr(loaded, key, value)

            Logger.print(f"Replicated {loaded} from server! ({loaded.uuid})", channel=2)

@PacketId(0x05)
@PacketFields(uuid.UUID, str)
class P_DownstreamResourceEdit(Packet):
    """UUID[0]: The UUID of a specific object
    str[1]: Property Name
    object[2]: Property Value, depends on type
    0x05 Resource Edit: Tells the client to change an object's property
    """
    def handle(self, parent, connection, ip):
        uid = self.read_UUID()
        property = self.read_string()
        value = self.read_with_type()

        try:

            obj = PyNamical.LINKER[uid]
            setattr(obj, property, value)
        except KeyError as e:

            Logger.print(f"No corresponding object with UUID {uid}, refetching...", channel=4)
            p = P_UpstreamResourceRequest(parent.uuid, uid)
            parent.send(p)

@PacketId(0x3f)
@PacketFields(int, u_int8, str)
class P_DownstreamStatusBroadcast(Packet):

    def handle(self, parent, connection, ip):
        typ = self.read_varint()
        status = self.read_uint8()
        msg = self.read_string()

        if typ == 0x00: #UpstreamResourceEditResponse (Used in debuggers)
            if status == 0x00:
                parent.broadcast_error("Property Editor", msg)
            else:
                pass


@PacketId(0x06)
@PacketFields(uuid.UUID, uuid.UUID, str)
class P_UpstreamResourceEdit(Packet):

    def handle(self, parent, connection, ip):
        who = parent.users[self.read_UUID()]
        what = PyNamical.LINKER[self.read_UUID()]
        k = self.read_string()
        v = self.read_with_type()
        if not who.admin:
            connection.send(P_DownstreamStatusBroadcast(0, u_int8(0), f"Property {k} of object {what} is protected. Only server administrators can change its value.").buffer)
        else:
            setattr(what, k, v)
            connection.send(P_DownstreamStatusBroadcast(0, u_int8(1), "Success resource edit").buffer)

@PacketId(0x09)
@PacketFields(uuid.UUID, uuid.UUID)
class P_UpstreamResourceRequest(Packet):

    def handle(self, parent, connection, ip):

        uid = self.read_UUID()
        obj = self.read_UUID()
        object = PyNamical.LINKER[obj]

        k = obj_to_bytes(object).buffer
        packet = P_DownstreamResource()
        packet.write_uint8(0)  # General PyNamics Object
        packet.buffer += k

        parent.send(uid, packet)

@PacketId(0x07)
@PacketFields(u_int8)
class P_DownstreamRegisterEvents(Packet):

    def handle(self, parent, connection, ip):
        e = self.read_uint8()
        event = dict(EventType.__dict__)
        event = list(event.keys())[list(event.values()).index(e)]


        @parent.parent.add_event_listener(event=getattr(EventType, event))
        def call(self, *args, **kwargs):
            packet = P_UpstreamEventCalled(parent.uuid, u_int8(e))
            packet.write_uint8(len(args))
            for i in args:
                packet.write_with_type(i)
            packet.write_uint8(len(kwargs))
            for k, v in kwargs.items():
                packet.write_string(k)
                packet.write_with_type(v)
            parent.send(packet)


@PacketId(0x08)
@PacketFields(uuid.UUID, u_int8)
class P_UpstreamEventCalled(Packet):

    def handle(self, parent, connection, ip):
        usr = parent.users[self.read_UUID()]


        e = self.read_uint8()
        event = dict(EventType.__dict__)
        event = list(event.keys())[list(event.values()).index(e)]

        args = []
        for i in range(self.read_uint8()):
            args.append(self.read_with_type())
        kwargs = {}
        for i in range(self.read_uint8()):
            k, v = self.read_string(), self.read_with_type()
            kwargs[k] = v

        usr.call_event_listeners(event=getattr(EventType, event), *args, **kwargs)


# https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
def H_FormatBytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return "{:,.2f}".format(size) + " " + power_labels[n] + 'B'

class ConnectedClient(PyNamical):

    def __init__(self, parent, uuid, admin):
        super().__init__(parent)
        self.uuid = uuid
        self.last_renewed = time.time()
        self.admin = admin
        self.packets = []

    def add_object(self, object): # Replacing function of GameManager
        pass

    def send_packet(self, packet):
        self.packets.append(packet)

    def sync(self, object: PyNamical):

        for i in object.P_whitelisted:
            packet = P_DownstreamResourceEdit(object.uuid, i)
            packet.write_with_type(getattr(object, i))
            self.send_packet(packet)

    def add_event_listener(self, event: EventType = EventType.NONE, priority: EventPriority=EventPriority.LOWEST, condition=lambda i: True, tick_delay=0, replicated=False):
        # Overriding Events because we are sending event creation
        def inner(function):
            PyNamical.add_event_listener(self, event, priority, condition, tick_delay, replicated)(function)

        packet = P_DownstreamRegisterEvents(u_int8(event))
        self.packets.append(packet)


        return inner

# Mask Class for object identification
    
class DedicatedServerV2(PyNamical):

    def __init__(self, parent, address="127.0.0.1", port=11027, no_parent=False, uuid=None):
        super().__init__(parent, no_parent, uuid)
        self.parent.window = self
        self.address = address
        self.port = port
        self.users = {}

        self.events[EventType.CLIENT_CONNECTED] = []

    def listen(self):
        self.server = socket.socket()
        self.server.bind((self.address, self.port))
        self.server.listen()
        Logger.print(f"Listening on {self.address}:{self.port}", prefix="[DedicatedServer]")

        while True:
            connection, ip = self.server.accept()
            print("accepting")
            thread = threading.Thread(target=self.client_handle, args=(connection, ip))
            thread.start()

    def client_handle(self, conn, ip):
        print("handle")
        data = conn.recv(1024)
        packet = P_PacketIdFinder[data[0]](buffer=data, write_packetid=False)
        packet.read_pointer = 1
        if not isinstance(packet, P_UpstreamStayAlive):
            Logger.print(f"&aDownstream &b<- {ip[0]}:{ip[1]} : {packet} ({H_FormatBytes(packet.size())})",
                            prefix="[DedicatedServer]")
        
        packet.handle(self, conn, ip)
        conn.close()

    def send(self, user, packet):
        self.users[user].send_packet(packet)

    def update(self):
        pass






class DedicatedServer(PyNamical):

    UPSTREAM_PACKET_WAIT_TIME = 15
    DOWNSTREAM_PING_TIMEOUT = 30

    def __init__(self, parent, address="127.0.0.1", port=11027, admin_password=None):
        PyNamical.__init__(self, parent)

        PyNamical.linkedNetworkingDispatcher = self
        Logger.print("Completed setting linked Network Dispatcher!", channel=2)

        self.address = address
        self.port = port
        self.password = admin_password
        self.users = {}
        # We do not initlize by using ProjectWindow because we dont need tk and stuff
        self.parent.window = self

        self._timer_check_timeout = 0

        self.events[EventType.CLIENT_CONNECTED] = []


    def process(self, connection, ip):

        try:
            content = connection.recv(1)
            content += connection.recv(1048575)
            packet = P_PacketIdFinder[content[0]](buffer=content, write_packetid=False)
            packet.read_pointer = 1
            if not isinstance(packet, P_UpstreamStayAlive):
                Logger.print(f"&aDownstream &b<- {ip[0]}:{ip[1]} : {packet} ({H_FormatBytes(packet.size())})",
                             prefix="[DedicatedServer]")
            
            packet.handle(self, connection, ip)
            connection.close()
        except:
            connection.close()

    def disconnect(self, user, reason="Disconnected", exception=TimeoutError):
        r = dict(self.users)
        u = self.users[user]
        e = exception(reason)
        Logger.print(f"&cUser {u} disconnected: {str(e)}", prefix="[DedicatedServer]")
        del r[user]
        self.users = r

    def H_check_timeout(self):
        for user in self.users:
            u = self.users[user]
            if time.time() - u.last_renewed > self.DOWNSTREAM_PING_TIMEOUT:
                self.disconnect(user, reason="Timeout after not pinging for 30 seconds.")

    def update(self):
        self._timer_check_timeout += 1
        #  or time.time() - self.last_ping_sent > self.PING_PACKET_WAIT_TIME
        if self._timer_check_timeout == self.parent.tps:
            self.H_check_timeout()
            self._timer_check_timeout = 0

    def sync(self, obj: PyNamical):

        for i in obj.P_whitelisted:
            print(i)

    def send(self, userid, packet):
        self.users[userid].packets.append(packet)


    def listen(self):
        self.server = socket.socket()
        self.server.bind((self.address, self.port))
        self.server.listen()
        Logger.print(f"Listening on {self.address}:{self.port}", prefix="[DedicatedServer]")

        while True:

            connection, ip = self.server.accept()
            threading.Thread(target=self.process, args=(connection, ip)).start()

    def network_edit(self, object, key, value):
        packet = P_DownstreamResourceEdit(object.uuid, key)
        packet.write_with_type(value)
        for i in self.users:
            self.send(i, packet)

    def network_newly_created(self, object: PyNamical):
        k = obj_to_bytes(object).buffer
        packet = P_DownstreamResource()
        packet.write_uint8(0) # General PyNamics Object
        packet.buffer += k
        for i in self.users:
            self.send(i, packet)

            
            

class DedicatedClient(PyNamical):

    def __init__(self, parent: PyNamical, address="127.0.0.1", port=11027, admin_password=None):
        PyNamical.__init__(self, parent)
        PyNamical.linkedNetworkingDispatcher = self
        self.events[EventType.CLIENT_CONNECTED] = []
        self.parent.client = self
        self.address = address
        self.port = port
        self.name = None

        self.password = admin_password

        self.ping_backed = True
        self.last_ping_sent = time.time()

        self.connected = False
        self._rx = 0
        self._tx = 0
        self._loss = 0

        self.PING_PACKET_WAIT_TIME = 15

        self.p = None
        self.socket = None

        self.latency = -1

        self.packets = []




    def join_server(self):
        self.name = uuid.uuid4()
        self.edit_uuid(self.name)
        if self.password is None:
            p = str(uuid.uuid4())
        else:
            p = self.password
        packet = P_UpstreamHandshake(self.name, p)
        self.send(packet)

        self.pinger = threading.Thread(target=self.packet_broadcaster)
        self.pinger.start()



    def broadcast_error(self, title, msg):
        tkmsg.showerror(title, msg)

    def disconnect(self):
        self.address = None
        self.port = None


    def packet_broadcaster(self):

        while not self.parent.terminated:
            
            try:


                if len(self.packets) > 0:

                    p = self.packets.pop(0)
                    self.true_send(p)
            except Exception as e:
                Logger.print(f"Problem with packet broadcaster: {e}", channel=4)

            time.sleep(0.01)


    def connect(self):
        self.socket = None
        self.socket = socket.socket()
        self.socket.connect((self.address, self.port))


    def H_pinger(self):
        time.sleep(1)
        while not self.parent.terminated:

            if self.ping_backed:
                
                self.last_ping_sent = time.time()
                packet = P_UpstreamStayAlive(self.name)
                self.send(packet)
                self.ping_backed = False

            time.sleep(0.01)

    def true_send(self, packet):

        try:
            self.connect()
        except Exception as e:
            Logger.print(f"Unable to send packet: {e}", channel=4)
            return
        
        print(packet)

        if isinstance(packet, P_UpstreamHandshake):
            self.connected = True
            self.call_event_listeners(event=EventType.CLIENT_CONNECTED)
            self.H_pinger_thread = threading.Thread(target=self.H_pinger)
            self.H_pinger_thread.start()

        try:
            
            a = time.time()
            self.socket.send(packet.buffer)

        except:
            self._loss += 1
            Logger.print(f"Unable to send packet", channel=4)
            self.socket.close()
        self._tx += 1
        try:
            data = self.socket.recv(2**20)

            print(data)

            if len(data) > 0:
                self.latency = time.time() - a
                self._rx += 1
                self.ping_backed = True
                packet = P_PacketIdFinder[data[0]](buffer=data, write_packetid=False)
                packet.handle(self, None, None)

            self.socket.close()
        except ConnectionAbortedError:
            pass
        except OSError:
            pass
        except Exception as e:
            #print(traceback.format_exc())
            Logger.print(f"Bad Packet: {str(e)}", channel=4)
            data = b""


        

    def send(self, packet: Packet):
        try:

            
            # self.p = threading.Thread(target=self.true_send, args=(packet,))
            # self.p.start()
            
            self.packets.append(packet)
            
            
        except Exception as e:
            Logger.print(f"Disconnected: {e.__class__.__name__}: {e}", channel=4)
            self.disconnect()

    def send_packet(self, packet: Packet):
        self.send(packet)

    def network_edit(self, object, key, value):
        #print(object, key, value)
        pass

    def network_newly_created(self, obj):
        pass