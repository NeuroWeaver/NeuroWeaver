grammar AbstractDomain;

/* scanner tokens */
ABSTRACT : 'abstract';
DOMAIN : 'domain';
CAPABILITY : 'capability';
INPUT : 'input';
OUTPUT : 'output';
STATE : 'state';
PARAM : 'param';
IMPORT : 'import';
AS : 'as';
LEFT_CURLY : '{';
RIGHT_CURLY : '}';
LEFT_PAREN : '(';
RIGHT_PAREN : ')';
COMMA : ',';
DEFAULT : 'default';
REFERENCE : 'reference';
LANGUAGE : 'language';
VERBATIM : 'verbatim';
CODE : 'code';
FILE : 'file';

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
        : import_stmt_list domain_def
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
        : '.' ID namespace_tail
        | // epsilon
        ;

domain_def
        : ABSTRACT DOMAIN ID block
        | // epsilon
        ;

block
        : LEFT_CURLY default_stmt capability_list RIGHT_CURLY
        ;

default_stmt
        : DEFAULT REFERENCE ID
        ;

capability_list
        : capability*
        ;

capability
        : CAPABILITY ID LEFT_PAREN params RIGHT_PAREN
        ;

params
        : capability_arg capability_arg_list
        | // epsilon
        ;

capability_arg
        : memory_interface data_type var
        | // epsilon
        ;

capability_arg_list
        : COMMA capability_arg capability_arg_list
        | // epsilon
        ;

memory_interface
        : INPUT
        | OUTPUT
        | STATE
        | PARAM
        ;

data_type
        : ID
        ;

var
        : var_id
        ;

var_id
        : ID
        ;

// ID
//         : [a-z]+            // match lower-case identifiers
//         ;
// WS
//         : [ \t\r\n]+ -> skip  // skip spaces, tabs, newlines
//         ;
