## Tokens

these are the tokens that needs regexp the tokens that are string constants can be found within the grammar. The current
lexer don't seam to understand unicode groups, therefore they are only kept as comments.

```ebnf
LINE_COMMENT: "--[^\n]*\n?";
MULTILINE_COMMENT: "{-([^-]*(-[^}])?)*-}";
LINE_INDENT: "\n[\s]*";
IGNORE: "\s|\n";
IGNORE: "\s|\n";
PROPER_NAME
    : "[A-Z]([A-Za-z0-9_'])*"
#    : "\p{Uppercase_Letter}(\p{Letter}|\p{Mark}|\p{Number}|[_'])*"
    ;
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
# let lower match after all keywords and ad them back efter
LOWER: "[a-z_ηℏεµα]([A-Za-z0-9_ηℏεµα']|\xca\x94)*";
#LOWER: "\p{Ll}_(p{L}|\p{M}|\p{N}[_'])*";
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
identifier: <LOWER> | <"as">;
proper_name: <PROPER_NAME> | <"True"> | <"False">;
qualified_proper_name
    : module_name
    | proper_name
    ;
qual_op: (module_name ["."])? OPERATOR;
qualified_identifier: (module_name ["."])? identifier;
hole: ["?"] <identifier>;
number: INTEGER | NUMBER;
```
## Module Layout
```ebnf
module
    : [SEP]? ["module"] module_name export_list? ["where"] [SEP]
        (import_declaration [SEP])*
        (declaration [SEP]?)*
    [EOF]
    ;
export_list
    : ["("] [")"]
    | ["("] (exported_item [","])* exported_item [")"]
    ;
layout: SEP | INDENT | DEDENT;
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
    | qualified_proper_name
    | identifier
    | ["("] type_1 [")"]
    | ["{"] row ["}"]
    | ["{"] ["}"]
    | ["("] row [")"]
    | ["("] [")"]
    ;
row
    : (row_lable [SEP]? [","] [SEP]?)* row_lable [SEP]? ("|" type)?
    | "|" type
    ;
row_lable: identifier double_colon type;
type_var: identifier;
type: type_1 ("::" type)?;
type_1: ([FORALL] type_var+ ["."])? type_2 ;
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
    | ["do"] do_statements
    | ["ado"] do_statement ["in"] expression
    | ["ado"] do_statements [SEP] ["in"] expression
    | ["let"] [INDENT] (let_binding [SEP])+ [DEDENT]
    | ["case"] (expression [","])* expression ["of"]
        [INDENT] ((binder [","])* binder ARROW expression [SEP])+
        [DEDENT]
    ;
expression_6 : expression_7 ("{" ((record_update [","])* record_update)? "}")? ;
expression_7: expression_atom ("." identifier)*;
expression_atom
    : "_"
    | hole
    | qualified_identifier
    | qualified_symbol
# qualified_proper_name matches the beginning of 
# all qualified so it must apear after
    | qualified_proper_name
    | boolean
    | CHAR
    | STRING
    | INTEGER
    | NUMBER
    | ["["] ["]"]
    | ["["] (expression [","] )* expression ["]"]
    | ["{"] ["}"]
    | ["{"] (record_label [","]) * record_label ["}"]
    | ["("] expression [")"]
    | ["("] expression [")"]
    ;

record_label: identifier [":"] expression ;
record_update
    : identifier ["="] expression
    | identifier ["{"] (record_update [","])* record_update ["}"]
    ;
do_statements
    : [INDENT] (do_statement [SEP])+ [DEDENT]
    | do_statement
    ;
do_statement 
    : binder [LEFT_ARROW] expression
    | ["let"] [INDENT] (let_binding [SEP])+ [DEDENT]
    | expression
    ;

let_binding
    : value_signature
    | value_declaration 
    ;


backtick_expression: "`" identifier "`";
guarded_declaration_expression
    : guard ["="] expression_where
    ;
expression_where
    : expression ["where"]
        [INDENT] (let_binding [SEP])+
        [DEDENT] 
    | expression
    ;
guard: ["|"] (pattern_guard [","])* pattern_guard; 
pattern_guard:(binder LEFT_ARROW)? expression;
```

## Declarations
```ebnf
declaration
    : <data_declaration>
    | <data_head_declaration>
    | <newtype_declaration>
#   | type_role_declaration
#   | type_signature_declaration
    | <type_declaration>
    | <value_signature>
    | <value_declaration>
    | <foreign_declaration>
    | <foreign_data_declaration>
    | <class_declaration>
#    | <class_signature_declaration>
    | <derive_declaration>
    | <instance_declaration>
    ;
derive_declaration: ["derive"] ["instance"] (identifier double_colon)? type;
instance_declaration: ["instance"] ([identifier] double_colon)? proper_name type_atom* ["where"] 
    [INDENT] (value_declaration [SEP])+
    [DEDENT]
    ;
instance_binding
    : identifier double_colon type
    | identifier binder_atom* guarded_declaration
    ;
#class_signature_declaration: ["class"] proper_name [double_colon] type; 
class_declaration
    : ["class"] 
        # Super class
        (proper_name type_var* LEFT_DOUBLE_ARROW)?
        # Class name
         proper_name type_var*
        # functional dependencies
        ("|" type_var ARROW type_var )?
    ["where"] 
    [INDENT] (class_member [SEP])+
    [DEDENT]
    ;
class_member: identifier [double_colon] type;
foreign_declaration: ["foreign"] ["import"] identifier [double_colon] type;
foreign_data_declaration: ["foreign"] ["import"] ["data"] proper_name [double_colon] type;
type_declaration
    : ["type"] proper_name binder_atom* layout* ["="] type
    ;
newtype_declaration: ["newtype"] proper_name binder_atom* ["="] proper_name type_atom;
value_signature : identifier [double_colon] type ;
value_declaration : identifier binder_atom* ["="] expression_where? ;
data_head_declaration: ["data"] proper_name type_parameter*;
data_declaration: ["data"] proper_name type_parameter* ["="]
    (data_constructor ["|"])* data_constructor ;
data_constructor: proper_name type_atom* ;
guarded_declaration
    : ["="] expression_where
    | guarded_declaration_expression
    ;
```

## Binders

```ebnf

binder_atom
    : "_"
    | identifier ("@" binder_atom)?
    | qualified_proper_name
    | boolean
    | CHAR
    | STRING
    | number
    | MULTILINE_STRING
    | ["{"] ((record_binder [","])* record_binder)? ["}"]
    | ["["] ((binder [","])* binder)? ["]"]
    | ["("] binder [")"]
    ;
record_binder : identifier ([":"] binder)? ;
binder: binder_1 (double_colon type)? ;
binder_1: (binder_2 qual_op)* binder_2 ;
binder_2: "-" number | binder_atom+ ;
```