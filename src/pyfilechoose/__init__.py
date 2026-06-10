"""pyfilechoose - R's ``file.choose()``, reimplemented for Python.

Open a native file-selection dialog and get back an absolute path:

    >>> from pyfilechoose import file_choose
    >>> path = file_choose()
"""

from .core import file_choose, files_choose

__all__ = ["file_choose", "files_choose"]
__version__ = "0.1.0"
