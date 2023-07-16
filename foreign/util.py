from types import FunctionType, BuiltinFunctionType

from corefn.abs import Foreign, Native1, Native2
from corefn.literals import String
from rpython.rlib.objectmodel import not_rpython


@not_rpython
def to_foreign(value):
    t = type(value)
    if t == str:
        return String(value)
    elif t in [FunctionType, BuiltinFunctionType]:
        arguments = value.func_code.co_argcount
        if arguments == 1:
            raise TypeError("expected at least the 2 arguments a interpreter and a expression")
        elif arguments == 2:
            return Native1(value)
        elif arguments == 3:
            return Native2(value)
        else:
            NotImplementedError("dont support %s number of arguments" % arguments)
    else:
        NotImplementedError("cant translate %r of type %r" % (value, t))


