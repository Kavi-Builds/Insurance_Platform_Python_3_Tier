# database.py
# This simulates a database. In real world, this would connect to PostgreSQL or MongoDB
# But for now, we'll store data in memory (RAM) for simplicity

from typing import List, Optional
from models import Policy
import json
from datetime import datetime
import os

class PolicyDatabase:
    """
    This class handles all data storage operations.
    Currently using in-memory storage (dictionary) for simplicity.
    """
    
    def __init__(self):
        # This dictionary will store our policies
        # Key: policy_id (integer), Value: Policy object
        self.policies = {}
        self.counter = 1  # To generate new IDs
        
        # Add some sample data so we have something to work with
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Add some sample policies for testing"""
        sample_policies = [
            {
                "policy_number": "POL-2024-001",
                "customer_name": "John Smith",
                "customer_email": "john.smith@email.com",
                "policy_type": "auto",
                "coverage_amount": 50000.00,
                "premium_amount": 120.50,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "status": "active"
            },
            {
                "policy_number": "POL-2024-002",
                "customer_name": "Sarah Johnson",
                "customer_email": "sarah.j@email.com",
                "policy_type": "home",
                "coverage_amount": 350000.00,
                "premium_amount": 85.75,
                "start_date": "2024-02-15",
                "end_date": "2025-02-14",
                "status": "active"
            }
        ]
        
        for policy_data in sample_policies:
            policy = Policy(**policy_data)
            self.create_policy(policy)
    
    def create_policy(self, policy: Policy) -> Policy:
        """
        Save a new policy to our "database"
        """
        # Add ID and timestamp to the policy
        policy.id = self.counter
        policy.created_at = datetime.now().isoformat()
        
        # Store in our dictionary
        self.policies[self.counter] = policy
        
        # Increment counter for next policy
        self.counter += 1
        
        return policy
    
    def get_policy(self, policy_id: int) -> Optional[Policy]:
        """
        Retrieve a policy by its ID
        """
        return self.policies.get(policy_id)
    
    def get_all_policies(self) -> List[Policy]:
        """
        Get all policies
        """
        return list(self.policies.values())
    
    def update_policy(self, policy_id: int, policy_update: dict) -> Optional[Policy]:
        """
        Update an existing policy
        """
        if policy_id not in self.policies:
            return None
        
        # Get existing policy
        existing_policy = self.policies[policy_id]
        
        # Update only the fields that were provided
        for key, value in policy_update.items():
            if hasattr(existing_policy, key) and value is not None:
                setattr(existing_policy, key, value)
        
        return existing_policy
    
    def delete_policy(self, policy_id: int) -> bool:
        """
        Delete a policy
        """
        if policy_id in self.policies:
            del self.policies[policy_id]
            return True
        return False
    
    def get_policies_by_customer(self, email: str) -> List[Policy]:
        """
        Find all policies for a specific customer
        """
        return [p for p in self.policies.values() if p.customer_email == email]