# app.py
# Main application file for Claims Management Service

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Claim, ClaimUpdate
from database import ClaimDatabase
import uvicorn
import requests
import os

# Initialize FastAPI app
app = FastAPI(
    title="Claims Management Service",
    description="Microservice for managing insurance claims",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = ClaimDatabase()

# Policy Service URL (will be used to verify policies)
POLICY_SERVICE_URL = "http://localhost:8001"  # Our Policy Service

# ===================== API ENDPOINTS =====================

@app.get("/")
async def root():
    """Check if service is running"""
    return {
        "message": "Claims Management Service is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /claims": "Get all claims",
            "GET /claims/{claim_id}": "Get specific claim",
            "POST /claims": "File a new claim",
            "PUT /claims/{claim_id}": "Update claim",
            "DELETE /claims/{claim_id}": "Delete claim",
            "GET /claims/policy/{policy_number}": "Get claims by policy",
            "GET /claims/customer/{email}": "Get claims by customer",
            "GET /claims/status/{status}": "Get claims by status"
        }
    }

@app.get("/claims", response_model=List[Claim])
async def get_all_claims():
    """Get all claims"""
    return db.get_all_claims()

@app.get("/claims/{claim_id}", response_model=Claim)
async def get_claim(claim_id: int):
    """Get a specific claim by ID"""
    claim = db.get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@app.post("/claims", response_model=Claim, status_code=201)
async def create_claim(claim: Claim):
    """
    File a new insurance claim
    First verifies that the policy exists by calling Policy Service
    """
    # Verify that the policy exists by calling Policy Service
    try:
        # In a real app, you'd have a proper endpoint to get policy by number
        # For now, we'll just check if the policy service is running
        response = requests.get(f"{POLICY_SERVICE_URL}/policies")
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Policy service unavailable")
        
        # Note: In production, you'd validate if the specific policy number exists
        # For demo purposes, we'll assume it exists
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Policy service is not reachable. Please ensure Policy Service is running on port 8001"
        )
    
    # Check if claim number already exists
    existing_claims = db.get_all_claims()
    for c in existing_claims:
        if c.claim_number == claim.claim_number:
            raise HTTPException(status_code=400, detail="Claim number already exists")
    
    return db.create_claim(claim)

@app.put("/claims/{claim_id}", response_model=Claim)
async def update_claim(claim_id: int, claim_update: ClaimUpdate):
    """Update an existing claim"""
    update_data = {k: v for k, v in claim_update.dict().items() if v is not None}
    
    updated_claim = db.update_claim(claim_id, update_data)
    if not updated_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return updated_claim

@app.delete("/claims/{claim_id}")
async def delete_claim(claim_id: int):
    """Delete a claim"""
    success = db.delete_claim(claim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return {"message": f"Claim {claim_id} deleted successfully"}

@app.get("/claims/policy/{policy_number}", response_model=List[Claim])
async def get_claims_by_policy(policy_number: str):
    """Get all claims for a specific policy"""
    return db.get_claims_by_policy(policy_number)

@app.get("/claims/customer/{email}", response_model=List[Claim])
async def get_claims_by_customer(email: str):
    """Get all claims for a specific customer"""
    return db.get_claims_by_customer(email)

@app.get("/claims/status/{status}", response_model=List[Claim])
async def get_claims_by_status(status: str):
    """Get all claims with a specific status"""
    return db.get_claims_by_status(status)

# ===================== RUN THE APPLICATION =====================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8002,  # Different port from Policy Service
        reload=True
    )