"""
02-clinical-documentation.py: Generate clinical documentation from provider-patient transcript.
pip install openai
"""
from typing import Dict, Any
import json
import cohere


def generate_clinical_doc(transcript: str):
    """
    Use LLM to generate SOAP note + coding suggestions
    
    OpenAI GPT-4 Example Prompt:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight LLM good for prototyping
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
    """
    
    prompt = f"""
    You are a clinical documentation assistant.
    Convert the following provider-patient transcript into a structured SOAP note
    and suggest possible ICD-10 and CPT codes.

    Transcript:
    {transcript}

    Output format:
    - Subjective:
    - Objective:
    - Assessment:
    - Plan:
    - Suggested ICD-10 Codes:
    - Suggested CPT Codes:

    Required JSON fields:
    {{
        "subjective": string,
        "objective": string,
        "assessment": string,
        "plan": string,
        "icd10_codes": list of strings,
        "cpt_codes": list of strings
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
    sample_transcript = """
    Patient reports chest tightness and shortness of breath for the past 2 days.
    Denies fever or cough. 
    On exam: BP 140/90, HR 96, O2 Sat 94% on room air, mild wheezing on auscultation.
    Provider suspects asthma exacerbation, will start inhaled corticosteroids,
    order chest X-ray, and follow up in 1 week.
    """

    clinical_doc = generate_clinical_doc(sample_transcript)
    print("=== AI-Generated Clinical Documentation ===")
    print(clinical_doc)

    state["clinical_doc"] = clinical_doc
    return state