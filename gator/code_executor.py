"""
Code execution environment for <exec> and {{}} blocks

1. Provides a package-isolated environment
2. Provides some helper functions and pre-imports packages
"""

import math
import re
import datetime

from gator.site import Page as __Page
from gator.util import StringBuffer as __StringBuffer
from typing import List as __List

__python_exec = exec
__python_eval = eval

def __preprocess_code(code: str) -> str:
    # Replace "$var_name" with "env.var['name']"
    code = re.sub(r'\$(\w+)', r'env.var["\1"]', code)
    return code

def __first_non_whitespace_index(s):
    for index, char in enumerate(s):
        if not char.isspace():
            return index
    return -1

def __remove_indent(code: str) -> str:
    """
    We need to remove indents because the code in the template may be indented
    like so:
    <div>
    ----<exec>
    --------print("this is a test)
    ----</exec>
    </div>
    but python exec() expects code given to it to initially have indentation
    level 0
    """
    lines = code.split("\n")
    first_code_line = next((i for i, l in enumerate(lines) if len(l.strip()) > 0), -1)
    if first_code_line == -1:
        return code
    i = __first_non_whitespace_index(lines[first_code_line])
    if i == -1:
        return code
    lines = [l[i:] if i <= len(l) else l for l in lines]
    return "\n".join(lines)

def exec(code: str, env) -> str:
    __output = __StringBuffer()
    def print(*values):
        for v in values:
            __output.write(v)

    def template(template_name: str, content: None | str = None, **kwargs) -> None:
        env.template[template_name].render(__output, env, content=content)

    def pages(in_dir: str = "") -> __List[__Page]:
        return [page for path, page in env.site.pages.items() if path.startswith(in_dir)]

    code = __preprocess_code(code)
    code = __remove_indent(code)
    __python_exec(code)
    return __output.flush()

def eval(code: str, env) -> str:
    code = __preprocess_code(code)
    return __python_eval(code)
