from .gamemanager import GameManager
from .styling import StyleLoader
from .gameobject.gameobject import *
from .gameobject.physics import *
import time
import math
import os

USE_OPENGL = False
USE_OPENGLTK = False

import traceback

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *

    USE_OPENGL = True

    try:
        from pyopengltk import OpenGLFrame
        USE_OPENGLTK = True
    except Exception as e:
        Logger.warn(f"PyOpenGL occured an error. Attempting to use native GLFW window: {e}")

    
    USE_OPENGL = True
    
except ModuleNotFoundError as e:
    Logger.print(f"PyOpenGL: {e}", channel=4)
    Logger.print("PyOpenGL is not found. ProjectWindow is using legacy tkinter canvas.", channel=3)
except ImportError as e:
    Logger.print(f"PyOpenGL: {e}", channel=4)
    Logger.print(f"PyOpenGL occured an error. ProjectWindow is using legacy tkinter canvas", channel=3)

if not USE_OPENGL:
    os.environ.setdefault("PN_WINDOW_MODE", "legacy")

import random


def _1x(x):
    if x == 0: return 0.0
    return (x + 1) / 256


class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        super().__init__(parent)
        parent.viewport = self
        self.position = position
        self.size = parent.size

    def offset(self, dimension: Dimension):
        return dimension.add(self.position)

    def crop_add(self):
        return self.size.add_dim(self.position)

    def crop_sub(self):
        return self.size.sub

    def shift(self, other: Dimension):
        return other.add_dim(self.position)


def rgb_to_hex(i):
    return f"#%02x%02x%02x" % (i.r, i.g, i.b)


if not USE_OPENGL or not USE_OPENGLTK:

    class Dummy:

        def __init__(self, arg0, width, height):
            self.root = arg0
            # glutInit()
            # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            # glutInitWindowSize(width, height)
            # glutInitWindowPosition(100, 100)
            # glutCreateWindow(b'Simple PyOpenGL Window')
            # glutDisplayFunc(draw)
            # glutIdleFunc(draw)
            # glutMainLoop()
            

    OpenGLFrame = Dummy

class _base_OpenGL_Frame(OpenGLFrame):

    def __init__(self, parent, root, size: Dimension = Dimension(1000, 1000), scale=1):

        OpenGLFrame.__init__(self, root, width=size.x, height=size.y)
        self.parent = parent
        self.renderable = []
        self.scale = scale

        self.texture_handler = {}

    # Overriding OpenGLFrame
    def initgl(self):
        glViewport(0, 0, self.width, self.height)
        glClearColor(*self.parent.color.tuple())

        # setup projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)

        # setup identity model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        #glEnable(GL_LINE_SMOOTH)


    # Overriding OpenGLFrame
    def redraw(self):

        glClear(GL_COLOR_BUFFER_BIT)

        self.parent.parent.f += 1

        for i in self.parent.parent.displayorder:

            if i.hidden:
                continue

            try:
                glColor4f(1.0, 1.0, 1.0, 1.0)
                overridecolor = StyleLoader.get_style(i, "color")
                if overridecolor is not None:
                    glColor4f(overridecolor.r, overridecolor.g, overridecolor.b, overridecolor.a)

                self.draw(i)
            except Exception as e:
                Logger.print(f"Render Error while rendering {i}: {e}", channel=4)
                print(traceback.format_exc())
                pass


        glFlush()

    def draw(self, i):
        self.parent._checks += 1

        if (i.position.x + i.size.x < -10 or i.position.y + i.size.y < -10) or (
                i.position.x > self.parent.parent.dimensions.x + 10 or i.position.y > self.parent.parent.dimensions.y + 10):
            if i.destroy_outside_boundary:
                i.delete()
            return

        f = False
        for n in self.parent.ignore_render:
            if isinstance(i, n):
                f = True
        if f:
            return

        posx = i.position.x * self.scale
        posy = i.position.y * self.scale

        if isinstance(i, (Image, AnimatedSprite)):
            # for n in range(i.image.texture.width):
            #     for m in range(i.image.texture.height):
            #         # print(n, m)
            #         glBegin(GL_POINTS)
            #         f = i.image.color_content(n, m)
            #         glColor4f(_1x(f[0]), _1x(f[1]), _1x(f[2]), _1x(f[3]))
            #         glVertex2f(i.x + n, i.y + m)
            #         glEnd()

            #print(i.image.width)

            if self.texture_handler.get(i.image.path, None) is None:
                id = glGenTextures(1)
                i.image.gl_bind_id = id
                self.texture_handler[i.image.path] = id

                Logger.print(f"Loading texture: {i.image.path} ({len(i.image.data)} bytes) [ID={id}]", channel=5)

                glBindTexture(GL_TEXTURE_2D, id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, i.image.width, i.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             None)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, i.image.width, i.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             i.image.data)
                glBindTexture(GL_TEXTURE_2D, 0)

            glBindTexture(GL_TEXTURE_2D, self.texture_handler[i.image.path])
            glBegin(GL_QUADS)

            if i.image.crop_resize:
                deltax = i.size.x
                deltay = i.size.y
            else:
                deltax = i.image.effective[2] - i.image.effective[0]
                deltay = i.image.effective[3] - i.image.effective[1]

            deltax *= self.scale
            deltay *= self.scale

            #print(i.photosize, deltax, deltay)

            glTexCoord2f((i.image.effective[0] / i.photosize.x), (i.image.effective[1] / i.photosize.y))
            glVertex2f(posx         , posy)
            glTexCoord2f((i.image.effective[2] / i.photosize.x), (i.image.effective[1] / i.photosize.y))
            glVertex2f(posx + deltax, posy)
            glTexCoord2f((i.image.effective[2] / i.photosize.x), (i.image.effective[3] / i.photosize.y))
            glVertex2f(posx + deltax, posy + deltay)
            glTexCoord2f((i.image.effective[0] / i.photosize.x), (i.image.effective[3] / i.photosize.y))
            glVertex2f(posx         , posy + deltay)
            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)

            # print(self.texture_handler)

            # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, i.image.width, i.image.height, 0,
            # GL_RGBA, GL_UNSIGNED_BYTE, i.image.data)

        elif isinstance(i, Particle):
            sides = i.circle_steps
            radius = i.radius
            glBegin(GL_POLYGON)
            for _ in range(sides):
                cosine = radius * math.cos(_ * 2 * math.pi / sides) + i.x
                sine = radius * math.sin(_ * 2 * math.pi / sides) + i.y
                glVertex2f(cosine, sine)
            glEnd()


        elif isinstance(i, Text):
            pass    

        elif isinstance(i, GameObject):
            glBegin(GL_POLYGON)
            glColor3f(1.0, 1.0, 1.0)
            for j in i.points:
                a = j[0]
                glVertex2f(a[0] + i.x, a[1] + i.y)
            glEnd()

        if i.start_debug_highlight_tracking:
            glBegin(GL_POLYGON)
            glColor4f(0.0, 1.0, 0.0, 0.5)
            glVertex2f(i.x, i.y)
            glVertex2f(i.x + i.size.x, i.y)
            glVertex2f(i.x + i.size.x, i.y + i.size.y)
            glVertex2f(i.x, i.y + i.size.y)
            glEnd()

            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
            glColor4f(1.0, 0.0, 1.0, 1.0)
            glVertex2f(0, i.y)
            glVertex2f(self.parent.parent.width, i.y)
            glEnd()

            glBegin(GL_LINE_STRIP)
            glColor4f(1.0, 0.0, 1.0, 1.0)
            glVertex2f(i.x, 0)
            glVertex2f(i.x, self.parent.parent.height)
            glEnd()

            if isinstance(i, PhysicsBody):
                glLineWidth(3)
                glBegin(GL_LINE_STRIP)
                glColor3f(0.0, 0.0, 1.0)
                glVertex2f(i.x, i.y)
                dx, dy = i.velocity.cart()
                glVertex2f(i.x + dx * 5, i.y + dy * -5)
                glEnd()

                glBegin(GL_LINE_STRIP)
                glColor3f(1, 0, 0)
                glVertex2f(i.x, i.y)
                dx, dy = i.force.cart()
                glVertex2f(i.x + dx * 5, i.y + dy * -5)
                glEnd()






    def set_color(self, color: Color):
        glClearColor(_1x(color.r), _1x(color.g), _1x(color.b), color.a)

    def create_line(self, a, b, x, y, *args, **kwargs):
        self.renderable.append(_RenderableLine(a, b, x, y))

    def create_image(self, x, y, texture):
        #print(x, y, texture)
        self.renderable.append(_RenderableImage(x, y, texture))




    def create_text(self, x, y, **kwargs):
        pass


class OpenGLProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(1000, 1000), title: str = "ViewPort Frame",
                 color: Color = Color(255, 255, 255), scale=1):
        super().__init__(parent)
        self.parent.window = self

        self.size = size
        self.title = title

        self.viewport = ViewPort(self, position=Dimension(0, 0))
        self.cropped_viewport = self.viewport.crop_add()
        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self._tk.title(title)
        self.color = color_alias(color)
        self._curcolor = Color(self.color.r, self.color.g, self.color.b)
        self.surface = _base_OpenGL_Frame(self, self._tk, size, scale=scale)
        self.surface.pack(fill=tk.BOTH, expand=tk.YES)
        self.surface.animate = 1
        self.ignore_render = []

        self._blits = 0
        self._checks = 0

        self.force_update = 0

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()
        self.surface.mainloop()


    

    def update(self):
        pass

    def _close_parent_close(self):
        self.parent.terminated = True
        if self.parent.debug != None:
            self.parent.debug.destroy()
        self._tk.destroy()
        #self.surface.destroy()

    def blit(self):
        try:
            self.real_blit()
        except Exception as e:
            if isinstance(e, GLError):
                c = str(e).replace('\n', '')
                Logger.print(f"OpenGL Error : {c}", channel=4)
            else:
                Logger.print(f"Error in printing object: {e}", channel=4)

    def real_blit(self):


        # self.surface.delete("all")
        self.surface.renderable = []

        if self._curcolor != self.color:
            self._curcolor = Color(self.color.r, self.color.g, self.color.b)
            self.surface.set_color(self._curcolor)


        for i in self.parent.ghosts:
            self.surface.delete(f"ID{i.blit_id}")


        # Object checks are migrated to opengl's draw function




            # if isinstance(i, GameObject):
            #
            #     a = time.time()
            #
            #     if i.start_debug_highlight_tracking:
            #         i._debug_blit_once()
            #
            #     g = random.randint(-2 ** 64, 2 ** 64)
            #
            #     cam = self.viewport.shift(i.position)
            #
            #     rotated = i.rotation != i.last_display_rotation
            #
            #     # If its a thing with ass image. why would u do it like this but not making another image class
            #     if isinstance(i, Image):
            #         self.surface.create_image(cam.x, cam.y, i.image) # Image -> ImageTexture -> PIL's Image
            #
            #     # If its text
            #     elif isinstance(i, Text):
            #         self.surface.create_text(i.x, i.y, text=i.text, fill=i.font.color, font=str(i.font), tags=f"ID{g}")
            #
            #     # If its a Particle
            #     elif isinstance(i, Particle):
            #         self.surface.create_oval(i.x - i.r, i.y - i.r, i.x + i.r, i.y + i.r, tags=f"ID{g}")
            #
            #     # If its a TopLevelWhateverBody
            #     elif isinstance(i, TopViewPhysicsBody):
            #         self.surface.create_rectangle(i.x, i.y, i.x + i.size.x, i.y + i.size.y, fill="white", outline="white", tags=f"ID{g}")
            #
            #     # If its a regular gameobject
            #     elif len(i.points) > 0:
            #         for j in i.points:
            #             pos1 = j[0]
            #             pos2 = j[1]
            #             self.surface.create_line(pos1[0] + i.x, pos1[1] + i.y, pos2[0] + i.x, pos2[1] + i.y, fill=i.color, )
            #
            #     i.last_display_position = Dimension(i.position.x, i.position.y)
            #     i.last_display_rotation = i.rotation

        #
        # # TODO: lag
        # for i in self.parent.displayorder:
        #     self.surface.tag_raise(f"ID{i.blit_id}")


    def remove(self):
        print("revmoved " + str(self))








class LegacyProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(1000, 1000), title: str = "ViewPort Frame",
                 color: tuple = Color(255, 255, 255), scale=1):
        super().__init__(parent)
        self.parent.window = self

        self.size = size
        self.title = title

        self.viewport = ViewPort(self, position=Dimension(0, 0))
        self.cropped_viewport = self.viewport.crop_add()
        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self._tk.title(title)

        self.color = color_alias(color)
        self._curcolor = Color(self.color.r, self.color.g, self.color.b)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg=str(color), highlightthickness=0)
        self.surface.pack()
        self.ignore_render = []

        self._blits = 0
        self._checks = 0

        self.force_update = 0

    def blit(self):
        try:
            self.real_blit()
        except Exception as e:
            print(traceback.format_exc())
            Logger.print(f"Error in printing object: {e}", channel=4)

    def real_blit(self):
        # self.surface.delete("all")

        s = time.time()

        if self._curcolor != self.color:
            self._curcolor = Color(self.color.r, self.color.g, self.color.b)


        for i in self.parent.objects:

            self._checks += 1

            if (i.position.x + i.size.x < -10 or i.position.y + i.size.y < -10) or (i.position.x > self.parent.dimensions.x + 10 or i.position.y > self.parent.dimensions.y + 10):
                self.surface.delete(f"ID{i.blit_id}")
                if i.destroy_outside_boundary:
                    i.delete()
                continue

            f = False
            for n in self.ignore_render:
                if isinstance(i, n):
                    f = True
            if f:
                continue


            if isinstance(i, GameObject):

                # print("check")

                # if i.topleft < self.cropped_viewport.x

                # print()

                a = time.time()

                moved = i.position != i.last_display_position
                rotated = i.rotation != i.last_display_rotation

                if ((moved or rotated) and not i.hidden) or i.force_update:

                    self._blits += 1

                    # print(i, i.position, i.last_position)

                    if i.clear_blit:
                        self.surface.delete(f"ID{i.blit_id}")

                    if i.start_debug_highlight_tracking:
                        i._debug_blit_once()

                    g = random.randint(-2 ** 64, 2 ** 64)

                    cam = self.viewport.shift(i.position)

                    # If its a thing with ass image. why would u do it like this but not making another image class
                    if isinstance(i, Image):
                        # if rotated:
                        #     i.content = ImageTk.PhotoImage(i.image.rotate(i.rotation))
                        self.surface.create_image(cam.x, cam.y, image=i.image.texture)

                    # If its text
                    elif isinstance(i, Text):
                        self.surface.create_text(i.x, i.y, text=i.text, fill=i.font.color, font=str(i.font), tags=f"ID{g}")

                    # If its a Particle
                    elif isinstance(i, Particle):
                        self.surface.create_oval(i.x - i.r, i.y - i.r, i.x + i.r, i.y + i.r, tags=f"ID{g}")

                    # If its a TopLevelWhateverBody
                    elif isinstance(i, TopViewPhysicsBody):
                        self.surface.create_rectangle(i.x, i.y, i.x + i.size.x, i.y + i.size.y, fill="white", outline="white", tags=f"ID{g}")

                    # If its a regular gameobject
                    elif len(i.points) > 0:

                        last = None

                        for j in i.points:

                            if last is not None:
                                pos1 = j[0]
                                pos2 = j[1]
                                self.surface.create_line(last[0] + i.x, last[1] + i.y, pos1 + i.x, pos2 + i.y,
                                                         tags=f"ID{g}", fill=i.color)
                            last = j

                    i.last_display_position = Dimension(i.position.x, i.position.y)
                    i.last_display_rotation = i.rotation
                    i.blit_id = g


            if i.force_update > 0:
                i.force_update -= 1

        # TODO: lag
        for i in self.parent.displayorder:
            self.surface.tag_raise(f"ID{i.blit_id}")


    def update(self):
        pass

    def remove(self, obj):
        self.surface.delete(f"ID{obj.blit_id}")

    def _close_parent_close(self):
        self.parent.terminated = True
        if self.parent.debug != None:
            self.parent.debug.tk.destroy()
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()