from gator.util import FileOutputStream, OutputStream, ScopedEnv, StringBuffer
import gator.code_executor as gator_code
from gator.site import Site

from pathlib import Path
from typing import Dict, List
from abc import abstractmethod, ABC
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
    site: Site
    template: Dict
    def __init__(self):
        self.var = ScopedEnv()
        self.template = dict()
    def __repr__(self) -> str:
        return f'Environment({repr(self.var)}, {repr(self.template.keys())})'

class Node(ABC):
    @abstractmethod
    def render(self, o: OutputStream, env: Environment) -> None:
        pass

class TextNode(Node):
    content: str
    def __init__(self, content):
        self.content = content
    def render(self, o: OutputStream, env: Environment) -> None:
        o.write(self.content)

class TemplateContent(Node):
    elements: List
    def __init__(self, elements: List):
        self.elements = elements

    def render(self, o: OutputStream, env: Environment) -> None:
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

    def render(self, o: OutputStream, env: Environment) -> None:
        template_name = self.args[TEMPLATE_NAME_KEY]
        template = env.template[template_name]
        env.var.push()
        env.var.update(self.args)
        template.render(o, env, self.content)
        env.var.pop()

    def __str__(self) -> str:
        return f'<template {self.args}>' + str(self.content) + '</template>'
    def __repr__(self) -> str:
        return str(self)

class ExecNode(Node):
    inner: str
    def __init__(self, inner: str):
        self.inner = inner

    def render(self, o: OutputStream, env: Environment):
        try:
            res = gator_code.exec(self.inner, env)
            o.write(res)
        except SyntaxError as e:
            raise SyntaxError(f"[ERROR] When executing {self.inner}: {e}")

    def __str__(self) -> str:
        return f'<exec>{self.inner}</exec>'
    def __repr__(self) -> str:
        return str(self)

class ExprNode(Node):
    inner: str
    def __init__(self, inner: str):
        self.inner = inner

    def render(self, o: OutputStream, env: Environment):
        try:
            res = gator_code.eval(self.inner, env)
            if res == None:
                print('[Warning] ', self.inner, 'resulted in a None output')
            o.write(str(res))
        except SyntaxError as e:
            raise SyntaxError(f"Error when evaluating {self.inner}: {e}")

    def __str__(self) -> str:
        return '{{' + str(self.inner) + '}}'
    def __repr__(self) -> str:
        return str(self)

class ContentNode(Node):
    def render(self, o: OutputStream, env: Environment):
        if "content" in env.var and (content := env.var["content"]) != None:
            if isinstance(content, str):
                o.write(content)
            elif isinstance(content, TemplateContent):
                content.render(o, env)
            elif isinstance(content, Template):
                content.render(o, env)
            else:
                print("[ERROR] Unexpected content type", type(content))
        else:
            print("[WARNING] Tried to print content but no content was given")

    def __str__(self) -> str:
        return '<content/>'
    def __repr__(self) -> str:
        return str(self)

class TemplateGenerator(ParseTreeVisitor):

    def visitRoot(self, ctx:TemplateParser.RootContext):
        return self.visitContent(ctx.getChild(0))

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
        return ExecNode(code)

    def visitExpr_element(self, ctx:TemplateParser.Expr_elementContext):
        text = ctx.getText()
        code = text[2:-2]
        return ExprNode(code)

class Template:

    content: TemplateContent

    __create_key = object()
    def __init__(self, content, create_key=None):
        assert(create_key == Template.__create_key), \
                "Template objects must be created using Template.from_str or Template.from_file"
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
        template_content = TemplateGenerator().visitRoot(parse_tree)

        return Template(template_content, create_key=Template.__create_key)

    def render(self, o: OutputStream, env: Environment, content: str | TemplateContent | None = None) -> None:
        env.var.push()
        env.var[CONTENT] = content
        self.content.render(o, env)
        env.var.pop()

    def render_to_str(self, env: Environment, content: str | TemplateContent | None = None) -> str:
        output = StringBuffer()
        self.render(output, env, content)
        return output.flush()

    def render_to_file(self, file_path: Path, env: Environment, content: str | TemplateContent | None = None) -> None:
        output = FileOutputStream(file_path.as_posix())
        self.render(output, env, content)
        output.flush()

    def __str__(self) -> str:
        return str(self.content)
    def __repr__(self) -> str:
        return str(self)
