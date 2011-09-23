from jspy.object import JSObject

class NilObject(JSObject):
    def __init__(self, name):
        self.name = name 

    def js_enumerate(self, thread):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot coerce')))

    def js_get_property(self, thread, *args, **kwargs):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot access properties on nilobject')))

    def js_set_property(self, thread, *args, **kwargs):
        thread.throw(thread.cons.object('TypeError', thread.cons.string('cannot access properties on nilobject')))

    def js_bool(self):
        return False

Null = NilObject('null')
Undefined = NilObject('undefined')

