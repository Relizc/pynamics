import random
import tkinter as tk
from tkinter import ttk
from PIL import Image as ImageUtils, ImageTk

import inspect
import tkinter.filedialog as filedialog

#https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class ImageBrowser(ttk.Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe, path):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        self.image = ImageUtils.open(path)  # open image
        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # minsize, maxsize, number = 5, 20, 10
        # for n in range(number):
        #     x0 = random.randint(0, self.width - maxsize)
        #     y0 = random.randint(0, self.height - maxsize)
        #     x1 = x0 + random.randint(minsize, maxsize)
        #     y1 = y0 + random.randint(minsize, maxsize)
        #     color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
        #     self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, activefill='black')
        self.show_image()

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None):

        print(self.imscale)

        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        # if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
        #     bbox[0] = bbox1[0]
        #     bbox[2] = bbox1[2]
        # if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
        #     bbox[1] = bbox1[1]
        #     bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), resample=ImageUtils.BOX))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

ALL_OBJECTS = {}
OBJECT_TYPING_HINTS = {}
DICT_ID_TO_OBJ = {}
WORKSPACE = None
TREE_HANDLER = None

def clone(widget):
    parent = widget.nametowidget(widget.winfo_parent())
    cls = widget.__class__

    clone = cls(parent)
    for key in widget.configure():
        clone.configure({key: widget.cget(key)})
    return clone

class ObjectSelectButton(tk.Button):

    def __init__(self, root, default=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root

        self.object = default
        if self.object is None:
            self["text"] = "Select Object"
        else:
            self["text"] = str(self.object)

        self["state"] = "disabled"
        self["command"] = self.choose

    def choose(self):
        self.popup = tk.Toplevel(self.root)
        self.popup.rowconfigure(0, weight=1)
        self.popup.columnconfigure(0, weight=1)
        self.popup.grab_set()
        self.find = ttk.Treeview(self.popup)
        self.find.heading("#0", text="Select an Object")

        for i in TREE_HANDLER.get_children():
            print(TREE_HANDLER.item(i))

        self.find.grid(row=0, column=0, sticky="news")

    @property
    def value(self):
        return self.object


class PathSelectButton(tk.Button):

    def __init__(self, root, default=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root

        self.path = default

        if self.path is None:
            self["text"] = "Select Path"
        else:
            self["text"] = self.path

        self["command"] = self.choose

    def choose(self):
        self.path = filedialog.askopenfilename(title="Select File")
        self["text"] = self.path

    @property
    def value(self):
        return self.path

class IterableMakerList(tk.Frame):

    def __init__(self, root, default=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root

        self.rowconfigure((0, 1, 2), weight=1)

        self.view = tk.Listbox(self)
        self.view.grid(row=0, column=0, columnspan=3, sticky="news")

        self.add = tk.Button(self, text='+')
        self.add.grid(row=1, column=0)

        self.sub = tk.Button(self, text='-')
        self.sub.grid(row=1, column=1)

        self.clr = tk.Button(self, text='Clear')
        self.clr.grid(row=1, column=2)

        self.contents = default

        if self.contents is None:
            self.contents = []
        else:
            self.contents = []

    def choose(self):
        self.path = filedialog.askopenfilename(title="Select File")
        self["text"] = self.path

    @property
    def value(self):
        return self.path


class CreationPrompt:

    def __init__(self, root, clazz):
        self.root = root
        self.clazz = clazz

        self.prompt = tk.Toplevel(root)
        self.prompt.title("Create New Object")
        self.prompt.grab_set()

        create = tk.Label(self.prompt, text="Object Class")
        create.grid(row=0, column=0, sticky="e", padx=8, pady=4)

        self.class_select = ttk.Combobox(self.prompt, values=list(ALL_OBJECTS), state="readonly")
        self.class_select.current(list(ALL_OBJECTS).index(str(self.clazz.__name__)))
        self.class_select.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        self.class_select.bind("<<ComboboxSelected>>", self.selected)

        self.kwargs = {}
        self.tags = []
        self.create = None

        self.update_inputs()

    def selected(self, e):
        select = self.class_select.get()
        self.clazz = ALL_OBJECTS[select]

        self.update_inputs()

    def update_inputs(self):

        if self.create is not None:
            self.create.destroy()
        for i in self.kwargs:
            self.kwargs[i].destroy()
        for i in self.tags:
            i.destroy()
        self.tags = []
        self.kwargs = {}

        h = OBJECT_TYPING_HINTS[self.clazz.__name__]

        k = inspect.getargspec(self.clazz.__init__)

        c = 0


        for i in range(len(OBJECT_TYPING_HINTS[self.clazz.__name__])):

            c = i



            label = tk.Label(self.prompt, text=f"{k.args[i + 1]}")
            label.grid(row=i+1, column=0, sticky="e", padx=8, pady=4)

            self.tags.append(label)

            if h[i] == "object":
                if TREE_HANDLER.focus() == '':
                    f = WORKSPACE
                else:
                    f = DICT_ID_TO_OBJ[TREE_HANDLER.focus()]

                content = ObjectSelectButton(self.prompt, default=f)



            elif h[i] == "path":
                content = PathSelectButton(self.prompt)

            elif h[i].startswith("iterable"):

                content = IterableMakerList(self.prompt)

            content.grid(row=i + 1, column=1, sticky="w", padx=8, pady=4)
            self.kwargs[k.args[i + 1]] = content

        self.create = tk.Button(self.prompt, text="Create", command=self.bake)
        self.create.grid(row=c+2, column=0, rowspan=2, sticky="w", padx=8, pady=4)

    def bake(self):

        processed = {}
        for i in self.kwargs:
            processed[i] = self.kwargs[i].value

        obj = self.clazz(**processed)

        self.prompt.destroy()
        del self
        return obj


