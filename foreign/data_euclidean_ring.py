from corefn.literals import Int


def int_mod(i, a, b):
    abs_b = abs(b.value)
    return Int(((a.value % abs_b) + abs_b) % abs_b)


def int_degree(i, x):
    return Int(min(abs(x.value), 2147483647))


def int_div(i, a, b):
    return Int(a.value // b.value)
