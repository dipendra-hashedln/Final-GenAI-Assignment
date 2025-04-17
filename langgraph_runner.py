# from langgraph.graph import END, StateGraph
# from langchain_core.runnables import RunnableLambda
# from dotenv import load_dotenv
# load_dotenv()
# from langchain_groq import ChatGroq

# llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# # Define your state as a plain dictionary
# class GraphState(dict):
#     pass

# # Node 1: Parse SRS
# def parse_srs_fn(state: dict) -> dict:
#     print("[parse_srs_fn] Received state:", state)

#     srs_text = state.get("srs_text", "").lower()

#     # Simulated keyword-based parsing
#     requirements = []
#     if "register" in srs_text or "signup" in srs_text:
#         requirements.append("User registration")
#     if "login" in srs_text:
#         requirements.append("User login")
#     if "logout" in srs_text:
#         requirements.append("User logout")
#     if "profile" in srs_text:
#         requirements.append("User profile management")

#     state = state.copy()
#     state["requirements"] = requirements
#     print("[parse_srs_fn] Returning:", state)
#     return state






# # Node 2: Generate Code
# def generate_code_fn(state: GraphState):
#     print("[generate_code_fn] Received state:", state)
#     reqs = state.get("requirements", [])
#     code = "\n".join([f"# Code for {r}" for r in reqs])
#     new_state = state.copy()  # Copy existing state
#     new_state.update({"code": code})  # Update with new key
#     print("[generate_code_fn] Returning:", new_state)
#     return new_state

# # Node 3: Generate Tests
# def generate_tests_fn(state: dict) -> dict:
#     print("[generate_tests_fn] Received state:", state)
#     code = state.get("code", "")
#     # Simulate test generation (replace with real LLM later)
#     test_code = "\n".join([
#         "import unittest",
#         "",
#         "class TestApp(unittest.TestCase):",
#         "    def test_example(self):",
#         "        self.assertEqual(1 + 1, 2)",
#         "",
#         "if __name__ == '__main__':",
#         "    unittest.main()"
#     ])
#     state = state.copy()
#     state["tests"] = test_code
#     print("[generate_tests_fn] Returning:", state)
#     return state

# # Node 4: Run Tests

# import subprocess
# import tempfile
# import os

# def run_tests_fn(state: GraphState) -> GraphState:
#     print("[run_tests_fn] Received state:", state)
#     test_code = state.get("tests", "")

#     # Write test code to a temporary file
#     with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
#         temp_file.write(test_code)
#         temp_path = temp_file.name

#     # Run tests using subprocess
#     try:
#         result = subprocess.run(
#             ["python", temp_path],
#             capture_output=True,
#             text=True,
#             timeout=10
#         )
#         state["test_output"] = result.stdout
#         state["test_passed"] = result.returncode == 0
#     except subprocess.TimeoutExpired:
#         state["test_output"] = "Test execution timed out."
#         state["test_passed"] = False
#     except Exception as e:
#         state["test_output"] = f"Error running tests: {str(e)}"
#         state["test_passed"] = False
#     finally:
#         os.unlink(temp_path)  # delete temp test file

#     print("[run_tests_fn] Returning:", state)
#     return state

# # Node 5: Regenerate code
# def generate_code_fn(state: dict) -> dict:
#     print("[generate_code_fn] Received state:", state)
#     requirements = state.get("requirements", [])

#     if not requirements:
#         state["code"] = "# No requirements parsed."
#         return state

#     # Prompt to send to LLM
#     prompt = (
#         "Generate Python FastAPI backend code for the following features:\n"
#         + "\n".join(f"- {r}" for r in requirements)
#         + "\nReturn only valid Python code."
#     )

#     try:
#         response = llm.invoke(prompt)
#         code = response.content if hasattr(response, "content") else str(response)
#     except Exception as e:
#         code = f"# LLM Error: {e}"

#     state = state.copy()
#     state["code"] = code
#     print("[generate_code_fn] Returning:", state)
#     return state

# import os

# def run_graph_with_text(srs_text: str, project_id: str) -> dict:
#     initial = GraphState({"srs_text": srs_text})
#     state = parse_srs_fn(initial)

#     max_retries = 2
#     for attempt in range(1, max_retries + 2):
#         state = generate_code_fn(state)
#         state = generate_tests_fn(state)
#         state = run_tests_fn(state)
#         if state.get("test_passed"):
#             break
#         else:
#             state = regenerate_code_fn(state, attempt)

#     output_dir = f"generated_projects/project_{project_id}/app"
#     os.makedirs(output_dir + "/routes", exist_ok=True)
#     os.makedirs(output_dir + "/tests", exist_ok=True)

#     with open(f"{output_dir}/routes/main.py", "w", encoding="utf-8") as f:
#         f.write(state["code"])

#     with open(f"{output_dir}/tests/test_main.py", "w", encoding="utf-8") as f:
#         f.write(state["tests"])

#     return state

# if __name__ == "__main__":
#     # Simulate graph execution manually
#     initial_state = GraphState({
#         "srs_text": """
#         The system should allow users to register using email and password, log in securely,
#         view or edit their profile, and log out.
#         """
#     })

#     print("[main] Initial state:", initial_state)

#     # Step 1: Run parse_srs node
#     state = parse_srs_fn(initial_state)

#     # Step 2–4 and retry loop
#     max_retries = 2
#     for attempt in range(1, max_retries + 2):  # initial + 2 retries
#         state = generate_code_fn(state)
#         state = generate_tests_fn(state)
#         state = run_tests_fn(state)

#         if state.get("test_passed"):
#             print(f"\n✅ Tests passed on attempt {attempt}")
#             break
#         else:
#             print(f"\n❌ Tests failed on attempt {attempt}. Retrying...")
#             state = regenerate_code_fn(state, attempt)

#     print("\n✅ Final Output:")
#     print("Requirements:", state.get("requirements"))
#     print("\nGenerated Code:\n", state.get("code"))
#     print("\nGenerated Tests:\n", state.get("tests"))
#     print("\nTest Passed:", state.get("test_passed"))
#     print("\nTest Output:\n", state.get("test_output"))





