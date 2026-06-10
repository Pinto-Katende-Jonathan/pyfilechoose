# Changelog

The authoritative changelog lives in
[`CHANGELOG.md`](https://github.com/Pinto-Katende-Jonathan/pyfilechoose/blob/main/CHANGELOG.md)
at the repository root. It follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-10

### Added
- `file_choose()`: open a native dialog and return the absolute path of the
  selected file (raises `FileNotFoundError` on cancel).
- `files_choose()`: multiple-selection variant returning a list of paths.
- `title`, `filetypes`, and `initialdir` options on both functions.
- Clear error message when `tkinter` is not installed.
- Type hints and `py.typed` marker for type checkers.
