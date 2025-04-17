# app/services/generate_tests.py

from app.models.graph_state import GraphState

def generate_tests_fn(state: GraphState) -> GraphState:
    print("[generate_tests_fn] Received state:", state)
    # Replace with LLM-based test gen if needed
    test_code = (
        "import unittest\n\n"
        "class TestApp(unittest.TestCase):\n"
        "    def test_example(self):\n"
        "        self.assertEqual(1+1, 2)\n\n"
        "if __name__ == '__main__':\n"
        "    unittest.main()"
    )
    new = state.copy()
    new["tests_code"] = test_code
    print("[generate_tests_fn] Returning:", new)
    return new


