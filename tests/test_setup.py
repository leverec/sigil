# test unit: ~/.sigil/tests/test_setup.py
# test_setup.py version: 1.0
import pytest
import os
from pathlib import Path
from unittest.mock import patch
from src.setup import setup, force_yes, confirmation


def test_force_yes_check():
    assert force_yes(['-y']) is True
    assert force_yes(['--yes']) is True
    assert force_yes(['some_path']) is False

def test_confirmation_yes(monkeypatch):
    
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert confirmation("Test message") is True

def test_confirmation_no(monkeypatch):
    
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert confirmation("Test message") is False



def test_setup_add_tool_success(tmp_path):
    sigil_home = tmp_path / "sigil_home"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    
    new_tool = tmp_path / "my_new_tool.py"
    new_tool.write_text("# new tool code")
    
    fake_data = {
        'TOKENS': ['-s', '?set', str(new_tool)]
    }
    
    setup(fake_data, str(sigil_home))
    
    
    assert (tools_dir / "my_new_tool.py").exists()

def test_setup_set_invalid_extension(tmp_path, capsys):
    sigil_home = tmp_path / "sigil_home"
    (sigil_home / "tools").mkdir(parents=True)
    
    
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("not a script")
    
    fake_data = {'TOKENS': ['-s', '?set', str(bad_file)]}
    setup(fake_data, str(sigil_home))
    
    captured = capsys.readouterr()
    assert "has to be python files" in captured.out



def test_setup_remove_tool_force(tmp_path):
    sigil_home = tmp_path / "sigil_home"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    
    target_tool = tools_dir / "old_tool.py"
    target_tool.write_text("pass")
    
    
    fake_data = {
        'TOKENS': ['-s', '?rm', 'old_tool', '-y']
    }
    
    setup(fake_data, str(sigil_home))
    
    
    assert not target_tool.exists()

def test_setup_remove_aborted(tmp_path, monkeypatch, capsys):
    sigil_home = tmp_path / "sigil_home"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    (tools_dir / "important.py").write_text("pass")
    
    
    monkeypatch.setattr('builtins.input', lambda _: "n")
    
    fake_data = {'TOKENS': ['-s', '?rm', 'important']}
    setup(fake_data, str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Aborted" in captured.out
    assert (tools_dir / "important.py").exists() 
