from corefn.expression import Expression
from corefn.literals import Bound

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

    def interpret(self, interpreter, frame):
        return AbsWithFrame(self, frame)

    def call_abs(self, interpreter, expression):
        return AbsWithFrame(self, {}).call_abs(interpreter, expression)

    def __repr__(self):
        argument = self.argument
        body = self.body.__repr__()
        return "\\" + argument + " -> " + body


class Foreign(AbsInterface):
    def __init__(self, repr_, function):
        self.repr = repr_
        self.function = function

    def interpret(self, interpreter, frame):
        return self

    def call_abs(self, interpreter, expression):
        ret = self.function(expression)
        assert isinstance(ret, Expression)
        return ret

    def __repr__(self):
        return self.repr

class AbsWithFrame(AbsInterface):

    def __init__(self, abs, frame):
        self.abs = abs
        self.frame = frame

    def call_abs(self, interpreter, expression):
        new_frame = {}
        new_frame.update(self.frame)
        new_frame[self.abs.argument] = expression
        return self.abs.body.interpret(interpreter, new_frame)

    def interpret(self, interpreter, frame):
        return self

    def __repr__(self):
        body_repr = self.abs.body.__repr__()
        if self.frame:
            frame_repr = "; ".join([k + " = " + v.__repr__() for k, v in self.frame.items()])
            return "\\" + self.abs.argument + " -> let " + frame_repr + " in " + body_repr
        else:
            return "\\" + self.abs.argument + " -> " + body_repr


class Dynamic(Expression):

    def __init__(self, function):
        self.function = function

    def interpret(self, interpreter, frame):
        return self.function(interpreter)
    def __repr__(self):
        return "<dynamic>"