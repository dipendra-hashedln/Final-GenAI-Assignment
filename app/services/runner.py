# File: app/services/runner.py

import os
from app.models.graph_state import GraphState
from app.services.parse_srs import parse_srs_fn
from app.services.generate_code import generate_code_fn
from app.services.generate_tests import generate_tests_fn
from app.services.run_tests import run_tests_fn
from app.services.regenerate_code import regenerate_code_fn

def run_graph_with_text(srs_text: str, project_id: str) -> GraphState:
    # 1. Parse SRS
    state = parse_srs_fn(GraphState({"srs_text": srs_text}))

    # 2. Retry loop
    for attempt in range(1, 4):
        state = generate_code_fn(state)
        state = generate_tests_fn(state)
        state = run_tests_fn(state)
        if state.get("test_passed"):
            break
        state = regenerate_code_fn(state, attempt)

    # 3. Build the file map from state["raw_code"]
    file_map = {}
    current_file = None
    buffer = []
    for line in state["raw_code"].splitlines():
        if line.startswith("# FILE:"):
            if current_file:
                file_map[current_file] = "\n".join(buffer)
            current_file = line.replace("# FILE:", "").strip()
            buffer = []
        else:
            buffer.append(line)
    if current_file:
        file_map[current_file] = "\n".join(buffer)

    # 4. Write files with logging
    base = f"generated_projects/project_{project_id}/app"
    print("🗂 Writing generated files to:", base)
    for rel_path, code in file_map.items():
        full_path = os.path.join(base, rel_path)
        print("  •", full_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code)
    print("✅ Finished writing generated files.")

    return state


