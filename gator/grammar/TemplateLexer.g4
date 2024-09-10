lexer grammar TemplateLexer;

//INLINE_TEMPLATE: '<template' .*? '/>';
OPEN_TEMPLATE: '<template' .*? '>';
CLOSE_TEMPLATE: '</template>';

EXEC_OPEN: '<exec>' -> pushMode(EXEC);
EXPR_OPEN: '{{' -> pushMode(EXPR);

CONTENT: '<content' WS* '/>';

OPEN_TAG: '<';
CLOSE_TAG: '>';
OPEN_SINGLE_BRACE: '{';
CLOSE_SINGLE_BRACE: '}';

TEXT: (~[<>{}])+;

WS: (' ' | '\t' | '\r'? '\n');

IDENT: [a-zA-Z] [_a-zA-Z]+;

mode EXEC;

EXEC_BODY: .*? '</exec>' -> popMode;

mode EXPR;

EXPR_BODY: .*? '}}' -> popMode;
