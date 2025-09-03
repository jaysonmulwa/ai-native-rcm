from typing import Dict, Any

class RCMState(Dict[str, Any]):
    workflow_type: str

    eligibility: Any
    prior_auth: Any
    clinical_doc: Any

    error_message: str
    success: bool
    retry_count: int
    source: str