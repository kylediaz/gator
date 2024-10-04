import os
from pathlib import Path
from typing import Any, List, Dict
from urllib.parse import urlparse
from abc import ABC, abstractmethod

def walk_files(dir: Path):
    for root, _, files in os.walk(dir):
        for file in files:
            yield Path(root, file)

def get_file_content(path: Path) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as f:
        f.write(content)


class OutputStream(ABC):
    @abstractmethod
    def write(self, v: str) -> None:
        pass
    @abstractmethod
    def flush(self) -> Any:
        pass

class StringBuffer(OutputStream):
    buffer: List[str]
    def __init__(self) -> None:
        self.buffer = []
    def write(self, v: str) -> None:
        self.buffer.append(v)
    def flush(self) -> str:
        output = "".join(map(str, self.buffer))
        self.buffer.clear()
        return output

class FileOutputStream(OutputStream):
    def __init__(self, file_path: str) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.f = open(file_path, "w+")
    def write(self, v: str) -> None:
        self.f.write(v)
    def flush(self) -> None:
        self.f.flush()


class ScopedEnvEntry:
    __stack: List
    def __init__(self):
        self.__stack = []

    def reduce(self, level: int) -> None:
        while self.__stack and self.__stack[-1][0] > level:
            self.__stack.pop()

    def get(self, current_level:None|int=None) -> None:
        if current_level != None:
            self.reduce(current_level)
        if self.__stack:
            return self.__stack[-1][1]
        else:
            return None

    def set(self, level: int, value: Any) -> None:
        self.reduce(level)
        self.__stack.append((level, value))

class ScopedEnv:
    """
    Key/value store with "scopes"
    """

    __current_level: int
    __kv: Dict[str, ScopedEnvEntry]

    def __init__(self):
        self.__current_level = 0
        self.__kv = {}

    def __contains__(self, k: str) -> bool:
        return k in self.__kv

    def __setitem__(self, key: str, value: Any) -> None:
        return self.set(key, value)

    def set(self, k: str, v: Any) -> None:
        if k in self.__kv:
            self.__kv[k].set(self.__current_level, v)
        else:
            new_entry = ScopedEnvEntry()
            new_entry.set(self.__current_level, v)
            self.__kv[k] = new_entry

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def get(self, k: str) -> Any:
        if k in self.__kv:
            return self.__kv[k].get(self.__current_level)
        else:
            return None

    def update(self, d: Dict) -> None:
        if d is not None:
            for k, v in d.items():
                self.set(k, v)

    def push(self) -> None:
        """Increases the current scope level"""
        self.__current_level += 1

    def pop(self) -> None:
        """
        Decreases the current scope level, discarding all values set in the
        previous scope level, reverting them to their old value
        """
        self.__current_level -= 1
        for v in self.__kv.values():
            v.reduce(self.__current_level)

    def __str__(self) -> str:
        items = ["ScopedEnv("]
        for k, v in self.__kv.items():
            items.append(f'{k}={v.get()}')
        items.append(")")
        return " ".join(items)

    def __repr__(self) -> str:
        return str(self)
