# pip install prefect langgraph
from concurrent.futures import thread
from typing import Dict, Any
# from prefect import task, flow
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
import requests
from deps import RCMState
from workflows import build_workflow


# Wrap agents as Prefect tasks
# @task
def eligibility_task(state: RCMState) -> RCMState:
    resp = requests.post("http://eligibility_agent:8000/run")
    state["eligibility"] = resp.json()
    return state

# @task
def prior_auth_task(state: RCMState) -> RCMState:
    resp = requests.post("http://prior_auth_agent:8001/run")
    state["prior_auth"] = resp.json()
    return state


# @task
def clinical_doc_task(state: RCMState) -> RCMState:
    resp = requests.post("http://clinical_doc_agent:8002/run")
    state["clinical_doc"] = resp.json()
    return state

def task_registry() -> Dict[str, Any]:
    return {
        "eligibility": eligibility_task,
        "prior_auth": prior_auth_task,
        "clinical_doc": clinical_doc_task,
    }

# Prefect Flow
# @flow
def rcm_pipeline(steps, workflow_type: str) -> RCMState:
    
    # Initial state
    state = {"workflow_type": workflow_type, "success": True, "retry_count": 0}
    
    # Run LangGraph workflow inside Prefect
    # workflow = StateGraph(RCMState)
    # workflow.add_node("eligibility", eligibility_task)
    # workflow.add_node("clinical_doc", clinical_doc_task)
    # workflow.add_node("prior_auth", prior_auth_task)

    # workflow.set_entry_point("eligibility")
    # workflow.add_edge("eligibility", "clinical_doc")
    # workflow.add_edge("clinical_doc", "prior_auth")
    # workflow.add_edge("prior_auth", END)

    workflow = build_workflow(steps, task_registry())
    
    memory = InMemorySaver()
    app = workflow.compile(checkpointer=memory)

    thread_id = "rcm_thread_1"

    final_state = app.invoke(state, config={"configurable": {"thread_id": thread_id}})
    return final_state

if __name__ == "__main__":
    steps = [] 
    result = rcm_pipeline(steps)
    print("\n=== Final Result ===")
    print(result)
