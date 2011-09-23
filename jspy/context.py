

class Context(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def has(self, prop):
        return prop in self.vars

    def delete(self, prop):
        del self.vars[prop]

    def get_from(self, thread, name):
        if name == 'this':
            return thread.get_this()
        elif name == 'arguments':
            return thread.get_args()

        if name in self.vars:
            return self.vars[name], self
        
        if self.parent is not None:
            return self.parent.get(thread, name)

        return thread.cons.undefined(), None

    def top(self):
        if self.parent is None:
            return self
        return self.parent.top()

    def sub(self):
        return Context(self) 

    def get(self, thread, name):
        return self.get_from(thread, name)[0]

    def set(self, thread, name, val):
        val, at = self.get_from(thread, name)
        if at is not None:
            at.vars[name] = val
            return

        # oh god, it's none.
        self.top().vars[name] = val

        return val
 
