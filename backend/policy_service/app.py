# app.py
# This is the main application file that creates our API endpoints
# It uses FastAPI to create REST endpoints

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import Policy, PolicyUpdate
from database import PolicyDatabase
import uvicorn

# Initialize our FastAPI application
app = FastAPI(
    title="Policy Administration Service",
    description="Microservice for managing insurance policies",
    version="1.0.0"
)

# Enable CORS so our frontend can talk to this API
# This is crucial for web applications running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our database
db = PolicyDatabase()

# ===================== API ENDPOINTS =====================

@app.get("/")
async def root():
    """Root endpoint - just to check if service is running"""
    return {
        "message": "Policy Administration Service is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /policies": "Get all policies",
            "GET /policies/{policy_id}": "Get specific policy",
            "POST /policies": "Create new policy",
            "PUT /policies/{policy_id}": "Update policy",
            "DELETE /policies/{policy_id}": "Delete policy",
            "GET /policies/customer/{email}": "Get customer policies"
        }
    }

@app.get("/policies", response_model=List[Policy])
async def get_all_policies():
    """
    Get all insurance policies
    Returns a list of all policies in the system
    """
    return db.get_all_policies()

@app.get("/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: int):
    """
    Get a specific policy by its ID
    """
    policy = db.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@app.post("/policies", response_model=Policy, status_code=201)
async def create_policy(policy: Policy):
    """
    Create a new insurance policy
    Expects a Policy object in the request body
    """
    # Check if policy number already exists (simple validation)
    existing_policies = db.get_all_policies()
    for p in existing_policies:
        if p.policy_number == policy.policy_number:
            raise HTTPException(status_code=400, detail="Policy number already exists")
    
    return db.create_policy(policy)

@app.put("/policies/{policy_id}", response_model=Policy)
async def update_policy(policy_id: int, policy_update: PolicyUpdate):
    """
    Update an existing policy
    Only the fields provided in the request will be updated
    """
    # Convert policy_update to dict, excluding None values
    update_data = {k: v for k, v in policy_update.dict().items() if v is not None}
    
    updated_policy = db.update_policy(policy_id, update_data)
    if not updated_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return updated_policy

@app.delete("/policies/{policy_id}")
async def delete_policy(policy_id: int):
    """
    Delete a policy
    """
    success = db.delete_policy(policy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return {"message": f"Policy {policy_id} deleted successfully"}

@app.get("/policies/customer/{email}", response_model=List[Policy])
async def get_customer_policies(email: str):
    """
    Get all policies for a specific customer by email
    """
    return db.get_policies_by_customer(email)

@app.get("/policies/type/{policy_type}", response_model=List[Policy])
async def get_policies_by_type(policy_type: str):
    """
    Get all policies of a specific type (auto, home, life, health)
    """
    all_policies = db.get_all_policies()
    return [p for p in all_policies if p.policy_type.lower() == policy_type.lower()]

# ===================== RUN THE APPLICATION =====================

if __name__ == "__main__":
    """
    This runs the server when we execute this file directly
    """
    uvicorn.run(
        "app:app",  # "app:app" means "from app import app"
        host="0.0.0.0",  # Listen on all network interfaces
        port=8001,  # Port 8001 for policy service
        reload=True  # Auto-restart when code changes (development only)
    )