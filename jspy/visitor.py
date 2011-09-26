from jspy.operators import *
from jspy.expressions import *
from jspy.statement import *
from jspy.tokenizer import Token

unary_operators = {
    '(':        op_passthrough,
    '~':        op_invert,
    '!':        op_not,
    '+':        op_positive,
    '-':        op_negative,
    'typeof':   op_typeof,
    'delete':   op_delete,
    'void':     op_void,
    'new':      op_new,

# missing:
#    '{':        op_new_object,
#    '[':        op_new_array,
#    '---':      op_neg_decr,
#    '+++':      op_pos_incr,
    '++':       op_incr,
    '--':       op_decr,
}

suffix_operators = {
    '++':       op_postincr,
    '--':       op_postdecr,
}

binary_operators = {
    '<<':   op_bitwise_lshift,
    '>>':   op_bitwise_rshift,
    '>>>':  op_bitwise_zrshift,
    '^':    op_bitwise_xor,
    '|':    op_bitwise_or,
    '&':    op_bitwise_and,
    '<':    op_less,
    '<=':   op_less_equal,
    '>':    op_greater,
    '>=':   op_greater_equal,
    '&&':   op_and,
    '||':   op_or,
    '==':   op_equal,
    '===':  op_strict_equal,
    '+':    op_add,
    '-':    op_sub,
    '*':    op_mul,
    '/':    op_div,
    '%':    op_mod,
    '.':    op_lookup,
    '[':    op_dynamic_lookup,
    'in':   op_in,
    '(':    op_call,
    '=':    op_assign,
    '+=':   op_assign_add,
    '-=':   op_assign_sub,
    '*=':   op_assign_mul,
    '/=':   op_assign_div,
    '%=':   op_assign_mod,
    '^=':   op_assign_bitwise_xor,
    '|=':   op_assign_bitwise_or,
    '&=':   op_assign_bitwise_and,
    '>>=':  op_assign_bitwise_rshift,
    '>>>=': op_assign_bitwise_zrshift,
    '<<=':  op_assign_bitwise_lshift,
}

stmt_map = {
    'for':      ForStatement,
    'forin':    ForInStatement,
    'if':       IfStatement,
    'try':      TryStatement,
    'return':   ReturnStatement,
    'break':    BreakStatement,
    'continue': ContinueStatement,
    'throw':    ThrowStatement,
    'while':    WhileStatement,
    'do':       DoWhileStatement,
}


class Visitor(object):
    def __init__(self, statements):
        self.statements = statements

    def run(self):
        return [self.visit(node) for node in self.statements]

    def visit(self, node):
        if isinstance(node, list):
            # it's a var expression, probably.
            return [self.visit(n) for n in node]
        elif node.arity in ['unary', 'binary', 'ternary', 'function']:
            return Statement(self.visit_expression(node), None, None, None)
        elif node.arity == 'statement':
            klass = stmt_map.get(node.id)
            return klass(
                node.first and klass.visit[0] and self.visit(node.first),
                node.second and klass.visit[1] and self.visit(node.second),
                node.third and klass.visit[2] and self.visit(node.third),
                node.fourth and klass.visit[3] and self.visit(node.fourth)
            )

    def visit_expression(self, node, **kwargs):
        if node.arity == 'name':
            return UnaryExpression(node, op_name)
        elif node.arity == 'unary':
            return LiteralExpression(node, lambda:0)
        elif node.arity == 'binary':
            return self.visit_binary_expression(node)
        elif node.arity == 'ternary':
            return self.visit_ternary_expression(node)
        elif node.arity == 'function':
            return self.visit_function_expression(node)
        elif node.arity == 'literal':
            return self.visit_literal_expression(node)
        raise Exception('Visited node with unsupported arity: "%s"' % node.arity)

    def visit_unary_expression(self, node, **kwargs):
        expression_klass = UnaryExpression
        op = None 
        visit_method = self.visit_expression
        if node.id == '{':
            expression_klass = ObjectExpression
            visit_method = self.visit_object_keys
        elif node.id == '[':
            expression_klass = ArrayExpression
            visit_method = self.visit_array_elements
        elif node.arity == 'name':
            expression_klass = LoadExpression
            visit_method = lambda x: x
        else:
            op = unary_operators.get(node.id)
        return expression_klass(visit_method(node.first), op)

    def visit_binary_expression(self, node, **kwargs):
        expression_klass = BinaryExpression
        op = binary_operators.get(node.id)
        visit_method = self.visit_expression
        return expression_klass(visit_method(node.first), node.id == '.' and node.second or visit_method(node.second), op)

    def visit_ternary_expression(self, node, **kwargs):
        return TernaryExpression(
            self.visit_expression(node.first),
            self.visit_expression(node.second),
            self.visit_expression(node.third)
        )

    def visit_literal_expression(self, node, **kwargs):
        return {
            Token.Number:NumberExpression,
            Token.String:StringExpression,
            Token.Boolean:BooleanExpression,
            Token.Undefined:UndefinedExpression,
            Token.Null:NullExpression,
            Token.Regex:RegExpExpression,
        }[node.token.type](node.token.value, lambda:0)

    def visit_function_expression(self, node, **kwargs):
        pass

    def visit_var_expression(self, node, **kwargs):
        pass

