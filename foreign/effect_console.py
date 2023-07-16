from corefn.literals import NullLiteral, nullLiteral


def log(x):
    """

    :type x: corefn.literals.StringLiteral
    """
    print x.value
    return nullLiteral
