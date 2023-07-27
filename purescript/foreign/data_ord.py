from purescript.corefn.abs import NativeX

exports = {
    'ordBooleanImpl': NativeX(lambda lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordIntImpl': NativeX(lambda lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordNumberImpl': NativeX(lambda lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordStringImpl': NativeX(lambda lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordCharImpl': NativeX(lambda lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
}