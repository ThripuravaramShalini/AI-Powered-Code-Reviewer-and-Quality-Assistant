# AI Code Reviewer & Quality Assistant

A Java + Python + SQL starter project. Java reads a source file and sends it to a Python Flask API. Python checks common quality issues, calculates a score, and stores review history in SQLite.

**Honest project scope:** this version is a rule-based MVP, not a connected large-language-model service. You can extend `reviewer.py` with an LLM API later.

## Structure
```text
ai-code-reviewer-quality-assistant/
  python_backend/app.py
  python_backend/reviewer.py
  python_backend/requirements.txt
  java_client/src/CodeReviewClient.java
  database/schema.sql
  sample_code.java
  sample_code.py
  .gitignore
  README.md
```

## Run Python API
From `python_backend`:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The API runs at `http://127.0.0.1:5000`.

## Run Java client
Open a second terminal from the project root:
```bash
cd java_client
javac src/CodeReviewClient.java
java -cp src CodeReviewClient ../sample_code.java
```
Use `../sample_code.py` to review Python code.

## API
`POST /review` with JSON:
```json
{"language":"java","code":"public class Demo {}"}
```
`GET /reviews` lists the latest saved reviews.

## Push to GitHub
Create an empty GitHub repository, then run these commands from the project root:
```bash
git init
git add .
git commit -m "Initial commit - Code Reviewer"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-code-reviewer-quality-assistant.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username.
