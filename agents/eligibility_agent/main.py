"""
01-eligibility.py: Extract insurance ID from card image and check eligibility.
"""

import redis
from rq import Queue
from typing import Dict, Any
import pytesseract
from PIL import Image
from openai import OpenAI
import json
import requests
import cohere

# client = OpenAI()

# Mock eligibility database
mock_db = {
    "ABC123456": {"status": "Eligible", "plan": "Gold PPO", "copay": "$25"},
    "XYZ987654": {"status": "Inactive", "plan": "Silver HMO", "copay": "N/A"},
    "5678 1234-A": {"status": "Eligible", "plan": "Gold PPO", "copay": "$25"},
}

def extract_insurance_details_ocr(image_path) -> str:
    """Extract insurance ID from image using OCR"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def extract_with_llm(text: str) -> dict:
    """
    Use an LLM to extract insurance details as JSON

    OpenAI GPT-4 Example Prompt:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight model
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    raw_output = response.choices[0].message.content.strip()
    print("[LLM] Raw Output:", raw_output)
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {"insurance_id": None, "plan": None, "copay": None}
    
    """
    prompt = f"""
    You are a medical insurance card parser.
    Extract key fields from this OCR text and return as valid JSON:

    OCR Text:
    {text}

    Required JSON fields:
    {{
      "insurance_id": string,
      "plan": string,
      "copay": string
    }}
    """
    try:
        co = cohere.ClientV2()
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt}],
        )

        res = response.message.content[0].text.strip()
        return json.loads(res)
    except (requests.RequestException, KeyError) as e:
        print("[LLM] Error:", e)
        return {"insurance_id": None, "plan": None, "copay": None}
    except json.JSONDecodeError:
        return {"insurance_id": None, "plan": None, "copay": None}

def check_eligibility(insurance_id):
    """Mock eligibility check against database"""
    if mock_db.get(insurance_id):
        return True
    return False

def enqueue_task(state: Dict[str, Any]) -> None:
    q = Queue(connection=redis.Redis(host="localhost", port=6379))
    job = q.enqueue("tasks.process_eligibility", state)
    print(f"Enqueued job {job.id} to process eligibility.")

def dequeue_task() -> Any:
    r = redis.Redis(host="localhost", port=6379)
    q = Queue(connection=r)
    if q.jobs:
        next_job = q.jobs[0]
        print(f"Next job in queue: {next_job.id}")
        print(f"Function name: {next_job.func_name}")
        print(f"Arguments: {next_job.args}")
    else:
        print("Queue is empty.")

def persist_to_redis(state: Dict[str, Any], key: str = "eligibility_state") -> None:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.set("claim:123", "eligibility_passed")
    print(r.get("claim:123"))

def run_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # insurance_id = "ABC123456"
    # result = {"eligible": True, "plan": "Gold PPO", "copay": "$25", "insurance_id": insurance_id}
    # print(f"[EligibilityAgent] {result}")
    # state["eligibility"] = result


    if "file_path" in state:
        text = extract_insurance_details_ocr(state["file_path"])
        details = extract_with_llm(text)
        state["eligibility"] = details

        if details.get("insurance_id"):
            eligibility_result = check_eligibility(details["insurance_id"])
            state["eligibility"]["eligible"] = eligibility_result
            state["success"] = True
    else:
        state["success"] = False
        state["error_message"] = "file_path not provided"
    
    #persist_to_redis(state)
    #enqueue_task(state)
    #dequeue_task()

    return state