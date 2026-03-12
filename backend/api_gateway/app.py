# app.py - API Gateway
# This service acts as a single entry point for all frontend requests

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from functools import wraps

app = Flask(__name__, static_folder='../../frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Service URLs
POLICY_SERVICE = "http://localhost:8001"
CLAIMS_SERVICE = "http://localhost:8002"
BILLING_SERVICE = "http://localhost:8003"

# ===================== HELPER FUNCTIONS =====================

def handle_service_request(service_url, endpoint, method='GET', data=None):
    """Helper function to forward requests to microservices"""
    try:
        url = f"{service_url}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url, params=request.args)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            return jsonify({"error": "Method not supported"}), 405
        
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Service at {service_url} is unavailable"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===================== POLICY SERVICE ROUTES =====================

@app.route('/api/policies', methods=['GET', 'POST'])
def policies():
    """Route for policy operations"""
    if request.method == 'GET':
        return handle_service_request(POLICY_SERVICE, '/policies', 'GET')
    elif request.method == 'POST':
        return handle_service_request(POLICY_SERVICE, '/policies', 'POST', request.json)

@app.route('/api/policies/<int:policy_id>', methods=['GET', 'PUT', 'DELETE'])
def policy_detail(policy_id):
    """Route for individual policy operations"""
    if request.method == 'GET':
        return handle_service_request(POLICY_SERVICE, f'/policies/{policy_id}', 'GET')
    elif request.method == 'PUT':
        return handle_service_request(POLICY_SERVICE, f'/policies/{policy_id}', 'PUT', request.json)
    elif request.method == 'DELETE':
        return handle_service_request(POLICY_SERVICE, f'/policies/{policy_id}', 'DELETE')

@app.route('/api/policies/customer/<email>', methods=['GET'])
def customer_policies(email):
    """Get policies by customer email"""
    return handle_service_request(POLICY_SERVICE, f'/policies/customer/{email}', 'GET')

# ===================== CLAIMS SERVICE ROUTES =====================

@app.route('/api/claims', methods=['GET', 'POST'])
def claims():
    """Route for claim operations"""
    if request.method == 'GET':
        return handle_service_request(CLAIMS_SERVICE, '/claims', 'GET')
    elif request.method == 'POST':
        return handle_service_request(CLAIMS_SERVICE, '/claims', 'POST', request.json)

@app.route('/api/claims/<int:claim_id>', methods=['GET', 'PUT', 'DELETE'])
def claim_detail(claim_id):
    """Route for individual claim operations"""
    if request.method == 'GET':
        return handle_service_request(CLAIMS_SERVICE, f'/claims/{claim_id}', 'GET')
    elif request.method == 'PUT':
        return handle_service_request(CLAIMS_SERVICE, f'/claims/{claim_id}', 'PUT', request.json)
    elif request.method == 'DELETE':
        return handle_service_request(CLAIMS_SERVICE, f'/claims/{claim_id}', 'DELETE')

@app.route('/api/claims/policy/<policy_number>', methods=['GET'])
def policy_claims(policy_number):
    """Get claims by policy number"""
    return handle_service_request(CLAIMS_SERVICE, f'/claims/policy/{policy_number}', 'GET')

@app.route('/api/claims/customer/<email>', methods=['GET'])
def customer_claims(email):
    """Get claims by customer email"""
    return handle_service_request(CLAIMS_SERVICE, f'/claims/customer/{email}', 'GET')

@app.route('/api/claims/status/<status>', methods=['GET'])
def claims_by_status(status):
    """Get claims by status"""
    return handle_service_request(CLAIMS_SERVICE, f'/claims/status/{status}', 'GET')

# ===================== BILLING SERVICE ROUTES =====================

@app.route('/api/invoices', methods=['GET', 'POST'])
def invoices():
    """Route for invoice operations"""
    if request.method == 'GET':
        return handle_service_request(BILLING_SERVICE, '/invoices', 'GET')
    elif request.method == 'POST':
        return handle_service_request(BILLING_SERVICE, '/invoices', 'POST', request.json)

@app.route('/api/invoices/customer/<email>', methods=['GET'])
def customer_invoices(email):
    """Get invoices by customer email"""
    return handle_service_request(BILLING_SERVICE, f'/invoices/customer/{email}', 'GET')

@app.route('/api/payments', methods=['GET', 'POST'])
def payments():
    """Route for payment operations"""
    if request.method == 'GET':
        return handle_service_request(BILLING_SERVICE, '/payments', 'GET')
    elif request.method == 'POST':
        return handle_service_request(BILLING_SERVICE, '/payments', 'POST', request.json)

@app.route('/api/payments/customer/<email>', methods=['GET'])
def customer_payments(email):
    """Get payments by customer email"""
    return handle_service_request(BILLING_SERVICE, f'/payments/customer/{email}', 'GET')

@app.route('/api/payouts', methods=['GET', 'POST'])
def payouts():
    """Route for payout operations"""
    if request.method == 'GET':
        return handle_service_request(BILLING_SERVICE, '/payouts', 'GET')
    elif request.method == 'POST':
        return handle_service_request(BILLING_SERVICE, '/payouts', 'POST', request.json)

@app.route('/api/payment-methods', methods=['POST'])
def add_payment_method():
    """Add payment method"""
    return handle_service_request(BILLING_SERVICE, '/payment-methods', 'POST', request.json)

@app.route('/api/payment-methods/customer/<email>', methods=['GET'])
def customer_payment_methods(email):
    """Get customer payment methods"""
    return handle_service_request(BILLING_SERVICE, f'/payment-methods/customer/{email}', 'GET')

# ===================== FRONTEND ROUTES =====================

@app.route('/')
def serve_index():
    """Serve the main frontend page"""
    return send_from_directory('../../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files"""
    return send_from_directory('../../frontend', path)

# ===================== HEALTH CHECK =====================

@app.route('/health')
def health_check():
    """Check health of all services"""
    services = {
        'api_gateway': 'healthy',
        'policy_service': 'unknown',
        'claims_service': 'unknown',
        'billing_service': 'unknown'
    }
    
    # Check Policy Service
    try:
        requests.get(f"{POLICY_SERVICE}/", timeout=2)
        services['policy_service'] = 'healthy'
    except:
        services['policy_service'] = 'unhealthy'
    
    # Check Claims Service
    try:
        requests.get(f"{CLAIMS_SERVICE}/", timeout=2)
        services['claims_service'] = 'healthy'
    except:
        services['claims_service'] = 'unhealthy'
    
    # Check Billing Service
    try:
        requests.get(f"{BILLING_SERVICE}/", timeout=2)
        services['billing_service'] = 'healthy'
    except:
        services['billing_service'] = 'unhealthy'
    
    return jsonify(services)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)