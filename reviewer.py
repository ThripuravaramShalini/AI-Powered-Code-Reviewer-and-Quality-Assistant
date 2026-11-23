"""Rule-based starter checks for Java and Python code."""

import ast
import re


def make_issue(severity, title, detail, suggestion):
    return {
        "severity": severity,
        "title": title,
        "detail": detail,
        "suggestion": suggestion,
    }


def review_code(language, code):
    language = language.lower().strip()
    issues = []
    lines = code.splitlines()

    if not code.strip():
        issues.append(make_issue("high", "Empty source code",
                                 "No source code was supplied.",
                                 "Paste code and submit the review again."))
    elif language == "python":
        try:
            ast.parse(code)
        except SyntaxError as exc:
            issues.append(make_issue(
                "high", "Python syntax error",
                f"{exc.msg} at line {exc.lineno}.",
                "Correct the syntax error before running the program."
            ))

        if "except:" in code:
            issues.append(make_issue(
                "medium", "Bare except clause",
                "A bare except can hide unexpected errors.",
                "Catch a specific exception type."
            ))
        if re.search(r"\\beval\\s*\\(", code):
            issues.append(make_issue(
                "high", "Use of eval()",
                "eval() can execute dynamically supplied code.",
                "Avoid eval(); use safer parsing or explicit logic."
            ))
        if re.search(r"\\bprint\\s*\\(", code):
            issues.append(make_issue(
                "low", "Print statement found",
                "Print statements may be temporary debugging output.",
                "Use logging for application diagnostics when appropriate."
            ))

    elif language == "java":
        if not re.search(r"\\bclass\\s+\\w+", code):
            issues.append(make_issue(
                "high", "Class declaration not found",
                "No Java class declaration was detected.",
                "Add a class declaration and match the public class name to the file name."
            ))
        if "System.out.println" in code:
            issues.append(make_issue(
                "low", "Console output found",
                "System.out.println is useful in beginner programs and debugging.",
                "Consider a logging framework for larger applications."
            ))
        if re.search(r"\\bcatch\\s*\\(\\s*Exception\\b", code):
            issues.append(make_issue(
                "medium", "Broad exception handling",
                "Catching Exception may hide the exact failure.",
                "Catch the specific exception types your code can handle."
            ))
    else:
        raise ValueError("Unsupported language. Choose java or python.")

    long_lines = [n for n, line in enumerate(lines, start=1) if len(line) > 120]
    if long_lines:
        issues.append(make_issue(
            "low", "Long source lines",
            f"Lines longer than 120 characters: {long_lines[:10]}.",
            "Break long statements into smaller, readable lines."
        ))

    deductions = {"high": 25, "medium": 12, "low": 5}
    score = max(0, 100 - sum(deductions[x["severity"]] for x in issues))
    suggestions = [x["suggestion"] for x in issues]
    if not suggestions:
        suggestions = ["No issues were detected by the current checks. Add tests and review edge cases."]

    return {"quality_score": score, "issues": issues, "suggestions": suggestions}
