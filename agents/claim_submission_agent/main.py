import cohere
import json
from typing import Dict, Any

# Mock payer claim rules (in real-world this comes from payer APIs / PDFs)
payer_claim_rules = {
    "Knee Replacement": {
        "covered": True,
        "required_codes": ["27447", "M17.11"],
        "required_docs": ["operative report", "discharge summary"]
    },
    "MRI Brain": {
        "covered": True,
        "required_codes": ["70551", "G93.9"],
        "required_docs": ["radiology report"]
    },
    "Genetic Testing": {
        "covered": False,
        "required_codes": [],
        "required_docs": []
    },
}

def generate_claim_submission(clinical_note: str, procedure: str):
    """
    Generate claim submission draft and predict payment likelihood.
    """

    # Check mock claim rules
    claim_rule = payer_claim_rules.get(procedure, {"covered": False, "required_codes": [], "required_docs": []})
    required_codes = ", ".join(claim_rule["required_codes"]) if claim_rule["required_codes"] else "None"
    required_docs = ", ".join(claim_rule["required_docs"]) if claim_rule["required_docs"] else "None"
    coverage_status = "Yes" if claim_rule["covered"] else "No"

    prompt = f"""
    You are an AI assistant for healthcare claim submission.
    Create a draft claim for the procedure: {procedure}.
    
    Clinical note:
    {clinical_note}
    
    Payer claim rules:
    - Covered: {coverage_status}
    - Required codes: {required_codes}
    - Required documentation: {required_docs}

    Output format:
    - Patient Clinical Summary
    - Procedure Performed
    - ICD/CPT Codes
    - Documentation Attached
    - Predicted Payment Likelihood (%)

    Required JSON fields:
    {{
        "patient_summary": string,
        "procedure_performed": string,
        "codes": list of strings,
        "documentation": list of strings,
        "payment_likelihood": float (0 to 1)
    }}
    """
    co = cohere.ClientV2()
    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": prompt}],
    )

    res = response.message.content[0].text.strip()
    return json.loads(res)

def run_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    clinical_note = """
    55-year-old male with chronic right knee pain for 3 years. 
    X-ray shows severe osteoarthritis. 
    Patient underwent right total knee replacement. 
    Discharge summary: stable, no complications.
    """

    procedure = "Knee Replacement"
    claim = generate_claim_submission(clinical_note, procedure)

    print("=== AI-Generated Claim Submission ===")
    print(claim)

    state["claim_submission"] = claim
    return state
