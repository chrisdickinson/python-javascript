from javascript.expressions.base import Expression

class BinaryExpression(Expression):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def eval(self, thread, **kwargs):
        return self.op(thread, self.lhs, self.rhs, **kwargs)
