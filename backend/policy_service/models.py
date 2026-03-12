# models.py
# This file defines what a "Policy" looks like in our system
# Think of it as a blueprint for insurance policy data

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Policy(BaseModel):
    """
    This is our Policy model - it defines all the fields that an insurance policy has.
    Each field has a type (str = string/text, float = decimal number, etc.)
    """
    # Required fields (must be provided when creating a policy)
    policy_number: str           # Unique identifier like "POL-2024-001"
    customer_name: str            # Name of the policyholder
    customer_email: str           # Email for notifications
    policy_type: str              # "auto", "home", "life", "health"
    coverage_amount: float        # How much coverage in dollars
    premium_amount: float         # Monthly premium in dollars
    start_date: str               # When policy starts (YYYY-MM-DD)
    end_date: str                 # When policy ends (YYYY-MM-DD)
    
    # Optional fields (can be None if not provided)
    id: Optional[int] = None      # Database ID (auto-generated)
    status: str = "active"        # active, cancelled, expired
    created_at: Optional[str] = None  # Timestamp when created
    
class PolicyUpdate(BaseModel):
    """
    This model is for UPDATING an existing policy
    All fields are optional since you might only update one field
    """
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    coverage_amount: Optional[float] = None
    premium_amount: Optional[float] = None
    status: Optional[str] = None