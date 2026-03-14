"""AST-based Python code parser for functions, classes, and docstrings."""

import ast
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# from ai_code_reviewer.configs.settings import get_settings  # unused

class FunctionInfo(ast.NodeVisitor):
    def __init__(self):
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = [arg.arg for arg in node.args.args]
        has_docstring = self._has_docstring(node)
        
        func_info = {
            "name": node.name,
            "arguments": args,
            "has_docstring": has_docstring,
            "lineno": node.lineno,
            "code_snippet": None  # Filled later
        }
        
        if self.current_class:
            func_info["class"] = self.current_class
            self.current_class["methods"].append(func_info)
        else:
            self.functions.append(func_info)
        
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        class_info = {
            "name": node.name,
            "methods": [],
            "docstring_present": self._has_docstring(node),
            "lineno": node.lineno
        }
        self.current_class = class_info
        self.classes.append(class_info)
        self.generic_visit(node)
        self.current_class = None

    def _has_docstring(self, node: ast.AST) -> bool:
        docstring = ast.get_docstring(node)
        return bool(docstring)

def parse_python_file(file_path: str) -> Dict[str, Any]:
    """Parse single Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    visitor = FunctionInfo()
    visitor.visit(tree)
    
    # Extract code snippets
    for func in visitor.functions + [m for c in visitor.classes for m in c["methods"]]:
        func["code_snippet"] = _extract_code_snippet(file_path, func["lineno"])
    
    return {
        "functions": visitor.functions,
        "classes": visitor.classes
    }

def parse_directory(dir_path: str) -> Dict[str, Any]:
    """Parse entire directory recursively."""
    results = {
        "files": {},
        "summary": {
            "total_files": 0,
            "total_functions": 0,
            "total_classes": 0,
            "docstring_coverage": 0.0
        }
    }
    
    py_files = list(Path(dir_path).rglob("*.py"))
    results["summary"]["total_files"] = len(py_files)
    
    total_funcs = 0
    funcs_with_docs = 0
    
    for py_file in py_files:
        file_results = parse_python_file(str(py_file))
        results["files"][str(py_file)] = file_results
        
        total_funcs += len(file_results["functions"])
        for cls in file_results["classes"]:
            total_funcs += len(cls["methods"])
        
        # Coverage calc (simplified)
        funcs_with_docs += sum(1 for f in file_results["functions"] if f["has_docstring"])
    
    if total_funcs > 0:
        results["summary"]["docstring_coverage"] = (funcs_with_docs / total_funcs) * 100
    
    results["summary"]["total_functions"] = total_funcs
    # Classes count separate
    
    return results

def _extract_code_snippet(file_path: str, lineno: int, lines: int = 10) -> str:
    """Extract code snippet around function."""
    with open(file_path, "r") as f:
        lines_list = f.readlines()
    start = max(0, lineno - lines)
    end = min(len(lines_list), lineno + lines)
    return "".join(lines_list[start:end])

if __name__ == "__main__":
    # Test
    print(parse_directory("."))
