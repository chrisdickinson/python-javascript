from jspy.value import Number, Boolean, String 
from jspy.js_function import JSFunction, JSBuiltInFunction, JSArguments 
class Cons(object):
    def __init__(self, thread, context):
        self.thread = thread
        self.context = context
        self.stack = None

    def number(self, val):
        return Number(str(val))
 
    def boolean(self, val):
        return Boolean(val and 'true' or 'false')

    def string(self, val):
        return String('"%s"' % val)

    def undefined(self):
        from jspy.special_objects import Undefined
        return Undefined

    def null(self):
        from jspy.special_objects import Null
        return Null

    def object(self, constructor, *args):
        cons = self.context.js_get_property(self.thread, constructor).js_box(thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(thread)
        obj = JSObject(proto)
        return cons.js_execute(self.thread, obj, self.arguments(args)) 

    def function(self, statements, context, arguments, name):
        cons = self.context.js_get_property(self.thread, 'Function').js_box(thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(thread)
        fn = JSFunction(proto, statements, context, arguments)

        if name is not None:
            fn.js_set_property(self.thread, 'name', self.thread.cons.string(name)) 

        return fn

    def arguments(self, args):
        cons = self.context.js_get_property(self.thread, 'Arguments').js_box(thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(thread)
        return JSArguments(proto, args)
