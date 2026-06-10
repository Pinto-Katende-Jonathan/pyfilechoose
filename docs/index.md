# pyfilechoose

R's `file.choose()`, reimplemented for Python.

In R, `file.choose()` opens a graphical file picker and returns the path you
select, so you can write `read.csv(file.choose())` and pick a file at runtime.
`pyfilechoose` provides the same behaviour in Python through two functions,
`file_choose()` and `files_choose()`.

```python
from pyfilechoose import file_choose

path = file_choose()   # opens a dialog, returns an absolute path string
```

## Why it exists

Opening a file dialog in Python normally means writing several lines of
`tkinter` setup: create a root window, hide it, raise it to the front, open the
dialog, then destroy the window. `pyfilechoose` packages that boilerplate into a
single call and adds path normalization and clear error handling.

## Design goals

- **One call, one path.** Each function returns ready-to-use absolute paths.
- **No third-party dependencies.** It relies only on `tkinter` from the standard
  library.
- **Predictable failures.** Cancelling the dialog raises `FileNotFoundError`
  rather than silently returning an empty value.
- **Typed.** Full type hints and a `py.typed` marker, so type checkers see the
  signatures.

## Where to go next

- [Installation](installation.md): pip and uv.
- [Usage](usage.md): task-oriented examples.
- [API reference](api.md): every parameter and return value.
- [How it works](internals.md): the Tk lifecycle and design decisions.
- [Troubleshooting](troubleshooting.md): common problems and fixes.
