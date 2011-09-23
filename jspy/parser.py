

body ::= stmt EOF | EOF

stmt ::= [statement] | statement
statement ::= 
        expr
    |   for_stmt
    |   while_stmt
    |   with_stmt
    |   do_stmt
    |   if_stmt
    |   try_stmt
    |   continue_stmt
    |   break_stmt
    |   return_stmt

block_body ::= "{" [statement] "}" | statement

for_stmt ::= "for" "(" EXPR ";" EXPR ";" EXPR ")" block_body

while_stmt ::= "while" "(" EXPR ")" block_body

with_stmt ::= "with" "(" EXPR ")" block_body

do_stmt ::= "do" block_body "while" "(" EXPR ")"

if_stmt ::= "if" "(" EXPR ")" block_body |
            "if" "(" EXPR ")" block_body "else" block_body

try_stmt ::= "try" block_body catch_clause

catch_clause ::= "catch" "(" ARG_EXPR ")" block_body
             |   "catch" "(" ARG_EXPR ")" block_body "finally" block_body
             |   "finally" block_body

continue_stmt ::= "continue"
break_stmt ::= "break"
return_stmt ::= "return" expr | "return"

EXPR ::= VALUE
        | expr "." expr
        | expr "[" expr "]"
        | "new" expr
        | expr "(" arglist ")"
        | "++" expr
        | expr "++"
        | "--" expr
        | expr "--"
        | "-" expr
        | "+" expr
        | "~" expr
        | "!" expr
        | "typeof" expr
        | "void" expr
        | "delete" expr
        | expr "*" expr
        | expr "/" expr
        | expr "%" expr
        | expr "+" expr
        | expr "-" expr
        | expr "<<" expr
        | expr ">>" expr
        | expr ">>>" expr
        | expr "<" expr
        | expr "<=" expr
        | expr ">" expr
        | expr ">=" expr
        | expr "in" expr
        | expr "instanceof" expr
        | expr "==" expr
        | expr "!=" expr
        | expr "===" expr
        | expr "!==" expr
        | expr "&" expr
        | expr "^" expr
        | expr "|" expr
        | expr "&&" expr
        | expr "||" expr
        | expr "?" expr ":" expr
        | expr "=" expr
        | expr "+=" expr
        | expr "-=" expr
        | expr "*=" expr
        | expr "/=" expr
        | expr "%=" expr
        | expr "<<=" expr
        | expr ">>=" expr
        | expr ">>>=" expr
        | expr "&=" expr
        | expr "^=" expr
        | expr "|=" expr
        | expr "," expr

VALUE ::= function | regex | number | string | boolean | "undefined" | "null"

function ::= "function" "(" ARG_EXPR_LIST ")" "{" stmts "}"




