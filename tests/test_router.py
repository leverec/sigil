# test unit: ~/.sigil/tests/test_router.py
# test_router.py version: 1.0
import pytest
import os
from unittest.mock import patch, MagicMock
from src.router import router

def test_router_v_command(setup_sigil_env):
    """Tes apakah command -v mengarah ke info.py"""
    fake_data = {
        'COMMANDS': '-v',
        'TARGET': '',
        'SCR_ARGV': [],
        'TOKENS': ['-v']
    }

    
    with patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec") as mock_module:
        
        
        mock_info_path = MagicMock()
        mock_module.return_value = mock_info_path
        
        router(fake_data)

        
        expected_path = os.path.join(os.getenv("SIGIL_HOME"), "src", "info.py")
        mock_spec.assert_called_once()
        assert mock_spec.call_args[0][1] == expected_path
        
        
        mock_info_path.info.assert_called_once()

def test_router_t_command(setup_sigil_env):
    """Tes apakah command -t mengarah ke script.py"""
    fake_data = {
        'COMMANDS': '-t',
        'TARGET': 'my_tool',
        'SCR_ARGV': ['--flag'],
        'TOKENS': ['-t', 'my_tool', '--flag']
    }

    with patch("importlib.util.spec_from_file_location"), \
         patch("importlib.util.module_from_spec") as mock_module:
        
        mock_script_path = MagicMock()
        mock_module.return_value = mock_script_path
        
        router(fake_data)
        
        
        mock_script_path.script.assert_called_once_with(fake_data, os.getenv("SIGIL_HOME"))

def test_router_invalid_command(capsys, setup_sigil_env):
    """Tes command ngasal"""
    fake_data = {'COMMANDS': 'ngasal', 'TARGET': '', 'SCR_ARGV': []}
    
    router(fake_data)
    
    captured = capsys.readouterr()
    assert "Try: sigil -h" in captured.out
