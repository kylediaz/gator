from gator.util import ScopedEnv, StringBuffer
import gator.executor

from pathlib import Path
from typing import Dict, List
from abc import abstractmethod
import re

from antlr4 import *
from gator.grammar.TemplateLexer import TemplateLexer
from gator.grammar.TemplateParser import TemplateParser
import gator.grammar.TemplateParserVisitor


TEMPLATE_NAME_KEY="t"
CONTENT='content'
ARGS='args'


class Environment:
    var: ScopedEnv
    template: Dict
    def __init__(self):
        self.var = ScopedEnv()
        self.template = dict()
    def __repr__(self) -> str:
        return f'Environment({repr(self.var)}, {repr(self.template.keys())})'

class Node:

    @abstractmethod
    def get_children(self) -> List:
        return []

    @abstractmethod
    def render(self, o: StringBuffer, env: Environment) -> None:
        pass

class TextNode(Node):
    content: str
    def __init__(self, content):
        self.content = content

    def render(self, o: StringBuffer, env: Environment) -> None:
        o.append(self.content)


class TemplateContent(Node):
    elements: List
    def __init__(self, elements: List):
        self.elements = elements

    def get_children(self) -> List:
        return self.elements
    def render(self, o: StringBuffer, env: Environment) -> None:
        for e in self.elements:
            e.render(o, env)

    def __str__(self) -> str:
        return "\n".join(map(str, self.elements))
    def __repr__(self) -> str:
        return str(self)

class TemplateNode(Node):
    args: Dict
    content: TemplateContent
    def __init__(self, args: Dict, content: TemplateContent):
        self.args = args
        self.content = content

    def render(self, o: StringBuffer, env: Environment) -> None:
        if self.content:
            b = StringBuffer()
            content = self.content.render(b, env)
            content = b.flush()
        else:
            content = None

        template_name = self.args[TEMPLATE_NAME_KEY]
        template = env.template[template_name]
        env.var.push()
        env.var.update(self.args)
        template.render_with_content(o, env, content)
        env.var.pop()

    def __str__(self) -> str:
        return f'<template {self.args}>' + str(self.content) + '</template>'
    def __repr__(self) -> str:
        return str(self)

class ExecNode(Node):
    inner: str
    def __init__(self, inner: str):
        self.inner = inner

    def render(self, o: StringBuffer, env: Environment):
        try:
            res = gator.executor.exec(self.inner, env)
            o.append(res)
        except SyntaxError as e:
            raise SyntaxError(f"Error when executing {self.inner}: {e}")

    def __str__(self) -> str:
        return f'<exec>{self.inner}</exec>'
    def __repr__(self) -> str:
        return str(self)

class ExprNode(Node):
    inner: str
    def __init__(self, inner: str):
        self.inner = inner

    def render(self, o: StringBuffer, env: Environment):
        try:
            res = gator.executor.eval(self.inner, env)
            o.append(res)
        except SyntaxError as e:
            raise SyntaxError(f"Error when evaluating {self.inner}: {e}")

    def __str__(self) -> str:
        return '{{' + str(self.inner) + '}}'
    def __repr__(self) -> str:
        return str(self)

class ContentNode(Node):

    def render(self, o: StringBuffer, env: Environment):
        if "content" in env.var:
            o.append(env.var["content"])
        else:
            print("[WARNING] Tried to print content but no content given to template")

    def __str__(self) -> str:
        return '<content/>'
    def __repr__(self) -> str:
        return str(self)

def preprocess_code(code: str) -> str:
    code = re.sub(r'\$(\w+)', r'env.var["\1"]', code)
    return code

class TemplateGenerator(ParseTreeVisitor):

    def visitRoot(self, ctx:TemplateParser.RootContext):
        content = self.visitContent(ctx.getChild(0))
        return Template(content)

    def visitContent(self, ctx:TemplateParser.ContentContext):
        output = []
        str_builder = []
        for child in ctx.getChildren():
            if type(child) == TemplateParser.TextContext:
                str_builder.append(child.getText())
            elif str_builder:
                text = "".join(str_builder)
                output.append(TextNode(text))
                str_builder.clear()
            if type(child) == TemplateParser.ElementContext:
                output.append(self.visitElement(child))

        if str_builder:
            text = "".join(str_builder)
            output.append(TextNode(text))
            str_builder.clear()

        return TemplateContent(output)


    def visitElement(self, ctx:TemplateParser.ElementContext):
        child = ctx.getChild(0)

        if type(child) == TemplateParser.Template_elemContext:
            return self.visitTemplate_elem(child)
        elif type(child) == TemplateParser.Exec_elementContext:
            return self.visitExec_element(child)
        elif type(child) == TemplateParser.Expr_elementContext:
            return self.visitExpr_element(child)
        elif type(child) == TemplateParser.Content_elemContext:
            return self.visitContent_elem(child)

    def visitTemplate_elem(self, ctx:TemplateParser.Template_elemContext):
        args = ctx.getChild(0).getText()
        TEMPLATE_TAG_OPENER = "<template"
        args = args[len(TEMPLATE_TAG_OPENER):-1]
        args = args.strip()
        args = eval(f'dict({args})')

        if ctx.getChildCount() == 3:
            content = ctx.getChild(1)
            content_ast = self.visitContent(content)
        else:
            content_ast = TemplateContent([])
        return TemplateNode(args, content_ast)

    def visitContent_elem(self, ctx:TemplateParser.Content_elemContext):
        return ContentNode()

    def visitExec_element(self, ctx:TemplateParser.Exec_elementContext):
        text = ctx.getText()
        opener = "<exec>"
        closer = "</exec>"
        code = text[len(opener): -len(closer)]
        code = preprocess_code(code)
        return ExecNode(code)

    def visitExpr_element(self, ctx:TemplateParser.Expr_elementContext):
        text = ctx.getText()
        code = text[2:-2]
        code = preprocess_code(code)
        return ExprNode(code)

class Template:
    content: TemplateContent
    def __init__(self, content):
        self.content = content

    @staticmethod
    def from_file(path: Path):
        with open(path) as f:
            content = f.read()
            return Template.from_str(content)

    @staticmethod
    def from_str(input: str):
        lexer = TemplateLexer(InputStream(input))
        stream = CommonTokenStream(lexer)
        parser = TemplateParser(stream)

        parse_tree = parser.root()
        ast = TemplateGenerator().visitRoot(parse_tree)

        return ast

    def render(self, env: Environment) -> str:
        output = StringBuffer()
        env.var.push()
        self.content.render(output, env)
        env.var.pop()
        res = output.flush()
        return res

    def render_with_content(self, o: StringBuffer, env: Environment, content: str) -> None:
        env.var.push()
        env.var[CONTENT] = content
        self.content.render(o, env)
        env.var.pop()

    def __str__(self) -> str:
        return str(self.content)
    def __repr__(self) -> str:
        return str(self)
