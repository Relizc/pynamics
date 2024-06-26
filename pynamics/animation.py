from typing import Iterable
from .interface import PyNamical
from .events import EventHolder
from .dimensions import Dimension, Color
from .events import EventType
import enum
import random

class AnimationFunction:

    def __init__(self, executor=None):
        self.executor = executor

    # Example y=x function
    def __call__(self, x):
        return x
    
class AnimationType(enum.Enum):
    LINEAR = 0x00
    SCALE = 0x01

class CubicBezier(AnimationFunction):
    """Cubic Bezier Function (Scale Type)"""

    def __init__(self, x0 = 0.5, x1 = 0.5, y0 = 0.5, y1 = 0.5):
        super().__init__()
        self.point_0 = Dimension(x0, x1)
        self.point_1 = Dimension(y0, y1)

    def function_x(self, t):
        return (3 * t * ((1 - t) ** 2) * self.point_0.x) + (3 * (t ** 2) * (1 - t) * self.point_1.x) + (t ** 3)
    
    def function_y(self, t):
        return (3 * t * ((1 - t) ** 2) * self.point_0.y) + (3 * (t ** 2) * (1 - t) * self.point_1.y) + (t ** 3)

    def __call__(self, x):
        return (self.function_x(x), self.function_y(x))
    
class Linear(AnimationFunction):
    pass

EASE        = CubicBezier(0.25, 0.1, 0.25, 1.0)
EASE_IN     = CubicBezier(0.42, 0, 1.0, 1.0)
EASE_OUT    = CubicBezier(0   , 0, 0.58, 1.0)
EASE_IN_OUT = CubicBezier(0.42, 0, 0.58, 1.0)
LINEAR      = CubicBezier(0, 0, 1, 1)
    


class Animation(PyNamical):
    
    def __init__(self,
                 animation_function: AnimationFunction = None, 
                 duration: int = 128, 
                 type: AnimationType = AnimationType.SCALE,
                 step: int = None,
                 fields: Iterable = []):
        super().__init__(None, no_parent=True)
        self.function = animation_function
        self.function.executor = self
        self.duration = int(duration)
        self.type = type
        self.fields = fields

        self.step = step
        if self.step is None:
            self.step = self.duration

        self.tick_value = {}

        if self.type == AnimationType.SCALE:
            f = 0
            stepsize = 1 / self.step
            for i in range(self.step):
                ix, iy = self.function(f)
                x = int(self.duration * ix)
                self.tick_value[x] = iy
                f += stepsize

    def play(self, play_at = None, final_value = [], function = None):

        # if not isinstance(play_at, iter):
        #     delta = final_value - play_at
        #
        #     @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.TICK, killafter=self.duration)
        #     def t(this):
        #         for tar in range(len(self.fields)):
        #             d = delta[tar] * self.tick_value.get(self.age, 0)
        #             if d == 0:
        #                 v = play_at
        #             else:
        #                 v = play_at + d
        #             setattr(play_at, self.fields[tar], v)
        #         self.age += 1
        #         if self.age == self.duration:
        #             setattr(play_at, self.fields[tar], final_value[tar])
        #
        #     return

        if len(self.fields) != len(final_value):
            raise ValueError(
                f"length of final_value ({len(final_value)}) must equal to length of editable fields ({len(self.fields)})."
            )

        self.age = 0
        delta = []
        for i in range(len(self.fields)):
            delta.append(final_value[i] - getattr(play_at, self.fields[i]))

        initial = []
        for i in range(len(self.fields)):
            initial.append(getattr(play_at, self.fields[i]))

        self.id = random.randint(-2147483648, 2147483647)

        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.TICK, threaded=False, killafter=self.duration, name="AnimationProgressionEvent", id=self.id)
        def t(this):
            n = self.tick_value.get(self.age, 0)

            if function is not None:
                function(n)

            for tar in range(len(self.fields)):
                d = delta[tar] * n
                # print(d)
                if d == 0:
                    v = getattr(play_at, self.fields[tar])
                else:
                    v = initial[tar] + d
                setattr(play_at, self.fields[tar], v)
            self.age += 1
            if self.age == self.duration:
                if function is not None:
                    function(1)
                else:
                    setattr(play_at, self.fields[tar], final_value[tar])

        return self.id

    def stop(self):
        PyNamical.MAIN_GAMEMANAGER.kill_event(self.id)

        
def play_position_animation(function, object, final=(0, 0)):
    fields = []
    f = []
    if final[0] is not None:
        fields.append("x")
        f.append(final[0])
    if final[1] is not None:
        fields.append("y")
        f.append(final[1])
    Animation(function, duration=64, fields=fields).play(object.position, f)


        
    

