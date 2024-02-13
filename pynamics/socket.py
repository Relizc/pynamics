import sys
import uuid
from .interface import PyNamical
import socket
import threading
import time
from .logger import Logger
import pickle
import struct
import traceback
from numpy import float32, float64
from .dimensions import Dimension, Vector

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
        
        if isinstance(obj.__getattribute__(i), tuple(T_TypeToInt.keys())):
            stream.write_string(i)
            stream.write_with_type(obj.__getattribute__(i))

    return stream

@PacketId(0x00)
class P_DownstreamSayNothing(Packet):
    """0x00 Say Nothing: Server has nothing to say to client. Usually a response when client pings and there are no packets to send to client
    """
    pass

@PacketFields(uuid.UUID)
@PacketId(0x01)
class P_UpstreamHandshake(Packet):
    """UUID[0]: User ID - The User ID for login.
    0x01 Handshake: Tells the server that you are here.
    """
    def handle(self, parent, connection, ip):
        x = self.read_UUID()
        parent.users[x] = ConnectedClient(parent, x)
        Logger.print(f"User {parent.users[x]} has logged on!", prefix="[DedicatedServer]")

        # Sending Resources to User
        for i in parent.parent.children:
            if isinstance(i, DedicatedServer):
                continue
            k = obj_to_bytes(i).buffer
            packet = P_DownstreamResource(buffer=k)
            parent.send(x, packet)

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
                Logger.print(f"&eUpstream   &b-> {ip[0]}:{ip[1]} : {pack} ({H_FormatBytes(pack.size())})",
                             prefix="[DedicatedServer]")
                # print(f"Sth to esnd, packet size: {pack.buffer}")
                connection.send(pack.buffer)
                break
            if time.time() - n > parent.UPSTREAM_PACKET_WAIT_TIME:
                pack = P_DownstreamSayNothing()
                Logger.print(f"&eUpstream   &b-> {ip[0]}:{ip[1]} : {pack} ({H_FormatBytes(pack.size())})",
                             prefix="[DedicatedServer]")
                connection.send(pack.buffer)
                break
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
        hasparent = self.read_bool()
        if hasparent:
            pp = self.read_UUID()
            p = PyNamical.LINKER[pp]
        else:
            p = parent.parent

        id = self.read_UUID()
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

        obj = PyNamical.LINKER[uid]
        setattr(obj, property, value)

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

    def __init__(self, parent, uuid):
        super().__init__(parent)
        self.uuid = uuid
        self.last_renewed = time.time()
        self.packets = []

class DedicatedServer(PyNamical):

    UPSTREAM_PACKET_WAIT_TIME = 15
    DOWNSTREAM_PING_TIMEOUT = 30

    def __init__(self, parent, address="127.0.0.1", port=11027):
        PyNamical.__init__(self, parent)
        PyNamical.linkedNetworkingDispatcher = self
        self.address = address
        self.port = port
        self.users = {}
        # We do not initlize by using ProjectWindow because we dont need tk and stuff
        self.parent.window = self

        self._timer_check_timeout = 0


    def process(self, connection, ip):
        content = connection.recv(1)
        content += connection.recv(1048575)
        packet = P_PacketIdFinder[content[0]](buffer=content, write_packetid=False)
        packet.read_pointer = 1
        Logger.print(f"&aDownstream &b<- {ip[0]}:{ip[1]} : {packet} ({H_FormatBytes(packet.size())})", prefix="[DedicatedServer]")
        packet.handle(self, connection, ip)
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
        if self._timer_check_timeout == self.parent.tps:
            self.H_check_timeout()
            self._timer_check_timeout = 0

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
        print(object, key, value)
        packet = P_DownstreamResourceEdit(object.uuid, key)
        packet.write_with_type(value)
        for i in self.users:
            self.send(i, packet)

            
            

class DedicatedClient(PyNamical):

    def __init__(self, parent, address="127.0.0.1", port=11027):
        PyNamical.__init__(self, parent)
        PyNamical.linkedNetworkingDispatcher = self
        self.parent.client = self
        self.address = address
        self.port = port
        self.name = None
        self.ping_backed = True



    def join_server(self):
        self.name = uuid.uuid4()
        packet = P_UpstreamHandshake(self.name)
        self.send(packet)

        self.H_pinger_thread = threading.Thread(target=self.H_pinger)
        self.H_pinger_thread.start()

    def disconnect(self):
        self.address = None
        self.port = None

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.address, self.port))

    def H_pinger(self):
        time.sleep(1)
        while not self.parent.terminated:
            if self.ping_backed:
                packet = P_UpstreamStayAlive(self.name)
                self.send(packet)
                self.ping_backed = False
            time.sleep(0.01)

    def true_send(self, packet):
        self.connect()
        self.socket.send(packet.buffer)
        try:
            data = self.socket.recv(2**20)
            if len(data) > 0:
                self.ping_backed = True
                packet = P_PacketIdFinder[data[0]](buffer=data, write_packetid=False)
                packet.handle(self, None, None)
        except Exception as e:
            print(traceback.format_exc())
            Logger.print(f"Bad Packet: {str(e)}", channel=4)
            data = b""

        self.socket.close()

    def send(self, packet: Packet):
        try:
            p = threading.Thread(target=self.true_send, args=(packet,))
            p.start()
            
            
        except Exception as e:
            Logger.print(f"Disconnected: {e.__class__.__name__}: {e}", channel=4)
            self.disconnect()

    def network_edit(self, object, key, value):
        #print(object, key, value)
        pass