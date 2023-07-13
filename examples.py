
hello_world = {
    "builtWith": "0.15.8",
    "comments": [],
    "decls":
        [{"bindType": "NonRec",
          "expression": {
              "abstraction": {
                  "type": "Var",
                  "value": {"identifier": "log", "moduleName": ["Effect", "Console"]}
              },
              "argument": {
                  "type": "Literal",
                  "value": {"literalType": "StringLiteral", "value": "hello world!"}},
              "type": "App"
          },
          "identifier": "main"
          }],
    "exports": ["main"],
    "foreign": [],
    "imports": [
        {"moduleName": ["Effect"]}, {"moduleName": ["Effect", "Console"]}, {"moduleName": ["Prelude"]},
        {"moduleName": ["Prim"]}
    ],
    "moduleName": ["Main"],
    "reExports": {}
}

hello_concat = {
    "builtWith": "0.15.8", "comments": [],
    "decls": [{
        "bindType": "NonRec",
        "expression": {
            "abstraction": {"type": "Var", "value": {"identifier": "log", "moduleName": ["Effect", "Console"]}},
            "argument": {
                "abstraction": {
                    "abstraction": {
                        "abstraction": {
                            "type": "Var",
                            "value": {"identifier": "append", "moduleName": ["Data", "Semigroup"]}
                        },
                        "argument": {
                            "type": "Var",
                            "value": {
                                "identifier": "semigroupString",
                                "moduleName": ["Data", "Semigroup"]
                            }
                        },
                        "type": "App"
                    },
                    "argument": {"type": "Literal", "value": {"literalType": "StringLiteral", "value": "hello "}},
                    "type": "App"
                },
                "argument": {"type": "Literal", "value": {"literalType": "StringLiteral", "value": "world!"}},
                "type": "App"
            }, "type": "App"
        }, "identifier": "main"
    }],
    "exports": ["main"], "foreign": [],
    "imports": [
        {"moduleName": ["Data", "Semigroup"]},
        {"moduleName": ["Effect"]},
        {"moduleName": ["Effect", "Console"]},
        {"moduleName": ["Prelude"]},
        {"moduleName": ["Prim"]}
    ],
    "moduleName": ["Main"],
    "reExports": {}
}