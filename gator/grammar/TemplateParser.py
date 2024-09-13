# Generated from gator/grammar/TemplateParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,1,0,1,1,1,1,3,1,22,8,1,1,1,1,1,3,1,26,8,1,4,1,
        28,8,1,11,1,12,1,29,3,1,32,8,1,1,2,1,2,1,2,1,2,3,2,38,8,2,1,3,1,
        3,3,3,42,8,3,1,3,1,3,1,4,1,4,1,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,3,7,
        56,8,7,1,7,1,7,3,7,60,8,7,4,7,62,8,7,11,7,12,7,63,3,7,66,8,7,1,7,
        0,0,8,0,2,4,6,8,10,12,14,0,1,1,0,6,9,71,0,16,1,0,0,0,2,31,1,0,0,
        0,4,37,1,0,0,0,6,39,1,0,0,0,8,45,1,0,0,0,10,47,1,0,0,0,12,50,1,0,
        0,0,14,65,1,0,0,0,16,17,3,2,1,0,17,18,5,0,0,1,18,1,1,0,0,0,19,32,
        3,14,7,0,20,22,3,14,7,0,21,20,1,0,0,0,21,22,1,0,0,0,22,27,1,0,0,
        0,23,25,3,4,2,0,24,26,3,14,7,0,25,24,1,0,0,0,25,26,1,0,0,0,26,28,
        1,0,0,0,27,23,1,0,0,0,28,29,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,
        30,32,1,0,0,0,31,19,1,0,0,0,31,21,1,0,0,0,32,3,1,0,0,0,33,38,3,6,
        3,0,34,38,3,8,4,0,35,38,3,10,5,0,36,38,3,12,6,0,37,33,1,0,0,0,37,
        34,1,0,0,0,37,35,1,0,0,0,37,36,1,0,0,0,38,5,1,0,0,0,39,41,5,1,0,
        0,40,42,3,2,1,0,41,40,1,0,0,0,41,42,1,0,0,0,42,43,1,0,0,0,43,44,
        5,2,0,0,44,7,1,0,0,0,45,46,5,5,0,0,46,9,1,0,0,0,47,48,5,3,0,0,48,
        49,5,13,0,0,49,11,1,0,0,0,50,51,5,4,0,0,51,52,5,14,0,0,52,13,1,0,
        0,0,53,66,5,10,0,0,54,56,5,10,0,0,55,54,1,0,0,0,55,56,1,0,0,0,56,
        61,1,0,0,0,57,59,7,0,0,0,58,60,5,10,0,0,59,58,1,0,0,0,59,60,1,0,
        0,0,60,62,1,0,0,0,61,57,1,0,0,0,62,63,1,0,0,0,63,61,1,0,0,0,63,64,
        1,0,0,0,64,66,1,0,0,0,65,53,1,0,0,0,65,55,1,0,0,0,66,15,1,0,0,0,
        10,21,25,29,31,37,41,55,59,63,65
    ]

class TemplateParser ( Parser ):

    grammarFileName = "TemplateParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'</template>'", "'<exec>'", 
                     "'{{'", "<INVALID>", "'<'", "'>'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "OPEN_TEMPLATE", "CLOSE_TEMPLATE", "EXEC_OPEN", 
                      "EXPR_OPEN", "CONTENT", "OPEN_TAG", "CLOSE_TAG", "OPEN_SINGLE_BRACE", 
                      "CLOSE_SINGLE_BRACE", "TEXT", "WS", "IDENT", "EXEC_BODY", 
                      "EXPR_BODY" ]

    RULE_root = 0
    RULE_content = 1
    RULE_element = 2
    RULE_template_elem = 3
    RULE_content_elem = 4
    RULE_exec_element = 5
    RULE_expr_element = 6
    RULE_text = 7

    ruleNames =  [ "root", "content", "element", "template_elem", "content_elem", 
                   "exec_element", "expr_element", "text" ]

    EOF = Token.EOF
    OPEN_TEMPLATE=1
    CLOSE_TEMPLATE=2
    EXEC_OPEN=3
    EXPR_OPEN=4
    CONTENT=5
    OPEN_TAG=6
    CLOSE_TAG=7
    OPEN_SINGLE_BRACE=8
    CLOSE_SINGLE_BRACE=9
    TEXT=10
    WS=11
    IDENT=12
    EXEC_BODY=13
    EXPR_BODY=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def content(self):
            return self.getTypedRuleContext(TemplateParser.ContentContext,0)


        def EOF(self):
            return self.getToken(TemplateParser.EOF, 0)

        def getRuleIndex(self):
            return TemplateParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = TemplateParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.content()
            self.state = 17
            self.match(TemplateParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def text(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TemplateParser.TextContext)
            else:
                return self.getTypedRuleContext(TemplateParser.TextContext,i)


        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TemplateParser.ElementContext)
            else:
                return self.getTypedRuleContext(TemplateParser.ElementContext,i)


        def getRuleIndex(self):
            return TemplateParser.RULE_content

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContent" ):
                return visitor.visitContent(self)
            else:
                return visitor.visitChildren(self)




    def content(self):

        localctx = TemplateParser.ContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_content)
        self._la = 0 # Token type
        try:
            self.state = 31
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 19
                self.text()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1984) != 0):
                    self.state = 20
                    self.text()


                self.state = 27 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 23
                    self.element()
                    self.state = 25
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1984) != 0):
                        self.state = 24
                        self.text()


                    self.state = 29 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 58) != 0)):
                        break

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def template_elem(self):
            return self.getTypedRuleContext(TemplateParser.Template_elemContext,0)


        def content_elem(self):
            return self.getTypedRuleContext(TemplateParser.Content_elemContext,0)


        def exec_element(self):
            return self.getTypedRuleContext(TemplateParser.Exec_elementContext,0)


        def expr_element(self):
            return self.getTypedRuleContext(TemplateParser.Expr_elementContext,0)


        def getRuleIndex(self):
            return TemplateParser.RULE_element

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElement" ):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)




    def element(self):

        localctx = TemplateParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_element)
        try:
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 33
                self.template_elem()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 34
                self.content_elem()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 35
                self.exec_element()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 36
                self.expr_element()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Template_elemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPEN_TEMPLATE(self):
            return self.getToken(TemplateParser.OPEN_TEMPLATE, 0)

        def CLOSE_TEMPLATE(self):
            return self.getToken(TemplateParser.CLOSE_TEMPLATE, 0)

        def content(self):
            return self.getTypedRuleContext(TemplateParser.ContentContext,0)


        def getRuleIndex(self):
            return TemplateParser.RULE_template_elem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemplate_elem" ):
                return visitor.visitTemplate_elem(self)
            else:
                return visitor.visitChildren(self)




    def template_elem(self):

        localctx = TemplateParser.Template_elemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_template_elem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(TemplateParser.OPEN_TEMPLATE)
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2042) != 0):
                self.state = 40
                self.content()


            self.state = 43
            self.match(TemplateParser.CLOSE_TEMPLATE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Content_elemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTENT(self):
            return self.getToken(TemplateParser.CONTENT, 0)

        def getRuleIndex(self):
            return TemplateParser.RULE_content_elem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContent_elem" ):
                return visitor.visitContent_elem(self)
            else:
                return visitor.visitChildren(self)




    def content_elem(self):

        localctx = TemplateParser.Content_elemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_content_elem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(TemplateParser.CONTENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Exec_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXEC_OPEN(self):
            return self.getToken(TemplateParser.EXEC_OPEN, 0)

        def EXEC_BODY(self):
            return self.getToken(TemplateParser.EXEC_BODY, 0)

        def getRuleIndex(self):
            return TemplateParser.RULE_exec_element

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExec_element" ):
                return visitor.visitExec_element(self)
            else:
                return visitor.visitChildren(self)




    def exec_element(self):

        localctx = TemplateParser.Exec_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_exec_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(TemplateParser.EXEC_OPEN)
            self.state = 48
            self.match(TemplateParser.EXEC_BODY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expr_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXPR_OPEN(self):
            return self.getToken(TemplateParser.EXPR_OPEN, 0)

        def EXPR_BODY(self):
            return self.getToken(TemplateParser.EXPR_BODY, 0)

        def getRuleIndex(self):
            return TemplateParser.RULE_expr_element

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_element" ):
                return visitor.visitExpr_element(self)
            else:
                return visitor.visitChildren(self)




    def expr_element(self):

        localctx = TemplateParser.Expr_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_expr_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(TemplateParser.EXPR_OPEN)
            self.state = 51
            self.match(TemplateParser.EXPR_BODY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(TemplateParser.TEXT)
            else:
                return self.getToken(TemplateParser.TEXT, i)

        def OPEN_TAG(self, i:int=None):
            if i is None:
                return self.getTokens(TemplateParser.OPEN_TAG)
            else:
                return self.getToken(TemplateParser.OPEN_TAG, i)

        def CLOSE_TAG(self, i:int=None):
            if i is None:
                return self.getTokens(TemplateParser.CLOSE_TAG)
            else:
                return self.getToken(TemplateParser.CLOSE_TAG, i)

        def OPEN_SINGLE_BRACE(self, i:int=None):
            if i is None:
                return self.getTokens(TemplateParser.OPEN_SINGLE_BRACE)
            else:
                return self.getToken(TemplateParser.OPEN_SINGLE_BRACE, i)

        def CLOSE_SINGLE_BRACE(self, i:int=None):
            if i is None:
                return self.getTokens(TemplateParser.CLOSE_SINGLE_BRACE)
            else:
                return self.getToken(TemplateParser.CLOSE_SINGLE_BRACE, i)

        def getRuleIndex(self):
            return TemplateParser.RULE_text

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitText" ):
                return visitor.visitText(self)
            else:
                return visitor.visitChildren(self)




    def text(self):

        localctx = TemplateParser.TextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_text)
        self._la = 0 # Token type
        try:
            self.state = 65
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.match(TemplateParser.TEXT)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==10:
                    self.state = 54
                    self.match(TemplateParser.TEXT)


                self.state = 61 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 57
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 960) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 59
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==10:
                        self.state = 58
                        self.match(TemplateParser.TEXT)


                    self.state = 63 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 960) != 0)):
                        break

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





