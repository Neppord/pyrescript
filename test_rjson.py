from rjson import loads

def test_object_with_one_member():
    assert {"builtWith": "0.15.8"} == loads('{"builtWith":"0.15.8"}')

def test_literals():
    loads('1')
    loads('-1')
    loads('1.1')
    loads('true')
    loads('false')
    loads('null')
    loads('[]')
    loads("{}")
    assert True


def test_list_with_one_item():
    loads('["builtWith"]')
    assert True


def test_full_module():
    loads("""{"builtWith":"0.15.8","comments":[],"decls":[{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[13,29],"start":[13,27]}},"type":"Var","value":{"identifier":"eq","moduleName":["Data","Eq"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[13,31],"start":[13,19]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"eqInt","moduleName":["Data","Eq"]}},"type":"App"},"identifier":"eq"},{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[13,22],"start":[13,19]}},"type":"Var","value":{"identifier":"mod","moduleName":["Data","EuclideanRing"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[13,24],"start":[13,19]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"euclideanRingInt","moduleName":["Data","EuclideanRing"]}},"type":"App"},"identifier":"mod"},{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[20,18],"start":[20,17]}},"type":"Var","value":{"identifier":"mul","moduleName":["Data","Semiring"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[20,20],"start":[20,15]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"semiringInt","moduleName":["Data","Semiring"]}},"type":"App"},"identifier":"mul"},{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[20,36],"start":[20,34]}},"type":"Var","value":{"identifier":"append","moduleName":["Data","Semigroup"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[20,43],"start":[20,27]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"semigroupString","moduleName":["Data","Semigroup"]}},"type":"App"},"identifier":"append"},{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[23,14],"start":[23,10]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[23,16],"start":[23,10]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"showInt","moduleName":["Data","Show"]}},"type":"App"},"identifier":"show"},{"annotation":{"meta":null,"sourceSpan":{"end":[12,37],"start":[12,1]}},"bindType":"NonRec","expression":{"annotation":{"meta":null,"sourceSpan":{"end":[12,37],"start":[12,1]}},"argument":"n","body":{"annotation":{"meta":null,"sourceSpan":{"end":[12,37],"start":[12,1]}},"argument":"d","body":{"abstraction":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"eq","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[13,31],"start":[13,19]}},"argument":{"abstraction":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"mod","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[13,24],"start":[13,19]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[13,24],"start":[13,23]}},"type":"Var","value":{"identifier":"n","sourcePos":[13,1]}},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[13,26],"start":[13,19]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[13,26],"start":[13,25]}},"type":"Var","value":{"identifier":"d","sourcePos":[13,1]}},"type":"App"},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[13,31],"start":[13,19]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[13,31],"start":[13,30]}},"type":"Literal","value":{"literalType":"IntLiteral","value":0}},"type":"App"},"type":"Abs"},"type":"Abs"},"identifier":"divisibleBy"},{"annotation":{"meta":null,"sourceSpan":{"end":[15,26],"start":[15,1]}},"bindType":"NonRec","expression":{"annotation":{"meta":null,"sourceSpan":{"end":[15,26],"start":[15,1]}},"argument":"n","body":{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[17,3]}},"binds":[{"annotation":{"meta":null,"sourceSpan":{"end":[18,26],"start":[18,5]}},"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[18,24],"start":[18,13]}},"type":"Var","value":{"identifier":"divisibleBy","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[18,26],"start":[18,13]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[18,26],"start":[18,25]}},"type":"Var","value":{"identifier":"n","sourcePos":[16,1]}},"type":"App"},"identifier":"divBy"}],"expression":{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[20,5]}},"caseAlternatives":[{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[20,5]}},"binderType":"LiteralBinder","literal":{"literalType":"BooleanLiteral","value":true}}],"expression":{"abstraction":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"append","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[20,43],"start":[20,27]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[20,33],"start":[20,27]}},"type":"Literal","value":{"literalType":"StringLiteral","value":"Fizz"}},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[20,43],"start":[20,27]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[20,43],"start":[20,37]}},"type":"Literal","value":{"literalType":"StringLiteral","value":"Buzz"}},"type":"App"},"isGuarded":false},{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[20,5]}},"binderType":"NullBinder"}],"expression":{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[21,10]}},"caseAlternatives":[{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[21,10]}},"binderType":"LiteralBinder","literal":{"literalType":"BooleanLiteral","value":true}}],"expression":{"annotation":{"meta":null,"sourceSpan":{"end":[21,32],"start":[21,26]}},"type":"Literal","value":{"literalType":"StringLiteral","value":"Fizz"}},"isGuarded":false},{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[21,10]}},"binderType":"NullBinder"}],"expression":{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[22,10]}},"caseAlternatives":[{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[22,10]}},"binderType":"LiteralBinder","literal":{"literalType":"BooleanLiteral","value":true}}],"expression":{"annotation":{"meta":null,"sourceSpan":{"end":[22,32],"start":[22,26]}},"type":"Literal","value":{"literalType":"StringLiteral","value":"Buzz"}},"isGuarded":false},{"binders":[{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[22,10]}},"binderType":"NullBinder"}],"expression":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"show","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[23,10]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[23,16],"start":[23,15]}},"type":"Var","value":{"identifier":"n","sourcePos":[16,1]}},"type":"App"},"isGuarded":false}],"caseExpressions":[{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[22,18],"start":[22,13]}},"type":"Var","value":{"identifier":"divBy","sourcePos":[18,5]}},"annotation":{"meta":null,"sourceSpan":{"end":[22,20],"start":[22,13]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[22,20],"start":[22,19]}},"type":"Literal","value":{"literalType":"IntLiteral","value":5}},"type":"App"}],"type":"Case"},"isGuarded":false}],"caseExpressions":[{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[21,18],"start":[21,13]}},"type":"Var","value":{"identifier":"divBy","sourcePos":[18,5]}},"annotation":{"meta":null,"sourceSpan":{"end":[21,20],"start":[21,13]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[21,20],"start":[21,19]}},"type":"Literal","value":{"literalType":"IntLiteral","value":3}},"type":"App"}],"type":"Case"},"isGuarded":false}],"caseExpressions":[{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[20,13],"start":[20,8]}},"type":"Var","value":{"identifier":"divBy","sourcePos":[18,5]}},"annotation":{"meta":null,"sourceSpan":{"end":[20,21],"start":[20,8]}},"argument":{"abstraction":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"mul","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[20,20],"start":[20,15]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[20,16],"start":[20,15]}},"type":"Literal","value":{"literalType":"IntLiteral","value":3}},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[20,20],"start":[20,15]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[20,20],"start":[20,19]}},"type":"Literal","value":{"literalType":"IntLiteral","value":5}},"type":"App"},"type":"App"}],"type":"Case"},"type":"Let"},"type":"Abs"},"identifier":"fizzbuzz"},{"annotation":{"meta":null,"sourceSpan":{"end":[25,20],"start":[25,1]}},"bindType":"NonRec","expression":{"abstraction":{"abstraction":{"abstraction":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[26,12],"start":[26,8]}},"type":"Var","value":{"identifier":"for_","moduleName":["Data","Foldable"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[26,22],"start":[26,8]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"applicativeEffect","moduleName":["Effect"]}},"type":"App"},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[26,22],"start":[26,8]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[0,0],"start":[0,0]}},"type":"Var","value":{"identifier":"foldableArray","moduleName":["Data","Foldable"]}},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[26,22],"start":[26,8]}},"argument":{"abstraction":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[26,18],"start":[26,16]}},"type":"Var","value":{"identifier":"range","moduleName":["Data","Array"]}},"annotation":{"meta":null,"sourceSpan":{"end":[26,21],"start":[26,14]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[26,15],"start":[26,14]}},"type":"Literal","value":{"literalType":"IntLiteral","value":1}},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[26,21],"start":[26,14]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[26,21],"start":[26,19]}},"type":"Literal","value":{"literalType":"IntLiteral","value":15}},"type":"App"},"type":"App"},"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[26,8]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[26,23]}},"argument":"n","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[27,8],"start":[27,5]}},"type":"Var","value":{"identifier":"log","moduleName":["Effect","Console"]}},"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[27,5]}},"argument":{"abstraction":{"annotation":{"meta":null,"sourceSpan":{"end":[27,18],"start":[27,10]}},"type":"Var","value":{"identifier":"fizzbuzz","moduleName":["Main"]}},"annotation":{"meta":null,"sourceSpan":{"end":[27,20],"start":[27,10]}},"argument":{"annotation":{"meta":null,"sourceSpan":{"end":[27,20],"start":[27,19]}},"type":"Var","value":{"identifier":"n","sourcePos":[26,24]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"App"},"identifier":"main"}],"exports":["divisibleBy","fizzbuzz","main"],"foreign":[],"imports":[{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Array"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Eq"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","EuclideanRing"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Foldable"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Semigroup"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Semiring"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Data","Show"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Effect"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Effect","Console"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Main"]},{"annotation":{"meta":null,"sourceSpan":{"end":[3,15],"start":[3,1]}},"moduleName":["Prelude"]},{"annotation":{"meta":null,"sourceSpan":{"end":[27,21],"start":[1,1]}},"moduleName":["Prim"]}],"moduleName":["Main"],"modulePath":"src\\Main.purs","reExports":{},"sourceSpan":{"end":[27,21],"start":[1,1]}}""")
    assert True