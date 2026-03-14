# AI-Powered Code Reviewer & Quality Assistant

## Quick Start

1. Setup venv:
   ```
   cd ai_code_reviewer
   python -m venv venv
   venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. Setup Ollama (LLaMA):
   ```
   ollama pull llama3.2
   ```

3. Run dashboard:
   ```
   streamlit run ui/dashboard.py
   ```

## Features
- AST parsing & docstring analysis
- LLaMA-powered docstring generation
- 4 Milestone dashboard
- JSON reports
- CI integration ready

Upload Python project folder via sidebar.

