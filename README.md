# Docstring Checker

A tool to analyze Python files for docstring parameter mismatches with function signatures.

## Installation

1. Clone the repository:
```bash
git clone git@github.com:ausdavoud/docdoc.git
cd docdoc
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

4. Install necessary packages (required only for web API):
```bash
pip install -r requirements.txt
```

## Usage

You can use this tool in two ways:

### 1. Local Command Line Usage

Run the checker directly from the command line:

```bash
python checker.py <filename>
```

Example:
```bash
python checker.py sample_code.py
```

Output:
```txt
Function: add
    Extra args in docstring: ['c']
Function: greet
    Missing args in docstring: ['age']
```

### 2. Web API Usage

Start the FastAPI server:

```bash
uvicorn checker:app --reload
```

Then navigate to `http://127.0.0.1:8000/docs` in your browser, click "Try it out" on the `/analyze/` endpoint, and upload your Python file for analysis.

Output:
```json
{
  "filename": "checker.py", // Yes, the checker is checking itself. Will it halt? XD
  "analysis": [
    {
      "function": "extract_doc_params",
      "missing_in_doc": [],
      "extra_in_doc": [],
      "status": "ok"
    },
    {
      "function": "analyze_file",
      "missing_in_doc": [],
      "extra_in_doc": [],
      "status": "ok"
    }
  ]
}
```
## Features

- Identifies missing parameters in docstrings
- Detects extra parameters documented but not in function signature
- Supports both command line and web interface usage
- Returns structured analysis results