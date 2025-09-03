"""
02-clinical-documentation.py: Generate clinical documentation from provider-patient transcript.
pip install openai
"""
# from openai import OpenAI

# client = OpenAI()

# def generate_clinical_doc(transcript: str):
#     """Use LLM to generate SOAP note + coding suggestions"""
    
#     prompt = f"""
#     You are a clinical documentation assistant.
#     Convert the following provider-patient transcript into a structured SOAP note
#     and suggest possible ICD-10 and CPT codes.

#     Transcript:
#     {transcript}

#     Output format:
#     - Subjective:
#     - Objective:
#     - Assessment:
#     - Plan:
#     - Suggested ICD-10 Codes:
#     - Suggested CPT Codes:
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",  # lightweight LLM good for prototyping
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2,
#     )

#     return response.choices[0].message.content


# # --- Demo run ---
# if __name__ == "__main__":
#     sample_transcript = """
#     Patient reports chest tightness and shortness of breath for the past 2 days.
#     Denies fever or cough. 
#     On exam: BP 140/90, HR 96, O2 Sat 94% on room air, mild wheezing on auscultation.
#     Provider suspects asthma exacerbation, will start inhaled corticosteroids,
#     order chest X-ray, and follow up in 1 week.
#     """

#     clinical_doc = generate_clinical_doc(sample_transcript)
#     print("=== AI-Generated Clinical Documentation ===")
#     print(clinical_doc)


from typing import Dict, Any

def run_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    transcript = state.get("transcript", "")
    result = {
        "SOAP": "Asthma exacerbation...",
        "ICD10": ["J45.901"],
        "CPT": ["99213"]
    }
    print(f"[ClinicalDocAgent] {result}")
    state["clinical_doc"] = result
    return state