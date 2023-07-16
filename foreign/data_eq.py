from corefn.literals import Boolean


def eq_int_impl(a, b):
    return Boolean(a.value == b.value)
