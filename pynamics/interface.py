from .styling import StyleLoader


class PyNamical:

    def __init__(self, parent):
        self.style = StyleLoader()
        self.parent = parent
        self.parent.children.append(self)
        self.children = []

    def delete(self):
        pass
