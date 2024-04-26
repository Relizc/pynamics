import pynamics_legacy, time

ctx = pynamics_legacy.GameManager(pynamics_legacy.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics_legacy.ProjectWindow(ctx)
camera = pynamics_legacy.ViewPort(window)
bob1 = pynamics_legacy.GameObject(ctx, 0, 0, 10, 10, from_points=pynamics_legacy.load_object_from_binary("output/platforms.obj"))
player = pynamics_legacy.GameObject(ctx, 10, 10, 10, 10)

curTime = time.time()
count = 1
movingUp = False

# @ctx.add_event_listener(event=pynamics_legacy.EventType.TICK)
# def checkfordel(self):
#     pass
#     global curTime, count
#     if time.time() - curTime > 1:
#         if count == 1:
#             bob1.hide()
#         else:
#             bob1.unhide()
#         curTime = time.time()
#         count *= -1
@ctx.add_event_listener(event = pynamics_legacy.EventType.TICK)
def apply_gravity(self):
    if not player.collide(bob1):
        for i in range(5):
            player.position.y += 1 if not player.collide(bob1) else -1
    else:
        player.position.y -= 5

@ctx.add_event_listener(event = pynamics_legacy.EventType.TICK)
def hit_wall(self):
    if player.collide(bob1):
        if movingUp:player.position.y += 15

        else: player.position.y -= 7
@ctx.add_event_listener(event = pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_UP))
def goUp(self):
    global movingUp
    if not player.collide(bob1):
        player.position.y -= 10
        movingUp = True
@ctx.add_event_listener(event=pynamics_legacy.EventType.KEYUP, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_UP))
def releaseUp(self):
    global movingUp
    movingUp = False
@ctx.add_event_listener(event = pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_RIGHT))
def goright(self):
    if not player.collide(bob1):
        player.position.x += 5
@ctx.add_event_listener(event = pynamics_legacy.EventType.KEYHOLD, condition=pynamics_legacy.KeyEvaulator(pynamics_legacy.K_LEFT))
def goright(self):
    if not player.collide(bob1):
        player.position.x -= 5
ctx.start()
