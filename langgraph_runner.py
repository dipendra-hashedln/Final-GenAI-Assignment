from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableLambda

# Define your state as a plain dictionary
class GraphState(dict):
    pass

# Node 1: Parse SRS
def parse_srs_fn(state: GraphState):
    print("[parse_srs_fn] Received state:", state)
    requirements = ["Create user", "Login", "Get profile"]
    new_state = state.copy()  # Copy existing state
    new_state.update({"requirements": requirements})  # Update with new key
    print("[parse_srs_fn] Returning:", new_state)
    return new_state

# Node 2: Generate Code
def generate_code_fn(state: GraphState):
    print("[generate_code_fn] Received state:", state)
    reqs = state.get("requirements", [])
    code = "\n".join([f"# Code for {r}" for r in reqs])
    new_state = state.copy()  # Copy existing state
    new_state.update({"code": code})  # Update with new key
    print("[generate_code_fn] Returning:", new_state)
    return new_state

# Node 3: Generate Tests
def generate_tests_fn(state: dict) -> dict:
    print("[generate_tests_fn] Received state:", state)
    code = state.get("code", "")
    # Simulate test generation (replace with real LLM later)
    test_code = "\n".join([
        "import unittest",
        "",
        "class TestApp(unittest.TestCase):",
        "    def test_example(self):",
        "        self.assertEqual(1 + 1, 2)",
        "",
        "if __name__ == '__main__':",
        "    unittest.main()"
    ])
    state = state.copy()
    state["tests"] = test_code
    print("[generate_tests_fn] Returning:", state)
    return state

# Node 4: Run Tests

import subprocess
import tempfile
import os

def run_tests_fn(state: GraphState) -> GraphState:
    print("[run_tests_fn] Received state:", state)
    test_code = state.get("tests", "")

    # Write test code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
        temp_file.write(test_code)
        temp_path = temp_file.name

    # Run tests using subprocess
    try:
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        state["test_output"] = result.stdout
        state["test_passed"] = result.returncode == 0
    except subprocess.TimeoutExpired:
        state["test_output"] = "Test execution timed out."
        state["test_passed"] = False
    except Exception as e:
        state["test_output"] = f"Error running tests: {str(e)}"
        state["test_passed"] = False
    finally:
        os.unlink(temp_path)  # delete temp test file

    print("[run_tests_fn] Returning:", state)
    return state

# Node 5: Regenerate code
def regenerate_code_fn(state: dict, attempt: int = 1) -> dict:
    print(f"[regenerate_code_fn] Attempt {attempt} - Received state:", state)
    requirements = state.get("requirements", [])
    # Simulate improved code generation (or use LLM later)
    regenerated_code = "\n".join([f"# REGENERATED Code for {r}" for r in requirements])

    new_state = state.copy()
    new_state["code"] = regenerated_code
    print(f"[regenerate_code_fn] Returning (Attempt {attempt}):", new_state)
    return new_state




# Build the LangGraph (for structure, but we'll simulate execution)
builder = StateGraph(GraphState)
builder.add_node("parse_srs", RunnableLambda(parse_srs_fn))
builder.add_node("generate_code", RunnableLambda(generate_code_fn))

# Declare edges
builder.set_entry_point("parse_srs")
builder.add_edge("parse_srs", "generate_code")
builder.add_edge("generate_code", END)

# Compile (optional, for reference)
graph = builder.compile()

# Simulate graph execution manually
initial_state = GraphState()
print("[main] Initial state:", initial_state)

# Step 1: Run parse_srs node
state = parse_srs_fn(initial_state)

# # Step 2: Run generate_code node
# state = generate_code_fn(state)

# # Step 3: Run generate_tests node
# state = generate_tests_fn(state)

# # Step 4: Run run_tests node
# state = run_tests_fn(state)

max_retries = 2
for attempt in range(1, max_retries + 2):  # initial + 2 retries
    state = generate_code_fn(state)
    state = generate_tests_fn(state)
    state = run_tests_fn(state)

    if state.get("test_passed"):
        print(f"\n✅ Tests passed on attempt {attempt}")
        break
    else:
        print(f"\n❌ Tests failed on attempt {attempt}. Retrying...")
        state = regenerate_code_fn(state, attempt)


print("\n✅ Final Output:")
print("Requirements:", state.get("requirements"))
print("\nGenerated Code:\n", state.get("code"))
print("\nGenerated Tests:\n", state.get("tests"))
print("\nTest Passed:", state.get("test_passed"))
print("\nTest Output:\n", state.get("test_output"))




