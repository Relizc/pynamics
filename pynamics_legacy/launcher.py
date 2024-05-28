from typing import Any


class LaunchEnv:

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def __init__(self, args) -> None:
        self.args = args
        self.vars = [x for x in self.args if x.startswith("-")]
        self.path = None
        for i in range