# app.py
# Main application file for Billing & Payments Service

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Invoice, Payment, ClaimPayout, PaymentMethod
from database import BillingDatabase
import uvicorn
import requests
from datetime import datetime, timedelta

# Initialize FastAPI app
app = FastAPI(
    title="Billing & Payments Service",
    description="Microservice for managing premiums, payments, and claim payouts",
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
db = BillingDatabase()

# Other service URLs
POLICY_SERVICE_URL = "http://localhost:8001"
CLAIMS_SERVICE_URL = "http://localhost:8002"

# ===================== API ENDPOINTS =====================

@app.get("/")
async def root():
    """Check if service is running"""
    return {
        "message": "Billing & Payments Service is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /invoices": "Get all invoices",
            "POST /invoices": "Create invoice",
            "GET /invoices/customer/{email}": "Get customer invoices",
            "POST /payments": "Process payment",
            "GET /payments/customer/{email}": "Get customer payments",
            "POST /payouts": "Create claim payout",
            "GET /payouts/claim/{claim_number}": "Get payouts by claim",
            "POST /payment-methods": "Add payment method"
        }
    }

# ==================== INVOICE ENDPOINTS ====================

@app.get("/invoices", response_model=List[Invoice])
async def get_all_invoices():
    """Get all invoices"""
    return db.get_all_invoices()

@app.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int):
    """Get specific invoice by ID"""
    invoice = db.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@app.post("/invoices", response_model=Invoice, status_code=201)
async def create_invoice(invoice: Invoice):
    """Create a new invoice for premium payment"""
    
    # Verify policy exists
    try:
        response = requests.get(f"{POLICY_SERVICE_URL}/policies")
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Policy service unavailable")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Policy service is not reachable"
        )
    
    # Check if invoice number already exists
    existing = db.get_invoice_by_number(invoice.invoice_number)
    if existing:
        raise HTTPException(status_code=400, detail="Invoice number already exists")
    
    return db.create_invoice(invoice)

@app.get("/invoices/customer/{email}", response_model=List[Invoice])
async def get_customer_invoices(email: str):
    """Get all invoices for a specific customer"""
    return db.get_invoices_by_customer(email)

@app.get("/invoices/policy/{policy_number}", response_model=List[Invoice])
async def get_policy_invoices(policy_number: str):
    """Get all invoices for a specific policy"""
    return db.get_invoices_by_policy(policy_number)

# ==================== PAYMENT ENDPOINTS ====================

@app.post("/payments", response_model=Payment, status_code=201)
async def process_payment(payment: Payment):
    """Process a payment for an invoice"""
    
    # Verify invoice exists
    invoice = db.get_invoice_by_number(payment.invoice_number)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Check if amount matches
    if payment.amount != invoice.amount_due:
        raise HTTPException(status_code=400, detail="Payment amount does not match invoice amount")
    
    return db.create_payment(payment)

@app.get("/payments", response_model=List[Payment])
async def get_all_payments():
    """Get all payments"""
    return list(db.payments.values())

@app.get("/payments/customer/{email}", response_model=List[Payment])
async def get_customer_payments(email: str):
    """Get all payments for a customer"""
    return db.get_payments_by_customer(email)

@app.get("/payments/invoice/{invoice_number}", response_model=List[Payment])
async def get_invoice_payments(invoice_number: str):
    """Get all payments for an invoice"""
    return db.get_payments_by_invoice(invoice_number)

# ==================== PAYOUT ENDPOINTS ====================

@app.post("/payouts", response_model=ClaimPayout, status_code=201)
async def create_payout(payout: ClaimPayout):
    """Create a payout for an approved claim"""
    
    # Verify claim exists and is approved
    try:
        response = requests.get(f"{CLAIMS_SERVICE_URL}/claims")
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Claims service unavailable")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503, 
            detail="Claims service is not reachable"
        )
    
    return db.create_payout(payout)

@app.get("/payouts", response_model=List[ClaimPayout])
async def get_all_payouts():
    """Get all claim payouts"""
    return list(db.payouts.values())

@app.get("/payouts/claim/{claim_number}", response_model=List[ClaimPayout])
async def get_payouts_by_claim(claim_number: str):
    """Get all payouts for a specific claim"""
    return db.get_payouts_by_claim(claim_number)

@app.put("/payouts/{payout_id}/process")
async def process_payout(payout_id: int):
    """Mark a payout as processed"""
    payout = db.get_payout(payout_id)
    if not payout:
        raise HTTPException(status_code=404, detail="Payout not found")
    
    updated = db.update_payout(payout_id, {
        "status": "processed",
        "payout_date": datetime.now().strftime("%Y-%m-%d")
    })
    
    return {"message": f"Payout {payout.payout_number} processed successfully"}

# ==================== PAYMENT METHODS ENDPOINTS ====================

@app.post("/payment-methods", response_model=PaymentMethod, status_code=201)
async def add_payment_method(payment_method: PaymentMethod):
    """Add a new payment method for a customer"""
    return db.create_payment_method(payment_method)

@app.get("/payment-methods/customer/{email}", response_model=List[PaymentMethod])
async def get_customer_payment_methods(email: str):
    """Get all payment methods for a customer"""
    return db.get_payment_methods_by_customer(email)

@app.delete("/payment-methods/{pm_id}")
async def delete_payment_method(pm_id: int):
    """Delete a payment method"""
    success = db.delete_payment_method(pm_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    return {"message": "Payment method deleted successfully"}

# ==================== UTILITY ENDPOINTS ====================

@app.post("/generate-invoice/{policy_number}")
async def generate_monthly_invoice(policy_number: str):
    """
    Generate a new invoice for a policy (would be called by a scheduler)
    """
    # In real app, this would be called automatically each month
    # For demo, we'll create a sample invoice
    
    # Get policy details from policy service
    try:
        response = requests.get(f"{POLICY_SERVICE_URL}/policies")
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Policy service unavailable")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Policy service not reachable")
    
    # Create invoice number
    invoice_count = len(db.get_all_invoices()) + 1
    invoice_number = f"INV-2024-{str(invoice_count).zfill(3)}"
    
    # Calculate dates
    today = datetime.now()
    next_month = today.replace(day=1) + timedelta(days=32)
    due_date = next_month.replace(day=1).strftime("%Y-%m-%d")
    period_start = today.strftime("%Y-%m-%d")
    period_end = next_month.strftime("%Y-%m-%d")
    
    # For demo, using fixed premium amount
    new_invoice = Invoice(
        invoice_number=invoice_number,
        policy_number=policy_number,
        customer_name="Customer Name",  # Would come from policy service
        customer_email="customer@email.com",  # Would come from policy service
        amount_due=120.50,  # Would come from policy
        due_date=due_date,
        billing_period_start=period_start,
        billing_period_end=period_end,
        status="pending"
    )
    
    return db.create_invoice(new_invoice)

# ===================== RUN THE APPLICATION =====================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8003,  # Different port from other services
        reload=True
    )