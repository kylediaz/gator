"""
Code execution environment for <exec> and {{}} blocks

1. Provides a package-isolated environment
2. Provides some helper functions and pre-imports packages
"""

import math
import re

__python_exec = exec
__python_eval = eval

def __preprocess_code(code: str) -> str:
    # Replace "$var_name" with "env.var['name']"
    code = re.sub(r'\$(\w+)', r'env.var["\1"]', code)
    return code

def exec(code: str, env) -> str:
    __output = []
    def print(*values):
        __output.extend(values)
    code = __preprocess_code(code)
    __python_exec(code)
    return "".join(__output)

def eval(code: str, env) -> str:
    code = __preprocess_code(code)
    return __python_eval(code)
