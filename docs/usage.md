# Usage

Every example below assumes the import:

```python
from pyfilechoose import file_choose, files_choose
```

## Pick a single file

```python
path = file_choose()
print(path)   # e.g. C:\Users\you\Documents\data.csv
```

`file_choose()` returns a single absolute path as a `str`. If the user closes
the dialog without choosing anything, it raises `FileNotFoundError`.

## Read a file directly with pandas

Because the return value is a path string, it drops into any function that
accepts a file path:

```python
import pandas as pd

# Equivalent to df <- read.csv(file.choose()) in R
df = pd.read_csv(file_choose())
```

You can combine it with the usual reader options:

```python
df = pd.read_csv(file_choose(filetypes=[("CSV files", "*.csv")]), sep=";")
```

## Set the dialog title

```python
path = file_choose(title="Select your input dataset")
```

## Filter by file type

`filetypes` takes a list of `(label, pattern)` tuples. The label is shown in the
dialog's type dropdown; the pattern controls which files are visible.

```python
path = file_choose(
    filetypes=[
        ("CSV files", "*.csv"),
        ("Excel files", "*.xlsx *.xls"),
        ("All files", "*.*"),
    ]
)
```

Patterns follow the platform's glob rules. Several extensions can share one
label by separating them with spaces, as in `"*.xlsx *.xls"`.

## Open in a specific directory

```python
path = file_choose(initialdir="~/Documents")
```

If `initialdir` is omitted, the dialog opens wherever the platform last left it.

## Pick several files at once

```python
paths = files_choose()
for p in paths:
    print(p)
```

`files_choose()` returns a `list[str]` of absolute paths in selection order. It
raises `FileNotFoundError` if nothing is selected.

```python
images = files_choose(
    title="Select images to process",
    filetypes=[("Images", "*.png *.jpg *.jpeg")],
)
```

## Handle cancellation

Both functions raise `FileNotFoundError` on cancel, so wrap the call when a user
might back out:

```python
try:
    path = file_choose()
except FileNotFoundError:
    print("No file selected, aborting.")
    raise SystemExit
```
