# database.py
# Handles all claim data storage operations

from typing import List, Optional
from models import Claim
from datetime import datetime
import random

class ClaimDatabase:
    """
    Manages claim data storage (in-memory for now)
    """
    
    def __init__(self):
        self.claims = {}
        self.counter = 1
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Add sample claims for testing"""
        sample_claims = [
            {
                "claim_number": "CLM-2024-001",
                "policy_number": "POL-2024-001",
                "customer_name": "John Smith",
                "customer_email": "john.smith@email.com",
                "claim_type": "auto",
                "incident_date": "2024-03-15",
                "filing_date": "2024-03-16",
                "description": "Rear-ended at traffic light. Minor damage to bumper.",
                "claim_amount": 2500.00,
                "status": "under_review",
                "documents": ["accident_photo1.jpg", "police_report.pdf"]
            },
            {
                "claim_number": "CLM-2024-002",
                "policy_number": "POL-2024-002",
                "customer_name": "Sarah Johnson",
                "customer_email": "sarah.j@email.com",
                "claim_type": "home",
                "incident_date": "2024-03-10",
                "filing_date": "2024-03-11",
                "description": "Basement flooding due to heavy rain. Water damage to flooring and furniture.",
                "claim_amount": 12500.00,
                "status": "approved",
                "documents": ["damage_photos.zip", "plumber_report.pdf"],
                "approved_amount": 11500.00,
                "adjuster_notes": "Water damage confirmed. Deductible applied."
            }
        ]
        
        for claim_data in sample_claims:
            claim = Claim(**claim_data)
            self.create_claim(claim)
    
    def create_claim(self, claim: Claim) -> Claim:
        """
        Save a new claim
        """
        claim.id = self.counter
        now = datetime.now().isoformat()
        claim.created_at = now
        claim.updated_at = now
        
        self.claims[self.counter] = claim
        self.counter += 1
        return claim
    
    def get_claim(self, claim_id: int) -> Optional[Claim]:
        """Get claim by ID"""
        return self.claims.get(claim_id)
    
    def get_all_claims(self) -> List[Claim]:
        """Get all claims"""
        return list(self.claims.values())
    
    def get_claims_by_policy(self, policy_number: str) -> List[Claim]:
        """Get all claims for a specific policy"""
        return [c for c in self.claims.values() if c.policy_number == policy_number]
    
    def get_claims_by_customer(self, email: str) -> List[Claim]:
        """Get all claims for a specific customer"""
        return [c for c in self.claims.values() if c.customer_email == email]
    
    def update_claim(self, claim_id: int, claim_update: dict) -> Optional[Claim]:
        """Update an existing claim"""
        if claim_id not in self.claims:
            return None
        
        claim = self.claims[claim_id]
        for key, value in claim_update.items():
            if hasattr(claim, key) and value is not None:
                setattr(claim, key, value)
        
        claim.updated_at = datetime.now().isoformat()
        return claim
    
    def delete_claim(self, claim_id: int) -> bool:
        """Delete a claim"""
        if claim_id in self.claims:
            del self.claims[claim_id]
            return True
        return False
    
    def get_claims_by_status(self, status: str) -> List[Claim]:
        """Get all claims with a specific status"""
        return [c for c in self.claims.values() if c.status.lower() == status.lower()]