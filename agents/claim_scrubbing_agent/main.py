import json
from typing import Dict, Any

# Mock payer claim rules (in real-world this comes from payer APIs / PDFs)
payer_claim_rules = {
    "MRI Brain": {
        "required_fields": ["diagnosis_code", "procedure_code", "physician_signature"],
        "denial_reasons": ["missing documentation", "invalid diagnosis code"],
    },
    "Knee Replacement": {
        "required_fields": ["diagnosis_code", "procedure_code", "operative_report", "pre-op clearance"],
        "denial_reasons": ["incomplete operative report", "missing pre-op clearance"],
    },
    "Genetic Testing": {
        "required_fields": ["diagnosis_code", "procedure_code", "genetic counseling note"],
        "denial_reasons": ["not medically necessary", "missing counseling note"],
    },
}

def scrub_claim(claim: Dict[str, Any], procedure: str) -> Dict[str, Any]:
    """
    Scrub claim for completeness and compliance with payer rules.
    Returns a dict with status and issues found.
    """
    rules = payer_claim_rules.get(procedure, {"required_fields": [], "denial_reasons": []})
    missing_fields = [field for field in rules["required_fields"] if field not in claim or not claim[field]]
    issues = []

    if missing_fields:
        issues.append(f"Missing fields: {', '.join(missing_fields)}")

    # Example: check for invalid diagnosis code format (mock logic)
    if "diagnosis_code" in claim and not claim["diagnosis_code"].startswith("M"):
        issues.append("Diagnosis code does not match expected format (should start with 'M').")

    status = "Clean" if not issues else "Issues Found"
    return {
        "status": status,
        "issues": issues,
        "claim": claim,
        "procedure": procedure,
    }

def run_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # Example claim data
    claim = {
        "diagnosis_code": "M17.11",
        "procedure_code": "27447",
        "operative_report": "Attached",
        "pre-op_clearance": "Attached",
        "physician_signature": "Dr. Smith",
    }
    procedure = "Knee Replacement"
    scrubbed = scrub_claim(claim, procedure)

    print("=== Claims Scrubbing Agent Output ===")
    print(json.dumps(scrubbed, indent=2))

    state["scrubbed_claim"] = scrubbed
    return state

