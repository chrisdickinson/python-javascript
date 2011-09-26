from javascript.expressions.base import Expression
from javascript.expressions.unary import UnaryExpression

class LoadExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.context().js_get_property(thread, self.expr.id)

class LiteralExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return self.expr.id

class DefinitionExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        context = thread.context()
        val = context.js_set_property(thread, self.expr.id, thread.cons.undefined())
        return val

class NumberExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.number(self.expr)

class StringExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.string(self.expr)

class BooleanExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.bool(self.expr)

class NullExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.null()

class UndefinedExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.undefined()

class ArrayExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return thread.cons.object('Array', *[expr.eval(thread) for expr in self.expressions])

class ObjectExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        obj = thread.cons.object('Object')
        for key, val_expr in self.expr:
            val = val_expr.eval(thread)
            obj.define_property(key, val)
        return obj

class RegExpExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        source = self.token.source[1:source.rindex('/')]
        flags = self.token.replace('/%s/' % source, '')

        obj = thread.cons.object(
            'RegExp',
            thread.cons.string(source),
            thread.cons.string(flags)
        )
        return obj

class FunctionExpression(Expression):
    def __init__(self, first, second, name):
        self.arguments = first
        self.body = second
        self.name = name

    def eval(self, thread, **kwargs):
        ctxt = thread.context().sub()
        return thread.cons.function(self.body, ctxt, self.arguments, self.name)         

class LiteralExpression(UnaryExpression):
    def eval(self, thread, **kwargs):
        return self.expr.id

