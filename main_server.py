import pynamics as pn
import random

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)
server = pn.DedicatedServer(ctx, address="127.0.0.1")
ctx.NUM = random.randint(0, 2**32)

@pn.PacketId(0x70)
@pn.PacketFields(str, int)
class SendUniverseData(pn.Packet):

    def handle(self, parent, connection, ip):
        pass

POSITION_DICT = {}

@pn.PacketId(0x71)
class SyncPositions(pn.Packet):

    def handle(self, parent: pn.DedicatedServer, connection, ip):
        usr = self.read_UUID()
        pos = self.read_dimension()
        POSITION_DICT[usr] = pos

        for i in POSITION_DICT:
            print(i)
            parent.send(i, self)


@server.add_event_listener(event=pn.EventType.CLIENT_CONNECTED)
def join(event, client: pn.ConnectedClient):
    packet = SendUniverseData("ND", ctx.NUM)
    client.send_packet(packet)

    @client.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator("space"))
    def press(event, key):
        print(key)


ctx.start()