# pyfilechoose

R's `file.choose()`, reimplemented for Python.

[![PyPI version](https://img.shields.io/pypi/v/pyfilechoose.svg)](https://pypi.org/project/pyfilechoose/0.1.0/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyfilechoose.svg)](https://pypi.org/project/pyfilechoose/0.1.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

In R, `file.choose()` opens a file picker and returns the path you select.
`pyfilechoose` gives you the same one-liner in Python, with no GUI boilerplate
and no leftover Tk windows.

It uses `tkinter` from the standard library, so it has no third-party
dependencies.

## Installation

With pip:

```bash
pip install pyfilechoose
```

With [uv](https://docs.astral.sh/uv/):

```bash
# Add it to your project
uv add pyfilechoose

# ...or install it into the current environment
uv pip install pyfilechoose

# ...or run a one-off script that uses it, no install needed
uv run --with pyfilechoose your_script.py
```

On Linux, `tkinter` ships with most Python builds but may need to be installed
separately, e.g. `sudo apt install python3-tk`.

## Usage

### Pick a single file

```python
from pyfilechoose import file_choose

path = file_choose()
print(path)  # absolute path of the file you selected
```

### With pandas (the classic R workflow)

`file_choose()` returns a path string, so it works with any function that takes
a file path, including `pd.read_csv`:

```python
import pandas as pd
from pyfilechoose import file_choose

# Just like df <- read.csv(file.choose()) in R
df = pd.read_csv(file_choose())
```

You can still pass the usual pandas options, and filter the picker to CSVs:

```python
df = pd.read_csv(file_choose(filetypes=[("CSV files", "*.csv")]), sep=";")
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

Opens a dialog and returns the absolute path of the chosen file.
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
git clone https://github.com/Pinto-Katende-Jonathan/pyfilechoose.git
cd pyfilechoose
```

With uv, which creates and manages the virtualenv for you:

```bash
uv sync --extra dev   # set up the environment with dev dependencies
uv run pytest         # run the test suite
```

With pip:

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE) © Jonathan Katende Pinto
