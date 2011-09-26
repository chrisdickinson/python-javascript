Continue = object()
Break = object() 

class Return(Exception):
    def __init__(self, val):
        self.value = val

class Statement(object):
    visit = (True, True, True, True)

    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

    def eval(self, thread, **kwargs):
        return self.first.eval(thread)

class IfStatement(Statement):
    def eval(self, thread):
        val = self.first.eval(thread)
        if val.js_bool():
            [thread.eval(statement) for statement in self.second]
        elif self.third:
            [thread.eval(statement) for statement in self.third]

class ForStatement(Statement):
    def eval(self, thread):
        self.first.eval(thread)

        predicate = self.second.eval(thread).js_bool()
        while predicate:
            for statement in self.fourth:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            self.third.eval(thread)
            predicate = predicate and self.second.eval(thread).js_bool()

class ForInStatement(Statement):
    visit = (False, True, True, True)

    def eval(self, thread):
        pass

class TryStatement(Statement):
    visit = (True, False, True, True)

    def eval(self, thread):
        retval = None
        try:
            for statement in self.first:
                thread.eval(statement)
        except RuntimeError, e:
            thread.context().sub()
            thread.context().js_set_property(self.second.id, e.what)
            for statement in self.third:
                thread.eval(statement)
        except Return, ret:
            retval = ret

        if self.fourth:
            for statement in self.fourth:
                thread.eval(statement)
            if retval:
                raise retval

class WhileStatement(Statement):
    def eval(self, thread):
        predicate = self.first.eval(thread).js_bool() 
        while predicate:
            for statement in self.second:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            predicate = predicate and self.first.eval(thread).js_bool()

class DoWhileStatement(WhileStatement):
    def eval(self, thread):
        predicate = True
        while predicate:
            for statement in self.first:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            predicate = predicate and self.second.eval(thread).js_bool()

# this doesn't work:
class SwitchStatement(Statement):
    def eval(self, thread):
        val = self.expr.eval(thread).js_unbox(thread)
        matched = False
        try:
            for expr, code in self.cases:
                if expr.eval(thread).js_unbox(thread).value == val.value or matched:
                    matched = True
                    for statement in code:
                        thread.eval(statement)
        except Break:
            pass

        if not matched and self.default_case is not None:
            try:
                for expr, code in self.default_case:
                    for statement in code:
                        thread.eval(statement)
            except Break:
                pass

class BreakStatement(Statement):
    def __init__(self):
        pass

    def eval(self, thread):
        raise Break

class ContinueStatement(Statement):
    def __init__(self):
        pass

    def eval(self, thread):
        raise Continue 

class ThrowStatement(Statement):
    def eval(self, thread):
        thread.throw(self.first.eval(thread))

class ReturnStatement(Statement):
    def eval(self, thread):
        if self.first:
            raise Return(self.first.eval(thread))
        raise Return(thread.cons.undefined())
