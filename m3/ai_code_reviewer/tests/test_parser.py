"""Basic tests."""

import pytest
import tempfile
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.parser import parse_python_file

def test_parser():
    # Create temp py file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def test_func(a, b):
    \"""Doc.\"""
    return a + b
        """)
        temp_path = f.name
    
    try:
        result = parse_python_file(temp_path)
        assert len(result["functions"]) == 1
        assert result["functions"][0]["name"] == "test_func"
        assert result["functions"][0]["has_docstring"] == True
    finally:
        os.unlink(temp_path)

if __name__ == "__main__":
    pytest.main([__file__])

