# Generated from gator/grammar/TemplateParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TemplateParser import TemplateParser
else:
    from TemplateParser import TemplateParser

# This class defines a complete generic visitor for a parse tree produced by TemplateParser.

class TemplateParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TemplateParser#root.
    def visitRoot(self, ctx:TemplateParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#content.
    def visitContent(self, ctx:TemplateParser.ContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#element.
    def visitElement(self, ctx:TemplateParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#template_elem.
    def visitTemplate_elem(self, ctx:TemplateParser.Template_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#content_elem.
    def visitContent_elem(self, ctx:TemplateParser.Content_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#exec_element.
    def visitExec_element(self, ctx:TemplateParser.Exec_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#expr_element.
    def visitExpr_element(self, ctx:TemplateParser.Expr_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TemplateParser#text.
    def visitText(self, ctx:TemplateParser.TextContext):
        return self.visitChildren(ctx)



del TemplateParser