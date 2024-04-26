import pynamics_legacy as pn
import random

def encode(number):
    """Pack `number` into varint bytes"""
    

def decode(stream):
    """Read a varint from `stream`"""
    



ctx = pn.GameManager(pn.Dim(500, 500), tps=128, fps=0, event_tracker=True)
window = pn.ProjectWindow(ctx, size=pn.Dim(500, 500))
camera = pn.ViewPort(window)

client = pn.DedicatedClient(ctx)

@ctx.add_event_listener(event=pn.EventType.STARTUP)
def start(this):
    client.join_server()

ctx.start()