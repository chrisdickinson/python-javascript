from javascript.value import Number, Boolean, String 
from javascript.js_function import JSFunction, JSBuiltInFunction, JSArguments 
from javascript.object import JSObject

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
        return String(unicode(val))

    def undefined(self):
        from javascript.special_objects import Undefined
        return Undefined

    def null(self):
        from javascript.special_objects import Null
        return Null

    def object(self, constructor, *args):
        cons = self.context.js_get_property(self.thread, constructor).js_box(self.thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(self.thread)
        obj = JSObject(proto)
        return cons.js_execute(self.thread, obj, self.arguments(args)) 

    def function(self, statements, context, arguments, name):
        cons = self.context.js_get_property(self.thread, 'Function').js_box(self.thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(self.thread)
        fn = JSFunction(proto, statements, context, arguments)

        if name is not None:
            fn.js_set_property(self.thread, 'name', self.thread.cons.string(name)) 

        return fn

    def internal_function(self, fn, proto=None):
        return JSBuiltInFunction(proto, fn)

    def arguments(self, args):
        cons = self.context.js_get_property(self.thread, 'Arguments').js_box(self.thread)
        proto = cons.js_get_property(self.thread, 'prototype').js_box(self.thread)
        return JSArguments(proto, args)
