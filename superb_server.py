import pynamics as pn
import random
import uuid
import time

ctx = pn.GameManager(dimensions=pn.Dim(500, 500))
view = pn.DedicatedServer(ctx, port=random.randint(1024, 65536))

view.DOWNSTREAM_PING_TIMEOUT = 5
view.UPSTREAM_PACKET_WAIT_TIME = 3

matcher = {}

@pn.PacketId(0x80)
@pn.PacketFields(uuid.UUID)
class AnyNameYouWantButSamePacketId(pn.Packet):

    def handle(self, parent, connection, ip):
        pass


@view.add_event_listener(event=pn.EventType.CLIENT_CONNECTED)
def join(this, client: pn.ConnectedClient):

    circle = pn.Particle(ctx, random.randint(100, 400), random.randint(100, 400), use_gravity=False, use_airres=True)

    circle.dedicated_user_id = client.uuid

    

    #client.add_object(circle)

    @client.add_event_listener(event=pn.EventType.KEYHOLD)
    def cpress(self, key):
        if key == "Left":
            matcher[client.uuid].velocity.add_self(pn.Vector(180, 1))
        if key == "Right":
            matcher[client.uuid].velocity.add_self(pn.Vector(0, 1))
        if key == "Up":
            matcher[client.uuid].velocity.add_self(pn.Vector(90, 1))
        if key == "Down":
            matcher[client.uuid].velocity.add_self(pn.Vector(-90, 1))

        # for i in this.users:
        #     if i != client.uuid:
        #         this.users[i].sync(matcher[client.uuid])

    client.send_packet(AnyNameYouWantButSamePacketId(circle.uuid))
    matcher[client.uuid] = circle

a = 0
@ctx.add_event_listener(event=pn.EventType.TICK)
def b(self):
    global a

    a += 1
    if a == ctx.tps / 8:
        a = 0

        for i in matcher:
            for x in matcher.values():
                view.users[i].sync(x)
ctx.start()