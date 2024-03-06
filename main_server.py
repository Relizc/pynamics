import pynamics as pn
import random
import uuid

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)
server = pn.DedicatedServer(ctx, address="127.0.0.1")
ctx.NUM = random.randint(0, 2**32)

@pn.PacketId(0x70)
@pn.PacketFields(str, int)
class SendUniverseData(pn.Packet):

    def handle(self, parent, connection, ip):
        pass

KEY_DICT = {}

@pn.PacketId(0x71)
@pn.PacketFields(uuid.UUID, int, bool)
class SendMovementData(pn.Packet):

    def handle(self, parent, connection, ip):
        pass

@pn.PacketId(0x72)
@pn.PacketFields(uuid.UUID, str)
class SendUserJoined(pn.Packet):

    def handle(self, parent, connection, ip):
        pass

def guy_moved(client, toggle, direction):

    global KEY_DICT

    d = 0

    if direction == "Up":
        d = 0
    if direction == "Down":
        d = 1
    if direction == "Left":
        d = 2
    if direction == "Right":
        d = 3

    packet = SendMovementData(client.uuid, d, toggle)

    for i in KEY_DICT:
        if i != client:
            i.send_packet(packet)

@server.add_event_listener(event=pn.EventType.CLIENT_CONNECTED)
def join(event, client: pn.ConnectedClient):
    packet = SendUniverseData("ND", ctx.NUM)
    client.send_packet(packet)

    for i in KEY_DICT:
        packet = SendUserJoined(client.uuid, f"randomname{random.randint(1, 114514)}")
        i.send_packet(packet)

    KEY_DICT[client] = [False, False, False, False]



    @client.add_event_listener(event=pn.EventType.KEYDOWN)
    def press(event, key):
        if key == "Up":
            KEY_DICT[client][0] = True
        if key == "Down":
            KEY_DICT[client][1] = True
        if key == "Left":
            KEY_DICT[client][2] = True
        if key == "Right":
            KEY_DICT[client][3] = True

        guy_moved(client, True, key)
    @client.add_event_listener(event=pn.EventType.KEYUP)
    def press(event, key):
        if key == "Up":
            KEY_DICT[client][0] = False
        if key == "Down":
            KEY_DICT[client][1] = False
        if key == "Left":
            KEY_DICT[client][2] = False
        if key == "Right":
            KEY_DICT[client][3] = False
        guy_moved(client, False, key)


ctx.start()