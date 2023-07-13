lib = {
    ("Effect", "Console"): {
        "decls":[
            {"bindType":"NonRec","expression":{"argument":"dictShow","body":{"binds":[{"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[26,24],"start":[26,20]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[26,26],"start":[26,20]}},"argument":{"type":"Var","value":{"identifier":"dictShow","sourcePos":[0,0]}},"type":"App"},"identifier":"show"}],"expression":{"argument":"a","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[26,18],"start":[26,14]}},"type":"Var","value":{"identifier":"warn","moduleName":["Effect","Console"]}},"argument":{"abstraction":{"type":"Var","value":{"identifier":"show","sourcePos":[0,0]}},"argument":{"type":"Var","value":{"identifier":"a","sourcePos":[26,1]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"Let"},"type":"Abs"},"identifier":"warnShow"},
            {"bindType":"NonRec","expression":{"argument":"dictShow","body":{"binds":[{"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[16,22],"start":[16,18]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[16,24],"start":[16,18]}},"argument":{"type":"Var","value":{"identifier":"dictShow","sourcePos":[0,0]}},"type":"App"},"identifier":"show"}],"expression":{"argument":"a","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[16,16],"start":[16,13]}},"type":"Var","value":{"identifier":"log","moduleName":["Effect","Console"]}},"argument":{"abstraction":{"type":"Var","value":{"identifier":"show","sourcePos":[0,0]}},"argument":{"type":"Var","value":{"identifier":"a","sourcePos":[16,1]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"Let"},"type":"Abs"},"identifier":"logShow"},{"bindType":"NonRec","expression":{"argument":"dictShow","body":{"binds":[{"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[46,24],"start":[46,20]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[46,26],"start":[46,20]}},"argument":{"type":"Var","value":{"identifier":"dictShow","sourcePos":[0,0]}},"type":"App"},"identifier":"show"}],"expression":{"argument":"a","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[46,18],"start":[46,14]}},"type":"Var","value":{"identifier":"info","moduleName":["Effect","Console"]}},"argument":{"abstraction":{"type":"Var","value":{"identifier":"show","sourcePos":[0,0]}},"argument":{"type":"Var","value":{"identifier":"a","sourcePos":[46,1]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"Let"},"type":"Abs"},"identifier":"infoShow"},{"bindType":"NonRec","expression":{"argument":"dictShow","body":{"binds":[{"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[36,26],"start":[36,22]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[36,28],"start":[36,22]}},"argument":{"type":"Var","value":{"identifier":"dictShow","sourcePos":[0,0]}},"type":"App"},"identifier":"show"}],"expression":{"argument":"a","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[36,20],"start":[36,15]}},"type":"Var","value":{"identifier":"error","moduleName":["Effect","Console"]}},"argument":{"abstraction":{"type":"Var","value":{"identifier":"show","sourcePos":[0,0]}},"argument":{"type":"Var","value":{"identifier":"a","sourcePos":[36,1]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"Let"},"type":"Abs"},"identifier":"errorShow"},{"bindType":"NonRec","expression":{"argument":"dictShow","body":{"binds":[{"bindType":"NonRec","expression":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[56,26],"start":[56,22]}},"type":"Var","value":{"identifier":"show","moduleName":["Data","Show"]}},"annotation":{"meta":{"metaType":"IsSyntheticApp"},"sourceSpan":{"end":[56,28],"start":[56,22]}},"argument":{"type":"Var","value":{"identifier":"dictShow","sourcePos":[0,0]}},"type":"App"},"identifier":"show"}],"expression":{"argument":"a","body":{"abstraction":{"annotation":{"meta":{"metaType":"IsForeign"},"sourceSpan":{"end":[56,20],"start":[56,15]}},"type":"Var","value":{"identifier":"debug","moduleName":["Effect","Console"]}},"argument":{"abstraction":{"type":"Var","value":{"identifier":"show","sourcePos":[0,0]}},"argument":{"type":"Var","value":{"identifier":"a","sourcePos":[56,1]}},"type":"App"},"type":"App"},"type":"Abs"},"type":"Let"},"type":"Abs"},"identifier":"debugShow"}],"exports":["log","logShow","warn","warnShow","error","errorShow","info","infoShow","debug","debugShow","time","timeLog","timeEnd","clear"],
        "foreign": ["log","warn","error","info","debug","time","timeLog","timeEnd","clear"],
        "imports":[
            {"moduleName":["Data","Show"]},
            {"moduleName":["Data","Unit"]},
            {"moduleName":["Effect"]},
            {"moduleName":["Effect","Console"]},
            {"moduleName":["Prim"]}
        ],
        "moduleName":["Effect","Console"],
        "reExports":{}
    },
    ("Data", "Semigroup"): {
        "decls": [
            {
                "bindType": "NonRec",
                "expression": {
                    "argument": "x",
                    "body": {
                        "type": "Var",
                        "value": {"identifier": "x", "sourcePos": [0, 0]}
                    },
                    "type": "Abs"
                }, "identifier": "SemigroupRecord$Dict"
            },
            {
                "bindType": "NonRec",
                "expression": {
                    "argument": "x",
                    "body": {
                        "type": "Var",
                        "value": {"identifier": "x", "sourcePos": [0, 0]}
                    },
                    "type": "Abs"
                },
                "identifier": "Semigroup$Dict"
            },
            {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var", "value": {
                            "identifier": "Semigroup$Dict",
                            "moduleName": ["Data", "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal", "value": {
                            "literalType": "ObjectLiteral",
                            "value": [["append",
                                       {
                                           "argument": "v",
                                           "body": {
                                               "type": "Var",
                                               "value": {
                                                   "identifier": "absurd",
                                                   "moduleName": [
                                                       "Data",
                                                       "Void"]}
                                           },
                                           "type": "Abs"}]]}
                    },
                    "type": "App"
                }, "identifier": "semigroupVoid"
            }, {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var",
                        "value": {
                            "identifier": "Semigroup$Dict",
                            "moduleName": [
                                "Data",
                                "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal",
                        "value": {
                            "literalType": "ObjectLiteral",
                            "value": [[
                                "append",
                                {
                                    "argument": "v",
                                    "body": {
                                        "argument": "v1",
                                        "body": {
                                            "type": "Var",
                                            "value": {
                                                "identifier": "unit",
                                                "moduleName": [
                                                    "Data",
                                                    "Unit"]}
                                        },
                                        "type": "Abs"
                                    },
                                    "type": "Abs"}]]}
                    },
                    "type": "App"
                },
                "identifier": "semigroupUnit"
            },
            {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var", "value": {
                            "identifier": "Semigroup$Dict",
                            "moduleName": ["Data",
                                           "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal", "value": {
                            "literalType": "ObjectLiteral",
                            "value": [["append",
                                       {
                                           "type": "Var",
                                           "value": {
                                               "identifier": "concatString",
                                               "moduleName": [
                                                   "Data",
                                                   "Semigroup"]}}]]}
                    },
                    "type": "App"
                }, "identifier": "semigroupString"
            }, {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var",
                        "value": {
                            "identifier": "SemigroupRecord$Dict",
                            "moduleName": [
                                "Data",
                                "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal",
                        "value": {
                            "literalType": "ObjectLiteral",
                            "value": [[
                                "appendRecord",
                                {
                                    "argument": "v",
                                    "body": {
                                        "argument": "v1",
                                        "body": {
                                            "argument": "v2",
                                            "body": {
                                                "type": "Literal",
                                                "value": {
                                                    "literalType": "ObjectLiteral",
                                                    "value": []}
                                            },
                                            "type": "Abs"
                                        },
                                        "type": "Abs"
                                    },
                                    "type": "Abs"}]]}
                    },
                    "type": "App"
                },
                "identifier": "semigroupRecordNil"
            },
            {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var", "value": {
                            "identifier": "Semigroup$Dict",
                            "moduleName": ["Data",
                                           "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal", "value": {
                            "literalType": "ObjectLiteral",
                            "value": [["append",
                                       {
                                           "argument": "v",
                                           "body": {
                                               "argument": "v1",
                                               "body": {
                                                   "annotation": {
                                                       "meta": {
                                                           "constructorType": "ProductType",
                                                           "identifiers": [],
                                                           "metaType": "IsConstructor"
                                                       },
                                                       "sourceSpan": {
                                                           "end": [
                                                               55,
                                                               21],
                                                           "start": [
                                                               55,
                                                               16]}
                                                   },
                                                   "type": "Var",
                                                   "value": {
                                                       "identifier": "Proxy",
                                                       "moduleName": [
                                                           "Type",
                                                           "Proxy"]}
                                               },
                                               "type": "Abs"
                                           },
                                           "type": "Abs"}]]}
                    },
                    "type": "App"
                }, "identifier": "semigroupProxy"
            }, {
                "bindType": "NonRec",
                "expression": {
                    "abstraction": {
                        "type": "Var",
                        "value": {
                            "identifier": "Semigroup$Dict",
                            "moduleName": [
                                "Data",
                                "Semigroup"]}
                    },
                    "argument": {
                        "type": "Literal",
                        "value": {
                            "literalType": "ObjectLiteral",
                            "value": [[
                                "append",
                                {
                                    "type": "Var",
                                    "value": {
                                        "identifier": "concatArray",
                                        "moduleName": [
                                            "Data",
                                            "Semigroup"]}}]]}
                    },
                    "type": "App"
                },
                "identifier": "semigroupArray"
            },
            {
                "bindType": "NonRec", "expression": {
                "argument": "dict", "body": {
                    "caseAlternatives": [{
                        "binders": [
                            {
                                "binderType": "ConstructorBinder", "binders": [{
                                "binderType": "VarBinder", "identifier": "v"}],
                                "constructorName": {
                                    "identifier": "SemigroupRecord$Dict", "moduleName": ["Data", "Semigroup"]},
                                "typeName": {
                                    "identifier": "SemigroupRecord$Dict", "moduleName": ["Data", "Semigroup"]}}],
                        "expression": {
                            "expression": {
                                "type": "Var", "value": {
                                    "identifier": "v", "sourcePos": [0, 0]}
                            },
                            "fieldName": "appendRecord", "type": "Accessor"
                        }, "isGuarded": False}], "caseExpressions": [
                        {
                            "type": "Var", "value": {
                            "identifier": "dict", "sourcePos": [0, 0]}}], "type": "Case"
                },
                "type": "Abs"
            },
                "identifier": "appendRecord"
            }, {
                "bindType": "NonRec", "expression": {
                    "argument": "$__unused", "body": {
                        "argument": "dictSemigroupRecord", "body": {
                            "abstraction": {
                                "type": "Var",
                                "value": {
                                    "identifier": "Semigroup$Dict",
                                    "moduleName": ["Data",
                                                   "Semigroup"]}
                            },
                            "argument": {
                                "type": "Literal",
                                "value": {
                                    "literalType": "ObjectLiteral",
                                    "value": [
                                        ["append", {
                                            "abstraction": {
                                                "abstraction": {
                                                    "type": "Var",
                                                    "value": {
                                                        "identifier": "appendRecord",
                                                        "moduleName": [
                                                            "Data",
                                                            "Semigroup"]}
                                                },
                                                "argument": {
                                                    "type": "Var",
                                                    "value": {
                                                        "identifier": "dictSemigroupRecord",
                                                        "sourcePos": [
                                                            0,
                                                            0]}
                                                },
                                                "type": "App"
                                            },
                                            "argument": {
                                                "annotation": {
                                                    "meta": {
                                                        "constructorType": "ProductType",
                                                        "identifiers": [],
                                                        "metaType": "IsConstructor"
                                                    },
                                                    "sourceSpan": {
                                                        "end": [58,
                                                                31],
                                                        "start": [58,
                                                                  26]}
                                                },
                                                "type": "Var",
                                                "value": {
                                                    "identifier": "Proxy",
                                                    "moduleName": [
                                                        "Type",
                                                        "Proxy"]}
                                            },
                                            "type": "App"}]]}
                            },
                            "type": "App"
                        }, "type": "Abs"
                    }, "type": "Abs"
                },
                "identifier": "semigroupRecord"
            }, {
                "bindType": "NonRec",
                "expression": {
                    "argument": "dict",
                    "body": {
                        "caseAlternatives": [
                            {
                                "binders": [
                                    {
                                        "binderType": "ConstructorBinder",
                                        "binders": [
                                            {
                                                "binderType": "VarBinder",
                                                "identifier": "v"}],
                                        "constructorName": {
                                            "identifier": "Semigroup$Dict",
                                            "moduleName": [
                                                "Data",
                                                "Semigroup"]},
                                        "typeName": {
                                            "identifier": "Semigroup$Dict",
                                            "moduleName": [
                                                "Data",
                                                "Semigroup"]}}],
                                "expression": {
                                    "expression": {
                                        "type": "Var",
                                        "value": {
                                            "identifier": "v",
                                            "sourcePos": [
                                                0,
                                                0]}
                                    },
                                    "fieldName": "append",
                                    "type": "Accessor"
                                },
                                "isGuarded": False}],
                        "caseExpressions": [
                            {
                                "type": "Var",
                                "value": {
                                    "identifier": "dict",
                                    "sourcePos": [
                                        0,
                                        0]}}],
                        "type": "Case"
                    },
                    "type": "Abs"
                },
                "identifier": "append"
            },
            {
                "bindType": "NonRec", "expression": {
                "argument": "dictSemigroup", "body": {
                    "binds": [{
                        "bindType": "NonRec",
                        "expression": {
                            "abstraction": {
                                "type": "Var",
                                "value": {
                                    "identifier": "append",
                                    "moduleName": [
                                        "Data",
                                        "Semigroup"]}
                            },
                            "argument": {
                                "type": "Var",
                                "value": {
                                    "identifier": "dictSemigroup",
                                    "sourcePos": [
                                        0,
                                        0]}
                            },
                            "type": "App"
                        },
                        "identifier": "append1"}],
                    "expression": {
                        "abstraction": {
                            "type": "Var",
                            "value": {
                                "identifier": "Semigroup$Dict",
                                "moduleName": [
                                    "Data",
                                    "Semigroup"]}
                        },
                        "argument": {
                            "type": "Literal",
                            "value": {
                                "literalType": "ObjectLiteral",
                                "value": [
                                    ["append",
                                     {
                                         "argument": "f",
                                         "body": {
                                             "argument": "g",
                                             "body": {
                                                 "argument": "x",
                                                 "body": {
                                                     "abstraction": {
                                                         "abstraction": {
                                                             "type": "Var",
                                                             "value": {
                                                                 "identifier": "append1",
                                                                 "sourcePos": [
                                                                     0,
                                                                     0]}
                                                         },
                                                         "argument": {
                                                             "abstraction": {
                                                                 "type": "Var",
                                                                 "value": {
                                                                     "identifier": "f",
                                                                     "sourcePos": [
                                                                         49,
                                                                         3]}
                                                             },
                                                             "argument": {
                                                                 "type": "Var",
                                                                 "value": {
                                                                     "identifier": "x",
                                                                     "sourcePos": [
                                                                         49,
                                                                         3]}
                                                             },
                                                             "type": "App"
                                                         },
                                                         "type": "App"
                                                     },
                                                     "argument": {
                                                         "abstraction": {
                                                             "type": "Var",
                                                             "value": {
                                                                 "identifier": "g",
                                                                 "sourcePos": [
                                                                     49,
                                                                     3]}
                                                         },
                                                         "argument": {
                                                             "type": "Var",
                                                             "value": {
                                                                 "identifier": "x",
                                                                 "sourcePos": [
                                                                     49,
                                                                     3]}
                                                         },
                                                         "type": "App"
                                                     },
                                                     "type": "App"
                                                 },
                                                 "type": "Abs"
                                             },
                                             "type": "Abs"
                                         },
                                         "type": "Abs"}]]}
                        },
                        "type": "App"
                    },
                    "type": "Let"
                },
                "type": "Abs"
            }, "identifier": "semigroupFn"
            }, {
                "bindType": "NonRec",
                "expression": {
                    "argument": "dictIsSymbol",
                    "body": {
                        "binds": [{
                            "bindType": "NonRec",
                            "expression": {
                                "abstraction": {
                                    "type": "Var",
                                    "value": {
                                        "identifier": "reflectSymbol",
                                        "moduleName": [
                                            "Data",
                                            "Symbol"]}
                                },
                                "argument": {
                                    "type": "Var",
                                    "value": {
                                        "identifier": "dictIsSymbol",
                                        "sourcePos": [
                                            0,
                                            0]}
                                },
                                "type": "App"
                            },
                            "identifier": "reflectSymbol"}],
                        "expression": {
                            "argument": "$__unused",
                            "body": {
                                "argument": "dictSemigroupRecord",
                                "body": {
                                    "binds": [
                                        {
                                            "bindType": "NonRec",
                                            "expression": {
                                                "abstraction": {
                                                    "type": "Var",
                                                    "value": {
                                                        "identifier": "appendRecord",
                                                        "moduleName": [
                                                            "Data",
                                                            "Semigroup"]}
                                                },
                                                "argument": {
                                                    "type": "Var",
                                                    "value": {"identifier": "dictSemigroupRecord", "sourcePos": [0, 0]}
                                                },
                                                "type": "App"
                                            },
                                            "identifier": "appendRecord1"}],
                                    "expression": {
                                        "argument": "dictSemigroup",
                                        "body": {
                                            "binds": [
                                                {
                                                    "bindType": "NonRec",
                                                    "expression": {
                                                        "abstraction": {
                                                            "type": "Var",
                                                            "value": {
                                                                "identifier": "append",
                                                                "moduleName": [
                                                                    "Data",
                                                                    "Semigroup"]}
                                                        },
                                                        "argument": {
                                                            "type": "Var",
                                                            "value": {"identifier": "dictSemigroup", "sourcePos": [0, 0]}
                                                        },
                                                        "type": "App"
                                                    },
                                                    "identifier": "append1"}],
                                            "expression": {
                                                "abstraction": {
                                                    "type": "Var",
                                                    "value": {
                                                        "identifier": "SemigroupRecord$Dict",
                                                        "moduleName": [
                                                            "Data",
                                                            "Semigroup"]}
                                                },
                                                "argument": {
                                                    "type": "Literal",
                                                    "value": {
                                                        "literalType": "ObjectLiteral",
                                                        "value": [
                                                            [
                                                                "appendRecord",
                                                                {
                                                                    "argument": "v",
                                                                    "body": {
                                                                        "argument": "ra",
                                                                        "body": {
                                                                            "argument": "rb",
                                                                            "body": {
                                                                                "binds": [
                                                                                    {
                                                                                        "bindType": "NonRec",
                                                                                        "expression": {
                                                                                            "abstraction": {
                                                                                                "abstraction": {
                                                                                                    "abstraction": {
                                                                                                        "type": "Var",
                                                                                                        "value": {
                                                                                                            "identifier": "appendRecord1",
                                                                                                            "sourcePos": [
                                                                                                                0,
                                                                                                                0]}
                                                                                                    },
                                                                                                    "argument": {
                                                                                                        "type": "Var",
                                                                                                        "value": {
                                                                                                            "identifier": "Proxy",
                                                                                                            "moduleName": [
                                                                                                                "Type",
                                                                                                                "Proxy"]}
                                                                                                    },
                                                                                                    "type": "App"
                                                                                                },
                                                                                                "argument": {
                                                                                                    "type": "Var",
                                                                                                    "value": {
                                                                                                        "identifier": "ra",
                                                                                                        "sourcePos": [
                                                                                                            79,
                                                                                                            3]}
                                                                                                },
                                                                                                "type": "App"
                                                                                            },
                                                                                            "argument": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "rb",
                                                                                                    "sourcePos": [
                                                                                                        79,
                                                                                                        3]}
                                                                                            },
                                                                                            "type": "App"
                                                                                        },
                                                                                        "identifier": "tail"
                                                                                    },
                                                                                    {
                                                                                        "bindType": "NonRec",
                                                                                        "expression": {
                                                                                            "abstraction": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "reflectSymbol",
                                                                                                    "sourcePos": [
                                                                                                        0,
                                                                                                        0]}
                                                                                            },
                                                                                            "argument": {
                                                                                                "annotation": {
                                                                                                    "meta": {
                                                                                                        "constructorType": "ProductType",
                                                                                                        "identifiers": [],
                                                                                                        "metaType": "IsConstructor"
                                                                                                    },
                                                                                                    "sourceSpan": {
                                                                                                        "end": [
                                                                                                            81,
                                                                                                            31],
                                                                                                        "start": [
                                                                                                            81,
                                                                                                            26]}
                                                                                                },
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "Proxy",
                                                                                                    "moduleName": [
                                                                                                        "Type",
                                                                                                        "Proxy"]}
                                                                                            },
                                                                                            "type": "App"
                                                                                        },
                                                                                        "identifier": "key"
                                                                                    },
                                                                                    {
                                                                                        "bindType": "NonRec",
                                                                                        "expression": {
                                                                                            "abstraction": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "unsafeSet",
                                                                                                    "moduleName": [
                                                                                                        "Record",
                                                                                                        "Unsafe"]}
                                                                                            },
                                                                                            "argument": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "key",
                                                                                                    "sourcePos": [
                                                                                                        81,
                                                                                                        5]}
                                                                                            },
                                                                                            "type": "App"
                                                                                        },
                                                                                        "identifier": "insert"
                                                                                    },
                                                                                    {
                                                                                        "bindType": "NonRec",
                                                                                        "expression": {
                                                                                            "abstraction": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "unsafeGet",
                                                                                                    "moduleName": [
                                                                                                        "Record",
                                                                                                        "Unsafe"]}
                                                                                            },
                                                                                            "argument": {
                                                                                                "type": "Var",
                                                                                                "value": {
                                                                                                    "identifier": "key",
                                                                                                    "sourcePos": [
                                                                                                        81,
                                                                                                        5]}
                                                                                            },
                                                                                            "type": "App"
                                                                                        },
                                                                                        "identifier": "get"}],
                                                                                "expression": {
                                                                                    "abstraction": {
                                                                                        "abstraction": {
                                                                                            "type": "Var",
                                                                                            "value": {
                                                                                                "identifier": "insert",
                                                                                                "sourcePos": [
                                                                                                    83,
                                                                                                    5]}
                                                                                        },
                                                                                        "argument": {
                                                                                            "abstraction": {
                                                                                                "abstraction": {
                                                                                                    "type": "Var",
                                                                                                    "value": {
                                                                                                        "identifier": "append1",
                                                                                                        "sourcePos": [
                                                                                                            0,
                                                                                                            0]}
                                                                                                },
                                                                                                "argument": {
                                                                                                    "abstraction": {
                                                                                                        "type": "Var",
                                                                                                        "value": {
                                                                                                            "identifier": "get",
                                                                                                            "sourcePos": [
                                                                                                                82,
                                                                                                                5]}
                                                                                                    },
                                                                                                    "argument": {
                                                                                                        "type": "Var",
                                                                                                        "value": {
                                                                                                            "identifier": "ra",
                                                                                                            "sourcePos": [
                                                                                                                79,
                                                                                                                3]}
                                                                                                    },
                                                                                                    "type": "App"
                                                                                                },
                                                                                                "type": "App"
                                                                                            },
                                                                                            "argument": {
                                                                                                "abstraction": {
                                                                                                    "type": "Var",
                                                                                                    "value": {
                                                                                                        "identifier": "get",
                                                                                                        "sourcePos": [
                                                                                                            82,
                                                                                                            5]}
                                                                                                },
                                                                                                "argument": {
                                                                                                    "type": "Var",
                                                                                                    "value": {
                                                                                                        "identifier": "rb",
                                                                                                        "sourcePos": [
                                                                                                            79,
                                                                                                            3]}
                                                                                                },
                                                                                                "type": "App"
                                                                                            },
                                                                                            "type": "App"
                                                                                        },
                                                                                        "type": "App"
                                                                                    },
                                                                                    "argument": {
                                                                                        "type": "Var",
                                                                                        "value": {
                                                                                            "identifier": "tail",
                                                                                            "sourcePos": [
                                                                                                84,
                                                                                                5]}
                                                                                    },
                                                                                    "type": "App"
                                                                                },
                                                                                "type": "Let"
                                                                            },
                                                                            "type": "Abs"
                                                                        },
                                                                        "type": "Abs"
                                                                    },
                                                                    "type": "Abs"}]]}
                                                },
                                                "type": "App"
                                            },
                                            "type": "Let"
                                        },
                                        "type": "Abs"
                                    },
                                    "type": "Let"
                                },
                                "type": "Abs"
                            },
                            "type": "Abs"
                        },
                        "type": "Let"
                    },
                    "type": "Abs"
                },
                "identifier": "semigroupRecordCons"}],
        "exports": ["append", "appendRecord", "semigroupString", "semigroupUnit", "semigroupVoid", "semigroupFn",
                    "semigroupArray", "semigroupProxy", "semigroupRecord", "semigroupRecordNil", "semigroupRecordCons"],
        "foreign": ["concatString", "concatArray"],
        "imports": [
            {"moduleName": ["Data", "Semigroup"]},
            {"moduleName": ["Data", "Symbol"]},
            {"moduleName": ["Data", "Unit"]},
            {"moduleName": ["Data", "Void"]},
            {"moduleName": ["Prim"]},
            {"moduleName": ["Prim", "Row"]},
            {"moduleName": ["Prim", "RowList"]},
            {"moduleName": ["Record", "Unsafe"]},
            {"moduleName": ["Type", "Proxy"]}
        ],
        "moduleName": ["Data", "Semigroup"],
        "reExports": {}
    }
}
