parser grammar TemplateParser;
options { tokenVocab=TemplateLexer; }

root: content EOF;

content
    : text
    | text? (element text?)+;

element
    : template_elem
    | content_elem
    | exec_element
    | expr_element;

template_elem
    : OPEN_TEMPLATE text? (element text?)* CLOSE_TEMPLATE
    ;

content_elem: CONTENT;

exec_element: EXEC_OPEN EXEC_BODY;

expr_element: EXPR_OPEN EXPR_BODY;


text
    : TEXT
    | TEXT? ((OPEN_TAG | CLOSE_TAG | OPEN_SINGLE_BRACE | CLOSE_SINGLE_BRACE) TEXT?)+;
