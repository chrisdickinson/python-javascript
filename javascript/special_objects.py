from javascript.object import JSObject

class NilObject(JSObject):
    def __init__(self, name):
        self.name = name 
        self.properties = {}

    def js_enumerate(self):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot coerce')))

    def js_get_property(self, thread, *args, **kwargs):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot access properties on nilobject')))

    def js_set_property(self, thread, *args, **kwargs):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot access properties on nilobject')))

    def js_unbox(self, thread, *args, **kwargs):
        return self.name

    def js_bool(self):
        return False

Null = NilObject('null')
Undefined = NilObject('undefined')

