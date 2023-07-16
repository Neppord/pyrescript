from corefn.expression import Expression

"""
Abs aka Lambda, Callable etc.

Represents a mapping between two values of type Expr. A function that takes 
more then one argument is represented by nesting multiple Abs, one returning
 the other

"""


class AbsInterface(Expression):

    def call_abs(self, interpreter, expression):
        """
        :param interpreter:
        :type expression: Expression
        :rtype: Expression
        """
        raise NotImplementedError("Should return expr")


class Abs(AbsInterface):
    def __init__(self, argument, body):
        self.argument = argument
        self.body = body

    def eval(self, interpreter, frame):
        return AbsWithFrame(self, frame)

    def call_abs(self, interpreter, expression):
        return AbsWithFrame(self, {}).call_abs(interpreter, expression)

    def __repr__(self):
        argument = self.argument
        body = self.body.__repr__()
        return "\\" + argument + " -> " + body


class AbsWithFrame(AbsInterface):

    def __init__(self, abs, frame):
        self.abs = abs
        self.frame = frame

    def call_abs(self, interpreter, expression):
        new_frame = {}
        new_frame.update(self.frame)
        new_frame[self.abs.argument] = expression
        return self.abs.body.eval(interpreter, new_frame)

    def eval(self, interpreter, frame):
        return self

    def __repr__(self):
        body_repr = self.abs.body.__repr__()
        if self.frame:
            frame_repr = "; ".join([k + " = " + v.__repr__() for k, v in self.frame.items()])
            return "\\" + self.abs.argument + " -> let " + frame_repr + " in " + body_repr
        else:
            return "\\" + self.abs.argument + " -> " + body_repr


class Foreign(AbsInterface):
    def __init__(self, repr_, function):
        self.repr = repr_
        self.function = function

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        ret = self.function(expression)
        assert isinstance(ret, Expression)
        return ret

    def __repr__(self):
        return self.repr


class Native1(AbsInterface):
    def __init__(self, native):
        self.native = native

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return self.native(interpreter, expression)

    def __repr__(self):
        return "<placeholder>"


class BoundNative1(Expression):
    def __init__(self, native, bound):
        self.bound = bound
        self.native = native

    def eval(self, interpreter, frame):
        return self.native(interpreter, self.bound)

    def __repr__(self):
        return "<placeholder>"


class Native2(AbsInterface):
    def __init__(self, native):
        self.native = native

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return BoundNative2(self.native, expression)

    def __repr__(self):
        return "<placeholder>"


class BoundNative2(AbsInterface):
    def __init__(self, native, bound):
        self.native = native
        self.bound = bound

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return self.native(interpreter, self.bound, expression)

    def __repr__(self):
        return "<placeholder>"


class Native3(AbsInterface):
    def __init__(self, native):
        self.native = native

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return BoundNative2(self.native, expression)

    def __repr__(self):
        return "<placeholder>"


class BoundNative3(AbsInterface):
    def __init__(self, native, bound):
        self.native = native
        self.bound = bound

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return BoundBoundNative3(self.native, self.bound, expression)

    def __repr__(self):
        return "<placeholder>"


class BoundBoundNative3(AbsInterface):
    def __init__(self, native, bound1, bound2):
        self.native = native
        self.bound1 = bound1
        self.bound2 = bound2

    def eval(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        return self.native(interpreter, self.bound1, self.bound2, expression)

    def __repr__(self):
        return "<placeholder>"


class Dynamic(Expression):

    def __init__(self, function):
        self.function = function

    def eval(self, interpreter, frame):
        return self.function(interpreter)

    def __repr__(self):
        return "<dynamic>"
