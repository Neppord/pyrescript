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
LOWER: "[a-z_ηℏεµα]([A-Za-z0-9_ηℏεµα']|\xca\x94)*";
#LOWER: "\p{Ll}_(p{L}|\p{M}|\p{N}[_'])*";
ARROW: "->|→";
STRING
    : "\"([^\\\"]*(\\.)?)*\""
    ;
MULTILINE_STRING: "\"{3}.*\"{3}";
INTEGER: "\d+";
NUMBER: "\d+\.\d+";
CHAR: "'(\\x[^']{1,4}|\\\\'|\\\\|\\.|[^']{1,2}|\xe2\x99\xa5|☺|\xe6\x9c\xac|\xe3\x80\x80|日|２|③|—|語)'";
FORALL: "forall|∀";
DUBBLE_ARROW: "=>|⇒";
LEFT_ARROW: "<-|←";
LEFT_DOUBLE_ARROW: "<=|⇐";
# let operators match last and then read them in the `operator` definition
OPERATOR: "([?:\!#\$%&*<=>@\\\^\|\-~/+⊕⊖⊗⊘.🌱🌸🍒≅⤓⇥⋈]|\xe2\x8a\xa0)+";
```

## Grammar

Order matter, this grammar will select the first match if multiple may match

## Atoms, Literals and Names
```ebnf
module_name: (proper_name ["."])* proper_name;
operator: OPERATOR | ".." | ":" | "-" | "?" ;
symbol: "(" operator ")" ;
qualified_symbol: module_name ["."] symbol ;
boolean: "True" | "False" ;
double_colon: "::" | "∷";
identifier: <LOWER> | <"as"> ;
proper_name: <PROPER_NAME> | <"True"> | <"False">;
qual_op: (module_name ["."])? OPERATOR;
qualified_identifier: module_name ["."] identifier;
hole: ["?"] <identifier>;
```
## Module Layout
```ebnf
module
    : [SEP]? ["module"] [whitespace]? module_name [SEP]? [INDENT]? export_list? [whitespace]* ["where"] [whitespace]*
        (import_declaration [SEP])*
        (declaration [SEP]?)*
    [EOF]
    ;
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
```
## Import declaration
```ebnf
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
members
    : ".."
    | (proper_name [","])* proper_name
    ;
```

## Type
```ebnf
type_parameter: identifier ;
type_atom
    : "_"
    | "?" identifier
    | proper_name
    | identifier
    | ["("] type_1 [")"]
    | ["{"] row ["}"]
    | ["{"] ["}"]
    ;
row: (row_lable [","])* row_lable;
row_lable: identifier double_colon type;
type_var: identifier;
type: type_1 ("::" type)?;
type_1: ([FORALL] type_var+ ".")? type_2 ;
type_2
    : type_3 ARROW type_1
    | type_3 DUBBLE_ARROW type_1
    | type_3
    ;
type_3: (type_4 qual_op)* type_4 ;
type_4: type_5 | "-" INTEGER ;
type_5: type_atom+ ;
```


## Expression
```ebnf
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
    
guard_declaration
    : ["="] where_expression
#   | guarded_declaration_expression
    ;


record_label: identifier [":"] expression ;

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


backtick_expression: "`" identifier "`";
where: "where" ;

```

## Declarations
```ebnf
declaration
    : <data_declaration>
    | <newtype_declaration>
#   | type_role_declaration
#   | type_signature_declaration
    | <type_declaration>
    | <value_signature>
    | <value_declaration>
    | <foreign_declaration>
    | <class_declaration>
#   | derive_declaration
    | <instance_declaration>
    ;
instance_declaration: ["instance"] proper_name type_atom*  ["where"] 
    [INDENT] (value_declaration [SEP])+
    [DEDENT]
    ;
class_declaration: ["class"] proper_name type_var*  ["where"] 
    [INDENT] (class_member [SEP])+
    [DEDENT]
    ;
class_member: identifier double_colon type;
foreign_declaration: "foreign" "import" identifier double_colon type;
type_declaration: ["type"] proper_name binder_atom* "=" type;
newtype_declaration: ["newtype"] proper_name binder_atom* "=" proper_name type_atom;
value_signature : identifier [double_colon] type ;
value_declaration : identifier binder_atom* guard_declaration ; 

data_declaration: ["data"] proper_name type_parameter* ["="]
    (data_constructor ["|"])* data_constructor ;
data_constructor: proper_name type_atom* ;
```

## Binders

```ebnf

binder_atom
    : "_"
    | proper_name
    | identifier
    ;
 
binder: binder_atom ;
```