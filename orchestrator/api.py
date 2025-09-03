from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from main import rcm_pipeline

app = FastAPI(title="RCM interface", version="1.0.0")

UPLOAD_DIR = Path("/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/run")
async def run(workflow_type: str = Form(...), file: UploadFile = File(...)):
    """
    Run different workflows as required
    
    Args:
        file: The file to upload
        
    Returns:
        JSON response with upload status and file info
    """

    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    

    print(workflow_type, file_path)

    if workflow_type == "eligibility_only":
        steps = ["eligibility"]
    elif workflow_type == "clinical_doc_only":
        steps = ["clinical_doc"]
    elif workflow_type == "prior_auth_only":
        steps = ["prior_auth"]
    elif workflow_type == "pre_auth_clinical_doc":
        steps = [
            "eligibility",
            "prior_auth",
            "clinical_doc",
        ]
    elif workflow_type == "full":
        steps = [
            "eligibility",
            "prior_auth",
            "clinical_doc",
            "medical_coding",
            "claim_scrubbing",
            "claim_submission",
        ]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid workflow type: {workflow_type}"
        )

    result = rcm_pipeline(steps, workflow_type="full", file_path=str(file_path))
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