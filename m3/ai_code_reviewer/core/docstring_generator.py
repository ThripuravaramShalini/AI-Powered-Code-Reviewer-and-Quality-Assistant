"""AI Docstring generator using LLaMA."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from typing import Dict, Any
from models.llama_interface import llama_client
from configs.settings import DocstringStyle

def generate_docstrings_for_file(file_analysis: Dict[str, Any], style: str = "google") -> Dict[str, Any]:
    """Generate missing docstrings."""
    for func in file_analysis.get("functions", []):
        if not func["has_docstring"]:
            func["generated_docstring"] = llama_client.generate_docstring(
                func["code_snippet"], style
            )
            func["quality_score"] = 0.87  # Placeholder; from validator
    
    for cls in file_analysis.get("classes", []):
        for method in cls["methods"]:
            if not method["has_docstring"]:
                method["generated_docstring"] = llama_client.generate_docstring(
                    method["code_snippet"], style
                )
    
    return file_analysis

def generate_style_formatted(style: str) -> str:
    """Map style."""
    return DocstringStyle(style.upper()).value

