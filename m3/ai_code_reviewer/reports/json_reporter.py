"""JSON report generator."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from typing import Dict, Any
import json
from pathlib import Path
from core.parser import parse_directory
from core.docstring_generator import generate_docstrings_for_file
from core.validator import validate_analysis

def generate_report(dir_path: str, output_path: Optional[str] = None, style: str = "google") -> Dict[str, Any]:
    """Full pipeline: parse -> generate -> validate -> report."""
    
    # Parse
    analysis = parse_directory(dir_path)
    
    # Generate docstrings
    for file_name, file_data in analysis["files"].items():
        generate_docstrings_for_file(file_data, style)
    
    # Validate & score
    analysis = validate_analysis(analysis)
    
    # Summary
    report = {
        "project_name": Path(dir_path).name,
        "scan_timestamp": datetime.now().isoformat(),
        "total_files": analysis["summary"]["total_files"],
        "total_functions": analysis["summary"]["total_functions"],
        "total_classes": sum(len(f["classes"]) for f in analysis["files"].values()),
        "docstring_coverage": f"{analysis['summary']['docstring_coverage']:.0f}%",
        "issues_detected": analysis.get("issues_detected", 0),
        "files": list(analysis["files"].values())
    }
    
    if output_path:
        Path(output_path).write_text(json.dumps(report, indent=2))
    
    return report

if __name__ == "__main__":
    report = generate_report(".")
    print(json.dumps(report, indent=2))

