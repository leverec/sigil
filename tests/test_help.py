# test unit: ~/.sigil/tests/test_help.py
# test_help.py version: 1.0
import pytest
import os
from src.help import sigil_help, tools_help

def test_sigil_help_success(tmp_path, capsys):
    sigil_home = tmp_path / "sigil"
    docs_dir = sigil_home / "docs"
    docs_dir.mkdir(parents=True)
    
    help_file = docs_dir / "help.txt"
    help_text = "Ini adalah petunjuk Sigil."
    help_file.write_text(help_text)
    
    sigil_help(str(sigil_home))
    
    captured = capsys.readouterr()
    assert help_text in captured.out

def test_sigil_help_not_found(tmp_path, capsys):
    sigil_home = tmp_path / "empty_sigil"
    sigil_home.mkdir()
    
    sigil_help(str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Help file not found" in captured.out



def test_tools_help_with_sghelp(tmp_path, capsys):
    
    sigil_home = tmp_path / "sigil"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    
    tool_content = """
def sghelp():
    print("Petunjuk untuk tool ini.")
"""
    tool_file = tools_dir / "mytool.py"
    tool_file.write_text(tool_content)
    
    tools_help("mytool", str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Petunjuk untuk tool ini." in captured.out

def test_tools_help_missing_function(tmp_path, capsys):
    sigil_home = tmp_path / "sigil"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    
    tool_file = tools_dir / "nohelp.py"
    tool_file.write_text("x = 10")
    
    tools_help("nohelp", str(sigil_home))
    
    captured = capsys.readouterr()
    assert "has no sghelp() function" in captured.out

def test_tools_help_tool_not_found(tmp_path, capsys):
    sigil_home = tmp_path / "sigil"
    (sigil_home / "tools").mkdir(parents=True)
    
    tools_help("ghoib", str(sigil_home))
    
    captured = capsys.readouterr()
    assert "Tool 'ghoib' not found" in captured.out
