// frontend/js/app.js

// API Base URL
const API_BASE = 'http://localhost:5000/api';

// Current user (in real app, this would come from authentication)
const CURRENT_USER = {
    name: 'John Smith',
    email: 'john.smith@email.com'
};

// ===================== INITIALIZATION =====================

document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadPolicies();
    loadClaims();
    loadInvoices();
    loadPayments();
    loadPaymentMethods();
    
    // Set up navigation
    setupNavigation();
    
    // Set up search
    setupSearch();
    
    // Set default dates in forms
    setDefaultDates();
});

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href');
            showSection(sectionId);
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function showSection(sectionId) {
    // Remove # from sectionId if present
    sectionId = sectionId.replace('#', '');
    
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Update URL hash
    window.location.hash = sectionId;
}

function setupSearch() {
    const searchInput = document.getElementById('policySearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            filterPolicies(e.target.value);
        });
    }
}

function setDefaultDates() {
    const today = new Date().toISOString().split('T')[0];
    const nextYear = new Date();
    nextYear.setFullYear(nextYear.getFullYear() + 1);
    const nextYearDate = nextYear.toISOString().split('T')[0];
    
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    const incidentDate = document.getElementById('incidentDate');
    
    if (startDate) startDate.value = today;
    if (endDate) endDate.value = nextYearDate;
    if (incidentDate) incidentDate.value = today;
}

// ===================== TOAST NOTIFICATIONS =====================

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.background = type === 'success' ? '#4CAF50' : '#f44336';
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===================== POLICY FUNCTIONS =====================

function loadPolicies() {
    fetch(`${API_BASE}/policies`)
        .then(response => response.json())
        .then(policies => {
            displayPolicies(policies);
            updatePolicyDropdown(policies);
            updateDashboard();
        })
        .catch(error => {
            console.error('Error loading policies:', error);
            showToast('Error loading policies', 'error');
        });
}

function displayPolicies(policies) {
    const container = document.getElementById('policiesList');
    
    if (policies.length === 0) {
        container.innerHTML = '<p class="no-data">No policies found. Purchase your first policy today!</p>';
        return;
    }
    
    container.innerHTML = policies.map(policy => `
        <div class="policy-card">
            <div class="policy-header">
                <span class="policy-type">${policy.policy_type.toUpperCase()}</span>
                <span class="policy-number">${policy.policy_number}</span>
            </div>
            <div class="policy-details">
                <p><i class="fas fa-user"></i> ${policy.customer_name}</p>
                <p><i class="fas fa-dollar-sign"></i> Coverage: $${policy.coverage_amount.toLocaleString()}</p>
                <p><i class="fas fa-coins"></i> Premium: $${policy.premium_amount}/month</p>
                <p><i class="fas fa-calendar"></i> ${policy.start_date} to ${policy.end_date}</p>
            </div>
            <div class="policy-status status-${policy.status}">${policy.status.replace('_', ' ')}</div>
        </div>
    `).join('');
}

function filterPolicies(searchTerm) {
    const cards = document.querySelectorAll('.policy-card');
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function updatePolicyDropdown(policies) {
    const dropdown = document.getElementById('claimPolicyNumber');
    if (!dropdown) return;
    
    dropdown.innerHTML = '<option value="">Select Policy</option>';
    policies.forEach(policy => {
        dropdown.innerHTML += `<option value="${policy.policy_number}">${policy.policy_number} - ${policy.policy_type}</option>`;
    });
}

function showAddPolicyForm() {
    document.getElementById('policyModal').style.display = 'block';
}

function createPolicy(event) {
    event.preventDefault();
    
    const policyData = {
        policy_number: `POL-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`,
        customer_name: CURRENT_USER.name,
        customer_email: CURRENT_USER.email,
        policy_type: document.getElementById('policyType').value,
        coverage_amount: parseFloat(document.getElementById('coverageAmount').value),
        premium_amount: calculatePremium(document.getElementById('policyType').value, 
                                        parseFloat(document.getElementById('coverageAmount').value)),
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value,
        status: 'active'
    };
    
    fetch(`${API_BASE}/policies`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(policyData)
    })
    .then(response => response.json())
    .then(data => {
        closeModal('policyModal');
        showToast('Policy purchased successfully!');
        loadPolicies();
        
        // Generate first invoice
        generateInvoice(data.policy_number, data.premium_amount);
    })
    .catch(error => {
        console.error('Error creating policy:', error);
        showToast('Error creating policy', 'error');
    });
}

function calculatePremium(type, coverage) {
    // Simple premium calculation (in real app, this would be complex)
    const rates = {
        'auto': 0.002,
        'home': 0.001,
        'life': 0.005,
        'health': 0.003
    };
    return Math.round(coverage * rates[type] * 100) / 100;
}

// ===================== CLAIM FUNCTIONS =====================

function loadClaims() {
    fetch(`${API_BASE}/claims/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(claims => {
            displayClaims(claims);
            updateDashboard();
        })
        .catch(error => {
            console.error('Error loading claims:', error);
            showToast('Error loading claims', 'error');
        });
}

function displayClaims(claims) {
    const container = document.getElementById('claimsList');
    
    if (claims.length === 0) {
        container.innerHTML = '<p class="no-data">No claims found.</p>';
        return;
    }
    
    container.innerHTML = claims.map(claim => `
        <div class="claim-card">
            <div class="claim-header">
                <span class="claim-type">${claim.claim_type.toUpperCase()}</span>
                <span class="claim-number">${claim.claim_number}</span>
            </div>
            <div class="claim-details">
                <p><i class="fas fa-file-contract"></i> Policy: ${claim.policy_number}</p>
                <p><i class="fas fa-calendar"></i> Incident: ${claim.incident_date}</p>
                <p><i class="fas fa-dollar-sign"></i> Claim Amount: $${claim.claim_amount.toLocaleString()}</p>
                ${claim.approved_amount ? `<p><i class="fas fa-check-circle"></i> Approved: $${claim.approved_amount.toLocaleString()}</p>` : ''}
                <p><i class="fas fa-align-left"></i> ${claim.description.substring(0, 50)}${claim.description.length > 50 ? '...' : ''}</p>
            </div>
            <div class="claim-status status-${claim.status}">${claim.status.replace('_', ' ')}</div>
        </div>
    `).join('');
}

function filterClaims(status) {
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter claims
    const claims = document.querySelectorAll('.claim-card');
    claims.forEach(claim => {
        if (status === 'all') {
            claim.style.display = 'block';
        } else {
            const claimStatus = claim.querySelector('.claim-status').textContent.trim().replace(' ', '_');
            if (claimStatus === status) {
                claim.style.display = 'block';
            } else {
                claim.style.display = 'none';
            }
        }
    });
}

function showFileClaimForm() {
    document.getElementById('claimModal').style.display = 'block';
}

function createClaim(event) {
    event.preventDefault();
    
    const claimData = {
        claim_number: `CLM-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`,
        policy_number: document.getElementById('claimPolicyNumber').value,
        customer_name: CURRENT_USER.name,
        customer_email: CURRENT_USER.email,
        claim_type: document.getElementById('claimType').value,
        incident_date: document.getElementById('incidentDate').value,
        filing_date: new Date().toISOString().split('T')[0],
        description: document.getElementById('claimDescription').value,
        claim_amount: parseFloat(document.getElementById('claimAmount').value),
        status: 'submitted',
        documents: []
    };
    
    fetch(`${API_BASE}/claims`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(claimData)
    })
    .then(response => response.json())
    .then(data => {
        closeModal('claimModal');
        showToast('Claim filed successfully!');
        loadClaims();
    })
    .catch(error => {
        console.error('Error filing claim:', error);
        showToast('Error filing claim', 'error');
    });
}

// ===================== BILLING FUNCTIONS =====================

function loadInvoices() {
    fetch(`${API_BASE}/invoices/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(invoices => {
            displayInvoices(invoices);
            updateDashboard();
        })
        .catch(error => {
            console.error('Error loading invoices:', error);
        });
}

function displayInvoices(invoices) {
    const container = document.getElementById('invoicesList');
    
    if (invoices.length === 0) {
        container.innerHTML = '<p class="no-data">No invoices found.</p>';
        return;
    }
    
    container.innerHTML = invoices.map(invoice => `
        <div class="invoice-item">
            <div class="invoice-info">
                <h4>Invoice #${invoice.invoice_number}</h4>
                <p>Policy: ${invoice.policy_number} | Due: ${invoice.due_date}</p>
            </div>
            <div class="invoice-amount">$${invoice.amount_due.toLocaleString()}</div>
            <div class="invoice-status status-${invoice.status}">${invoice.status}</div>
        </div>
    `).join('');
}

function filterInvoices(status) {
    // Update active button
    document.querySelectorAll('#billing .filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter invoices
    const invoices = document.querySelectorAll('.invoice-item');
    invoices.forEach(invoice => {
        if (status === 'all') {
            invoice.style.display = 'flex';
        } else {
            const invoiceStatus = invoice.querySelector('.invoice-status').textContent.trim();
            if (invoiceStatus === status) {
                invoice.style.display = 'flex';
            } else {
                invoice.style.display = 'none';
            }
        }
    });
}

function loadPayments() {
    fetch(`${API_BASE}/payments/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(payments => {
            displayPayments(payments);
        })
        .catch(error => {
            console.error('Error loading payments:', error);
        });
}

function displayPayments(payments) {
    const container = document.getElementById('paymentsList');
    
    if (payments.length === 0) {
        container.innerHTML = '<p class="no-data">No payment history found.</p>';
        return;
    }
    
    container.innerHTML = payments.slice(0, 5).map(payment => `
        <div class="invoice-item">
            <div class="invoice-info">
                <h4>Payment #${payment.payment_number}</h4>
                <p>${payment.payment_date} | ${payment.payment_method}</p>
            </div>
            <div class="invoice-amount">$${payment.amount.toLocaleString()}</div>
            <div class="invoice-status status-${payment.status}">${payment.status}</div>
        </div>
    `).join('');
}

function loadPaymentMethods() {
    fetch(`${API_BASE}/payment-methods/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(methods => {
            displayPaymentMethods(methods);
        })
        .catch(error => {
            console.error('Error loading payment methods:', error);
        });
}

function displayPaymentMethods(methods) {
    const container = document.getElementById('paymentMethodsList');
    
    if (methods.length === 0) {
        container.innerHTML = '<p class="no-data">No payment methods added.</p>';
        return;
    }
    
    container.innerHTML = methods.map(method => `
        <div class="payment-method-card ${method.is_default ? 'default' : ''}">
            <i class="fas ${method.payment_type === 'credit_card' ? 'fa-credit-card' : 'fa-university'}"></i>
            <div class="payment-method-info">
                <h4>${method.payment_type.replace('_', ' ')} <span class="default-badge">${method.is_default ? 'Default' : ''}</span></h4>
                <p>**** **** **** ${method.last_four} ${method.expiry_date ? '| Exp: ' + method.expiry_date : ''}</p>
            </div>
        </div>
    `).join('');
}

function showAddPaymentMethodForm() {
    document.getElementById('paymentMethodModal').style.display = 'block';
}

function addPaymentMethod(event) {
    event.preventDefault();
    
    const accountNumber = document.getElementById('accountNumber').value;
    const lastFour = accountNumber.slice(-4);
    
    const methodData = {
        customer_email: CURRENT_USER.email,
        payment_type: document.getElementById('paymentType').value,
        last_four: lastFour,
        expiry_date: document.getElementById('expiryDate').value,
        is_default: document.getElementById('isDefault').checked
    };
    
    fetch(`${API_BASE}/payment-methods`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(methodData)
    })
    .then(response => response.json())
    .then(data => {
        closeModal('paymentMethodModal');
        showToast('Payment method added successfully!');
        loadPaymentMethods();
    })
    .catch(error => {
        console.error('Error adding payment method:', error);
        showToast('Error adding payment method', 'error');
    });
}

function generateInvoice(policyNumber, amount) {
    const invoiceData = {
        invoice_number: `INV-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`,
        policy_number: policyNumber,
        customer_name: CURRENT_USER.name,
        customer_email: CURRENT_USER.email,
        amount_due: amount,
        due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        billing_period_start: new Date().toISOString().split('T')[0],
        billing_period_end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        status: 'pending'
    };
    
    fetch(`${API_BASE}/invoices`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(invoiceData)
    })
    .then(response => response.json())
    .then(() => {
        loadInvoices();
    })
    .catch(error => {
        console.error('Error generating invoice:', error);
    });
}

// ===================== DASHBOARD FUNCTIONS =====================

function updateDashboard() {
    updateCoverageSummary();
    updateClaimsStatus();
    updatePaymentHistory();
    updateUpcomingPremiums();
}

function updateCoverageSummary() {
    fetch(`${API_BASE}/policies`)
        .then(response => response.json())
        .then(policies => {
            const container = document.getElementById('coverageSummary');
            if (!container) return;
            
            const totalCoverage = policies.reduce((sum, p) => sum + p.coverage_amount, 0);
            const byType = {};
            policies.forEach(p => {
                byType[p.policy_type] = (byType[p.policy_type] || 0) + p.coverage_amount;
            });
            
            let html = '<div style="display: flex; flex-direction: column; gap: 10px;">';
            Object.entries(byType).forEach(([type, amount]) => {
                const percentage = (amount / totalCoverage * 100).toFixed(1);
                html += `
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>${type.toUpperCase()}</span>
                            <span>$${(amount/1000000).toFixed(1)}M (${percentage}%)</span>
                        </div>
                        <div style="height: 10px; background: #f0f2ff; border-radius: 5px; overflow: hidden;">
                            <div style="height: 100%; width: ${percentage}%; background: linear-gradient(90deg, #667eea, #764ba2);"></div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            
            container.innerHTML = html;
        });
}

function updateClaimsStatus() {
    fetch(`${API_BASE}/claims/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(claims => {
            const container = document.getElementById('claimsStatus');
            if (!container) return;
            
            const statusCount = {
                'submitted': 0,
                'under_review': 0,
                'approved': 0,
                'rejected': 0
            };
            
            claims.forEach(c => {
                if (statusCount.hasOwnProperty(c.status)) {
                    statusCount[c.status]++;
                }
            });
            
            const total = claims.length || 1;
            
            let html = '<div style="display: flex; flex-direction: column; gap: 10px;">';
            Object.entries(statusCount).forEach(([status, count]) => {
                const percentage = (count / total * 100).toFixed(1);
                html += `
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>${status.replace('_', ' ')}</span>
                            <span>${count} (${percentage}%)</span>
                        </div>
                        <div style="height: 10px; background: #f0f2ff; border-radius: 5px; overflow: hidden;">
                            <div style="height: 100%; width: ${percentage}%; background: ${getStatusColor(status)};"></div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            
            container.innerHTML = html;
        });
}

function getStatusColor(status) {
    const colors = {
        'submitted': '#ffc107',
        'under_review': '#17a2b8',
        'approved': '#28a745',
        'rejected': '#dc3545'
    };
    return colors[status] || '#667eea';
}

function updatePaymentHistory() {
    fetch(`${API_BASE}/payments/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(payments => {
            const container = document.getElementById('paymentHistory');
            if (!container) return;
            
            // Group by month
            const monthlyTotals = {};
            payments.forEach(p => {
                const month = p.payment_date.substring(0, 7);
                monthlyTotals[month] = (monthlyTotals[month] || 0) + p.amount;
            });
            
            const months = Object.keys(monthlyTotals).sort().slice(-6);
            const maxAmount = Math.max(...Object.values(monthlyTotals));
            
            let html = '<div style="display: flex; align-items: flex-end; gap: 10px; height: 150px;">';
            months.forEach(month => {
                const amount = monthlyTotals[month] || 0;
                const height = (amount / maxAmount * 100) || 0;
                html += `
                    <div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <div style="height: ${height}px; width: 100%; background: linear-gradient(to top, #667eea, #764ba2); border-radius: 5px 5px 0 0;"></div>
                        <div style="font-size: 12px;">${month.substring(5)}</div>
                        <div style="font-size: 12px; font-weight: bold;">$${amount}</div>
                    </div>
                `;
            });
            html += '</div>';
            
            container.innerHTML = html;
        });
}

function updateUpcomingPremiums() {
    fetch(`${API_BASE}/invoices/customer/${CURRENT_USER.email}`)
        .then(response => response.json())
        .then(invoices => {
            const container = document.getElementById('upcomingPremiums');
            if (!container) return;
            
            const upcoming = invoices
                .filter(i => i.status === 'pending')
                .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
                .slice(0, 3);
            
            if (upcoming.length === 0) {
                container.innerHTML = '<p>No upcoming premiums</p>';
                return;
            }
            
            let html = '<div style="display: flex; flex-direction: column; gap: 10px;">';
            upcoming.forEach(invoice => {
                const dueDate = new Date(invoice.due_date);
                const today = new Date();
                const daysLeft = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
                
                html += `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background: white; border-radius: 5px;">
                        <div>
                            <div style="font-weight: 500;">${invoice.policy_number}</div>
                            <div style="font-size: 12px; color: #666;">Due in ${daysLeft} days</div>
                        </div>
                        <div style="font-weight: 700; color: #667eea;">$${invoice.amount_due}</div>
                    </div>
                `;
            });
            html += '</div>';
            
            container.innerHTML = html;
        });
}

// ===================== MODAL FUNCTIONS =====================

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Handle hash navigation
window.addEventListener('load', function() {
    if (window.location.hash) {
        showSection(window.location.hash);
    }
});

// Export functions for HTML onclick handlers
window.showSection = showSection;
window.showAddPolicyForm = showAddPolicyForm;
window.createPolicy = createPolicy;
window.closeModal = closeModal;
window.showFileClaimForm = showFileClaimForm;
window.createClaim = createClaim;
window.filterClaims = filterClaims;
window.filterInvoices = filterInvoices;
window.showAddPaymentMethodForm = showAddPaymentMethodForm;
window.addPaymentMethod = addPaymentMethod;