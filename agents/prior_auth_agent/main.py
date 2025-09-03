# from openai import OpenAI

# client = OpenAI()

# # Mock payer policy database (in real-world this comes from payer APIs / PDFs)
# payer_policies = {
#     "MRI Brain": {"covered": True, "needs_docs": ["neurological symptoms", "physician referral"]},
#     "Knee Replacement": {"covered": True, "needs_docs": ["X-ray results", "failed conservative therapy"]},
#     "Genetic Testing": {"covered": False, "needs_docs": []},
# }

# def generate_prior_auth(clinical_note: str, procedure: str):
#     """Generate PA request and predict approval likelihood"""

#     # Check mock policy rules
#     policy = payer_policies.get(procedure, {"covered": False, "needs_docs": []})
#     needs_docs = ", ".join(policy["needs_docs"]) if policy["needs_docs"] else "None"
#     coverage_status = "Yes" if policy["covered"] else "No"

#     prompt = f"""
#     You are an AI assistant for prior authorization.
#     Create a draft PA request for the procedure: {procedure}.
    
#     Clinical note:
#     {clinical_note}
    
#     Payer policy:
#     - Covered: {coverage_status}
#     - Documentation required: {needs_docs}

#     Output format:
#     - Patient Clinical Summary
#     - Requested Procedure
#     - Justification (aligned with policy)
#     - Predicted Approval Likelihood (%)
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#     )

#     return response.choices[0].message.content


# # --- Demo Run ---
# if __name__ == "__main__":
#     clinical_note = """
#     55-year-old male with chronic right knee pain for 3 years. 
#     X-ray shows severe osteoarthritis. 
#     Patient has failed conservative therapy (NSAIDs, PT, injections). 
#     Functional limitation: unable to walk more than 50m without pain.
#     """

#     procedure = "Knee Replacement"
#     pa_request = generate_prior_auth(clinical_note, procedure)

#     print("=== AI-Generated Prior Authorization Request ===")
#     print(pa_request)


from typing import Dict, Any

def run_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "procedure": "Knee Replacement",
        "justification": "Meets policy due to failed conservative therapy...",
        "approval_likelihood": 0.92
    }
    print(f"[PriorAuthAgent] {result}")
    state["prior_auth"] = result
    return state

