from corefn.literals import Null, nullLiteral, Effect


def log(x):
    """

    :type x: corefn.literals.String
    """
    print x.value
    return nullLiteral
