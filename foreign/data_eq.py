from corefn.literals import BoolLiteral


def eq_int_impl(a, b):
    return BoolLiteral(a.value == b.value)
