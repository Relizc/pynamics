import pynamics as pn
import random
import uuid

ctx = pn.GameManager(dimensions=pn.Dim(960, 540), event_tracker=True, tps=128)
server = pn.DedicatedServer(ctx, address="10.27.78.144")
ctx.NUM = random.randint(0, 2**32)

@pn.PacketId(0x70)
@pn.PacketFields(str, int, uuid.UUID)
class SendUniverseData(pn.Packet):

    def handle(self, parent, connection, ip):
        pass

@pn.PacketId(0x72)
@pn.PacketFields(uuid.UUID, pn.Dimension, pn.Vector)
class Shoot(pn.Packet):

    def handle(self, parent, connection, ip):
        user = parent.users[self.read_UUID()]
        cursor = self.read_dimension()
        pos = self.read_vector()

        x = pn.TopViewPhysicsBody(ctx, x=cursor.x, y=cursor.y, color="white",
                                            use_airress=False)
        x.velocity = pos

@pn.PacketId(0x71)
@pn.PacketFields(uuid.UUID, pn.Dimension)
class RefeedPosition(pn.Packet):

    def handle(self, parent, connection, ip):


        try:
            client = parent.users[self.read_UUID()]
            pos = self.read_dimension()
            KEY_DICT[client].position = pos

            for i in KEY_DICT:
                if i != client:
                    i.sync(KEY_DICT[client])

        except Exception as e:
            print(e)

KEY_DICT = {}


@server.add_event_listener(event=pn.EventType.CLIENT_CONNECTED)
def join(event, client: pn.ConnectedClient):



    n = pn.TopViewPhysicsBody(ctx, x=100, y=270, width=50, height=50, mass=5, color="white")
    KEY_DICT[client] = n
    

    k = pn.obj_to_bytes(n).buffer
    packet = pn.P_DownstreamResource()
    packet.write_uint8(0)  # General PyNamics Object
    packet.buffer += k

    for i in KEY_DICT:
        if i != client:
            i.send_packet(packet)

    p = SendUniverseData("ND", ctx.NUM, n.uuid)
    client.send_packet(p)






ctx.start()