import random
from typing import Literal
from langgraph.graph import StateGraph, START, END
from agent.configuration import Configuration
from agent.state import State


def node_1(state):
    print("----Node 1----")
    return {"graph_state": state["graph_state"] + " I am"}


def node_2(state):
    print("----Node 2----")
    return {"graph_state": state["graph_state"] + " happy"}


def node_3(state):
    print("----Node 3----")
    return {"graph_state": state["graph_state"] + " sad"}


# Conditional Edge
def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"

    return "node_3"


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("node_1", node_1)
workflow.add_node("node_2", node_2)
workflow.add_node("node_3", node_3)

# Set the entrypoint as `call_model`
workflow.add_edge(START, "node_1")
workflow.add_conditional_edges("node_1", decide_mood)
workflow.add_edge("node_2", END)
workflow.add_edge("node_3", END)

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "Simple Router"  # This defines the custom name in LangSmith
