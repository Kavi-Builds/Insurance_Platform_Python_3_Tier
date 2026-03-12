# Shield Insurance Platform 🛡️

A modern, microservices-based insurance platform built with Python. This application demonstrates a real-world 3-tier architecture with separate services for policy administration, claims management, and billing.

## Architecture

The platform consists of three microservices and an API gateway:
┌─────────────────────────────────────┐
│ Frontend (Port 5000)                │
│ HTML/CSS/JavaScript                 │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ API Gateway (Port 5000)             │
│ Flask                               │
└───────┬───────────────┬─────────────┘
        │      │        │
        ▼      ▼        ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Policy      │ │ Claims      │ │ Billing     │
│ Service     │ │ Service     │ │ Service     │
│ (8001)      │ │ (8002)      │ │ (8003)      │
└─────────────┘ └─────────────┘ └─────────────┘


## Features

- **Policy Administration**: Create and manage insurance policies
- **Claims Management**: File and track insurance claims
- **Billing & Payments**: Handle premiums, payments, and payouts
- **Interactive Dashboard**: Visual overview of your insurance data
- **Modern UI**: Responsive design with real-time updates

## Technology Stack

- **Backend**: Python, FastAPI, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: RESTful microservices
- **Documentation**: Swagger/OpenAPI

## Prerequisites

- Python 3.8 or higher
- Git
- VS Code (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kavi-Builds/Insurance_Platform_Python_3_Tier.git
   cd insurance-platform