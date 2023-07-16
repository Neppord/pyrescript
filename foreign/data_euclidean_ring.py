from corefn.literals import IntLiteral


def int_mod(a, b):
    abs_b = abs(b.value)
    return IntLiteral(((a.value % abs_b) + abs_b) % abs_b)


def int_degree(x):
    return IntLiteral(min(abs(x.value), 2147483647))


def int_div(a, b):
    return IntLiteral(a.value // b.value)
