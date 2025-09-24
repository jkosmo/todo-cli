import importlib
import json
from pathlib import Path

import pytest


def use_tmp_db(tmp_path: Path):
    mod = importlib.import_module("todo")
    mod.DB = tmp_path / "todo.json"
    return mod


def test_add_and_list(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("Handle melk")
    data = todo.load()
    assert len(data) == 1
    assert data[0]["title"] == "Handle melk"
    assert data[0]["done"] is False


def test_done_marks_item(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("A")
    todo.add("B")
    todo.done(1)
    data = todo.load()
    assert data[1]["done"] is True


def test_remove_deletes_item(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("A")
    todo.add("B")
    todo.add("C")
    todo.remove(1)  # fjern "B"
    data = todo.load()
    assert [it["title"] for it in data] == ["A", "C"]


def test_list_items_reports_empty(tmp_path, capsys):
    todo = use_tmp_db(tmp_path)
    todo.list_items()
    captured = capsys.readouterr()
    assert "(ingen oppgaver)" in captured.out


def test_list_items_outputs_json(tmp_path, capsys):
    todo = use_tmp_db(tmp_path)
    todo.add("A")
    todo.add("B")
    todo.list_items(as_json=True)
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload == [
        {"title": "A", "done": False},
        {"title": "B", "done": False},
    ]


def test_edit_changes_title(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("Gammel tittel")
    todo.edit(0, "Ny tittel")
    items = todo.load()
    assert items[0]["title"] == "Ny tittel"
    assert items[0]["done"] is False


def test_edit_invalid_index_raises(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("A")
    with pytest.raises(IndexError):
        todo.edit(1, "skal feile")


def test_edit_empty_title_raises(tmp_path):
    todo = use_tmp_db(tmp_path)
    todo.add("A")
    with pytest.raises(ValueError):
        todo.edit(0, "   ")
    assert todo.load()[0]["title"] == "A"
