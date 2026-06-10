# Development

## Getting the source

```bash
git clone https://github.com/Pinto-Katende-Jonathan/pyfilechoose.git
cd pyfilechoose
```

## Setting up an environment

With uv, which creates and manages the virtualenv for you:

```bash
uv sync --extra dev
uv run pytest
```

With pip:

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Project layout

```
pyfilechoose/
├── src/pyfilechoose/
│   ├── __init__.py     # exports + __version__
│   ├── core.py         # implementation
│   └── py.typed        # PEP 561 marker
├── tests/
│   └── test_core.py
├── docs/               # this documentation
├── pyproject.toml
├── mkdocs.yml
├── CHANGELOG.md
└── README.md
```

The package uses the `src/` layout, which keeps the import path the same in
development and after install and prevents accidentally importing the source
tree instead of the installed package.

## Running the tests

```bash
pytest
```

The tests replace the Tk dialog with a fake so they run headless, with no
display and no real window. They cover the logic around the dialog: path
normalization, the `FileNotFoundError` on cancel, and argument forwarding. The
`_open_dialog` helper is monkeypatched, so the suite never opens a real dialog.

## Building the documentation

The docs are built with [MkDocs](https://www.mkdocs.org/) and the Material
theme, with API pages generated from docstrings by
[mkdocstrings](https://mkdocstrings.github.io/).

```bash
uv sync --extra docs        # or: pip install -e ".[docs]"
mkdocs serve                # live preview at http://127.0.0.1:8000
mkdocs build                # static site into ./site
```

## Building the package

```bash
python -m build
twine check dist/*
```

This produces a source distribution and a wheel in `dist/`.

## Releasing a new version

A version can only be uploaded to PyPI once, so each release needs a new number.

1. Bump the version in two places:
   - `pyproject.toml` (`version = "..."`)
   - `src/pyfilechoose/__init__.py` (`__version__ = "..."`)
2. Add a section to `CHANGELOG.md`.
3. Rebuild from a clean tree:
   ```bash
   rm -rf dist build
   python -m build
   twine check dist/*
   ```
4. Upload:
   ```bash
   twine upload dist/*
   ```
5. Tag the release:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
