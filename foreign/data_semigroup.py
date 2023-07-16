from corefn.literals import StringLiteral


def concat_string(a, b):
    return StringLiteral(a.value + b.value)
