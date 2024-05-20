import pynamics_legacy as pn
import time
import winsound

def intro_sprite(texture, d):


    texture.crop(1, d, 1 + 256, d + 256)
    time.sleep(0.2)
    texture.crop(258, d, 258 + 256, d + 256)
    time.sleep(0.2)
    texture.crop(515, d, 515 + 256, d + 256)
    time.sleep(4)
    texture.crop(258, d, 258 + 256, d + 256)
    time.sleep(0.2)
    texture.crop(1, d, 1 + 256, d + 256)
    time.sleep(0.2)
    texture.crop(515, 282, 515 + 256, 282 + 256)
    time.sleep(0.5)


def mainloop(ctx, viewport):

    texture = pn.ImageTexture(path="texture.png", crop_resize=False)


    test = pn.Image(ctx, texture=texture)

    texture.crop(1, 11, 257, 267)
    time.sleep(0.2)
    texture.crop(258, 11, 258 + 256, 11 + 256)
    time.sleep(0.2)
    texture.crop(515, 11, 515 + 256, 11 + 256)
    time.sleep(4)
    texture.crop(258, 11, 258 + 256, 11 + 256)
    time.sleep(0.2)
    texture.crop(1, 11, 257, 267)
    time.sleep(0.2)
    test.delete()



    time.sleep(0.5)

    test = pn.Image(ctx, texture=texture)
    windowtexture = pn.ImageTexture(path="texture.png", crop_resize=False, crop=(1301, 1595, 1301 + 12, 1595 + 24))
    tabtexture = pn.ImageTexture(path="texture.png", crop_resize=False, crop=(1349, 1595, 1349 + 7, 1595 + 32))
    window0 = pn.Image(ctx, texture=windowtexture, x=195, y=40)
    window1 = pn.Image(ctx, texture=windowtexture, x=195, y=112)
    window2 = pn.Image(ctx, texture=windowtexture, x=227, y=40)
    window3 = pn.Image(ctx, texture=windowtexture, x=227, y=112)

    WINDOWS = [window3, window1, window2, window0]


    tab0 = pn.Image(ctx, texture=tabtexture, x=153)
    tab1 = pn.Image(ctx, texture=tabtexture, x=153, y=72)

    TABS = [tab1 , tab0]

    texture.crop(1, 282, 1 + 256, 282 + 256)
    time.sleep(0.1)

    windowtexture.crop(1318, 1595, 1318 + 12, 1595 + 24)
    tabtexture.crop(1358, 1595, 1358 + 7, 1595 + 32)
    texture.crop(258, 282, 258 + 256, 282 + 256)

    time.sleep(0.1)

    winsound.PlaySound("title.wav", winsound.SND_ASYNC)

    tabtexture.crop(1367, 1595, 1367 + 7, 1595 + 32)
    texture.crop(515, 282, 515 + 256, 282 + 256)
    windowtexture.crop(1335, 1595, 1335 + 12, 1595 + 24)

    time.sleep(0.2)


    intro_sprite(texture, 553)

    intro_sprite(texture, 810)

    intro_sprite(texture, 1067)

    intro_sprite(texture, 1324)

    intro_sprite(texture, 1581)

    texture.crop(1551, 11, 1551 + 256, 11 + 736)
    test.position.y = 256 - 736

    ani = pn.Animation(pn.LINEAR, duration=128*13, fields=["y"])
    x = ani.play(test.position, [0])



    for i in range(1, 15):
        a = pn.Image(ctx, texture=windowtexture, x=195, y=-72*(i-1)-34)
        b = pn.Image(ctx, texture=windowtexture, x=227, y=-72*(i-1)-34)
        c = pn.Image(ctx, texture=tabtexture, x=153, y=-72*i-2)
        WINDOWS.append(b)
        WINDOWS.append(a)
        TABS.append(c)

    ctx.downshift = 0

    @ctx.add_event_listener(event=pn.EventType.TICK, name="WindowTabMoveAnimation")
    def move(e):
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

    time.sleep(8.6)
    ani.stop()



    texture.crop(1551, 762, 1551 + 256, 762 + 736)
    test.position.y = 512 - 736

    @ctx.add_event_listener(event=pn.EventType.TICK, name="BuildingMoveAnimation")
    def move(e):
        if ctx.downshift < 72 * 16 + 32:
            test.position.y += 1
        else:
            test.position.y = 0
            e.terminate()

            time.sleep(2)
            menu(ctx, viewport, test, texture)



def menu(ctx, view, baseimage, basetexture):
    winsound.PlaySound(None, winsound.SND_PURGE)
    winsound.PlaySound("menu.wav", winsound.SND_ASYNC)
    basetexture.crop(776, 1595, 776 + 256, 1595 + 256)
    baseimage.position.y = 0




