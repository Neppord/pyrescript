from purescript.corefn.expression import Expression

"""
Abs aka Lambda, Callable etc.

Represents a mapping between two values of type Expr. A function that takes 
more then one argument is represented by nesting multiple Abs, one returning
 the other

"""


class Abs(Expression):
    def __init__(self, argument, body):
        self.argument = argument
        self.body = body

    def __repr__(self):
        argument = self.argument
        body = self.body.__repr__()
        return "\\" + argument + " -> " + body


class Constructor(Expression):
    def __init__(self, name, field_names):
        self.name = name
        self.field_names = field_names

    def __repr__(self):
        return self.name
