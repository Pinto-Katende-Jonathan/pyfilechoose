# How it works

This page explains what happens inside `pyfilechoose` when you call one of its
functions, and why it is written the way it is. None of this is needed to use
the library, but it is useful if you are extending it, debugging a platform
issue, or reviewing the code.

## Architecture

The package is two files:

```
src/pyfilechoose/
├── __init__.py   # public exports and __version__
└── core.py       # the implementation
```

`core.py` defines three functions:

- `file_choose()` and `files_choose()` are the public API.
- `_open_dialog()` is a private helper that both call. It holds all the
  `tkinter` interaction so the public functions only deal with paths and errors.

The public functions are thin: they call `_open_dialog()`, check the result,
normalize paths with `os.path.abspath`, and raise `FileNotFoundError` when the
selection is empty. Everything platform-specific lives in `_open_dialog()`.

## The Tk lifecycle

A file dialog in `tkinter` needs a root window to attach to. We do not want that
window visible, and we do not want it to outlive the dialog. `_open_dialog()`
runs this sequence:

```python
root = tk.Tk()              # 1. create the hidden root
root.withdraw()             # 2. remove it from the screen
root.wm_attributes("-topmost", 1)  # 3. force the dialog to the foreground
try:
    selection = filedialog.askopenfilename(**options)  # 4. show the dialog
finally:
    root.destroy()          # 5. tear everything down
```

Each step matters:

1. **`tk.Tk()`** creates a Tcl/Tk interpreter and a top-level window. The dialog
   functions need this context to exist.
2. **`withdraw()`** hides the empty root window. Without it you would see a small
   blank window appear next to the dialog.
3. **`wm_attributes("-topmost", 1)`** marks the window as always-on-top so the
   dialog is not buried behind the application or terminal that launched it. This
   is the usual fix for "the dialog opened but I cannot see it."
4. The dialog call blocks until the user chooses a file or cancels.
5. **`destroy()`** runs in a `finally` block so the interpreter and window are
   released even if the dialog raises. Leaking Tk roots across repeated calls can
   leave the process unable to create new ones.

## Single vs multiple selection

`_open_dialog()` takes a `multiple` flag and dispatches to the matching Tk call:

| `multiple` | Tk function | Returns when something is chosen | Returns on cancel |
| --- | --- | --- | --- |
| `False` | `filedialog.askopenfilename` | a single path string | `""` (empty string) |
| `True` | `filedialog.askopenfilenames` | a tuple of path strings | `()` (empty tuple) |

The public functions translate those raw results:

- `file_choose()` treats `""` as cancellation (`if not file_path:`).
- `files_choose()` builds a list and treats an empty list as cancellation.

In both cases an empty selection becomes a `FileNotFoundError`, which is the one
behavioural promise the library makes beyond returning paths.

## Path normalization

Tk returns paths using forward slashes on every platform, including Windows.
Each result is passed through `os.path.abspath`, which:

- resolves the path against the current working directory if it is relative, and
- converts separators to the platform's native form.

So on Windows you get `C:\Users\you\data.csv` rather than the
`C:/Users/you/data.csv` that Tk hands back.

`abspath` does not resolve symlinks or expand `~`. If you need either, apply
`os.path.realpath` or `os.path.expanduser` to the returned value yourself.

## Lazy import of tkinter

`tkinter` is imported inside `_open_dialog()`, not at the top of the module:

```python
try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError as exc:
    raise RuntimeError(
        "tkinter is not available in this Python installation. ..."
    ) from exc
```

Two reasons:

1. **Importing the package never fails.** On a headless server where `tkinter`
   is absent, `import pyfilechoose` still works. The error only appears if you
   actually call a function that needs a dialog.
2. **The error is actionable.** The raw `ImportError` is replaced with a
   `RuntimeError` that names the system package to install. The original
   exception is chained with `raise ... from exc` so the traceback keeps the root
   cause.

## Threading and event-loop notes

`tkinter` is not thread-safe and expects to run on the main thread. Because each
call creates and destroys its own root, `pyfilechoose` works well from a plain
script or a REPL. Some environments need care:

- **Background threads.** Calling these functions from a non-main thread can
  fail or behave unpredictably, the same as any direct `tkinter` use. Call them
  from the main thread.
- **Existing Tk applications.** If your program already runs a Tk main loop, you
  usually want that application's own dialog calls rather than a second root
  created here.
- **Jupyter / IPython.** Works in a local kernel that has display access; the
  dialog opens on the machine running the kernel, not in the browser. It does not
  work on a remote, headless kernel.

## Why a private helper instead of duplicated code

Both public functions need the identical five-step Tk lifecycle. Putting it in
`_open_dialog()` keeps that sequence in one place, so a change to the window
handling (for example, a new platform workaround) is made once and applies to
both entry points. The public functions stay readable: each is essentially "call
the helper, check for empty, normalize, return."
