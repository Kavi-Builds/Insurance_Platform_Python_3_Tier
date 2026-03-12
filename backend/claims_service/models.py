# models.py
# This file defines what a "Claim" looks like in our system

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Claim(BaseModel):
    """
    This is our Claim model - defines all fields for an insurance claim
    """
    # Required fields
    claim_number: str              # Unique identifier like "CLM-2024-001"
    policy_number: str             # Associated policy number
    customer_name: str             # Name of the claimant
    customer_email: str             # Email for notifications
    claim_type: str                 # "auto", "home", "health", "life"
    incident_date: str              # When the incident happened
    filing_date: str                 # When claim was filed
    description: str                 # Description of what happened
    claim_amount: float              # Amount being claimed
    
    # Optional fields (will be added by the system)
    id: Optional[int] = None         # Database ID
    status: str = "submitted"        # submitted, under_review, approved, rejected, paid
    documents: List[str] = []        # List of document URLs/names
    adjuster_notes: Optional[str] = None
    approved_amount: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ClaimUpdate(BaseModel):
    """
    Model for updating an existing claim
    """
    status: Optional[str] = None
    description: Optional[str] = None
    claim_amount: Optional[float] = None
    documents: Optional[List[str]] = None
    adjuster_notes: Optional[str] = None
    approved_amount: Optional[float] = None