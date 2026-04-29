# test unit: ~/.sigil/tests/test_parser.py
# test_parser.py version: 1.0
import pytest
from src.parser import parser, section, classify_head_commands

def test_section_mode_1_with_separator():
    tokens = ['-t', 'gentrees', '@', 'keep']
    head, tail = section(tokens, mode=1)
    assert head == ['-t', 'gentrees']
    assert tail == ['keep']

def test_section_mode_1_no_separator():
    tokens = ['-t', 'gentrees']
    head, tail = section(tokens, mode=1)
    assert head == ['-t', 'gentrees']
    assert tail == []

def test_section_mode_2_script_argv():
    head_tokens = ['-t', 'gentrees', '--ignore', '.git']
    script_argv = section(head_tokens, mode=2)
    assert script_argv == ['--ignore', '.git']

def test_classify_head_commands_valid():
    assert classify_head_commands(['-t', 'something']) == '-t'
    assert classify_head_commands(['-v']) == '-v'

def test_classify_head_commands_invalid():
    assert classify_head_commands(['ngasal']) == 'HINTS'
    assert classify_head_commands([]) == 'HINTS'

def test_parser_full_command():
    fake_argv = ['sigil', '-t', 'gentrees', '--ignore', '.git', '@', 'origin', 'keep']
    
    result = parser(fake_argv)
    
    assert result['COMMANDS'] == '-t'
    assert result['TARGET'] == 'gentrees'
    assert result['SCR_ARGV'] == ['--ignore', '.git']
    assert result['TAIL'] == ['origin', 'keep']
    assert '@' not in result['TAIL']

def test_parser_no_tail():
    fake_argv = ['sigil', '-t', 'gentrees', '--verbose']
    
    result = parser(fake_argv)
    
    assert result['TARGET'] == 'gentrees'
    assert result['SCR_ARGV'] == ['--verbose']
    assert result['TAIL'] == []

def test_parser_simple_flag():
    fake_argv = ['sigil', '-v']
    
    result = parser(fake_argv)
    
    assert result['COMMANDS'] == '-v'
    assert result['TARGET'] == []
    assert result['TAIL'] == []

def test_parser_missing_target():
    fake_argv = ['sigil', '-t']
    result = parser(fake_argv)
    assert result['TARGET'] == []
