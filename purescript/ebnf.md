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
DOUBLE_ARROW: "=>|⇒";
LEFT_ARROW: "<-|←";
LEFT_DOUBLE_ARROW: "<=|⇐";
LAMBDA: "[\\]";
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
operator: <OPERATOR> | <".."> | <":"> | <"-"> | <"?"> ;
symbol: "(" operator ")" ;
qualified_symbol: module_name ["."] symbol ;
boolean: "True" | "False" ;
double_colon: "::" | "∷";
identifier: <LOWER> | <"as"> | <"kind">;
proper_name: <PROPER_NAME> | <"True"> | <"False">;
qualified_proper_name
    : module_name
    | proper_name
    ;
qual_op: (module_name ["."])? operator;
qualified_identifier: (module_name ["."])? identifier;
hole: ["?"] <identifier>;
number: INTEGER | NUMBER;
string: STRING| MULTILINE_STRING ;
label: identifier | string;
```

## Module Layout

```ebnf
module
    : [SEP]? ["module"] [SEP]? module_name [SEP]? export_list? [SEP]? ["where"] [SEP]
        (import_declaration [SEP])*
        (declaration [SEP]?)*
    [EOF]
    ;
   
# Allow SEP every where in exportlist
# since it cant contain any blocks and therefore don't care about layout
export_list
    : ["("] [SEP]? [")"]
    | ["("] [SEP]? (exported_item [SEP]? [","] [SEP]?)* [SEP]? exported_item [SEP]? [")"]
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
    | "kind" proper_name
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
    | qualified_symbol
    | ["("] ARROW [")"]
    | ["("] type_1 [")"]
    | ["{"] row ["}"]
    | ["{"] ["}"]
    | ["("] row [")"]
    | ["("] [")"]
    | string
    | number
    ;
row
    : (row_label [SEP]? [","] [SEP]?)* row_label [SEP]? ("|" type)?
    | "|" type
    ;
row_label: label double_colon type;
type_var_binding_plain
    : identifier
    | "(" identifier double_colon type")"
    ;
type_var_binding
    : identifier
    | "(" identifier double_colon type")"
    | "@" identifier
    | "(" "@" identifier double_colon type")"
    ;
type: type_1 ("::" type_1)*;
type_1: ([FORALL] type_var_binding+ ["."])* type_2 ;
type_2
    : type_3 ARROW type_1
    | type_3 DOUBLE_ARROW type_1
    | type_3
    ;
type_3: (type_4 qual_op)* type_4 ;
type_4: type_atom+ | "-" INTEGER ;
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
    | [LAMBDA] binder_atom* ARROW expression 
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
    | <newtype_signature>
    | <type_role_declaration>
#   | type_signature_declaration
    | <type_signature>
    | <type_declaration>
    | <value_signature>
    | <value_declaration>
    | <foreign_declaration>
    | <foreign_data_declaration>
    | <class_signature>
    | <class_declaration>
    | <derive_declaration>
    | <derive_newtype_declaration>
    | <instance_declaration>
    | <fixity>
    ;
type_role_declaration: "type" "role" proper_name role* ;
role: "nominal" | "representational" | "phantom";
fixity
    : infix INTEGER qualified_identifier ["as"] operator
    | infix INTEGER qualified_proper_name ["as"] operator
    | infix INTEGER ["type"] qualified_proper_name ["as"] operator
    ;
infix
  : "infix"
  | "infixl"
  | "infixr"
  ;
derive_declaration: ["derive"] ["instance"] (identifier double_colon)? type;
derive_newtype_declaration: ["derive"] ["newtype"] ["instance"] (identifier double_colon)? type;
instance_declaration: ["instance"] ([identifier] double_colon)? (constraints DOUBLE_ARROW)? proper_name type_atom* ["where"] 
    [INDENT] (value_declaration [SEP])+
    [DEDENT]
    ;
instance_binding
    : identifier double_colon type
    | identifier binder_atom* guarded_declaration
    ;
class_signature: ["class"] proper_name [double_colon] type;
class_head
    :["class"] 
        # Super class
        (constraints LEFT_DOUBLE_ARROW)?
        # Class name
         proper_name type_var_binding*
        # functional dependencies
        ("|" (identifier* ARROW identifier+ [","])*  identifier* ARROW identifier+)?
    ;
class_declaration
    : class_head (["where"] [INDENT] (class_member [SEP])+ [DEDENT])?
    | class_head (["where"] class_member )?
    ;
class_member: identifier [double_colon] type;
foreign_declaration: ["foreign"] ["import"] identifier [double_colon] type;
foreign_data_declaration: ["foreign"] ["import"] ["data"] proper_name [double_colon] type;
type_signature : ["type"] proper_name double_colon type ;
type_declaration : ["type"] proper_name type_var_binding_plain* layout* ["="] type ;
newtype_signature: ["newtype"] proper_name double_colon type;
newtype_declaration: ["newtype"] proper_name type_var_binding_plain* ["="] proper_name type_atom;
value_signature : identifier [double_colon] type ;
value_declaration : identifier binder_atom* ["="] expression_where? ;
data_head_declaration: ["data"] proper_name type_var_binding_plain*;
data_declaration: ["data"] proper_name type_parameter* ["="]
    (data_constructor ["|"])* data_constructor ;
data_constructor: proper_name type_atom* ;
guarded_declaration
    : ["="] expression_where
    | guarded_declaration_expression
    ;
constraints
    : constraint
    | "(" (constraint ",")? constraint ")"
    ;
constraint
    : qualified_proper_name type_atom*
    | "(" constraint ")"
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