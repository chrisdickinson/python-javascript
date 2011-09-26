from javascript.cons import Cons

class RuntimeError(Exception):
    def __init__(self, what):
        self.what = what

class Frame(object):
    def __init__(self, parent, func, this_obj, args, context):
        self.args = args
        self.context = context.sub()
        self.func = func
        self.parent = parent
        self.this_obj = this_obj

    def set_args(self, thread): 
        last = 0
        if self.func: 
            for idx, val in enumerate(self.args):
                self.context.define_property(self.func.args[idx], val)
                last = idx

            if last < len(self.func.args)-1:
                for i in range(last, len(self.func.args)):
                    self.context.define_property(self.func.args[i], thread.cons.undefined())

class Thread(object):
    def __init__(self, base_context):
        self.cons = Cons(self, base_context)
        self._context = base_context 
        self.frame = None

    def run(self, statements):
        from javascript.statement import Return

        self.push_frame(
            None,
            self._context,
            self.cons.arguments([]) 
        )

        try:
            for statement in statements:
                self.eval(statement)
        except Return, ret:
            self.pop_frame()
            return ret.value
        else:
            self.pop_frame()
            return self.cons.undefined()

    def eval(self, statement):
        return statement.eval(self)

    def throw(self, what):
        raise RuntimeError(what)

    def context(self):
        return self.frame.context

    def typeof(self, what):
        return what.typeof

    def get_this(self):
        return self.frame.this_obj

    def get_args(self):
        return self.frame.args

    def push_frame(self, fn, this_obj, args):
        self.frame = Frame(self.frame, fn, this_obj, args, fn and fn.context or self._context)
        self.frame.set_args(self)

    def pop_frame(self):
        self.frame = self.frame.parent
