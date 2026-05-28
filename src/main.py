from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# POINT-TO-PIN CONNECTION: We import our AI engine class from our adjacent file
from src.ai_engine import OpsMindAIEngine

# Initialize the web application
app = FastAPI(
    title="OpsMind AI Guardrail",
    description="Enterprise API engine for automated Infrastructure as Code static analysis.",
    version="1.0.0"
)

# Initialize a single, persistent instance of our AI engine to handle reasoning calls
ai_guardrail = OpsMindAIEngine()

# Strict schema definition for the incoming data payload
class CodePayload(BaseModel):
    file_name: str
    code_content: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "OpsMind AI Core"}

# THE CORE PIPELINE ENDPOINT
@app.post("/analyze")
def analyze_infrastructure_code(payload: CodePayload):
    """
    Accepts raw cloud code files, executes defensive data checks,
    and forwards the code payload directly into the automated AI reasoning engine.
    """
    # 1. Validation Safeguard
    if not payload.code_content.strip():
        raise HTTPException(status_code=400, detail="Code content cannot be empty.")
    
    try:
        print(f"[PROCESS] Sending '{payload.file_name}' to the AI Reasoning Engine...")
        
        # 2. RUNNING THE INTER-FILE PIPELINE:
        # We pass the incoming file variables into our engine's analysis method
        structured_report = ai_guardrail.analyze_code(
            file_name=payload.file_name, 
            code_content=payload.code_content
        )
        
        print(f"[SUCCESS] AI analysis completed for '{payload.file_name}'.")
        
        # 3. Return the fully structured, validated JSON data block directly to the caller
        return structured_report

    except Exception as e:
        print(f"[CRITICAL ERROR] Pipeline processing failure: {str(e)}")
        # If anything breaks (like an invalid API key), return an official Cloud 500 error
        raise HTTPException(status_code=500, detail=f"Internal AI Pipeline Error: {str(e)}")