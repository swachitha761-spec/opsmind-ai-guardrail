import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.main import app
from src.ai_engine import GuardrailReport

# Initialize the official FastAPI Test Client framework
client = TestClient(app)

@patch("src.ai_engine.genai.Client")
def test_analyze_endpoint_security_failure(mock_genai_client):
    """
    Test Case: Validates that when a user uploads insecure code, 
    our system successfully flags a 'FAILED' status.
    """
    # 1. SETUP THE FAKE AI STUNT DOUBLE RESPONSE
    mock_response = MagicMock()
    # We force the mock text output to mirror a real Guardrail JSON layout
    mock_response.text = '{"overall_status": "FAILED", "estimated_monthly_cost": 0.0, "findings": []}'
    
    # Wire the fake response directly into Google's generate_content call pattern
    mock_instance = mock_genai_client.return_value
    mock_instance.models.generate_content.return_value = mock_response

    # 2. EXECUTE THE SIMULATED TEST TRAFFIC
    test_payload = {
        "file_name": "insecure_vpc.tf",
        "code_content": "resource 'aws_security_group' 'open_port' {}"
    }
    
    # Send a mock POST request to our running FastAPI framework
    response = client.post("/analyze", json=test_payload)

    # 3. VERIFY EXCELLENCE (ASSERTIONS)
    assert response.status_code == 200
    assert response.json()["overall_status"] == "FAILED"


@patch("src.ai_engine.genai.Client")
def test_analyze_endpoint_exception_handling(mock_genai_client):
    """
    Test Case: Validates that if Google's network completely drops,
    our server gracefully catches the error and throws a clean 500 error.
    """
    # Force the mock client to explode with a simulated network connection failure
    mock_instance = mock_genai_client.return_value
    mock_instance.models.generate_content.side_effect = Exception("Google Network Timeout Error")

    test_payload = {
        "file_name": "broken.tf",
        "code_content": "resource 'aws_instance' 'test' {}"
    }

    response = client.post("/analyze", json=test_payload)

    # Our main.py exception handling blocks must return a 500 status code
    assert response.status_code == 500
    assert "Internal AI Pipeline Error" in response.json()["detail"]