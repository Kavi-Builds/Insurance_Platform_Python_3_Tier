# database.py
# Handles all billing data storage operations

from typing import List, Optional
from models import Invoice, Payment, ClaimPayout, PaymentMethod
from datetime import datetime, timedelta
import random

class BillingDatabase:
    """
    Manages billing data storage (in-memory for now)
    """
    
    def __init__(self):
        self.invoices = {}
        self.payments = {}
        self.payouts = {}
        self.payment_methods = {}
        
        self.invoice_counter = 1
        self.payment_counter = 1
        self.payout_counter = 1
        self.pm_counter = 1
        
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Add sample billing data for testing"""
        
        # Sample invoices
        sample_invoices = [
            {
                "invoice_number": "INV-2024-001",
                "policy_number": "POL-2024-001",
                "customer_name": "John Smith",
                "customer_email": "john.smith@email.com",
                "amount_due": 120.50,
                "due_date": "2024-04-01",
                "billing_period_start": "2024-03-01",
                "billing_period_end": "2024-03-31",
                "status": "paid",
                "paid_amount": 120.50,
                "paid_date": "2024-03-25",
                "payment_method": "credit_card"
            },
            {
                "invoice_number": "INV-2024-002",
                "policy_number": "POL-2024-001",
                "customer_name": "John Smith",
                "customer_email": "john.smith@email.com",
                "amount_due": 120.50,
                "due_date": "2024-05-01",
                "billing_period_start": "2024-04-01",
                "billing_period_end": "2024-04-30",
                "status": "pending"
            },
            {
                "invoice_number": "INV-2024-003",
                "policy_number": "POL-2024-002",
                "customer_name": "Sarah Johnson",
                "customer_email": "sarah.j@email.com",
                "amount_due": 85.75,
                "due_date": "2024-04-15",
                "billing_period_start": "2024-03-15",
                "billing_period_end": "2024-04-14",
                "status": "pending"
            }
        ]
        
        for inv_data in sample_invoices:
            invoice = Invoice(**inv_data)
            self.create_invoice(invoice)
        
        # Sample payments
        sample_payments = [
            {
                "payment_number": "PAY-2024-001",
                "invoice_number": "INV-2024-001",
                "policy_number": "POL-2024-001",
                "customer_name": "John Smith",
                "customer_email": "john.smith@email.com",
                "amount": 120.50,
                "payment_method": "credit_card",
                "payment_date": "2024-03-25",
                "status": "completed",
                "transaction_id": "txn_123456789"
            }
        ]
        
        for pay_data in sample_payments:
            payment = Payment(**pay_data)
            self.create_payment(payment)
        
        # Sample payment methods
        sample_pm = [
            {
                "customer_email": "john.smith@email.com",
                "payment_type": "credit_card",
                "last_four": "4242",
                "expiry_date": "12/25",
                "is_default": True
            },
            {
                "customer_email": "sarah.j@email.com",
                "payment_type": "bank_account",
                "last_four": "1234",
                "is_default": True
            }
        ]
        
        for pm_data in sample_pm:
            pm = PaymentMethod(**pm_data)
            self.create_payment_method(pm)
    
    # Invoice operations
    def create_invoice(self, invoice: Invoice) -> Invoice:
        invoice.id = self.invoice_counter
        invoice.created_at = datetime.now().isoformat()
        invoice.updated_at = datetime.now().isoformat()
        
        self.invoices[self.invoice_counter] = invoice
        self.invoice_counter += 1
        return invoice
    
    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        return self.invoices.get(invoice_id)
    
    def get_invoice_by_number(self, invoice_number: str) -> Optional[Invoice]:
        for invoice in self.invoices.values():
            if invoice.invoice_number == invoice_number:
                return invoice
        return None
    
    def get_all_invoices(self) -> List[Invoice]:
        return list(self.invoices.values())
    
    def get_invoices_by_policy(self, policy_number: str) -> List[Invoice]:
        return [i for i in self.invoices.values() if i.policy_number == policy_number]
    
    def get_invoices_by_customer(self, email: str) -> List[Invoice]:
        return [i for i in self.invoices.values() if i.customer_email == email]
    
    def update_invoice(self, invoice_id: int, invoice_update: dict) -> Optional[Invoice]:
        if invoice_id not in self.invoices:
            return None
        
        invoice = self.invoices[invoice_id]
        for key, value in invoice_update.items():
            if hasattr(invoice, key) and value is not None:
                setattr(invoice, key, value)
        
        invoice.updated_at = datetime.now().isoformat()
        return invoice
    
    # Payment operations
    def create_payment(self, payment: Payment) -> Payment:
        payment.id = self.payment_counter
        payment.created_at = datetime.now().isoformat()
        
        self.payments[self.payment_counter] = payment
        self.payment_counter += 1
        
        # If payment is for an invoice, update invoice status
        if payment.invoice_number:
            invoice = self.get_invoice_by_number(payment.invoice_number)
            if invoice:
                self.update_invoice(invoice.id, {
                    "status": "paid",
                    "paid_amount": payment.amount,
                    "paid_date": payment.payment_date,
                    "payment_method": payment.payment_method
                })
        
        return payment
    
    def get_payment(self, payment_id: int) -> Optional[Payment]:
        return self.payments.get(payment_id)
    
    def get_payments_by_invoice(self, invoice_number: str) -> List[Payment]:
        return [p for p in self.payments.values() if p.invoice_number == invoice_number]
    
    def get_payments_by_customer(self, email: str) -> List[Payment]:
        return [p for p in self.payments.values() if p.customer_email == email]
    
    # Payout operations
    def create_payout(self, payout: ClaimPayout) -> ClaimPayout:
        payout.id = self.payout_counter
        payout.created_at = datetime.now().isoformat()
        payout.updated_at = datetime.now().isoformat()
        
        self.payouts[self.payout_counter] = payout
        self.payout_counter += 1
        return payout
    
    def get_payout(self, payout_id: int) -> Optional[ClaimPayout]:
        return self.payouts.get(payout_id)
    
    def get_payouts_by_claim(self, claim_number: str) -> List[ClaimPayout]:
        return [p for p in self.payouts.values() if p.claim_number == claim_number]
    
    def update_payout(self, payout_id: int, payout_update: dict) -> Optional[ClaimPayout]:
        if payout_id not in self.payouts:
            return None
        
        payout = self.payouts[payout_id]
        for key, value in payout_update.items():
            if hasattr(payout, key) and value is not None:
                setattr(payout, key, value)
        
        payout.updated_at = datetime.now().isoformat()
        return payout
    
    # Payment method operations
    def create_payment_method(self, pm: PaymentMethod) -> PaymentMethod:
        pm.id = self.pm_counter
        pm.created_at = datetime.now().isoformat()
        
        # If this is default, unset default for others
        if pm.is_default:
            for existing_pm in self.payment_methods.values():
                if existing_pm.customer_email == pm.customer_email:
                    existing_pm.is_default = False
        
        self.payment_methods[self.pm_counter] = pm
        self.pm_counter += 1
        return pm
    
    def get_payment_methods_by_customer(self, email: str) -> List[PaymentMethod]:
        return [pm for pm in self.payment_methods.values() if pm.customer_email == email]
    
    def get_default_payment_method(self, email: str) -> Optional[PaymentMethod]:
        for pm in self.payment_methods.values():
            if pm.customer_email == email and pm.is_default:
                return pm
        return None
    
    def delete_payment_method(self, pm_id: int) -> bool:
        if pm_id in self.payment_methods:
            del self.payment_methods[pm_id]
            return True
        return False