# Documentation

## `pyflux.Runnable`
**Internal Reference**: `pyflux.interface.Runnable`<br>

**Implementations**
- python.object

**Functions**<br>
**def** `__init__(self, function, kwargs, parent)` **Constructor**
Creates a runnable that could be run. This is only for internal use only for adding event listeners.

**def** `__call__(self, *args, **kwargs)` **Python**
Run when this object is being called.

## `pyflux.GameContext`
**Internal Reference**: `pyflux.context.GameContext`<br>

A Game Context object that represents the main window and handles most of the game tick and processing events.

**Implementations**
- PygameProObject
  - python.object
- GameObjectCreator
  - python.object

**Functions**<br>
**def** `__init__(self, size_x: int, size_y: int, *args, **kwargs)` **Constructor**<br>
Creates a GameContext object. It is recommended to have only one instance in every python process.

**def** `from_dim(scale: Dimension, *args, **kwargs)` **Constructor**<br>
Creates a GameContext object using Dimension class.

**def** `set_title(self, caption: str)`<br>
Sets the title of the GameContext. `pygame.display.set_caption(text: string)`

**def** `start(self)`<br>
Starts the game tick. Normally the frame tick will be on the main thread and the tick thread will be an individual thread.


