grammar Esl;

/* scanner tokens */
ENGINE : 'engine';
CAPABILITY : 'capability';
IMPORT : 'import';
AS : 'as';
LEFT_CURLY : '{';
RIGHT_CURLY : '}';
LEFT_PAREN : '(';
RIGHT_PAREN : ')';
COMMA : ',';
DEFAULT : 'default';
LANGUAGE : 'language';
RUNTIME_COST: 'runtime_cost';
VERBATIM : 'verbatim';
CODE : 'code';
FILE : 'file';
TOUCHES : 'touches';
IMPLEMENTS : 'implements';
INTERFACE : 'interface';
ASSIGN : '=';
KLEENE_STAR : '*';
COLON: ':';
LEFT_BRACK : '[';
RIGHT_BRACK : ']';

/* var name */
ID
    : (LOWER | UPPER) (LOWER | UPPER | DIGIT | '_')*
    ;

fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
fragment DIGIT: '0'..'9';

WHITESPACE
    : (' ' | '\t' | '\n' | '\r')+ -> skip
    ;

COMMENT
//    : '/*' .*? '*/'
    : '//' .+? ('\n' | EOF) -> skip
    ;

INTLIT
    : '0'
    | '1'..'9' (DIGIT)*
    ;


/* parser rules */
start
        : import_stmt_list engine_def
        ;

import_stmt_list
        : import_stmt*
        ;

import_stmt
        : IMPORT namespace import_stmt_tail
        ;

import_stmt_tail
        : AS ID
        | // epsilon
        ;

namespace
        : ID namespace_tail
        ;

namespace_tail
        : '.' id_or_star namespace_tail
        | // epsilon
        ;

id_or_star
        : ID
        | KLEENE_STAR
        ;

engine_def
        : ENGINE ID impl block
        | // epsilon
        ;

impl
        : IMPLEMENTS ID
        | // epsilon
        ;

block
        : LEFT_CURLY interface_decl_list capability_list RIGHT_CURLY
        ;

interface_decl_list
        : interface_decl*
        ;

interface_decl
        : INTERFACE ID ASSIGN namespace
        ;

capability_list
        : capability*
        ;

capability
        : CAPABILITY ID LEFT_PAREN params RIGHT_PAREN touch cap_block
        ;

params
        : capability_arg capability_arg_list
        | // epsilon
        ;

capability_arg
        : memory_interface data_type var
        | param_interface ID ASSIGN LEFT_BRACK literals RIGHT_BRACK
        | // epsilon
        ;

capability_arg_list
        : COMMA capability_arg capability_arg_list
        | // epsilon
        ;

param_interface
        : ID
        ;

literals
        : literal literal_list
        | // epsilon
        ;

literal
        : INTLIT
//        | '"' ID '"'
        | STRING
        ;

literal_list
        : COMMA literal literal_list
        | // epsilon
        ;

memory_interface
        : ID
        ;

data_type
        : ID data_type_tail
        ;

data_type_tail
        : LEFT_BRACK RIGHT_BRACK data_type_tail
        | // epsilon
        ;

var
        : var_id
        ;

var_id
        : ID
        ;

touch
        : TOUCHES ID
        | // epsilon
        ;

cap_block
        : LEFT_CURLY specs RIGHT_CURLY
        ;

specs
        : spec spec_list
        ;

spec
        : attr COLON attr_val
        | // epsilon
        ;

spec_list
        : COMMA spec spec_list
        | // epsilon
        ;

attr
        : qualifier attr_id
        | // epsilon
        ;

attr_id
        : LANGUAGE
        | CODE
        | FILE
        | RUNTIME_COST
        ;

qualifier
        : VERBATIM
        | // epsilon
        ;

attr_val
        : ID
        | STRING
        | INTLIT
        ;

STRING
 : STRING_LITERAL
 | BYTES_LITERAL
 ;

/// stringliteral   ::=  [stringprefix](shortstring | longstring)
/// stringprefix    ::=  "r" | "u" | "R" | "U" | "f" | "F"
///                      | "fr" | "Fr" | "fR" | "FR" | "rf" | "rF" | "Rf" | "RF"
STRING_LITERAL
 : ( [rR] | [uU] | [fF] | ( [fF] [rR] ) | ( [rR] [fF] ) )? ( SHORT_STRING | LONG_STRING )
 ;


/// bytesliteral   ::=  bytesprefix(shortbytes | longbytes)
/// bytesprefix    ::=  "b" | "B" | "br" | "Br" | "bR" | "BR" | "rb" | "rB" | "Rb" | "RB"
BYTES_LITERAL
 : ( [bB] | ( [bB] [rR] ) | ( [rR] [bB] ) ) ( SHORT_BYTES | LONG_BYTES )
 ;

/// shortstring     ::=  "'" shortstringitem* "'" | '"' shortstringitem* '"'
/// shortstringitem ::=  shortstringchar | stringescapeseq
/// shortstringchar ::=  <any source character except "\" or newline or the quote>
fragment SHORT_STRING
 : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\''
 | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"'
 ;
/// longstring      ::=  "'''" longstringitem* "'''" | '"""' longstringitem* '"""'
fragment LONG_STRING
 : '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
 | '"""' LONG_STRING_ITEM*? '"""'
 ;

/// longstringitem  ::=  longstringchar | stringescapeseq
fragment LONG_STRING_ITEM
 : LONG_STRING_CHAR
 | STRING_ESCAPE_SEQ
 ;

/// longstringchar  ::=  <any source character except "\">
fragment LONG_STRING_CHAR
 : ~'\\'
 ;

/// stringescapeseq ::=  "\" <any source character>
fragment STRING_ESCAPE_SEQ
 : '\\' .
 | '\\' NEWLINE
 ;

NEWLINE
        : ( '\r'? '\n' | '\r' | '\f' )
        ;
/// shortbytes     ::=  "'" shortbytesitem* "'" | '"' shortbytesitem* '"'
/// shortbytesitem ::=  shortbyteschar | bytesescapeseq
fragment SHORT_BYTES
 : '\'' ( SHORT_BYTES_CHAR_NO_SINGLE_QUOTE | BYTES_ESCAPE_SEQ )* '\''
 | '"' ( SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE | BYTES_ESCAPE_SEQ )* '"'
 ;

/// longbytes      ::=  "'''" longbytesitem* "'''" | '"""' longbytesitem* '"""'
fragment LONG_BYTES
 : '\'\'\'' LONG_BYTES_ITEM*? '\'\'\''
 | '"""' LONG_BYTES_ITEM*? '"""'
 ;

/// longbytesitem  ::=  longbyteschar | bytesescapeseq
fragment LONG_BYTES_ITEM
 : LONG_BYTES_CHAR
 | BYTES_ESCAPE_SEQ
 ;

/// shortbyteschar ::=  <any ASCII character except "\" or newline or the quote>
fragment SHORT_BYTES_CHAR_NO_SINGLE_QUOTE
 : [\u0000-\u0009]
 | [\u000B-\u000C]
 | [\u000E-\u0026]
 | [\u0028-\u005B]
 | [\u005D-\u007F]
 ;

fragment SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE
 : [\u0000-\u0009]
 | [\u000B-\u000C]
 | [\u000E-\u0021]
 | [\u0023-\u005B]
 | [\u005D-\u007F]
 ;

/// longbyteschar  ::=  <any ASCII character except "\">
fragment LONG_BYTES_CHAR
 : [\u0000-\u005B]
 | [\u005D-\u007F]
 ;

/// bytesescapeseq ::=  "\" <any ASCII character>
fragment BYTES_ESCAPE_SEQ
 : '\\' [\u0000-\u007F]
 ;

// string_literal
//         : '"' string_characters? '"'
//         ;

// fragment
// string_characters
//         :	string_character+
//         ;

// fragment
// string_character
//         :	[a-zA-Z_]
//         ;
