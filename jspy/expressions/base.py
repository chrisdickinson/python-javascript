class BaseExpression(object):
    def eval(self, thread):
        return thread.cons.undefined()
