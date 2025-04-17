from app.models.graph_state import GraphState


def parse_srs_fn(state: GraphState) -> GraphState:
    print("[parse_srs_fn] Received state:", state)
    text = state.get("srs_text", "").lower()
    reqs = []
    if "register" in text: reqs.append("User registration")
    if "login" in text:    reqs.append("User login")
    if "logout" in text:   reqs.append("User logout")
    if "profile" in text:  reqs.append("User profile management")
    new = state.copy(); new["requirements"] = reqs
    print("[parse_srs_fn] Returning:", new)
    return new





