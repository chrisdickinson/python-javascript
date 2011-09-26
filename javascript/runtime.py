from javascript.tokenizer import tokenize
from javascript.parser import parse
from javascript.visitor import Visitor
from javascript.context import Context
from javascript.thread import Thread
from javascript.object import JSObject

class Runtime(object):
    def __init__(self):
        self.thread = None
        self.base_context = None

    def compile(self, src):
        tokens = tokenize(src)
        visitor = Visitor(parse(tokens))
        return visitor.run()        

    def run(self, src, extra_context=None):
        if extra_context is None:
            extra_context = {}

        base_context = Context()
        thread = Thread(base_context.sub())
        self.setup_context(base_context, thread)

        for key, item in extra_context.iteritems():
            if type(item) == int:
                base_context.define_property(key, thread.cons.number(item))
            elif type(item) in [unicode, str]:
                base_context.define_property(key, thread.cons.string(unicode(item)))
            elif type(item) == bool:
                base_context.define_property(key, thread.cons.boolean(item))

        return thread.run(self.compile(src))

    def setup_context(self, context, thread):
        def Object(thread, on, arguments):
            ret = on is thread.context().top() and JSObject(
                thread.context().js_get_property(thread, 'Object').js_get_property(thread, 'prototype').js_box(thread)
            ) or on

            if len(arguments):
                obj = arguments[0]
                keys = obj.js_box(thread).js_enumerate()
                for key in keys:
                    ret.js_set_property(thread, key, obj.js_get_property(thread, key).js_get(thread))

            return ret 
            
        def Function(thread, on, arguments):
            if len(arguments) > 0:
                # compile the function.
                args = [], body = ''
                if len(arguments) > 1:
                    args, body = arguments[0:-1], arguments[-1]
                src = 'function (%s) { %s }' % (u', '.join(args), body)
                return thread.cons.function(
                    self.compile(src),
                    thread.context().sub(),
                    args,
                    'anonymous'
                )
            return thread.cons.function(
                [],
                thread.context().sub(),
                [],
                'anonymous'
            )

        def Arguments(thread, on, arguments):
            return JSArguments(on.proto, arguments)

        def Array(thread, on, arguments):
            array = JSArray(on.proto)
            for idx, arg in enumerate(arguments):
                array.js_set_property(thread, str(idx), arg)
            return array

        JS_Object = thread.cons.internal_function(Object, None)
        JS_Function = thread.cons.internal_function(Function, None)
        JS_Object_Proto = JSObject(None)
        JS_Object_Proto.define_property('constructor', JS_Object)

        JS_Object.define_property('prototype', JS_Object_Proto)
        JS_Function_Proto = JSObject(JS_Object_Proto)
        JS_Function.define_property('prototype', JS_Function_Proto)
        JS_Object.proto = JS_Function_Proto

        JS_Array = thread.cons.internal_function(Array, JS_Function_Proto)
        JS_Array_Proto = JSObject(JS_Object_Proto)
        JS_Array_Proto.define_property('length', 0, configurable=False, get=thread.cons.internal_function(lambda t, o, x: t.cons.number(len(o)), JS_Function_Proto)) 
        JS_Array.define_property('prototype', JS_Array_Proto)

        JS_Arguments = thread.cons.internal_function(Arguments, JS_Function_Proto)
        JS_Arguments_Proto = JSObject(JS_Object_Proto)
        JS_Arguments.define_property('prototype', JS_Array_Proto)

        def toString(t, on, args):
            return t.cons.string(u'[object Object]')

        JS_Object_Proto.define_property(
            'toString', 
            thread.cons.internal_function(
                toString,
                JS_Function_Proto
            )
        ) 

        context.define_property('Object', JS_Object)
        context.define_property('Function', JS_Function)
        context.define_property('Array', JS_Array)
        context.define_property('Arguments', JS_Arguments)

        return context

 
 
