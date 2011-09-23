from jspy.object import JSObject
from jspy.statement import Return

class JSFunction(JSObject):
    typeof = 'function'

    def __init__(self, proto, statements, context, args):
        super(JSObject, self).__init__(proto)
        self.statements = statements
        self.context = context
        self.args = args

    def js_execute(self, thread, on_object, arguments):
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
        super(JSObject, self).__init__(proto)
        self.function = function

    def js_execute(self, thread, on_object, arguments):
        value = None
        try:
            value = self.function(thread, on_object, arguments)
        except Exception, e:
            thread.throw(thread.cons.object('RuntimeError', thread.cons.string(str(e))))
        else:
            return value

class JSArguments(JSFunction):
    def __init__(self, proto, args):
        super(JSArguments, self).__init__(proto)
        self.define_property('length', len(args), configurable=False)
