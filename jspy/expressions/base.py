class Expression(object):
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

    def eval(self, thread):
        return thread.cons.undefined()
