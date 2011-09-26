from javascript.expressions.base import Expression

class UnaryExpression(Expression):
    def __init__(self, expr, op):
        self.expr = expr
        self.op = op

    def eval(self, thread, **kwargs):
        return self.op(thread, self.expr, **kwargs)
 
