
"""
function (lt) {
  return function (eq) {
    return function (gt) {
      return function (x) {
        return function (y) {
          return x < y ? lt : x === y ? eq : gt;
        };
      };
    };
  };
};
"""
from purescript.corefn.abs import NativeX

exports = {
    'ordBooleanImpl': NativeX(lambda i, lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordIntImpl': NativeX(lambda i, lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordNumberImpl': NativeX(lambda i, lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordStringImpl': NativeX(lambda i, lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
    'ordCharImpl': NativeX(lambda i, lt, eq, gt, x, y: lt if x.value < y.value else (eq if x == y else gt), 5, []),
}