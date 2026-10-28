from pathlib import Path

import senor_claudio.tools as tools


def test_list_files_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "WORKSPACE", tmp_path)
    assert tools.list_files() == "No files found."


def test_write_read_list_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "WORKSPACE", tmp_path)
    assert tools.write_file("a.txt", "hello") == "File 'a.txt' written successfully."
    assert tools.read_file("a.txt") == "hello"
    assert "a.txt" in tools.list_files()
    assert tools.read_file("missing.txt") == "File 'missing.txt' does not exist."


def test_load_save_memory(tmp_path, monkeypatch):
    mf = tmp_path / "memory.md"
    monkeypatch.setattr(tools, "MEMORY_FILE", mf)
    assert tools.load_memory() == "(nothing saved yet)"
    assert tools.save_memory("likes coffee") == "saved: likes coffee"
    assert "likes coffee" in tools.load_memory()
