import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 1. THE STRUCTURED FORM (UNTOUCHED)
# ==========================================
# We keep our exact elite data structure so our server main.py doesn't break!
class GuardrailFinding(BaseModel):
    category: str = Field(description="Must be either 'Security' or 'FinOps'")
    severity: str = Field(description="Must be 'LOW', 'MEDIUM', or 'CRITICAL'")
    resource_target: str = Field(description="The exact resource identifier (e.g., aws_security_group.production_firewall)")
    risk_finding: str = Field(description="Deep technical analysis explaining the exact risk vulnerability or cost spike.")
    recommended_correction: str = Field(description="Step-by-step technical instructions on how to patch the configuration file.")

class GuardrailReport(BaseModel):
    overall_status: str = Field(description="Must be 'PASSED' or 'FAILED' (Fail if any MEDIUM or CRITICAL risks exist)")
    estimated_monthly_cost: float = Field(description="Rough dollar estimate of monthly cost impact for these resources")
    findings: List[GuardrailFinding] = Field(description="A collection of individual security or financial violations found.")


# ==========================================
# 2. THE GOOGLE GEMINI PROCESSING CORNER
# ==========================================
class OpsMindAIEngine:
    def __init__(self):
        # We fetch the new Google key safely from the terminal environment memory
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Initialize the official Google GenAI connection client
        self.client = genai.Client(api_key=self.api_key)

    def analyze_code(self, file_name: str, code_content: str) -> GuardrailReport:
        """
        Takes raw cloud code, bundles it with system engineering rules,
        and forces Gemini to output data directly matching our GuardrailReport model.
        """
        system_instruction = (
            "You are an Elite Principal Cloud Architect, FinOps Economist, and Lead Security Assessor.\n"
            "Analyze the provided Infrastructure as Code (Terraform) configuration with extreme scrutiny.\n"
            "Evaluate financial overhead issues and security posture vulnerabilities.\n"
            "You must return data that adheres strictly to the layout requested."
        )

        user_payload = f"File Name: {file_name}\n\nCode Content:\n{code_content}"

        # Request execution pointing to Google's stable, free gemini-2.5-flash model
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_payload,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=GuardrailReport,
            ),
        )

        # Convert the raw text JSON response back into a clean Python object
        return GuardrailReport.model_validate_json(response.text)
    

   