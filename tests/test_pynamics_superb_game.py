import pynamics
import time
ctx = pynamics.GameManager(pynamics.Dim(10000, 10000), tps=128, fps=0, event_tracker=True)
window = pynamics.ProjectWindow(ctx)
camera = pynamics.ViewPort(window)
player = pynamics.GameObject(ctx, 100, 100, 10, 10)

pynamics.utils.establish_basic_movement_wasd(ctx, player)
bulletsList = []


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_UP))
def shootup(self):
    bulletsList.append((0, pynamics.GameObject(ctx, player.position.x, player.position.y, 5, 5), time.time()))


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_RIGHT))
def shootright(self):
    bulletsList.append((1, pynamics.GameObject(ctx, player.position.x, player.position.y, 5, 5), time.time()))


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_DOWN))
def shootdown(self):
    bulletsList.append((2, pynamics.GameObject(ctx, player.position.x, player.position.y, 5, 5), time.time()))


@ctx.add_event_listener(event=pynamics.EventType.KEYDOWN, condition=pynamics.KeyEvaulator(pynamics.K_LEFT))
def shootleft(self):
    bulletsList.append((3, pynamics.GameObject(ctx, player.position.x, player.position.y, 5, 5), time.time()))


@ctx.add_event_listener(event=pynamics.EventType.TICK)
def updateBullets(self):
    for i in bulletsList:
        t, bullet,fireTime = i
        if t==0:
            bullet.position.y-=1
        elif t==1:
            bullet.position.x+=1
        elif t==2:
            bullet.position.y+=1
        elif t==3:
            bullet.position.x-=1
@ctx.add_event_listener(event=pynamics.EventType.TICK)
def timer(self):
    for i in bulletsList:
        t,bullet,fireTime = i
        if time.time() - fireTime > 2:
            bullet.delete()
            bulletsList.remove(i)


@ctx.add_event_listener(event = pynamics.EventType.KEYDOWN, condition = pynamics.KeyEvaulator(pynamics.K_r))
def display_positions(self):
    print(f"POSITIONS: Player:({player.position.x},{player.position.y})    bullet:({bulletsList[-1][1].position.x},{bulletsList[-1][1].position.y})")

ctx.start()
