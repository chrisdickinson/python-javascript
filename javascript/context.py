from jspy.object import JSObject

class Context(JSObject):
    def __init__(self, parent=None):
        super(Context, self).__init__(parent)
        self.parent = parent

    def has(self, prop):
        return prop in self.properties

    def top(self):
        if self.parent is None:
            return self
        return self.parent.top()

    def sub(self):
        return Context(self) 
