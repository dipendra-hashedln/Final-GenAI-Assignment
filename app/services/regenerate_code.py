# app/services/regenerate_code.py

from app.models.graph_state import GraphState

def regenerate_code_fn(state: GraphState, attempt: int = 1) -> GraphState:
    print(f"[regenerate_code_fn] Attempt {attempt} - Received state:", state)
    reqs = state.get("requirements", [])
    regen = "\n".join(f"# REGENERATED Code for {r}" for r in reqs)
    new = state.copy()
    new["raw_code"] = regen
    print(f"[regenerate_code_fn] Returning (Attempt {attempt}):", new)
    return new


