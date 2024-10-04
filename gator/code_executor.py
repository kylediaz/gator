"""
Code execution environment for <exec> and {{}} blocks

1. Provides a package-isolated environment
2. Provides some helper functions and pre-imports packages
"""

import math
import re
import datetime

from gator.util import StringBuffer

__python_exec = exec
__python_eval = eval

def __preprocess_code(code: str) -> str:
    # Replace "$var_name" with "env.var['name']"
    code = re.sub(r'\$(\w+)', r'env.var["\1"]', code)
    return code

def exec(code: str, env) -> str:
    __output = StringBuffer()
    def print(*values):
        for v in values:
            __output.write(v)

    def template(template_name: str, content: None | str = None, **kwargs) -> None:
        env.template[template_name].render(__output, env, content=content)

    code = __preprocess_code(code)
    __python_exec(code)
    return __output.flush()

def eval(code: str, env) -> str:
    code = __preprocess_code(code)
    return __python_eval(code)
