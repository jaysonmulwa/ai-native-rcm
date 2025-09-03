"""
01-eligibility.py: Extract insurance ID from card image and check eligibility.
pip install pytesseract pillow openai
"""

import redis
from rq import Queue

from typing import Dict, Any

import pytesseract
from PIL import Image

# Mock eligibility database
mock_db = {
    "ABC123456": {"status": "Eligible", "plan": "Gold PPO", "copay": "$25"},
    "XYZ987654": {"status": "Inactive", "plan": "Silver HMO", "copay": "N/A"},
}

def extract_insurance_id(image_path):
    """Extract insurance ID from image using OCR"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    # Simple parsing: look for ID-like string
    for word in text.split():
        if word.isalnum() and len(word) >= 6:
            return word
    return None

def check_eligibility(insurance_id):
    """Mock eligibility check against database"""
    return mock_db.get(insurance_id, {"status": "Unknown", "plan": "N/A", "copay": "N/A"})

# --- Demo ---
# if __name__ == "__main__":
#     image_path = "insurance_card_sample.png"  # Replace with real card image
#     insurance_id = extract_insurance_id(image_path)
    
#     if insurance_id:
#         print(f"Extracted Insurance ID: {insurance_id}")
#         result = check_eligibility(insurance_id)
#         print("Eligibility Check Result:", result)
#     else:
#         print("❌ Could not extract Insurance ID.")


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
    insurance_id = "ABC123456"
    result = {"eligible": True, "plan": "Gold PPO", "copay": "$25", "insurance_id": insurance_id}
    print(f"[EligibilityAgent] {result}")
    state["eligibility"] = result

    persist_to_redis(state)
    #enqueue_task(state)
    #dequeue_task()

    return state

if __name__ == "__main__":
    initial_state = {"transcript": "Patient has insurance ID ABC123456."}
    final_state = run_agent(initial_state)
    print("\n=== Final State ===")
    print(final_state)