module ExpressionAtoms where

x1 = 1
x2 = 1.0
x3 = "1"
x4 = [1]
x5 = {a : 1}
x6 = {"a" : 1}
x7 = _
x8 = ?x
x9 = x1
x10 = ExpressionAtom.x1
x11 1 = true
x11 _ = false
x12 = (1)
x13 = '1'
x14 = """1"""