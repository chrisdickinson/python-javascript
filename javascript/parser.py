from javascript.tokenizer import Token

class SymbolClass(object):
    lbp = 0
    value = None
    token = None
    arity = None
    _nud = None
    _led = None
    std = None
    assignment = False
    first = None
    second = None
    third = None
    fourth = None

    def __init__(self, token):
        self.token = token
        self.id = self.value = self.token.value
        self.assignment = getattr(token, 'assignment', False)

    def nud(self):
        raise Exception('nud error in %s (%s)!' % (self.id, repr(self.token)))

    def led(self, left):
        raise Exception('led error in %s (%s)!' % (self.id, repr(self.token)))

class Parser(object):
    BaseSymbol = SymbolClass
    symbols = [':', ';', ',', ')', ']', '}', 'else', '(end)', '(name)', '(literal)']
    exception_class = Exception

    def __init__(self, tokens):
        self.tokens = tokens
        self.max = len(tokens)
        self.token_idx = 0
        self.symbol_table = {}
        self._token = None

    @property
    def token(self):
        return self._token

    def symbol(self, id, bp=0):
        sym = self.symbol_table.get(id, None)
        if sym is not None:
            if bp >= sym.lbp:
                sym.lbp = bp
        else:
            _id = id
            class Symbol(self.BaseSymbol):
                id = _id
                value = _id
                lbp = bp
            sym = Symbol
            self.symbol_table[id] = sym
        return sym

    def advance(self, id=None):
        if id and self.token.value != id:
            raise self.exception_class('Expected ``%s``, got ``%s`` at %s' % (id, self.token.value, repr(self.token.token)))

        t = self.tokens[self.token_idx]
        self.token_idx += 1

        val = t.value
        type = t.type

        if type == Token.Name:
            # if it's a name, give us a parsertoken
            # with lbp of zero and a nud that returns itself
            o = self.symbol_table.get(val, None)
            if o is None:
                o = self.BaseSymbol(t)
                o.nud = lambda *a : o
            else:
                o = o(t)
        elif type == Token.Operator:
            o = self.symbol_table.get(val, None)
            if not o:
                raise self.exception_class('Unsupported operator ``%s`` at %s' % (val, repr(t)))
            else:
                o = o(t)
        elif type in Token.LITERALS:
            type = 'literal'
            o = self.symbol_table.get('(literal)')
            if o:
                o = o(t)
            else:
                o = self.BaseSymbol(t)
        elif type == Token.EOF:
            type = '(end)'
            o = self.symbol_table.get('(end)')
            o = o(t)
        else:
            raise Exception
        token = o
        token.value = val
        token.arity = type

        self._token = token 
        return token

    def expression(self, rbp):
        left = None
        t = self.token
        self.advance()

        if t.id == ';':
            self.token_idx -= 2 
            self.advance()
            return self.symbol_table.get('(noop)')(t)

        left = t.nud()

        while rbp < self.token.lbp:
            t = self.token
            self.advance()
            left = t.led(left)

        return left

    def assignment(self, id):

        def assign_led(tk, left):
            if left.value not in ['.', '['] and left.arity != 'name':
                raise Exception('Bad lvalue.')
            tk.first = left
            tk.second = self.expression(9)
            tk.assignment = True
            tk.arity = "binary"
            return tk 

        return self.infix_right(id, 10, assign_led)

    def constant(self, sym, val):
        x = self.symbol(sym)

        def constant_nud(tk):
            # scope.reserve(this)
            tk.value = self.symbol_table[tk.id].value
            tk.arity = 'literal'
            return tk

        x.value = val
        x.nud = constant_nud
        return x

    def statement(self, check_advance=True):
        n = self.token

        if n.std:
            self.advance()
            # scope.reserve(n)
            return n.std(check_advance)

        v = self.expression(0)

        if check_advance:
            self.advance(';')
        return v

    def statements(self):
        stmts = []
        while True:
            if self.token.id == '}' or self.token.token.type == Token.EOF:
                break
            s = self.statement()
            if s:
                stmts.append(s)
        return stmts

    def stmt(self, id, fn):
        x = self.symbol(id)
        x.std = fn
        return x

    def block(self, check_advance=True):
        t = self.token
        if t.id == '{':
            self.advance('{')
        elif t.id in ['return', 'throw', 'break', 'continue']:
            self.advance()
            return t.std(check_advance)
        else:
            expr = self.expression(9)
            return expr
        return t.std(check_advance)

    def infix(self, id, bp, led=None):
        s = self.symbol(id, bp)

        def base_led(tk, left):
            tk.first = left
            tk.second = self.expression(bp)
            tk.arity = 'binary'
            return tk

        s.led = led or base_led
        return s

    def infix_right(self, id, bp, led=None):
        s = self.symbol(id, bp)

        def base_led(tk, left):
            tk.first = left
            tk.second = self.expression(bp - 1)
            tk.arity = 'binary'
            return tk

        s.led = led or base_led
        return s

    def prefix(self, id, nud=None, bp=None):
        s = self.symbol(id, bp)

        def base_nud(tk):
            tk.first = self.expression(70)
            tk.arity = 'unary'
            return tk

        s.nud = nud or base_nud
        return s

    def suffix(self, id, led=None):
        s = self.symbol(id, 150)
        
        def base_led(tk, left):
            tk.first = left
            tk.arity = 'suffix'
            return tk

        s.led = led or base_led
        return s

    def setup_parser(self):
        def infix_ternary(tk, left):
            tk.first = left
            tk.second = self.expression(0)
            self.advance(':')
            tk.third = self.expression(0)
            tk.arity = 'ternary'
            return tk

        def infix_lookup(tk, left):
            tk.first = left
            if self.token.arity != 'name':
                raise Exception('Expected a property name.')
            self.token.arity = "literal"
            tk.second = self.token
            tk.arity = "binary"
            self.advance()
            return tk

        def infix_dynamic_lookup(tk, left):
            tk.first = left
            tk.second = self.expression(0)
            tk.arity = 'binary'
            self.advance(']')
            return tk

        def infix_call(tk, left):
            a = []
            tk.arity = 'binary'
            tk.first = left
            tk.second = a

            if self.token.id != ')':
                while True:
                    a.append(self.expression(0))
                    if self.token.id != ',':
                        break
                    self.advance(',')
            self.advance(')')
            return tk

        def prefix_paren(tk):
            e = self.expression(0)
            self.advance(')')
            return e

        def prefix_function(tk):
            a = []
            if self.token.arity == 'name':
                tk.name = self.token.value
                self.advance()
            self.advance('(')
            if self.token.id != ')':
                while True:
                    if self.token.arity != 'name':
                        raise Exception('Expected a parameter name')
                    a.append(self.token.value)
                    self.advance()
                    if self.token.id != ',':
                        break
                    self.advance(',')
            tk.first = a
            self.advance(')')
            self.advance('{')
            tk.second = self.statements()
            self.advance('}')
            tk.arity = 'function'
            return tk

        def prefix_array(tk):
            a = []
            if self.token.id != ']':
                while True:
                    a.append(self.expression(0))
                    if self.token.id != ',':
                        break
                    self.advance(',')
            self.advance(']')
            tk.first = a
            tk.arity = 'unary'
            return tk

        def prefix_object(tk):
            a = []
            if self.token.id != '}':
                while True:
                    n = self.token
                    if n.arity not in ['name', 'literal']:
                        raise Exception('Bad key')
                    self.advance()
                    self.advance(':')
                    v = self.expression(0)
                    v.key = n.value
                    a.append(v)
                    if self.token.id != ',':
                        break
                    self.advance(',')
            self.advance('}')
            tk.first = a
            tk.arity = 'unary'
            return tk

        def stmt_block(tk, check_advance=True):
            a = self.statements()
            self.advance('}')
            return a

        def stmt_var(tk, check_advance):

            a = []
            while True:
                n = self.token

                if n.arity != 'name':
                    raise Exception('Expected a new variable name')
                # scope.define
                self.advance()
                if self.token.id == '=':
                    t = self.token
                    self.advance('=')
                    t.first = n
                    t.second = self.expression(0)
                    t.arity = 'binary'
                    a.append(t)
                elif self.token.id == 'in':
                    t = self.token
                    self.advance('in')
                    t.first = n
                    t.second = self.expression(0)
                    a.append(t)

                if self.token.id != ',':
                    break
                self.advance(",")

            if check_advance:
                self.advance(';')
            return a

        def stmt_while(tk, check_advance):
            self.advance('(')
            tk.first = self.expression(0)
            self.advance(')')
            tk.second = self.block()
            tk.arity = 'statement'
            return tk

        def stmt_if(tk, check_advance):
            self.advance('(')
            tk.first = self.expression(0)
            self.advance(')')
            tk.second = self.block()
            if self.token.id == 'else':
                # scope.reserve(self.token)
                self.advance('else')
                tk.third = (self.token.id == 'if' and [self.statement()] or [self.block()])[0]
            else:
                tk.third = None
            tk.arity = 'statement'
            return tk 

        def stmt_for(tk, check_advance):
            self.advance('(')
            tk.first = self.statement(False)
            tk.arity = 'statement'
            if self.token.id == ';':
                self.advance(';')
                tk.second = self.statement()
                tk.third = self.statement(False)
                self.advance(')')
                tk.fourth = self.block()
            elif self.token.id == ')':
                self.advance(')')
                tk.second = self.block()
                tk.id = 'forin'
            else:
                raise self.exception_class('Expected ``)`` or ``;`` in %s, got ``%s``' % (repr(self.token.token), self.token.id))
            return tk

        def stmt_do(tk, check_advance):
            tk.first = self.block()
            self.advance('while')
            self.advance('(')
            tk.second = self.expression(0)
            self.advance(')')
            tk.arity = 'statement'
            return tk

        def stmt_try(tk, check_advance):
            tk.first = self.block()
            if self.token.id == 'catch':
                self.advance('catch')
                self.advance('(')
                tk.second = self.token
                self.advance()
                self.advance(')') 
                tk.third = self.block()

            if self.token.id == 'finally':
                self.advance('finally')
                tk.fourth = self.block()
            tk.arity = 'statement'
            return tk

        def stmt_break(tk, check_advance):
            self.advance(';')
            tk.arity = 'statement'
            return tk

        def stmt_return(tk, check_advance):
            if self.token.id != ';':
                tk.first = self.expression(0)
            self.advance(';')
            tk.arity = 'statement'
            return tk

        self.stmt('var', stmt_var)
        self.stmt('while', stmt_while)
        self.stmt('if', stmt_if)
        self.stmt('for', stmt_for)
        self.stmt('break', stmt_break)
        self.stmt('continue', stmt_break)
        self.stmt('return', stmt_return)
        self.stmt('throw', stmt_return)
        self.stmt('try', stmt_try)
        self.stmt('do', stmt_do)
        self.stmt('{', stmt_block)

        self.infix_right('&&', 30)
        self.infix_right('||', 30)
        self.infix("?", 20, infix_ternary)
        self.infix("instanceof", 40)
        self.infix("in", 40)
        self.infix('&', 40)
        self.infix('^', 40)
        self.infix('|', 40)
        self.infix("===", 40)
        self.infix("!==", 40)
        self.infix("<", 40)
        self.infix("<=", 40)
        self.infix(">", 40)
        self.infix(">=", 40)
        self.infix('+', 50)
        self.infix('-', 50)
        self.infix('---', 45)
        self.infix('+++', 45)
        self.infix('*', 60)
        self.infix('/', 60)
        self.infix('%', 60)
        self.infix('.', 80, infix_lookup)
        self.infix('[', 80, infix_dynamic_lookup)
        self.infix('(', 80, infix_call)
        self.prefix('++')
        self.prefix('+')
        self.prefix('--')
        self.prefix('-')
        self.prefix('~')
        self.prefix('!')
        self.prefix('(', prefix_paren)
        self.prefix('{', prefix_object)
        self.prefix('[', prefix_array)
        self.prefix('function', prefix_function)
        self.prefix('typeof')
        self.prefix('void')
        self.prefix('new')
        self.prefix('delete')
        self.assignment('=')
        self.assignment('&=')
        self.assignment('^=')
        self.assignment('|=')
        self.assignment('>>=')
        self.assignment('>>>=')
        self.assignment('<<=')
        self.assignment('+=')
        self.assignment('-=')
        self.assignment('*=')
        self.assignment('/=')
        self.assignment('%=')

        self.suffix('++')
        self.suffix('--')

        Null = object()
        Undefined = object()
        # not sure if this is a good idea:
        self.constant('true', True)
        self.constant('false', False)
        self.constant('null', Null)
        self.constant('undefined', Undefined)

        self.symbol('(noop)')
        x = self.symbol('(literal)')
        x.nud = lambda self : self
        
    def setup_symbols(self):
        [self.symbol(i) for i in self.symbols]    

    def parse(self):
        self.setup_symbols()
        self.setup_parser()

        self.advance()
        s = self.statements()
        return s

def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()
