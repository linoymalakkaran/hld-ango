# JUL System Quick Start Guide
## Janela Única Logística - Angola National Logistics Single Window

**Version:** 2.0  
**Date:** December 2025  
**Purpose:** Quick onboarding guide for developers, administrators, and business users

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [First Time Setup](#first-time-setup)
5. [User Access](#user-access)
6. [Common Operations](#common-operations)
7. [Troubleshooting](#troubleshooting)
8. [Support Contacts](#support-contacts)

---

## System Overview

The JUL (Janela Única Logística) system is Angola's National Logistics Single Window for customs and trade facilitation. The system provides:

- **Single Point Submission** for trade documents
- **Integrated Processing** with ASYCUDA, SINTECE, and OGAs
- **Real-time Tracking** of shipments and declarations
- **Digital Document Management** with secure storage
- **Comprehensive Reporting** for compliance and operations

### Key System Components
- **Frontend**: Angular 17+ web portal with PWA capabilities
- **Backend**: 11 microservices built on ASP.NET Core 8.0
- **Authentication**: Keycloak 23+ with MFA support
- **Database**: PostgreSQL 15+ with database-per-service pattern
- **Storage**: MinIO for documents, Redis for caching
- **Deployment**: Kubernetes on-premises with Docker containers

---

## Prerequisites

### For Developers
- **Development Tools**:
  - Visual Studio 2022 or VS Code
  - .NET 8.0 SDK
  - Node.js 18+ with npm
  - Angular CLI 17+
  - Docker Desktop
  - kubectl (Kubernetes CLI)

### For System Administrators
- **Infrastructure Requirements**:
  - Kubernetes cluster (v1.28+)
  - PostgreSQL 15+ cluster
  - MinIO storage cluster
  - Redis 7+ cluster
  - NGINX Ingress Controller

### For Business Users
- **Browser Requirements**:
  - Chrome 120+, Firefox 120+, Safari 17+, or Edge 120+
  - JavaScript enabled
  - Cookies enabled for authentication
  - PDF viewer for document downloads

---

## Environment Setup

### Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd jul-system

# Start local development environment
docker-compose -f docker-compose.dev.yml up -d

# Install frontend dependencies
cd frontend
npm install
ng serve

# Start backend services
cd ../backend
dotnet restore
dotnet run --project Gateway.API
```

### Staging Environment Access
```bash
# Configure kubectl context for staging
kubectl config use-context jul-staging

# Verify cluster access
kubectl get pods -n jul-staging

# Access staging web portal
https://staging.jul.gov.ao
```

### Production Environment
```bash
# Production access requires VPN and authorized certificates
# Contact system administrators for access credentials

# Production web portal
https://jul.gov.ao
```

---

## First Time Setup

### 1. Administrator Setup
```bash
# Create initial admin user in Keycloak
# Access Keycloak admin console
https://keycloak.jul.gov.ao/auth/admin

# Default admin credentials (change immediately):
# Username: admin
# Password: admin123

# Create first system administrator account
```

### 2. Database Initialization
```sql
-- Run database migration scripts
psql -h postgresql.jul.gov.ao -d company_db -f migrations/001_initial_schema.sql
psql -h postgresql.jul.gov.ao -d masterdata_db -f migrations/002_master_data.sql

-- Verify table creation
\dt
```

### 3. Master Data Loading
```bash
# Initialize master data synchronization
kubectl exec -it masterdata-service-pod -- /app/sync-master-data.sh

# Verify data loading
curl https://api.jul.gov.ao/masterdata/hs-codes | jq
```

### 4. External System Configuration
```bash
# Configure ASYCUDA integration
kubectl create secret generic asycuda-certs \
  --from-file=client.crt \
  --from-file=client.key \
  -n jul-production

# Configure SINTECE API keys
kubectl create secret generic sintece-api \
  --from-literal=api-key=<your-api-key> \
  -n jul-production
```

---

## User Access

### User Registration Process
1. **Company Registration**:
   - Visit https://jul.gov.ao
   - Click "Register Company"
   - Complete company information form
   - Upload required documents (business license, tax certificate)
   - Submit for verification

2. **User Account Creation**:
   - Company admin receives invitation email
   - Click activation link
   - Set password and configure MFA
   - Complete profile information

3. **Role Assignment**:
   - Company admin can invite additional users
   - Assign appropriate roles (Trader, Customs Broker, etc.)
   - Users receive activation emails

### User Roles and Permissions
| Role | Permissions | Use Case |
|------|-------------|----------|
| **System Administrator** | Full system access | Technical administration |
| **Customs Officer** | Declaration review, clearance | Government operations |
| **Customs Supervisor** | Officer oversight, exceptions | Government management |
| **Trader/Importer** | Submit declarations, track status | Business operations |
| **Customs Broker** | Represent clients, process declarations | Agent services |
| **Freight Forwarder** | Logistics management, tracking | Logistics operations |

---

## Common Operations

### 1. Submit Customs Declaration (DU)
```
Navigation: Dashboard → Declarations → New Declaration
Steps:
1. Select declaration type (Import/Export/Transit)
2. Enter goods information with HS codes
3. Upload supporting documents (invoice, packing list)
4. Review and validate declaration
5. Submit for processing
6. Track status in real-time
```

### 2. Apply for CNCA License
```
Navigation: Dashboard → Licenses → Apply for CNCA
Steps:
1. Complete application form
2. Upload financial statements and qualifications
3. Pay application fee
4. Submit for government review
5. Monitor approval status
6. Download certificate upon approval
```

### 3. Nominate Customs Agent
```
Navigation: Dashboard → Agents → Nominate Agent
Steps:
1. Search for qualified customs brokers
2. Select broker and define scope
3. Upload power of attorney document
4. Send nomination request
5. Await broker acceptance
6. Authorize agent for declarations
```

### 4. Track Shipment Status
```
Navigation: Dashboard → Tracking → Search
Steps:
1. Enter container number or declaration reference
2. View real-time status and location
3. Check processing milestones
4. Download clearance documents
5. Get delivery notifications
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Login Problems
**Issue**: Cannot login to system
**Solutions**:
- Verify username/password combination
- Check if MFA device is synchronized
- Clear browser cache and cookies
- Contact company administrator for account reset

#### 2. Declaration Submission Errors
**Issue**: Validation errors when submitting declaration
**Solutions**:
- Verify all required fields are completed
- Check HS code format (6-10 digits)
- Ensure document file sizes are under 10MB
- Validate currency codes (ISO 4217 format)

#### 3. Document Upload Issues
**Issue**: Cannot upload documents
**Solutions**:
- Check file format (PDF, JPG, PNG supported)
- Ensure file size is under 10MB
- Verify internet connection stability
- Try different browser if issue persists

#### 4. ASYCUDA Integration Errors
**Issue**: Declaration not processed by customs
**Solutions**:
- Check ASYCUDA system status
- Verify declaration contains all required WCO fields
- Contact customs office if delays exceed 24 hours
- Review error messages in system notifications

#### 5. Payment Processing Issues
**Issue**: Duty payment fails
**Solutions**:
- Verify bank account has sufficient funds
- Check payment method is supported
- Ensure payment details are accurate
- Contact bank for transaction authorization

### System Status Monitoring
- **System Health**: https://status.jul.gov.ao
- **Performance Metrics**: Real-time dashboard available to administrators
- **Maintenance Windows**: Announced 48 hours in advance via email

---

## Support Contacts

### Technical Support
- **Email**: support@jul.gov.ao
- **Phone**: +244 222 123 456
- **Hours**: Monday-Friday, 08:00-17:00 WAT
- **Emergency**: +244 923 456 789 (24/7 for critical issues)

### Business Support
- **Customs Inquiries**: customs@jul.gov.ao
- **License Support**: licenses@jul.gov.ao
- **Integration Support**: integration@jul.gov.ao
- **Training Requests**: training@jul.gov.ao

### Government Agencies
- **AGT (Customs Authority)**: contact@agt.gov.ao
- **SINTECE**: support@sintece.gov.ao
- **Ministry of Commerce**: info@mincommerce.gov.ao

### Documentation and Training
- **User Manual**: https://docs.jul.gov.ao/user-manual
- **API Documentation**: https://api.jul.gov.ao/docs
- **Video Tutorials**: https://training.jul.gov.ao
- **FAQ**: https://help.jul.gov.ao

### System Information
- **Current Version**: 2.0
- **Last Updated**: December 2025
- **Next Release**: March 2026
- **Maintenance Schedule**: Sunday 02:00-06:00 WAT (monthly)

---

## Quick Reference

### Important URLs
- **Production Portal**: https://jul.gov.ao
- **Staging Portal**: https://staging.jul.gov.ao
- **API Documentation**: https://api.jul.gov.ao/docs
- **System Status**: https://status.jul.gov.ao
- **Help Center**: https://help.jul.gov.ao

### Emergency Procedures
1. **System Outage**: Check status page, contact support if not planned
2. **Security Incident**: Immediately change passwords, report to security@jul.gov.ao
3. **Data Loss**: Contact support immediately, do not attempt recovery
4. **Integration Failure**: Check external system status, contact integration team

### Performance Targets
- **System Availability**: 99.9% (8.76 hours downtime/year max)
- **Response Time**: < 3 seconds (95th percentile)
- **Declaration Processing**: 4-6 hours typical
- **Document Upload**: < 30 seconds for files under 5MB

---

**Document Control**  
**Version**: 2.0  
**Last Review**: December 2025  
**Next Review**: March 2026  
**Owner**: JUL System Team