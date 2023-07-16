from types import FunctionType, BuiltinFunctionType

from corefn.abs import Foreign, ForeignUsingInterpreter
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
            return Foreign(value.func_code.co_name, lambda x: value(x))
        elif arguments == 2:
            return Foreign(value.func_code.co_name,
                lambda x: Foreign(
                    "%s (%s)" % (value.func_code.co_name, x.__repr__()),
                    lambda y: value(x, y)
              )
            )
        elif arguments == 3:
            return Foreign(
                value.func_code.co_name,
                lambda x: Foreign(
                    "%s (%s)" % (value.func_code.co_name, x.__repr__()),
                    lambda y: Foreign(
                    "%s (%s) (%s)" % (value.func_code.co_name, x.__repr__(), y.__repr__()),
                        lambda z: value(x, y, z)
                    )
                )
            )
        else:
            NotImplementedError("dont support %s number of arguments" % arguments)
    else:
        NotImplementedError("cant translate %r of type %r" % (value, t))


def with_interpreter(f):
    return ForeignUsingInterpreter(f)
