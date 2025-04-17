# File: app/services/generate_code.py

import os
from app.models.graph_state import GraphState
from app.services.llm_setup import llm

def generate_code_fn(state: GraphState) -> GraphState:
    """
    LLM-powered code generation node.
    Prompts the model to output a complete FastAPI project
    broken into separate files, each prefixed with a "# FILE: <path>" line.
    """
    print("[generate_code_fn] Received state:", state)
    requirements = state.get("requirements", [])

    # Build a prompt that instructs the LLM to split output into files
    prompt = f"""
You are an expert Python backend engineer using FastAPI.
Given the following feature list, generate a complete project under the `app/` folder.
List each file as:

# FILE: app/<subfolder>/<filename>.py
<valid Python code for that module>

Features:
{chr(10).join(f"- {r}" for r in requirements)}

Do NOT include any extra explanation or markdown—output only the file markers and code.
"""

    try:
        # Invoke the LLM to generate raw multi-file code
        resp = llm.invoke(prompt)
        raw = getattr(resp, "content", str(resp))
    except Exception as e:
        raw = f"# LLM Error: {e}"

    # Store the raw response for downstream parsing
    new_state = state.copy()
    new_state["raw_code"] = raw
    print("[generate_code_fn] Returning raw_code:\n", raw)
    return new_state



