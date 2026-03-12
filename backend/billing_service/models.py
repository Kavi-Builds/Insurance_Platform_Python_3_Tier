# models.py
# This file defines all billing and payment related models

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Invoice(BaseModel):
    """
    Model for premium invoices
    """
    invoice_number: str           # Unique invoice number
    policy_number: str            # Associated policy
    customer_name: str
    customer_email: str
    amount_due: float              # Amount to be paid
    due_date: str                  # Payment due date
    billing_period_start: str      # Start of billing period
    billing_period_end: str        # End of billing period
    
    # Optional fields
    id: Optional[int] = None
    status: str = "pending"        # pending, paid, overdue, cancelled
    paid_amount: Optional[float] = None
    paid_date: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class Payment(BaseModel):
    """
    Model for payment transactions
    """
    payment_number: str            # Unique payment identifier
    invoice_number: str            # Associated invoice
    policy_number: str
    customer_name: str
    customer_email: str
    amount: float                   # Payment amount
    payment_method: str             # credit_card, bank_transfer, cash, etc.
    payment_date: str               # When payment was made
    
    # Optional fields
    id: Optional[int] = None
    status: str = "completed"       # completed, pending, failed, refunded
    transaction_id: Optional[str] = None  # External payment gateway ID
    notes: Optional[str] = None
    created_at: Optional[str] = None

class ClaimPayout(BaseModel):
    """
    Model for claim payouts
    """
    payout_number: str             # Unique payout identifier
    claim_number: str              # Associated claim
    policy_number: str
    customer_name: str
    customer_email: str
    payout_amount: float            # Amount to pay out
    payout_date: str                # When payout is processed
    payout_method: str              # bank_transfer, check, etc.
    
    # Optional fields
    id: Optional[int] = None
    status: str = "pending"         # pending, processed, failed
    approved_by: Optional[str] = None
    transaction_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class PaymentMethod(BaseModel):
    """
    Model for storing customer payment methods
    """
    customer_email: str
    payment_type: str               # credit_card, bank_account
    last_four: str                  # Last 4 digits of card/account
    expiry_date: Optional[str] = None  # For credit cards
    is_default: bool = False
    
    # Optional fields
    id: Optional[int] = None
    token: Optional[str] = None      # Payment gateway token (never store real numbers!)
    created_at: Optional[str] = None