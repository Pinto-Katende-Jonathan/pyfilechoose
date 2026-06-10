# Installation

`pyfilechoose` supports Python 3.8 and later. It has no third-party runtime
dependencies, but it does need a working `tkinter`, which ships with most
Python distributions.

## With pip

```bash
pip install pyfilechoose
```

## With uv

```bash
# Add it to your project (updates pyproject.toml and the lockfile)
uv add pyfilechoose

# ...or install it into the current environment
uv pip install pyfilechoose

# ...or run a one-off script that uses it, no install needed
uv run --with pyfilechoose your_script.py
```

## The tkinter requirement

`tkinter` is the only thing `pyfilechoose` depends on, and it is part of the
Python standard library. On most platforms it is already present:

| Platform | Status |
| --- | --- |
| Windows (python.org installer) | Included by default. |
| macOS (python.org installer, Homebrew) | Included by default. |
| Linux (system Python) | Often a separate package. |

On Debian/Ubuntu, install it with:

```bash
sudo apt install python3-tk
```

On Fedora:

```bash
sudo dnf install python3-tkinter
```

If `tkinter` is missing, calling `file_choose()` raises a `RuntimeError` with a
message pointing to the package you need. See
[Troubleshooting](troubleshooting.md) for details.

## Verifying the install

```bash
python -c "from pyfilechoose import file_choose, files_choose; print('ok')"
```

To check that `tkinter` itself works:

```bash
python -c "import tkinter; tkinter.Tk().destroy(); print('tkinter ok')"
```
