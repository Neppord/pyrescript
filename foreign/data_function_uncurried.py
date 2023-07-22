from corefn.abs import Native1

exports = {
    'mkFn4': Native1(lambda i, fn: fn),
    'runFn4': Native1(lambda i, fn: fn),
    'mkFn2': Native1(lambda i, fn: fn),
    'runFn2': Native1(lambda i, fn: fn),
}