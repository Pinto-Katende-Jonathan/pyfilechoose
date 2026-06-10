"""Tests for pyfilechoose.

The Tk dialog itself is replaced with a fake so the suite can run headless
(in CI, without a display). We only verify the logic around the dialog:
absolute-path conversion, cancellation handling, and argument forwarding.
"""

import os

import pytest

from pyfilechoose import core, file_choose, files_choose


def test_file_choose_returns_absolute_path(tmp_path, monkeypatch):
    target = tmp_path / "data.csv"
    target.write_text("a,b\n1,2\n")

    monkeypatch.setattr(core, "_open_dialog", lambda **kwargs: str(target))

    result = file_choose()
    assert result == os.path.abspath(str(target))
    assert os.path.isabs(result)


def test_file_choose_raises_on_cancel(monkeypatch):
    # An empty string is what Tk returns when the user cancels.
    monkeypatch.setattr(core, "_open_dialog", lambda **kwargs: "")

    with pytest.raises(FileNotFoundError):
        file_choose()


def test_file_choose_forwards_arguments(monkeypatch):
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return "/some/file.csv"

    monkeypatch.setattr(core, "_open_dialog", fake)

    file_choose(
        title="Pick one",
        filetypes=[("CSV", "*.csv")],
        initialdir="/tmp",
    )

    assert captured["multiple"] is False
    assert captured["title"] == "Pick one"
    assert captured["filetypes"] == [("CSV", "*.csv")]
    assert captured["initialdir"] == "/tmp"


def test_files_choose_returns_list(monkeypatch):
    monkeypatch.setattr(
        core, "_open_dialog", lambda **kwargs: ("/a/one.txt", "/b/two.txt")
    )

    result = files_choose()
    assert result == [os.path.abspath("/a/one.txt"), os.path.abspath("/b/two.txt")]


def test_files_choose_raises_on_empty(monkeypatch):
    monkeypatch.setattr(core, "_open_dialog", lambda **kwargs: ())

    with pytest.raises(FileNotFoundError):
        files_choose()
