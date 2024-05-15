# I-Regexp checker

Check regular expressions for compliance with [RFC 9485](https://datatracker.ietf.org/doc/html/rfc9485).

## Install

```
pip install iregexp_check
```

## Usage

```python
from iregexp_check import check

check(r"[ab]{3}")  # True
check(r"[0-9]*?")  # False
```
