
ASSIGNMENT = True
"""
~
!
<<
>>
>>>
&
|
^
||
&&
%
*
/
-
+
=
"""

# bitwise operators

def op_invert(thread, rhs, **kwargs):
    """
        expr: ~a
    """
    rhs = rhs.eval(thread).js_unbox(thread)
    if thread.typeof(rhs) == 'number':
        return thread.cons.number(~int(rhs.value))
    return thread.cons.number('NaN')

def op_bitwise_lshift(thread, lhs, rhs, **kwargs):
    """
        expr: a << b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = 0

    if thread.typeof(rhs) == 'string':
        rhs = 0

    return thread.cons.number(int(lhs.value) << int(rhs.value))

def op_bitwise_rshift(thread, lhs, rhs, **kwargs):
    """
        expr: a >> b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = thread.cons.number(0) 

    if thread.typeof(rhs) == 'string':
        rhs = thread.cons.number(0) 

    return thread.cons.number(int(lhs.value) >> int(rhs.value))

def op_bitwise_zrshift(thread, lhs, rhs, **kwargs):
    """
        expr: a >>> b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = thread.cons.number(0) 

    if thread.typeof(rhs) == 'string':
        rhs = thread.cons.number(0)
 
    return thread.cons.number((int(lhs.value) & 0xFFFFFFFFL) >> int(rhs.value))

def op_bitwise_xor(thread, lhs, rhs, **kwargs):
    """
        expr: a ^ b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = thread.cons.number(0) 

    if thread.typeof(rhs) == 'string':
        rhs = thread.cons.number(0)

    return thread.cons.number(int(lhs.value) ^ int(rhs.value))

def op_bitwise_or(thread, lhs, rhs, **kwargs):
    """
        expr: a | b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = thread.cons.number(0) 

    if thread.typeof(rhs) == 'string':
        rhs = thread.cons.number(0)

    return thread.cons.number(int(lhs.value) & int(rhs.value))

def op_bitwise_and(thread, lhs, rhs, **kwargs):
    """
        expr: a & b
    """
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)

    if thread.typeof(lhs) == 'string':
        lhs = thread.cons.number(0) 

    if thread.typeof(rhs) == 'string':
        rhs = thread.cons.number(0)

    return thread.cons.number(int(lhs.value) & int(rhs.value))

# boolean
 
def op_not(thread, rhs, **kwargs):
    """
        expr: !a
    """
    rhs = rhs.eval(thread)
    return thread.cons.boolean(not rhs.js_bool())

def op_less(thread, lhs, rhs, **kwargs):
    return thread.cons.boolean(lhs.eval(thread).js_unbox(thread) < rhs.eval(thread).js_unbox(thread))

def op_less_equal(thread, lhs, rhs, **kwargs):
    return thread.cons.boolean(lhs.eval(thread).js_unbox(thread) <= rhs.eval(thread).js_unbox(thread))

def op_greater(thread, lhs, rhs, **kwargs):
    return thread.cons.boolean(lhs.eval(thread).js_unbox(thread) > rhs.eval(thread).js_unbox(thread))

def op_greater_equal(thread, lhs, rhs, **kwargs):
    return thread.cons.boolean(lhs.eval(thread).js_unbox(thread) >= rhs.eval(thread).js_unbox(thread))

def op_and(thread, lhs, rhs, **kwargs):
    """
        expr: a && b
    """
    lhs = lhs.eval(thread)
    if lhs.js_bool():
        return rhs.eval(thread)
    return lhs
    
def op_or(thread, lhs, rhs, **kwargs):
    """
        expr: a || b
    """
    lhs = lhs.eval(thread)
    if lhs.js_bool():
        return lhs
    return rhs.eval(thread)

def op_equal(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    return thread.cons.boolean(lhs.value == rhs.value)

def op_strict_equal(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread), rhs.eval(thread)
    lhs_is_obj = thread.typeof(lhs) == 'object'
    rhs_is_obj = thread.typeof(rhs) == 'object'

    if lhs_is_obj and rhs_is_obj:
        return thread.cons.boolean(lhs is rhs)

    if lhs_is_obj or rhs_is_obj:
        return thread.cons.boolean(False)

    return thread.cons.boolean(lhs.js_unbox(thread).value == rhs.js_unbox(thread).value)

# mathe-magical!

# + - * / %

def op_add(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string' or thread.typeof(rhs) == 'string':
        return thread.cons.string(str(lhs) + str(rhs)) 

    return thread.cons.number(lhs.value + rhs.value)

def op_sub(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string' or thread.typeof(rhs) == 'string':
        return thread.cons.number('NaN') 
    return thread.cons.number(lhs.value - rhs.value)

def op_mul(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string' or thread.typeof(rhs) == 'string':
        return thread.cons.number('NaN') 
    return thread.cons.number(lhs.value * rhs.value)

def op_div(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string' or thread.typeof(rhs) == 'string':
        return thread.cons.number('NaN')

    try: 
        return thread.cons.number(lhs.value / rhs.value)
    except ZeroDivisionError:
        return thread.cons.number('Infinity')

def op_mod(thread, lhs, rhs, **kwargs):
    lhs, rhs = lhs.eval(thread).js_unbox(thread), rhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string' or thread.typeof(rhs) == 'string':
        return thread.cons.number('NaN')

    try: 
        return thread.cons.number(lhs.value % rhs.value)
    except ZeroDivisionError:
        return thread.cons.number('NaN')

def op_typeof(thread, rhs, **kwargs):
    return thread.cons.string(thread.typeof(rhs.eval(thread)))

def op_delete(thread, rhs, **kwargs):
    obj, prop = rhs.eval(thread)
    can_delete = obj and prop and obj.has(prop)
    if can_delete:
        obj.delete(prop)
    return thread.cons.boolean(can_delete)

def op_void(thread, rhs, **kwargs):
    rhs.eval(thread)
    return thread.cons.undefined()

def op_lookup(thread, lhs, rhs, is_assign=False):
    obj = lhs.eval(thread).js_box(thread)
    key = str(rhs)
    prop = obj.js_get_property(thread, key, is_assign)
    if prop is None and is_assign:
        return obj.js_set_property(thread, key, thread.cons.undefined())
    else:
        return thread.cons.undefined()
    return prop

def op_dynamic_lookup(thread, lhs, rhs, is_assign=False):
    obj = lhs.eval(thread).js_box(thread)
    key = str(rhs.eval(thread).js_unbox(thread))
    prop = obj.js_get_property(thread, key, is_assign)
    if prop is None and is_assign:
        return obj.js_set_property(thread, key, thread.cons.undefined())
    else:
        return thread.cons.undefined()
    return prop

def op_in(thread, lhs, rhs, **kwargs):
    lhs = str(lhs.eval(thread).js_unbox(thread))
    rhs = rhs.eval(thread).js_box(thread)
    if rhs.js_get_property(thread, lhs, ASSIGNMENT) is not None:
        return thread.cons.boolean(True)
    return thread.cons.boolean(False)

def op_call(thread, lhs, rhs, **kwargs):
    fn = lhs.eval(thread)
    on = getattr(fn, 'target', None)
    args = [bit.eval(thread) for bit in rhs]
    return fn.js_execute(thread, on, args)  

def op_new(thread, lhs, rhs, **kwargs):
    fn = lhs.eval(thread).js_box(thread)
    on = JSObject(fn.js_get_property(thread, 'prototype').js_box(thread))
    args = [bit.eval(thread) for bit in rhs]
    return fn.js_execute(thread, on, args)  

def op_incr(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string':
        val = thread.cons.number('NaN')
    else:
        val = thread.cons.number(lhs.value + 1) 

    prop = lhs.eval(thread, ASSIGNMENT)
    return prop.js_set(thread, val)

def op_postdecr(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    original = lhs.value
    if thread.typeof(lhs) == 'string':
        original = 'NaN'
        val = thread.cons.number('NaN')
    else:
        val = thread.cons.number(lhs.value - 1) 

    prop = lhs.eval(thread, ASSIGNMENT)
    prop.js_set(thread, val)
    return thread.cons.number(original)

def op_postincr(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    original = lhs.value
    if thread.typeof(lhs) == 'string':
        original = 'NaN'
        val = thread.cons.number('NaN')
    else:
        val = thread.cons.number(lhs.value + 1) 

    prop = lhs.eval(thread, ASSIGNMENT)
    prop.js_set(thread, val)
    return thread.cons.number(original)

def op_decr(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string':
        val = thread.cons.number('NaN')
    else:
        val = thread.cons.number(lhs.value - 1) 

    prop = lhs.eval(thread, ASSIGNMENT)
    return prop.js_set(thread, val)

def op_positive(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string':
        return thread.cons.number('NaN')
    return thread.cons.number(lhs.value * 1) 

def op_negative(thread, lhs, **kwargs):
    lhs = lhs.eval(thread).js_unbox(thread)
    if thread.typeof(lhs) == 'string':
        return thread.cons.number('NaN')
    return thread.cons.number(lhs.value * -1) 

def op_passthrough(thread, lhs, **kwargs):
    return lhs.eval(thread)

# ugh, the assignment operator.

def op_name(thread, lhs, is_assign=False):
    name = str(lhs.id)
    return thread.context().js_get_property(thread, name, is_assign)

def op_assign(thread, lhs, rhs, **kwargs):
    if not hasattr(lhs, 'op') or lhs.op not in [op_name, op_lookup, op_dynamic_lookup]:
        return thread.throw(
            thread.cons.object('ReferenceError',
                thread.cons.string('Invalid left-hand side in assignment')
            )
        )

    prop = lhs.eval(thread, ASSIGNMENT)
    val = rhs.eval(thread)
    return prop.js_set(thread, val)


def create_assigner(op):
    def op_assign_add(thread, lhs, rhs, **kwargs):
        val = op(thread, lhs, rhs, **kwargs)

        if not hasattr(lhs, 'op') or lhs.op not in [op_name, op_lookup, op_dynamic_lookup]:
            return thread.throw(
                thread.cons.object('ReferenceError',
                    thread.cons.string('Invalid left-hand side in assignment')
                )
            )

        prop = lhs.eval(thread, ASSIGNMENT)
        return prop.js_set(thread, val)

op_assign_add = create_assigner(op_add)
op_assign_sub = create_assigner(op_sub)
op_assign_mul = create_assigner(op_mul)
op_assign_div  = create_assigner(op_div)
op_assign_mod = create_assigner(op_mod)
op_assign_bitwise_xor  = create_assigner(op_bitwise_xor)
op_assign_bitwise_or = create_assigner(op_bitwise_or)
op_assign_bitwise_and = create_assigner(op_bitwise_and)
op_assign_bitwise_lshift = create_assigner(op_bitwise_lshift)
op_assign_bitwise_rshift = create_assigner(op_bitwise_rshift)
op_assign_bitwise_zrshift = create_assigner(op_bitwise_zrshift)

