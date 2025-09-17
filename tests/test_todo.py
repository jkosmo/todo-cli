import importlib
from pathlib import Path

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
