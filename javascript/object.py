class JSObject(object):
    typeof = 'object'

    def __init__(self, proto):
        self.proto = proto
        self.properties = {} 
        self.sealed = False

    def has(self, prop):
        return prop in self.properties

    def delete(self, prop):
        if prop in self.properties:
            self.properties[prop].unset()
            del self.properties[prop]

    def define_property(self, name, value, enumerable=True, configurable=True, get=None, set=None, PropertyKlass=None):
        from jspy.property import Property
        PropertyKlass = PropertyKlass or Property

        self.properties[name] = PropertyKlass(
            self,
            value,
            enumerable,
            configurable,
            get,
            set
        )

    def js_enumerate(self):
        names = [key for key, prop in self.properties.iteritems() if prop.enumerable]
        return names

    def js_get_property(self, thread, prop, is_assign=False):
        if is_assign:
            if prop in self.properties:
                return self.properties[prop]
            return None
        else:
            if prop in self.properties:
                return self.properties[prop]
            if self.proto:
                return self.proto.js_get_property(thread, prop, is_assign)
            return thread.cons.undefined()

    def js_set_property(self, thread, name, val):
        if name not in self.properties:
            if self.sealed:
                return thread.throw(
                    thread.cons.object('TypeError', thread.cons.string("Can't add property %s, object is not extensible" % name))
                )
            self.define_property(name, val)
    
        prop = self.properties[name]
        prop.js_set(thread, val)
        return prop

    def js_execute(self, thread, on_object, arguments, FrameKlass):
        thread.throw(
            thread.cons.object('TypeError', thread.cons.string("OBJECT_NOT_FUNCTION"))
        )

    def js_bool(self):
        return True

    def js_box(self, thread):
        return self

    def js_unbox(self, thread):
        valueOf = self.js_get_property(thread, 'valueOf')
        if thread.typeof(valueOf) != 'undefined' and thread.typeof(valueOf) == 'function':
            val = valueOf.js_execute(thread, self, thread.cons.arguments([]))
            if thread.typeof(val) in ['string', 'number', 'boolean']:
                return val

        toString = self.js_get_property(thread, 'toString')
        if thread.typeof(toString) != 'undefined' and thread.typeof(toString) == 'function':
            val = toString.js_execute(thread, self, thread.cons.arguments([]))

            if thread.typeof(val) in ['string', 'number', 'boolean']:
                return val

        thread.throw(
            thread.cons.object('TypeError', thread.cons.string('cannot_convert_to_primitive'))
        )
