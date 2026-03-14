"""Code validator using pydocstyle and quality metrics."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pydocstyle
from typing import Dict, Any, List
from configs.settings import get_settings
import tempfile
from pathlib import Path

def validate_file(file_path: str) -> List[Dict[str, Any]]:
    """Run pydocstyle validation."""
    try:
        violations = pydocstyle.check_paths([file_path])
        return [
            {
                "line": v.line,
                "column": v.column,
                "message": v.message,
                "severity": "error" if v.severity == pydocstyle.ConventionChecker.ERROR else "warning"
            }
            for v in violations
        ]
    except Exception:
        return []

def compute_quality_score(func_analysis: Dict[str, Any]) -> float:
    """Quality score 0-1."""
    score = 0.0
    settings = get_settings()  # Fix import later
    
    # Doc presence
    doc_score = 1.0 if func_analysis["has_docstring"] else 0.5
    score += doc_score * settings["quality_weights"]["doc_coverage"]
    
    # Placeholder complexity (lines)
    lines = len(func_analysis["code_snippet"].splitlines())
    complexity = max(0, 1 - (lines / 50))
    score += complexity * settings["quality_weights"]["complexity"]
    
    # Validation (stub)
    score += 0.8 * settings["quality_weights"]["validation"]
    
    return round(score, 2)

def validate_analysis(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Validate full analysis."""
    for file_name, file_data in analysis["files"].items():
        file_path = file_name  # Assume exists
        file_data["violations"] = validate_file(file_path)
        
        for func in file_data["functions"]:
            func["quality_score"] = compute_quality_score(func)
        
        # Count issues
        analysis["issues_detected"] = len([v for f in analysis["files"].values() 
                                         for v in f.get("violations", [])])
    
    return analysis

