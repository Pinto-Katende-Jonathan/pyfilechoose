# API reference

The public API is two functions, both exported from the top-level package:

```python
from pyfilechoose import file_choose, files_choose
```

Both take keyword-only arguments. The leading `*` in the signatures means you
must pass `title`, `filetypes`, and `initialdir` by name, never positionally.

## The `filetypes` argument

`filetypes` is shared by both functions and has the type:

```python
Sequence[Tuple[str, str]]
```

Each tuple is `(label, pattern)`:

- `label` is the human-readable name shown in the dialog's type selector
  (for example `"CSV files"`).
- `pattern` is a glob the dialog uses to filter files (for example `"*.csv"`).
  Combine extensions with spaces: `"*.png *.jpg"`.

If `filetypes` is `None` (the default), every file is shown.

---

::: pyfilechoose.file_choose

---

::: pyfilechoose.files_choose

---

## Reference (without mkdocstrings)

If you read this page as plain Markdown rather than through the built docs site,
the `:::` directives above are placeholders that
[mkdocstrings](https://mkdocstrings.github.io/) expands into the rendered
docstrings. The signatures are:

### `file_choose`

```python
file_choose(
    *,
    title: str = "Select a file",
    filetypes: Sequence[Tuple[str, str]] | None = None,
    initialdir: str | None = None,
) -> str
```

Opens a dialog and returns the absolute path of the chosen file.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `str` | `"Select a file"` | Title of the dialog window. |
| `filetypes` | `Sequence[Tuple[str, str]] \| None` | `None` | `(label, pattern)` filters. |
| `initialdir` | `str \| None` | `None` | Directory the dialog opens in. |

Returns a `str`: the absolute path of the selected file.

Raises `FileNotFoundError` if the user cancels, and `RuntimeError` if `tkinter`
is unavailable.

### `files_choose`

```python
files_choose(
    *,
    title: str = "Select one or more files",
    filetypes: Sequence[Tuple[str, str]] | None = None,
    initialdir: str | None = None,
) -> list[str]
```

Same as `file_choose`, but the dialog allows multiple selections and the return
value is a `list[str]` of absolute paths in selection order.

Raises `FileNotFoundError` if nothing is selected, and `RuntimeError` if
`tkinter` is unavailable.
