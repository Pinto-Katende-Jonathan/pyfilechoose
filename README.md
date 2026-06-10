# pyfilechoose

> R's `file.choose()`, reimplemented for Python.

[![PyPI version](https://img.shields.io/pypi/v/pyfilechoose.svg)](https://pypi.org/project/pyfilechoose/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyfilechoose.svg)](https://pypi.org/project/pyfilechoose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

If you come from R, you probably miss the handy `file.choose()` that pops up a
file picker and hands you back a path. `pyfilechoose` brings that one-liner to
Python — no GUI boilerplate, no leftover Tk windows.

It is built on `tkinter` from the Python standard library, so it has **zero
third-party dependencies**.

## Installation

```bash
pip install pyfilechoose
```

> **Linux note:** `tkinter` ships with most Python builds but may need to be
> installed separately, e.g. `sudo apt install python3-tk`.

## Usage

### Pick a single file

```python
from pyfilechoose import file_choose

path = file_choose()
print(path)  # -> absolute path of the file you selected
```

The classic R-style workflow with pandas:

```python
import pandas as pd
from pyfilechoose import file_choose

# Just like df <- read.csv(file.choose()) in R
df = pd.read_csv(file_choose(filetypes=[("CSV files", "*.csv")]))
```

### Filter file types and set a starting directory

```python
path = file_choose(
    title="Pick your dataset",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    initialdir="~/Documents",
)
```

### Pick several files at once

```python
from pyfilechoose import files_choose

paths = files_choose(filetypes=[("Images", "*.png *.jpg")])
for p in paths:
    print(p)
```

## API

### `file_choose(*, title="Select a file", filetypes=None, initialdir=None) -> str`

Opens a dialog and returns the **absolute path** of the chosen file.
Raises `FileNotFoundError` if the user cancels.

### `files_choose(*, title="Select one or more files", filetypes=None, initialdir=None) -> list[str]`

Same as above but allows multiple selections; returns a list of absolute paths.
Raises `FileNotFoundError` if nothing is selected.

| Argument     | Type                          | Description                                               |
| ------------ | ----------------------------- | --------------------------------------------------------- |
| `title`      | `str`                         | Title of the dialog window.                               |
| `filetypes`  | `list[tuple[str, str]]` \| `None` | `(label, pattern)` pairs, e.g. `[("CSV", "*.csv")]`.  |
| `initialdir` | `str` \| `None`               | Directory the dialog opens in.                            |

## Development

```bash
git clone https://github.com/katendepinto/pyfilechoose.git
cd pyfilechoose
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE) © Jonathan Katende Pinto
