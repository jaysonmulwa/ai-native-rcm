from concurrent.futures import thread
from typing import Dict, Any
# from prefect import task, flow
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
import requests
from deps import RCMState
from workflows import build_workflow
import uuid


# Wrap agents as Prefect tasks
# @task
def eligibility_task(state: RCMState) -> RCMState:
    resp = requests.post("http://eligibility_agent:8000/run", json=state)
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

def medical_coding_task(state: RCMState) -> RCMState:
    resp = requests.post("http://medical_coding_agent:8003/run")
    state["medical_coding"] = resp.json()
    return state

def claim_scrubbing_task(state: RCMState) -> RCMState:
    resp = requests.post("http://claim_scrubbing_agent:8004/run")
    state["claim_scrubbing"] = resp.json()
    return state

def claim_submission_task(state: RCMState) -> RCMState:
    resp = requests.post("http://claim_submission_agent:8005/run")
    state["claim_submission"] = resp.json()
    return state

def task_registry() -> Dict[str, Any]:
    return {
        "eligibility": eligibility_task,
        "prior_auth": prior_auth_task,
        "clinical_doc": clinical_doc_task,
        "medical_coding": medical_coding_task,
        "claim_scrubbing": claim_scrubbing_task,
        "claim_submission": claim_submission_task,
    }

# Prefect Flow
# @flow
def rcm_pipeline(steps, workflow_type: str, file_path: str) -> RCMState:
    """
    Run RCM workflow based on selected steps.

    Lets us run different workflows based on user needs. Also for proper intergration with different UI's.
    """

    # Initial state
    state = {"workflow_type": workflow_type, "success": True, "retry_count": 0, "file_path": file_path}
    workflow = build_workflow(steps, task_registry())
    
    memory = InMemorySaver()
    app = workflow.compile(checkpointer=memory)

    id = str(uuid.uuid4())
    thread_id = f"rcm_thread_{id}"

    final_state = app.invoke(state, config={"configurable": {"thread_id": thread_id}})
    return final_state