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

# Step 2: Run generate_code node
state = generate_code_fn(state)

print("\n✅ Final Output:\n", state)