from jspy.expressions.base import Expression

class TernaryExpression(Expression):
    def eval(self, thread, **kwargs):
        if self.first.eval(thread).js_bool():
            return self.second.eval(thread)
        return self.third.eval(thread)
