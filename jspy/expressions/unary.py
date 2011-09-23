from jspy.expressions.base import BaseExpression

class UnaryExpression(BaseExpression):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op

    def eval(self, thread):
        return self.op(thread, self.expr)
 
