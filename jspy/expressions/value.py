from jspy.expressions.base import BaseExpression

class NumberExpression(BaseExpression):
    def __init__(self, token):
        self.token = token

    def eval(self, thread):
        return thread.cons.number(self.token)

class StringExpression(BaseExpression):
    def __init__(self, token):
        self.token = token

    def eval(self, thread):
        return thread.cons.string(self.token)

class BooleanExpression(BaseExpression):
    def __init__(self, token):
        self.token = token

    def eval(self, thread):
        return thread.cons.bool(self.token)

class NullExpression(BaseExpression):
    def eval(self, thread):
        return thread.cons.null()

class UndefinedExpression(BaseExpression):
    def eval(self, thread):
        return thread.cons.undefined()

class ArrayExpression(BaseExpression):
    def __init__(self, expressions):
        self.expressions = expressions

    def eval(self, thread):
        return thread.cons.object('Array', *[expr.eval(thread) for expr in self.expressions])

class ObjectExpression(BaseExpression):
    def __init__(self, exprs):
        self.exprs = exprs

    def eval(self, thread):
        obj = thread.cons.object('Object')
        for key_expr, val_expr in self.exprs:
            key = str(key_expr.eval(thread).js_unbox())
            val = val_expr.eval(thread)
            obj.js_set(thread, key, val)
        return obj

class RegExpExpression(BaseExpression):
    def __init__(self, source, flags):
        self.source = source
        self.flags = flags

    def eval(self, thread):
        obj = thread.cons.object(
            'RegExp',
            thread.cons.string(self.source),
            thread.cons.string(self.flags)
        )
        return obj

class FunctionExpression(BaseExpression):
    def __init__(self, args, body, name=None):
        self.name = name
        self.args = args
        self.body = body

    def eval(self, thread):
        ctxt = thread.context().sub()
        stmts = thread.parser.parse(self.body)
        return thread.cons.function(stmts, ctxt, self.args, self.name)         


