from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from main import run_agent

app = FastAPI(title="Claim Submission Agent", version="1.0.0")

@app.post("/run")
async def run():
    """
    Upload a file to the server
    
    Args:
        file: The file to upload
        
    Returns:
        JSON response with upload status and file info
    """

    try:
        initial_state = {}
        final_state = run_agent(initial_state)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Run successfully",
                "final_state": final_state
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)