import pynamics_legacy as pn
import time
import disabled_winsound as winsound

GAME_MAN = None


def check_game_state():
    return not GAME_MAN.GAME_STATE == "intro"


def intro_sprite(texture, d):
    texture.crop(1, d, 1 + 256, d + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(258, d, 258 + 256, d + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(515, d, 515 + 256, d + 256)
    time.sleep(4)
    if check_game_state(): return
    texture.crop(258, d, 258 + 256, d + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(1, d, 1 + 256, d + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(515, 282, 515 + 256, 282 + 256)
    time.sleep(0.5)
    if check_game_state(): return


WINDOWS = []
TABS = []
windowtexture = None
tabtexture = None


def mainloop(ctx: pn.GameManager, viewport):
    global GAME_MAN, WINDOWS, TABS, windowtexture, tabtexture
    GAME_MAN = ctx

    ctx.GAME_STATE = "intro"

    time.sleep(0.2)

    windowtexture = pn.ImageTexture(path="texture.png", crop_resize=False, crop=(1301, 1595, 1301 + 12, 1595 + 24))
    tabtexture = pn.ImageTexture(path="texture.png", crop_resize=False, crop=(1349, 1595, 1349 + 7, 1595 + 32))

    if check_game_state(): return

    global test, texture

    texture = pn.ImageTexture(path="texture.png", crop_resize=False)

    test = pn.Image(ctx, texture=texture)

    @ctx.add_event_listener(event=pn.EventType.KEYDOWN, condition=pn.KeyEvaulator("Return"), killafter=1)
    def press(e, key):

        global test, texture

        test.delete()
        time.sleep(0.15)
        texture.crop(776, 1595, 776 + 256, 1595 + 256)
        test = pn.Image(ctx, texture=texture)

        menu(GAME_MAN, viewport, test, texture)

    ###
    texture.crop(1, 11, 257, 267)

    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(258, 11, 258 + 256, 11 + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(515, 11, 515 + 256, 11 + 256)
    time.sleep(4)
    if check_game_state(): return
    texture.crop(258, 11, 258 + 256, 11 + 256)
    time.sleep(0.2)
    if check_game_state(): return
    texture.crop(1, 11, 257, 267)
    time.sleep(0.2)
    if check_game_state(): return
    test.delete()
    ###

    time.sleep(0.5)

    test = pn.Image(ctx, texture=texture)

    window0 = pn.Image(ctx, texture=windowtexture, x=195, y=40)
    window1 = pn.Image(ctx, texture=windowtexture, x=195, y=112)
    window2 = pn.Image(ctx, texture=windowtexture, x=227, y=40)
    window3 = pn.Image(ctx, texture=windowtexture, x=227, y=112)

    WINDOWS = [window3, window1, window2, window0]

    tab0 = pn.Image(ctx, texture=tabtexture, x=153)
    tab1 = pn.Image(ctx, texture=tabtexture, x=153, y=72)

    TABS = [tab1, tab0]

    ###
    texture.crop(1, 282, 1 + 256, 282 + 256)
    time.sleep(0.1)
    if check_game_state(): return

    windowtexture.crop(1318, 1595, 1318 + 12, 1595 + 24)
    tabtexture.crop(1358, 1595, 1358 + 7, 1595 + 32)
    texture.crop(258, 282, 258 + 256, 282 + 256)

    time.sleep(0.1)
    if check_game_state(): return

    winsound.PlaySound("title.wav", winsound.SND_ASYNC)

    tabtexture.crop(1367, 1595, 1367 + 7, 1595 + 32)
    texture.crop(515, 282, 515 + 256, 282 + 256)
    windowtexture.crop(1335, 1595, 1335 + 12, 1595 + 24)

    time.sleep(0.2)
    if check_game_state(): return

    intro_sprite(texture, 553)
    if check_game_state(): return

    intro_sprite(texture, 810)
    if check_game_state(): return

    intro_sprite(texture, 1067)
    if check_game_state(): return

    intro_sprite(texture, 1324)
    if check_game_state(): return

    intro_sprite(texture, 1581)
    if check_game_state(): return
    ###

    texture.crop(1551, 11, 1551 + 256, 11 + 736)
    test.position.y = 256 - 736

    ani = pn.Animation(pn.LINEAR, duration=128 * 13, fields=["y"])
    x = ani.play(test.position, [0])

    for i in range(1, 15):
        a = pn.Image(ctx, texture=windowtexture, x=195, y=-72 * (i - 1) - 34)
        b = pn.Image(ctx, texture=windowtexture, x=227, y=-72 * (i - 1) - 34)
        c = pn.Image(ctx, texture=tabtexture, x=153, y=-72 * i - 2)
        WINDOWS.append(b)
        WINDOWS.append(a)
        TABS.append(c)

    ctx.downshift = 0

    @ctx.add_event_listener(event=pn.EventType.TICK, name="WindowTabMoveAnimation")
    def move(e):
        if check_game_state(): e.terminate()
        for window in WINDOWS:
            window.position.y += 1

            if window.position.y + 24 > min(240 + 24, test.position.y + 656):
                window.delete()

        for tab in TABS:
            tab.position.y += 1

            if tab.position.y + 24 > min(240 + 32, test.position.y + 656):
                tab.delete()

        ctx.downshift += 1
        if ctx.downshift == 72 * 16 + 32:
            e.terminate()

    time.sleep(9)
    if check_game_state(): return
    ani.stop()

    texture.crop(1551, 762, 1551 + 256, 762 + 736)
    test.position.y = ctx.downshift - 1184
    print(test.position.y)

    @ctx.add_event_listener(event=pn.EventType.TICK, name="BuildingMoveAnimation")
    def move(e):
        if check_game_state(): e.terminate()
        if ctx.downshift < 72 * 16 + 32:
            test.position.y += 1
        else:
            print(test.position.y)
            test.position.y = 0
            e.terminate()

            time.sleep(2)
            menu(ctx, viewport, test, texture)


def menu(ctx, view, baseimage, basetexture):
    global WINDOWS, TABS, tabtexture, windowtexture

    for w in WINDOWS:
        w.delete()
    for t in TABS:
        t.delete()

    t = pn.FramedTexture(metadata="textmap.png.pntexture", frame="MM2_POINTER")

    global pointer
    pointer = pn.AnimatedSprite(ctx, texture=t, interval=16, x=48, y=153)

    @pn.PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=pn.EventType.KEYDOWN)
    def down(e, key):

        global pointer

        if key == pn.K_UP or key == pn.K_DOWN:

            if pointer.y == 153:
                pointer.y = 169
            else:
                pointer.y = 153

            winsound.PlaySound("beep.wav", winsound.SND_ASYNC)

            #pointer.frame = 0


    tabtexture.crop(1367, 1595, 1367 + 7, 1595 + 32)
    windowtexture.crop(1335, 1595, 1335 + 12, 1595 + 24)

    ctx.GAME_STATE = "menu"
    winsound.PlaySound(None, winsound.SND_PURGE)
    winsound.PlaySound("menu.wav", winsound.SND_ASYNC)
    basetexture.crop(776, 1595, 776 + 256, 1595 + 256)
    baseimage.position.y = 0

    window1 = pn.Image(ctx, texture=windowtexture, x=195, y=214)
    window3 = pn.Image(ctx, texture=windowtexture, x=227, y=214)

    WINDOWS = [window1, window3]

    tab1 = pn.Image(ctx, texture=tabtexture, x=153, y=174)

    TABS = [tab1]
