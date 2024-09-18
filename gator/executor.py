"""
Code execution environment for <exec> and {{}} blocks

1. Provides a package-isolated environment
"""

import math

__python_exec = exec
__python_eval = eval

def exec(code: str, env) -> str:
    __output = []
    def print(*values):
        __output.extend(values)
    __python_exec(code)
    return "".join(__output)

def eval(code: str, env) -> str:
    return __python_eval(code)
