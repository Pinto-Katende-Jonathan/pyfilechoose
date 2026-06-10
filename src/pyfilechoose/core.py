"""Core implementation of :func:`file_choose` and :func:`files_choose`.

These functions open a native "Open file" dialog using :mod:`tkinter`
(part of the Python standard library) and return the selected path(s).
"""

from __future__ import annotations

import os
from typing import Iterable, Optional, Sequence, Tuple

__all__ = ["file_choose", "files_choose"]

# Type alias for the ``filetypes`` argument, e.g. ``[("CSV files", "*.csv")]``.
FileTypes = Sequence[Tuple[str, str]]


def _open_dialog(
    *,
    multiple: bool,
    title: str,
    filetypes: Optional[FileTypes],
    initialdir: Optional[str],
):
    """Open a Tkinter file dialog and return the raw selection.

    A hidden root window is created, forced to the foreground, used for a
    single dialog, then destroyed so no resources leak.
    """
    # Imported lazily so that merely importing the package does not require
    # a working Tk installation (e.g. on a headless server).
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:  # pragma: no cover - platform dependent
        raise RuntimeError(
            "tkinter is not available in this Python installation. "
            "On Linux install it with your package manager, e.g. "
            "'sudo apt install python3-tk'."
        ) from exc

    root = tk.Tk()
    root.withdraw()
    # Force the dialog to appear on top of other windows.
    root.wm_attributes("-topmost", 1)

    options = {"title": title}
    if filetypes is not None:
        options["filetypes"] = list(filetypes)
    if initialdir is not None:
        options["initialdir"] = initialdir

    try:
        if multiple:
            selection = filedialog.askopenfilenames(**options)
        else:
            selection = filedialog.askopenfilename(**options)
    finally:
        # Always release the Tk resources, even if the dialog raises.
        root.destroy()

    return selection


def file_choose(
    *,
    title: str = "Select a file",
    filetypes: Optional[FileTypes] = None,
    initialdir: Optional[str] = None,
) -> str:
    """Open a dialog and return the absolute path of the chosen file.

    A small replication of R's ``file.choose()`` for Python.

    Parameters
    ----------
    title:
        Title shown in the dialog window.
    filetypes:
        Optional sequence of ``(label, pattern)`` pairs used to filter the
        files shown, e.g. ``[("CSV files", "*.csv"), ("All files", "*.*")]``.
    initialdir:
        Directory the dialog should open in. Defaults to the platform's
        last-used directory.

    Returns
    -------
    str
        The absolute path of the selected file.

    Raises
    ------
    FileNotFoundError
        If the user cancels the dialog without selecting a file.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv(file_choose(filetypes=[("CSV files", "*.csv")]))
    """
    file_path = _open_dialog(
        multiple=False,
        title=title,
        filetypes=filetypes,
        initialdir=initialdir,
    )

    # askopenfilename returns an empty string when the user cancels.
    if not file_path:
        raise FileNotFoundError("No file was selected.")

    return os.path.abspath(file_path)


def files_choose(
    *,
    title: str = "Select one or more files",
    filetypes: Optional[FileTypes] = None,
    initialdir: Optional[str] = None,
) -> list[str]:
    """Open a dialog allowing multiple selections and return absolute paths.

    Parameters
    ----------
    title, filetypes, initialdir:
        See :func:`file_choose`.

    Returns
    -------
    list of str
        Absolute paths of every selected file, in selection order.

    Raises
    ------
    FileNotFoundError
        If the user cancels the dialog without selecting any file.
    """
    selection: Iterable[str] = _open_dialog(
        multiple=True,
        title=title,
        filetypes=filetypes,
        initialdir=initialdir,
    )

    paths = [os.path.abspath(p) for p in selection]
    if not paths:
        raise FileNotFoundError("No file was selected.")

    return paths
