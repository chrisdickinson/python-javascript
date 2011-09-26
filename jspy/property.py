class Property(object):
    def __init__(self, target, value, enumerable, configurable, get, set):
        self.target = target
        self.value = value
        self.enumerable = value
        self.configurable = configurable
        self.get = get
        self.set = set

    @property
    def typeof(self):
        return self.value.typeof

    def unset(self):
        self.target = None

    def js_get(self, thread, on):
        if self.get is not None:
            return self.get.js_execute(thread, on, thread.cons.arguments([]))
        else:
            return self.value

    def js_set(self, thread, val):
        if self.configurable is False:
            return val
    
        if self.set is not None:
            self.value = self.set.js_execute(thread, self.target, thread.cons.arguments([val]))
        else:
            self.value = val

        return self.value

    # boxing and unboxing a property triggers the ``get`` property (if any).
    def js_box(self, thread):
        if self.get is not None:
            return self.get.js_execute(thread, on, thread.cons.arguments([])).js_box(thread)
        return self.value.js_box(thread)

    def js_unbox(self, thread):
        if self.get is not None:
            return self.get.js_execute(thread, on, thread.cons.arguments([])).js_unbox(thread)
        return self.value.js_unbox(thread)

    def js_bool(self):
        return self.value.js_bool()

    def js_execute(self, thread, on, args):
        return self.value.js_box(thread).js_execute(thread, on, args)
