# test unit: ~/.sigil/tests/conftest.py
# conftest.py version: 1.0
import pytest
import os
import sys
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_sigil_env(monkeypatch, tmp_path):
    fake_home = tmp_path / ".sigil"
    fake_home.mkdir()
    
    (fake_home / "src").mkdir()
    (fake_home / "tools").mkdir()
    
    monkeypatch.setenv("SIGIL_HOME", str(fake_home))
    
    root_src = str(Path(__file__).parent.parent / "src")
    if root_src not in sys.path:
        sys.path.insert(0, root_src)
        
    return fake_home
