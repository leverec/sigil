# test unit: ~/.sigil/tests/test_script.py
# test_script.py version: 1.0
import os
import pytest
from unittest.mock import patch, MagicMock
from src.script import new_filename_gen, tools_mover, script

def test_new_filename_gen_random():
    filename = "test_tool.py"
    res = new_filename_gen(filename, origin_modifier=False)
    assert res.startswith("TEST_TOOL-")
    assert res.endswith("-SIGIL.py")
    assert len(res) > 15

def test_new_filename_gen_origin():
    filename = "/path/to/my_tool.py"
    res = new_filename_gen(filename, origin_modifier=True)
    assert res == "my_tool.py"

def test_tools_mover_success(tmp_path):
    src = tmp_path / "source.py"
    src.write_text("print('hello')")
    dst = tmp_path / "destination.py"
    
    success = tools_mover(str(src), str(dst))
    
    assert success is True
    assert dst.exists()
    assert dst.read_text() == "print('hello')"

def test_script_execution_flow(monkeypatch, tmp_path):
    sigil_home = tmp_path / "sigil_home"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    
    tool_file = tools_dir / "hello.py"
    tool_file.write_text("print('action')")
    
    fake_data = {
        'COMMANDS': '-t',
        'TARGET': 'hello',
        'SCR_ARGV': ['--arg1'],
        'TAIL': []
    }
    
    with patch("subprocess.run") as mock_run, \
        patch("os.get_terminal_size", return_value=os.terminal_size((80, 24))):            
        current_dir = tmp_path / "workspace"
        current_dir.mkdir()
        monkeypatch.chdir(current_dir)
        
        script(fake_data, str(sigil_home))
        
        assert mock_run.called
        
        remaining_files = list(current_dir.glob("*.py"))
        assert len(remaining_files) == 0 

def test_script_keep_modifier(monkeypatch, tmp_path):
    sigil_home = tmp_path / "sigil_home"
    tools_dir = sigil_home / "tools"
    tools_dir.mkdir(parents=True)
    (tools_dir / "save_me.py").write_text("pass")
    
    fake_data = {
        'COMMANDS': '-t',
        'TARGET': 'save_me',
        'SCR_ARGV': [],
        'TAIL': ['keep']
    }
    
    with patch("subprocess.run"), \
         patch("os.get_terminal_size", return_value=MagicMock(columns=80)):
        
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        monkeypatch.chdir(workspace)
        
        script(fake_data, str(sigil_home))
        
        remaining_files = list(workspace.glob("*.py"))
        assert len(remaining_files) == 1
