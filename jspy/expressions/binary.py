from jspy.expressions.base import BaseExpression

class BinaryExpression(BaseExpression):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def eval(self, thread):
        return self.op(thread, self.lhs, self.rhs)
