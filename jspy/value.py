from jspy.object import JSObject
import math

class JSValue(object):
    box_to = 'Object'
    typeof = 'object'

    def __init__(self, string_token):
        self.source = str(string_token)

    def __str__(self):
        return str(self.value)

    def js_unbox(self, thread):
        return self

    def js_box(self, thread):
        thread.cons.object(box_to, self) 

class Number(JSValue):
    box_to = 'Number'
    typeof = 'number'

    def __init__(self, string_token):
        super(Number, self).__init__(string_token)
        if self.source == 'NaN':
            self.value = float('nan')
        elif self.source == 'Infinity':
            self.value = float('inf')
        elif '.' in self.source or 'e' in self.source:
            self.value = float(self.source)
        else:
            base = 10
            if self.source[0:2] == '0x':
                base = 16
            elif self.source[0] == '0':
                base = 8
            self.value = int(self.source, base)

    def js_bool(self):
        return self.value != 0

class String(JSValue):
    box_to = 'String'
    typeof = 'string'

    def __init__(self, string_token, needs_escaped=False):
        super(String, self).__init__(string_token)
        if needs_escaped:
            self.value = self.source[1:-1]
        else:
            self.value = self.source

    def js_bool(self):
        return len(self.value) > 0

class Boolean(JSValue):
    box_to = 'Boolean'
    typeof = 'boolean'

    def __str__(self):
        if self.value:
            return 'true'
        return 'false'

    def __init__(self, string_token):
        super(Boolean, self).__init__(string_token)
        self.value = self.source == 'true'

    def js_bool(self):
        return self.value 
