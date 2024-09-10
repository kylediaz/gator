import unittest
from gator.util import ScopedEnv, ScopedEnvEntry

class TestTemplate(unittest.TestCase):

    def test_basic_entry(self):
        entry = ScopedEnvEntry()
        entry.set(0, "a")
        assert entry.get(0) == "a"

    def test_entry_overwrite(self):
        entry = ScopedEnvEntry()
        entry.set(0, "a")
        assert entry.get(0) == "a"
        entry.set(0, "b")
        assert entry.get(0) == "b"

    def test_scope_change(self):
        entry = ScopedEnvEntry()
        entry.set(0, "a")
        assert entry.get(0) == "a"
        entry.set(1, "b")
        assert entry.get(1) == "b"
        entry.set(2, "c")
        assert entry.get(2) == "c"
        assert entry.get(1) == "b"
        assert entry.get(0) == "a"

    def test_scope_fallback(self):
        entry = ScopedEnvEntry()
        entry.set(0, "a")
        assert entry.get(0) == "a"
        entry.set(100, "b")
        assert entry.get(100) == "b"
        assert entry.get(99) == "a"

    def test_env(self):
        env = ScopedEnv()
        env["key"] = "a"
        assert env["key"] == "a"

    def test_env_scoping(self):
        env = ScopedEnv()
        env["key"] = "a"
        assert env["key"] == "a"
        env.push()
        assert env["key"] == "a"
        env["key"] = "b"
        assert env["key"] == "b"
        env.pop()
        assert env["key"] == "a"


if __name__ == '__main__':
    unittest.main()
