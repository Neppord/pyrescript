## Tokens

these are the tokens that needs regexp the tokens that are string constants can be found within the grammar. The current
lexer don't seam to understand unicode groups, therefore they are only kept as comments.

```ebnf
LINE_COMMENT: "--[^\n]*\n?";
MULTILINE_COMMENT: "{-([^-]*(-[^}])?)*-}";
LINE_INDENT: "\n[\s]*";
IGNORE: "\s|\n";
PROPER_NAME
    : "[A-Z]([A-Za-z0-9_'])*"
#    : "\p{Uppercase_Letter}(\p{Letter}|\p{Mark}|\p{Number}|[_'])*"
    ;
LOWER: "[a-z_ηℏεµα][A-Za-z0-9_ηℏεµα']*";
#LOWER: "\p{Ll}_(p{L}|\p{M}|\p{N}[_'])*";
OPERATOR: "[?:\!#\$%&*<=>@\\\^\|\-~/+⊕⊖⊗⊘.🌱🌸🍒≅⤓⇥⋈]+";
STRING
    : "\"([^\\\"]*(\\.)?)*\""
    ;
MULTILINE_STRING: "\"{3}.*\"{3}";
INTEGER: "\d+";
NUMBER: "\d+\.\d+";
CHAR: "'(\\x[^']{1,2}|\\\\'|\\\\|\\.|[^']{1,2})'";
FORALL: "forall|∀";
DUBBLE_ARROW: "=>|⇒";
ARROW: "->|→";
LEFT_ARROW: "<-|←";
LEFT_DOUBLE_ARROW: "<=|⇐";
```

## Grammar

Order matter, this grammar will select the first match if multiple may match

```ebnf
module
    : [SEP]? ["module"] [whitespace]? module_name [SEP]? [INDENT]? export_list? [whitespace]* ["where"] [whitespace]*
        (import_declaration [SEP])*
        (declaration [SEP]?)*
    [EOF]?
    ;
module_name: (proper_name ["."])* proper_name;
export_list
    : ["("] [")"]
    | ["("] [whitespace]* 
        (exported_item [whitespace]* [","] [whitespace]*)* 
        exported_item [whitespace]* 
    [")"]
    ;
whitespace: SEP | INDENT | DEDENT;
exported_item
    : ["class"] proper_name
    | proper_name (["("] members? [")"])? 
    | ["module"] module_name
    | symbol
    | ["type"] symbol
    | identifier
    ;
import_declaration: ["import"] module_name "hiding"? import_list? (["as"] module_name)?;
import_list: ["("] ( import_item [","])* import_item [")"];
import_item
    : "type" symbol
    | "class" proper_name
    | symbol
    | identifier
    | proper_name ["("] members [")"]
    | proper_name
    ;
operator: OPERATOR | ".." | ":" | "-" | "?";
symbol: "(" operator ")" ;
qualified_symbol: module_name ["."] symbol ;
members
    : ".."
    | (proper_name [","])* proper_name
    ;

declaration
    : <data_declaration>
#   | newtype_declaration
#   | type_role_declaration
#   | type_signature_declaration
#   | type_declaration
    | <value_signature>
    | <value_declaration>
#   | foreign_declaration
#   | class_declaration
#   | derive_declaration
#   | instance_declaration
    ;
double_colon: "::" | "∷";
value_signature
    : identifier [double_colon] type
    ;
value_declaration
    : identifier binder_atom* guard_declaration
    ; 

binder_atom
    : "_"
    ;
 
guard_declaration
    : ["="] where_expression
#   | guarded_declaration_expression
    ;
where_expression
    : expression where?
    ;
expression 
    : expression_1 ("::" type)?
    ;
expression_1
    : (expression_2 qual_op)* expression_2
    ;
expression_2
    :(expression_3 backtick_expression)* expression_3
    ;
expression_3
    : expression_4
    | "-" expression_4
    ;
expression_4
    : (expression_5 ("@" type_atom)?)+
    ;
expression_5
    : expression_6
    | ["if"] expression ["then"] expression ["else"] expression
    | do_block
    | ado_block
    ;
expression_6: expression_7;
expression_7: expression_atom ("." identifier)*;
expression_atom
    : "_"
    | hole
    | qualified_identifier
    | identifier
    | symbol
    | qualified_symbol
    | STRING
    | boolean
    | INTEGER
    | NUMBER
    | CHAR
    | ["["] ["]"]
    | ["["] (expression [","])* expression ["]"]
    | ["{"] ["}"]
    | ["{"] (record_label [","])* record_label ["}"]
    | ["("] expression [")"]
    ;

record_label: identifier [":"] expression ;

boolean
    : "True"
    | "False"
    ;

qualified_identifier: module_name ["."] identifier;

hole: ["?"] <identifier>;

do_block : ["do"] do_statements ;
ado_block : ["ado"] do_statements ["in"] expression ;
do_statements: [INDENT] do_statement+ [DEDENT];
do_statement 
    : binder [LEFT_ARROW] expression [SEP]
    | ["let"] [INDENT] (let_binder [SEP])+ [DEDENT]
    | expression [SEP]
    ;

let_binder
    : value_signature
    | value_declaration 
    ;

binder: identifier ;

backtick_expression: "`" identifier "`";
qual_op: (module_name ["."])? OPERATOR;
where
    : "where"
    ;

data_declaration: ["data"] proper_name type_parameter* ["="]
    (data_constructor ["|"])* data_constructor ;
type_parameter: identifier ;
data_constructor: proper_name type_atom* ;
type_atom
    : "_"
    | "?" identifier
    | "Effect Unit"
    ;
type_var: identifier;
type: type_1 ("::" type)?;
type_1: [FORALL] type_var+ "." type_2
    | type_2
    ;
type_2
    : type_3 ARROW type_1
    | type_3 DUBBLE_ARROW type_1
    | type_3
    ;
type_3: type_atom;
identifier: <LOWER> | <"as"> ;
proper_name: <PROPER_NAME> | <"True"> | <"False">;
```
