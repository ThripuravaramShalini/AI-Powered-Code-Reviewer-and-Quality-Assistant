"""Configuration settings for AI Code Reviewer."""

from enum import Enum
from typing import Dict, Any
import os
import textwrap

class DocstringStyle(Enum):
    GOOGLE = "google"
    NUMPY = "numpy"
    RST = "rst"

DEFAULT_SETTINGS = {
    "llm_model": "llama3.2",
    "docstring_style": DocstringStyle.GOOGLE.value,
    "coverage_threshold": 90.0,
    "max_tokens": 512,
    "docstring_prompt_template": textwrap.dedent("""
        Analyze the following Python function and generate a high-quality {style} style docstring.

        Code:
        ```python
        {function_code}
        ```

        Return ONLY the docstring in this exact format:
    """).strip(),
    "quality_weights": {
        "doc_coverage": 0.4,
        "complexity": 0.3,
        "validation": 0.3
    }
}

LLM_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def get_settings() -> Dict[str, Any]:
    return DEFAULT_SETTINGS.copy()

