import os
from pathlib import Path
from typing import Any, List
from urllib.parse import urlparse

def change_file_extension(url: str, new_ext: str) -> str:
    parse_result = urlparse(url)
    original_path = parse_result.path
    base_name, original_ext = os.path.splitext(original_path)

    new_path = base_name + f'.{new_ext}'
    new_url = parse_result._replace(path=new_path).geturl()

    return new_url

def walk_files(dir: Path):
    for root, _, files in os.walk(dir):
        for file in files:
            yield Path(root, file)

def get_file_content(path: Path) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as f:
        f.write(content)

class StringBuffer:
    buffer: List
    def __init__(self) -> None:
        self.buffer = []
    def append(self, v: str) -> None:
        self.buffer.append(v)
    def flush(self) -> str:
        return "".join(map(str, self.buffer))
        self.buffer.clear()

class FileSink:
    def __init__(self, file_path: str) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.f = open(file_path, "w+")
    def append(self, v: str) -> None:
        self.f.write(v)
    def flush(self) -> Any:
        self.f.close()
        return ""


class ScopedEnvEntry:

    # O(1) amortized get/set operations

    def __init__(self):
        self.stack = []

    def reduce(self, level):
        while self.stack and self.stack[-1][0] > level:
            self.stack.pop()

    def get(self, current_level=None):
        if current_level != None:
            self.reduce(current_level)
        if self.stack:
            return self.stack[-1][1]
        else:
            return None

    def set(self, level, value):
        self.reduce(level)
        self.stack.append((level, value))


class ScopedEnv:
    """
    Key/value store with "scopes"
    """

    def __init__(self):
        self.current_level = 0
        self.kv = {}

    def __contains__(self, k) -> bool:
        return k in self.kv

    def __setitem__(self, key, value):
        return self.set(key, value)

    def set(self, k, v) -> None:
        if k in self.kv:
            self.kv[k].set(self.current_level, v)
        else:
            new_entry = ScopedEnvEntry()
            new_entry.set(self.current_level, v)
            self.kv[k] = new_entry

    def __getitem__(self, key):
        return self.get(key)

    def get(self, k) -> any:
        if k in self.kv:
            return self.kv[k].get(self.current_level)
        else:
            return None

    def update(self, d: dict) -> None:
        if d is not None:
            for k, v in d.items():
                self.set(k, v)

    def push(self):
        """Increases the current scope level"""
        self.current_level += 1

    def pop(self):
        """
        Decreases the current scope level, discarding all values set in the
        previous scope level, reverting them to their old value
        """
        self.current_level -= 1

    def __str__(self) -> str:
        items = ["ScopedEnv("]
        for k, v in self.kv.items():
            items.append(f'{k}={v.get()}')
        items.append(")")
        return " ".join(items)

    def __repr__(self) -> str:
        return str(self)
