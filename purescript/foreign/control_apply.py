from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Array

"""
function (fs) {
  return function (xs) {
    var l = fs.length;
    var k = xs.length;
    var result = new Array(l*k);
    var n = 0;
    for (var i = 0; i < l; i++) {
      var f = fs[i];
      for (var j = 0; j < k; j++) {
        result[n++] = f(xs[j]);
      }
    }
    return result;
  };
};

"""
exports = {
    'arrayApply': NativeX(lambda i, fs, xs: Array([f(x) for x in xs.array for f in fs]), 2, [])
}
