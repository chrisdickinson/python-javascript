from javascript.object import JSObject
from javascript.statement import Return

class JSFunction(JSObject):
    typeof = 'function'

    def __init__(self, proto, statements, context, args, name='anonymous'):
        super(JSFunction, self).__init__(proto)
        self.statements = statements
        self.context = context
        self.args = args
        self.name = name

    def js_execute(self, thread, on, arguments):
        thread.push_frame(
            self,
            on,
            arguments
        )

        try:
            for statement in self.statements:
                thread.eval(statement)
        except Return, ret:
            thread.pop_frame()
            return ret.value
        else:
            thread.pop_frame()
            return thread.cons.undefined()

class JSBuiltInFunction(JSFunction):
    def __init__(self, proto, function):
        super(JSBuiltInFunction, self).__init__(proto, None, None, None)
        self.function = function
        self.name = 'Builtin function %s' % function.func_name
    def js_execute(self, thread, on_object, arguments):
        value = None
        try:
            value = self.function(thread, on_object, arguments)
        except Exception, e:
            thread.throw(thread.cons.object('RuntimeError', thread.cons.string(str(e))))
        else:
            return value

class JSArray(JSObject):
    def __init__(self, proto, args):
        super(JSArray, self).__init__(proto)
        self.items = []

    def js_set_property(self, thread, name, val):
        try:
            id = int(name)
            l = len(self.items)
            if id > l:
                items = []
                for i in range(l, id):
                    item = thread.cons.undefined()
                    items.append(item)
                    self.define_property(str(i), item)
                self.items += items
                self.items[id] = val
            else:
                self.items[id] = val
        except ValueError:
            pass
        super(JSArray, self).js_set_property(thread, name, val)

    def js_get_property(self, thread, name):
        try:
            id = int(name)
            return self.items[id]
        except (ValueError, IndexError), e:
            pass
        super(JSArray, self).js_get_property(thread, name, val)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, *args):
        return self.items.__getitem__(*args)

class JSArguments(JSArray):
    def __init__(self, proto, args):
        super(JSArguments, self).__init__(proto, args)
        self.define_property('length', len(args), configurable=False)
