# Troubleshooting

## `RuntimeError: tkinter is not available`

The function was called but `tkinter` is not installed in this Python.

- Debian/Ubuntu: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Windows/macOS: reinstall Python from python.org, which bundles Tk.

Check it directly:

```bash
python -c "import tkinter; tkinter.Tk().destroy(); print('ok')"
```

## The dialog opens but I cannot see it

It is probably behind the terminal or application window. `pyfilechoose` already
sets the always-on-top attribute, but some window managers ignore it. Alt-Tab to
the dialog, or move the front window aside.

## `FileNotFoundError: No file was selected`

This is intended behaviour, not a bug: it means the dialog was closed or
cancelled without choosing a file. Wrap the call if cancelling is a valid path
through your program:

```python
try:
    path = file_choose()
except FileNotFoundError:
    path = None
```

## Nothing happens on a remote or headless machine

A graphical dialog needs a display. Over plain SSH, in a container, or on a CI
runner there is no display, so Tk cannot draw the window. There is no way around
this; the file must be chosen on a machine with a screen, or selected
programmatically instead of through a dialog.

## The dialog hangs or crashes in a thread

`tkinter` expects the main thread. Calling `file_choose()` from a worker thread
can hang or raise. Move the call to the main thread. See
[How it works](internals.md#threading-and-event-loop-notes).

## Paths look wrong on Windows

The returned path is absolute and uses native separators (`\` on Windows). If
you need symlinks resolved or `~` expanded, apply `os.path.realpath` or
`os.path.expanduser` yourself; `pyfilechoose` only runs `os.path.abspath`.
