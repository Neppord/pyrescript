from purescript.corefn.expression import Expression

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

    def __repr__(self):
        argument = self.argument
        body = self.body.__repr__()
        return "\\" + argument + " -> " + body


class NativeX(AbsInterface):
    def __init__(self, native, x, arguments):
        self.x = x
        self.native = native
        self.arguments = arguments
        assert x >= len(arguments)

    def __repr__(self):
        return "NativeX(%s, %s, %s)" % (
            self.native.__name__,
            self.x,
            self.arguments.__repr__()
        )


class ConstructorInvocation(AbsInterface):

    def __init__(self, name, field_names, arguments):
        self.name = name
        self.field_names = field_names
        self.arguments = arguments
        assert len(field_names) >= len(arguments), "to many arguments"

    def __repr__(self):
        return " ".join([self.name] + ["(%s)" % a.__repr__() for a in self.arguments])


class Constructor(AbsInterface):
    def __init__(self, name, field_names):
        self.name = name
        self.field_names = field_names

    def __repr__(self):
        return self.name


class NotImplementedYet(AbsInterface):
    def __init__(self, reason):
        self.reason = reason
