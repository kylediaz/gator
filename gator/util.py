import os
from pathlib import Path

def walk_files(dir: Path):
    for root, _, files in os.walk(dir):
        #root = root.removeprefix(str(dir) + os.sep)
        for file in files:
            yield Path(root, file)

class ScopedEnvEntry:

    # O(1) amortized get/set operations

    def __init__(self):
        self.stack = []

    def reduce(self, level):
        while self.stack and self.stack[-1][0] > level:
            self.stack.pop()

    def get(self, current_level):
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
