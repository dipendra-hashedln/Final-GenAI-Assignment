# app/services/run_tests.py

import subprocess, tempfile, os
from app.models.graph_state import GraphState

def run_tests_fn(state: GraphState) -> GraphState:
    print("[run_tests_fn] Received state:", state)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(state["tests_code"])
        path = tmp.name

    result = subprocess.run(["python", path], capture_output=True, text=True)
    os.unlink(path)

    new = state.copy()
    new["test_passed"] = (result.returncode == 0)
    new["test_output"] = result.stdout
    print("[run_tests_fn] Returning:", new)
    return new


