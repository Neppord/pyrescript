from corefn.literals import String


def concat_string(a, b):
    return String(a.value + b.value)
