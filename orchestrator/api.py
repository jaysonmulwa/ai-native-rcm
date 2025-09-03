from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from main import rcm_pipeline

app = FastAPI(title="RCM interface", version="1.0.0")

class RunRequest(BaseModel):
    workflow_type: str

@app.post("/run")
async def run(request: RunRequest):
    """
    Run different workflows as required
    
    Args:
        file: The file to upload
        
    Returns:
        JSON response with upload status and file info
    """

    steps = []
    workflow_type = request.workflow_type

    if workflow_type == "eligibility_only":
        steps = ["eligibility"]
    elif workflow_type == "clinical_doc_only":
        steps = ["clinical_doc"]
    elif workflow_type == "prior_auth_only":
        steps = ["prior_auth"]
    elif workflow_type == "eligibility_clinical":
        steps = ["eligibility", "clinical_doc"]
    elif workflow_type == "clinical_prior_auth":
        steps = ["clinical_doc", "prior_auth"]
    elif workflow_type == "eligibility_prior_auth":
        steps = ["eligibility", "prior_auth"]
    elif workflow_type == "full":
        steps = [
            "eligibility",
            "clinical_doc",
            "prior_auth",
        ]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid workflow type: {workflow_type}"
        )

    result = rcm_pipeline(steps, workflow_type="full")
    print("\n=== Final Result ===")
    print(result)

    try:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Run successfully",
                "final_state": result
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)