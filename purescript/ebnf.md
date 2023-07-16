## Tokens
these are the tokens that needs regexp the tokens that are string constants can be found within the grammar. The current lexer don't seam to understand unicode groups, therefore they are only kept as comments.
```ebnf
LINE_INDENT: "\n[ \t]*";
IGNORE: "[ \t\f\r\n]";
PROPER_NAME
    : "[A-Z]([A-Za-z0-9_'])*"
#    : "\p{Uppercase_Letter}(\p{Letter}|\p{Mark}|\p{Number}|[_'])*"
    ;
LOWER: "[a-z_]([A-Za-z0-9_'])*";
#LOWER: "\p{Ll}_(p{L}|\p{M}|\p{N}[_'])*";
OPERATOR: "\p{S}+";
STRING: "\"[^\"]*\"";
```
## Grammar
```ebnf
module
    : ["module"] module_name export_list? ["where"] [SEP]
        (import_declaration [SEP])*
        (declaration [SEP]?)*
    [EOF]?
    ;
module_name: (PROPER_NAME ["."])* PROPER_NAME;
export_list: "(" (exported_item ",")* exported_item ")";
exported_item
    : ["class"] PROPER_NAME
    | PROPER_NAME ["("] members [")"] 
    | ["module"] module_name
    | symbol
    | ["type"] symbol
    | identifier
    ;
    
import_declaration: ["import"] module_name "hiding"? import_list? (["as"] module_name)?;
import_list: ["("] ( import_item [","])* import_item [")"];
import_item
    : "type" symbol
    | "class" PROPER_NAME
    | symbol
    | identifier
    | PROPER_NAME ["("] members [")"]
    | PROPER_NAME
    ;
symbol: "(" OPERATOR ")" ;
members
    : ".."
    | (PROPER_NAME [","])* PROPER_NAME
    ;

declaration
    : data_declaration
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
value_signature
    : identifier "::" type
    ;
type: "Effect Unit";
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
    : "-"? expression_4
    ;
expression_4: expression_5* expression_5;
expression_5
    : expression_7
    | do_block
    ;
expression_7: expression_atom ("." identifier)*;
expression_atom
    : identifier
    | STRING
    ;

do_block
    : ["do"] do_statement
    | ["do"] [INDENT] (do_statement [SEP])+ [DEDENT]
    ;
do_statement : expression ;

backtick_expression: "`" identifier "`";
qual_op: (module_name ["."])? OPERATOR;
where
    : "where"
    ;

data_declaration: ["data"] PROPER_NAME type_parameter* ["="]
    (data_constructor ["|"])* data_constructor ;
type_parameter: identifier ;
data_constructor: PROPER_NAME type_atom* ;
type_atom
    : "_"
    | "?" identifier
    ;
identifier: LOWER;
```
