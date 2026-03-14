"""LLaMA model interface using Ollama."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import ollama
from typing import Dict, Any, Optional
from configs.settings import get_settings, LLM_HOST

class LLaMAInterface:
    def __init__(self, model: str = None):
        self.model = model or get_settings()["llm_model"]
        # Ollama client uses env OLLAMA_HOST

    def generate_docstring(self, function_code: str, style: str = "google") -> str:
        """Generate docstring for function code."""
        settings = get_settings()
        prompt = settings["docstring_prompt_template"].format(
            style=style, function_code=function_code
        )
        
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.3,
                "num_predict": settings["max_tokens"]
            }
        )
        
        return response["message"]["content"].strip()

    def analyze_quality(self, code_snippet: str) -> Dict[str, Any]:
        """Get quality feedback."""
        prompt = f"""
Analyze this Python code for quality issues and suggest improvements:

{code_snippet}

Return JSON: {{"score": 0.0-1.0, "issues": [...], "suggestions": [...]}}
"""
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return {"raw": response["message"]["content"]}  # Parse later

# Global instance
llama_client = LLaMAInterface()

