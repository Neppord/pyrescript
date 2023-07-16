from corefn.literals import IntLiteral


def int_add(a, b):
    """

    :type a: IntLiteral
    :type b: IntLiteral
    """
    return IntLiteral(a.value + b.value)


def int_mul(a, b):
    return IntLiteral(a.value * b.value)
