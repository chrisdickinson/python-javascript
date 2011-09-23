Continue = object()
Break = object() 

class Return(object):
    def __init__(value):
        self.value = value

class Statement(object):
    def __init__(self, root_expr):
        self.root_expr = root_expr

    def eval(self, thread):
        self.root_expr.eval(thread)

class IfStatement(object):
    def __init__(self, root_expr, positive_list, negative_list):
        self.root_expr = root_expr
        self.positive_list = positive_list
        self.negative_list = negative_list

    def eval(self, thread):
        val = self.root_expr.eval(thread)
        if val.js_bool():
            for statement in self.positive_list:
                thread.eval(statement)
        else:
            for statement in self.negative_list:
                thread.eval(statement)

class ForLoop(object):
    def __init__(self, init_expr, test_expr, post_expr, loop_list):
        self.init_expr = init_expr
        self.test_expr = test_expr
        self.post_expr = post_expr
        self.loop_list = loop_list

    def eval(self, thread):
        self.init_expr.eval(thread)

        predicate = self.test_expr.eval(thread).js_bool()
        while predicate:
            for statement in self.loop_list:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            predicate = predicate and self.test_expr.eval(thread).js_bool()

class WhileLoop(object):
    def __init__(self, root_expr, loop_list):
        self.root_expr = root_expr
        self.loop_list = loop_list

    def eval(self, thread):
        predicate = self.test_expr.eval(thread).js_bool() 
        while predicate:
            for statement in self.loop_list:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            predicate = predicate and self.test_expr.eval(thread).js_bool()

class DoWhileLoop(WhileLoop):
    def eval(self, thread):
        predicate = True
        while predicate:
            for statement in self.loop_list:
                try:
                    thread.eval(statement)
                except Continue:
                    break
                except Break:
                    predicate = False
                    break
            predicate = predicate and self.test_expr.eval(thread).js_bool()

class SwitchStatement(object):
    def __init__(self, expr, cases):
        self.expr = expr
        self.cases = cases
        self.default_case = None
        for idx, data in enumerate(self.cases):
            expr, code = data
            if expr is None:
                self.default_case = self.cases[idx:]
                break
 
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

class BreakStatement(object):
    def __init__(self):
        pass

    def eval(self, thread):
        raise Break

class ContinueStatement(object):
    def __init__(self):
        pass

    def eval(self, thread):
        raise Continue 

class ThrowStatement(object):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, thread):
        thread.throw(self.expr.eval(thread))

class ReturnStatement(object):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, thread):
        if self.expr:
            raise Return(self.expr.eval(thread))
        raise Return(thread.cons.undefined())

class CatchStatement(object):
    def __init__(self, catch_expr, catch_list):
        self.catch_expr = catch_expr
        self.catch_list = catch_list

    def eval(self, thread):
        pass

class TryStatement(object):
    def __init__(self, try_list, catch_stmt, finally_list):
        pass

  
