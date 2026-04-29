# test unit: ~/.sigil/tests/test_main.py
# test_main.py version: 1.0
import pytest
import os
from src.info import info, list_tools

def test_info_display(tmp_path, capsys):
    
    sigil_home = tmp_path / "sigil"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    
    (tools_dir / "tool1.py").write_text("")
    (tools_dir / "tool2.py").write_text("")
    (tools_dir / "tool3.py").write_text("")
    
    info(str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Tools loaded    : 3" in captured.out
    assert "Author          : leverec" in captured.out

def test_list_tools_success(tmp_path, capsys):
    sigil_home = tmp_path / "sigil"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    (tools_dir / "gentrees.py").write_text("")
    
    list_tools(str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Available Tools" in captured.out
    assert "gentrees" in captured.out

def test_list_tools_empty(tmp_path, capsys):
    sigil_home = tmp_path / "sigil"
    (sigil_home / "tools").mkdir(parents=True)
    
    list_tools(str(sigil_home))
    
    captured = capsys.readouterr()
    assert "No tools available" in captured.out
