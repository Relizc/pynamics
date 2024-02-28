import pynamics as pn
import sys
import random
port = int(sys.argv[1])

ctx = pn.GameManager(dimensions=pn.Dim(500, 500), event_tracker=False)
view = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
client = pn.DedicatedClient(ctx, port=port)

global my_circle
my_circle = None

@pn.PacketId(0x80)
class CustomizedPacketAssociateParticleWithUserId(pn.Packet):

    def handle(self, parent, connection, ip):
        global my_circle
        circ = self.read_UUID()
        my_circle = circ

        print(my_circle)
f = 1
@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(self):
    client.join_server()

@ctx.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_UP))
def up(self, key):
    global my_circle
    if not isinstance(my_circle, pn.Particle): my_circle = pn.find_object_by_id(my_circle)

    my_circle.velocity.add_self(pn.Vector(90, f))

@ctx.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_DOWN ))
def up(self, key):
    global my_circle
    if not isinstance(my_circle, pn.Particle): my_circle = pn.find_object_by_id(my_circle)

    my_circle.velocity.add_self(pn.Vector(-90, f))

@ctx.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_LEFT ))
def up(self, key):
    global my_circle
    if not isinstance(my_circle, pn.Particle): my_circle = pn.find_object_by_id(my_circle)
    my_circle.velocity.add_self(pn.Vector(180, f))
@ctx.add_event_listener(event=pn.EventType.KEYHOLD, condition=pn.KeyEvaulator(pn.K_RIGHT ))
def up(self, key):
    global my_circle
    if not isinstance(my_circle, pn.Particle): my_circle = pn.find_object_by_id(my_circle)
    my_circle.velocity.add_self(pn.Vector(0, f))
ctx.start()