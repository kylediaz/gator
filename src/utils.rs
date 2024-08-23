use std::collections::HashMap;

struct ScopedEnvEntry<T> {
    stack: Vec<(i64, T)>,
}

impl<T> ScopedEnvEntry<T> {
    fn new() -> ScopedEnvEntry<T> {
        ScopedEnvEntry { stack: vec![] }
    }

    /// Shrinks stack, removing scope levels that are now "out of scope"
    fn reduce(&mut self, level: i64) {
        while let Some(&(lvl, _)) = self.stack.last() {
            if lvl > level {
                self.stack.pop();
            } else {
                break;
            }
        }
    }

    fn get(&mut self, current_level: i64) -> Option<&T> {
        self.reduce(current_level);
        let res = self.stack.last();
        return res.map(|&(_, ref t)| t);
    }

    fn set(&mut self, level: i64, value: T) {
        self.reduce(level);
        self.stack.push((level, value));
    }
}

// This is a utility for "scoped variables"
pub struct ScopedEnv<T> {
    current_level: i64,
    kv: HashMap<String, ScopedEnvEntry<T>>,
}

impl<T> ScopedEnv<T> {
    pub fn new() -> ScopedEnv<T> {
        ScopedEnv {
            current_level: 0,
            kv: HashMap::new(),
        }
    }

    pub fn push(&mut self) {
        self.current_level += 1;
    }

    pub fn set(&mut self, k: String, v: T) {
        if let Some(entry) = self.kv.get_mut(&k) {
            entry.set(self.current_level, v);
        } else {
            let mut new_entry = ScopedEnvEntry::new();
            new_entry.set(self.current_level, v);
            self.kv.insert(k, new_entry);
        }
    }

    pub fn get(&mut self, k: String, v: T) -> Option<&T> {
        if let Some(entry) = self.kv.get_mut(&k) {
            entry.get(self.current_level)
        } else {
            Option::None
        }
    }

    /// Pops variables in the highest scope level. Every value that has been
    /// set since the last time "push" was called will be discarded and will
    /// be its old value
    pub fn pop(&mut self) {
        self.current_level -= 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scoped_env_entry_simple_set() {
        let mut e = ScopedEnvEntry::new();
        e.set(0, 100);
        assert_eq!(e.get(0), Option::Some(&100));
    }

    #[test]
    fn test_scoped_env_entry_scope_change() {
        let mut e = ScopedEnvEntry::new();

        e.set(0, 100);
        assert_eq!(e.get(0), Option::Some(&100));

        e.set(1, 200);
        assert_eq!(e.get(1), Option::Some(&200));

        assert_eq!(e.get(0), Option::Some(&100));
    }

    #[test]
    fn test_scoped_env_entry_out_of_scope() {
        let mut e = ScopedEnvEntry::new();
        e.set(1, 100);
        assert_eq!(e.get(0), Option::None);
    }

    #[test]
    fn test_scoped_env_entry_scope_fallback() {
        let mut e = ScopedEnvEntry::new();

        e.set(0, 100);
        assert_eq!(e.get(0), Option::Some(&100));

        e.set(10, 200);
        assert_eq!(e.get(10), Option::Some(&200));

        assert_eq!(e.get(9), Option::Some(&100)); // Uses value at scope level 0
    }
}
