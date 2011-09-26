from jspy.expressions.base import BaseExpression

class UnaryExpression(BaseExpression):
    def __init__(self, token, expr, op):
        self.token = token
        self.expr = expr
        self.op = op

    def eval(self, thread, **kwargs):
        return self.op(thread, self.expr, **kwargs)
 
