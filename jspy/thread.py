from jspy.cons import Cons

class Frame(object):
    def __init__(self, parent, func, this_obj, args, context):
        self.args = args
        self.context = context.sub()
        self.func = func
        self.parent = parent
        self.this_obj = this_obj

    def set_args(self, thread): 
        last = 0 
        for idx, val in enumerate(args):
            self.context.set(thread, self.func.args[idx], val)
            last = idx

        if last < len(self.func.args):
            for i in range(last, len(self.func.args)):
                self.context.set(thread, self.func.args[idx], thread.cons.undefined())

class Thread(object):
    def __init__(self, base_context):
        self.cons = Cons(self, base_context)
        self.context = base_context 
        self.frame = None

    def throw(what):
        raise what

    def context(self):
        return self.frame.context

    def typeof(what):
        return what.typeof

    def get_this(self):
        return self.frame.this_obj

    def get_args(self):
        return self.frame.args

    def push_frame(self, fn, this_obj, args):
        self.frame = Frame(self.frame, fn, this_obj, args, fn.context)
        self.frame.set_args()

    def pop_frame(self):
        self.frame = self.frame.parent
