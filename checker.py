import ast
import os
import re
import sys

from fastapi import FastAPI, File, UploadFile


def extract_doc_params(docstring: str) -> list:
    """Extract parameter names from a docstring.

    Args:
        docstring (str): The docstring to parse.

    Returns:
        list: A list of parameter names found in the docstring.
    """

    matches = re.findall(r"\s*(\w+)\s*\(", docstring, re.MULTILINE)
    return matches


def analyze_file(filename: str) -> None:
    """Analyze a Python file for docstring parameter mismatches.

    Args:
        filename (str): The path to the Python file to analyze.
    """
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    results = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        func_name = node.name
        func_params = [arg.arg for arg in node.args.args]
        docstring = ast.get_docstring(node=node)
        doc_params = extract_doc_params(docstring)

        missing_in_doc = list(set(func_params) - set(doc_params))
        extra_in_doc = list(set(doc_params) - set(func_params))

        results.append(
            {
                "function": func_name,
                "missing_in_doc": missing_in_doc,
                "extra_in_doc": extra_in_doc,
                "status": "ok"
                if not missing_in_doc and not extra_in_doc
                else "mismatch",
            }
        )

        print(f"Function: {func_name}")
        if missing_in_doc:
            print(f"    Missing args in docstring: {missing_in_doc}")
        if extra_in_doc:
            print(f"    Extra args in docstring: {extra_in_doc}")
        if not missing_in_doc and not extra_in_doc:
            print("    Docstring matches function signature.")

    return results


app = FastAPI(title="Docstring Checker", version="0.1.0")


@app.post("/analyze/")
async def analyze_endpoint(file: UploadFile = File(...)):
    """API endpoint to analyze an uploaded Python file for docstring parameter mismatches.

    Args:
        file (UploadFile): The uploaded Python file.
    """
    contents = await file.read()
    with open("uploaded_code.py", "wb") as f:
        f.write(contents)
    results = analyze_file("uploaded_code.py")
    os.remove("uploaded_code.py")
    return {"filename": file.filename, "analysis": results}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checker.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    analyze_file(filename)
