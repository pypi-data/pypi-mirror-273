# Rust I-Regexp Checker

Check regular expressions for compliance with [RFC 9485](https://datatracker.ietf.org/doc/html/rfc9485).

```rust
use iregexp::check;

fn main() {
    println!("{:?}", check(r"[0-9]*?"));  // false
}
```
