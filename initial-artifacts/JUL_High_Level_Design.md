# HIGH LEVEL DESIGN DOCUMENT
## JUL (Janela Única Logística) - Single Window System

**Document Version:** 1.0  
**Date:** December 2024  
**Status:** Draft

---

## DOCUMENT CONTROL

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | December 2024 | System Architect | Initial Draft |

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Introduction](#2-introduction)
3. [System Overview](#3-system-overview)
4. [Infrastructure Architecture](#4-infrastructure-architecture)
5. [Application Architecture](#5-application-architecture)
6. [Data Conversion and Migration](#6-data-conversion-and-migration)
7. [Reporting and Information](#7-reporting-and-information)
8. [Deployment Architecture](#8-deployment-architecture)
9. [Infrastructure Architecture Details](#9-infrastructure-architecture-details)
10. [Standards and Compliance](#10-standards-and-compliance)

---

## 1. EXECUTIVE SUMMARY

### 1.1 Purpose

The JUL (Janela Única Logística) High Level Design document provides a comprehensive architectural blueprint for Angola's Single Window System. This document outlines the technical architecture, design decisions, and implementation approach for a modern, scalable trade facilitation platform that integrates multiple government agencies and private sector stakeholders.

### 1.2 Scope

This HLD covers Phase 1 implementation of the JUL system, including:

- Company Registration & Onboarding
- License & Permits Management
- Agent Nomination
- Track & Trace functionality
- Billing, Payments & Invoicing
- Master Data Management (HS-CODE, IMDG)
- Dashboards & Reports
- Rail Portal (Schedules, Tariffs, Payments)
- Alerts System (Ministry Quotas, Tariff Changes)
- Identity & Access Management
- Monitoring & Support

### 1.3 Document Organization

This document follows the standard HLD template structure and is organized into nine major sections covering infrastructure, application architecture, deployment, data management, security, and compliance with international standards including WCO Data Model Version 3.10.

---

## 2. INTRODUCTION

### 2.1 Background

The Government of Angola is implementing a Single Window System (JUL) to streamline trade processes, reduce clearance times, and enhance transparency in logistics operations. The system will integrate with multiple stakeholders including customs (ASYCUDA), port operations (JUP), terminal operations (TOS), and various Other Government Agencies (OGAs).

### 2.2 Business Context

The JUL system serves as a central platform where traders, shipping agents, freight forwarders, customs brokers, and truckers can:

- Submit trade-related documents once
- Track shipments and cargo
- Obtain licenses and permits
- Make payments and receive invoices
- Access real-time information and alerts

### 2.3 System Objectives

**Primary Objectives:**

1. Reduce trade transaction processing time by 50%
2. Eliminate redundant data entry through single submission
3. Provide real-time visibility of cargo and document status
4. Enable seamless integration between government agencies and private sector
5. Ensure compliance with WCO standards and international best practices
6. Support multi-language operations (Portuguese, English, French)

**Technical Objectives:**

1. Implement microservices-based architecture for scalability
2. Deploy on Kubernetes for container orchestration
3. Ensure 99.9% system availability
4. Support concurrent users up to 10,000
5. Process transactions with response time < 3 seconds
6. Implement comprehensive security and audit mechanisms

### 2.4 Stakeholders

**Primary Stakeholders:**

- **Government Entities:**
  - Ministry of Transport (MINTRANS)
  - Ministry of Commerce (MINDCOM)
  - Customs Authority (AGT via ASYCUDA)
  - ARCCLA (Regulatory Authority)
  - ANTT (National Transport Agency)
  - Port Authority

- **Private Sector:**
  - Import/Export Companies
  - Shipping Lines and Agents
  - Freight Forwarders
  - Customs Brokers
  - Terminal Operators
  - Trucking Companies
  - Banking Institutions

**System Users:**

- Traders (Importers/Exporters)
- Shipping Agents
- Freight Forwarders
- Customs Brokers
- Government Officials
- Port Operators
- System Administrators

### 2.5 Assumptions and Constraints

**Assumptions:**

1. External systems (ASYCUDA, JUP, TOS) provide stable API endpoints
2. Network connectivity is available between all integration points
3. Users have access to modern web browsers
4. Digital certificates infrastructure is available
5. Master data (HS Codes, Port Codes) is maintained and current

**Constraints:**

1. Must integrate with existing ASYCUDA system for customs clearance
2. Must comply with WCO Data Model 3.10
3. Must support both online and offline document upload capabilities
4. Must maintain backward compatibility during migration period
5. Budget limitations for infrastructure procurement
6. Implementation timeline of 18 months for Phase 1

---

## 3. SYSTEM OVERVIEW

### 3.1 System Context

**Diagram Reference:** See [01_System_Context_Diagram.mermaid](#diagrams)

The JUL Single Window System operates as a central integration hub connecting various stakeholders in the logistics and trade ecosystem. The system interfaces with:

- **External Government Systems:** ASYCUDA (Customs), SINTECE (Single Window), PICE (Import/Export Control), SIGT (Transport Management), SICOEX (Export Control)
- **Port Systems:** JUP (Port Management), TOS (Terminal Operating System), CPE (Port Community System)
- **Other Agencies:** ANTT (Transport Agency), DTSER (various services), Banks (Payment Gateway)
- **User Communities:** Traders, Agents, Brokers, Transporters

### 3.2 High-Level Architecture

**Diagram Reference:** See [02_High_Level_Architecture.mermaid](#diagrams)

The JUL system implements a modern, cloud-native architecture based on:

**Layered Architecture:**

1. **Presentation Layer**
   - Web Portal (Angular-based SPA)
   - Mobile Applications (iOS/Android)
   - API Console for developers

2. **Application Layer**
   - API Gateway (Kong/NGINX)
   - Microservices (Spring Boot/Node.js)
   - Business Process Management (Camunda)
   - Integration Services (Apache Camel/MuleSoft)

3. **Data Layer**
   - Primary Database (PostgreSQL Cluster)
   - Document Store (MongoDB)
   - Cache Layer (Redis)
   - Message Queue (RabbitMQ/Kafka)

4. **Integration Layer**
   - ESB/Message Broker
   - API Management
   - Protocol Adapters (REST, SOAP, EDI, XML)

5. **Security Layer**
   - Identity & Access Management (Keycloak)
   - API Security Gateway
   - Certificate Management
   - Encryption Services

### 3.3 Key Architectural Decisions

**Decision 1: Microservices Architecture**
- **Rationale:** Enables independent scaling, deployment, and technology choices per service
- **Impact:** Increases operational complexity but provides better agility and resilience

**Decision 2: Kubernetes Deployment**
- **Rationale:** Industry-standard container orchestration with auto-scaling and self-healing
- **Impact:** Requires DevOps expertise but ensures high availability

**Decision 3: API-First Design**
- **Rationale:** Enables integration flexibility and supports multiple client types
- **Impact:** All functionality exposed via RESTful APIs

**Decision 4: Event-Driven Architecture**
- **Rationale:** Supports asynchronous processing and loose coupling between services
- **Impact:** Improves system responsiveness and scalability

**Decision 5: Multi-Tenancy Support**
- **Rationale:** Enables SaaS model for future expansion to other countries
- **Impact:** Requires careful data isolation and security design

### 3.4 Technology Stack

**Frontend Technologies:**
- Angular 14+ for web application
- React Native for mobile apps
- HTML5, CSS3, TypeScript
- Material UI component library

**Backend Technologies:**
- Java 17 with Spring Boot 3.x
- Node.js 18+ for specific services
- Python 3.10+ for data processing
- Camunda 8 for workflow orchestration

**Databases:**
- PostgreSQL 14+ (Primary relational database)
- MongoDB 6+ (Document store)
- Redis 7+ (Cache and session store)

**Integration:**
- Apache Camel 3.x for integration patterns
- Kong API Gateway for API management
- RabbitMQ/Apache Kafka for messaging
- Apache ActiveMQ for legacy integrations

**Infrastructure:**
- Kubernetes 1.27+ (On-premise K8s cluster)
- Docker for containerization
- Helm for package management
- Prometheus + Grafana for monitoring

**Security:**
- Keycloak 22+ for SSO and IAM
- OAuth 2.0 / OpenID Connect
- HashiCorp Vault for secrets management
- ModSecurity WAF

**DevOps:**
- GitLab CI/CD for pipelines
- Terraform for infrastructure as code
- Ansible for configuration management
- ELK Stack for logging (Elasticsearch, Logstash, Kibana)

---

## 4. INFRASTRUCTURE ARCHITECTURE

### 4.1 Deployment Model

**Diagram Reference:** See [03_Deployment_Architecture.mermaid](#diagrams)

The JUL system is deployed on an on-premise Kubernetes cluster with the following characteristics:

**Environment Strategy:**

1. **Development Environment**
   - 3 worker nodes (8 CPU, 32GB RAM each)
   - Single database instance
   - Reduced replica counts
   - Purpose: Feature development and unit testing

2. **Testing/UAT Environment**
   - 5 worker nodes (16 CPU, 64GB RAM each)
   - Database cluster with replica
   - Production-like configuration
   - Purpose: Integration testing and user acceptance

3. **Staging Environment**
   - 5 worker nodes (identical to production)
   - Full database cluster
   - Identical to production configuration
   - Purpose: Pre-production validation and performance testing

4. **Production Environment**
   - 10+ worker nodes (32 CPU, 128GB RAM each)
   - High-availability database cluster (3+ nodes)
   - Full redundancy and load balancing
   - Geographic distribution considerations

### 4.2 Kubernetes Architecture

**Diagram Reference:** See [04_Kubernetes_Architecture.mermaid](#diagrams)

**Cluster Components:**

1. **Control Plane (3 nodes for HA)**
   - API Server
   - Scheduler
   - Controller Manager
   - etcd cluster

2. **Worker Nodes (10+ nodes)**
   - Container Runtime (containerd)
   - Kubelet
   - Kube-proxy
   - Node-level monitoring agents

3. **Add-ons:**
   - Ingress Controller (NGINX)
   - DNS (CoreDNS)
   - Dashboard
   - Metrics Server
   - Cluster Autoscaler

**Namespace Strategy:**

- `jul-production` - Production services
- `jul-staging` - Staging environment
- `jul-integration` - Integration services
- `jul-monitoring` - Monitoring stack
- `jul-security` - Security services
- `jul-data` - Data layer services

### 4.3 Network Architecture

**Diagram Reference:** See [05_Network_Architecture.mermaid](#diagrams)

**Network Zones:**

1. **DMZ (Demilitarized Zone)**
   - External Load Balancer
   - Web Application Firewall (WAF)
   - SSL/TLS Termination
   - DDoS Protection

2. **Application Zone**
   - API Gateway
   - Application Services
   - BPM Engine
   - Integration Services

3. **Data Zone**
   - Database Clusters
   - Cache Servers
   - Message Brokers
   - File Storage

4. **Management Zone**
   - Kubernetes Control Plane
   - Monitoring Services
   - Backup Services
   - Administrative Tools

**Firewall Rules:**

- Internet → DMZ: HTTPS (443), HTTP (80)
- DMZ → Application: HTTPS (443), HTTP (8080)
- Application → Data: Database ports, Cache ports
- Management → All: SSH (22), Management ports
- All → Internet (selective): HTTPS outbound for external integrations

### 4.4 Load Balancing Strategy

**External Load Balancer:**
- Layer 7 (Application) load balancing
- SSL termination
- Health check configuration
- Session affinity support
- Geographic load distribution

**Internal Load Balancing:**
- Service-level load balancing via Kubernetes Services
- Pod-to-pod communication via ClusterIP
- Load distribution algorithms: Round-robin, Least connections

**Database Load Balancing:**
- Read replica load balancing
- Connection pooling
- Automatic failover configuration

---

## 5. APPLICATION ARCHITECTURE

### 5.1 Layered Architecture

**Diagram Reference:** See [06_Layered_Architecture.mermaid](#diagrams)

The application follows a standard multi-tier architecture:

#### 5.1.1 Presentation Layer

**Web Portal Components:**

- **User Interface (Angular):**
  - Responsive design for desktop and tablet
  - Progressive Web App (PWA) capabilities
  - Offline document preparation
  - Multi-language support (Portuguese, English, French)
  - Accessibility compliance (WCAG 2.1 Level AA)

- **Component Structure:**
  - Dashboard module
  - Company management module
  - License & permits module
  - Declaration submission module
  - Payment module
  - Document management module
  - Notification center
  - Reports module

**Mobile Applications:**
- Track & Trace functionality
- Push notifications
- Barcode/QR code scanning
- Document upload capability
- Payment processing

**API Console:**
- Interactive API documentation (Swagger/OpenAPI)
- Test environment for integrators
- Code samples and SDKs

#### 5.1.2 API Gateway Layer

**Diagram Reference:** See [07_API_Gateway_Architecture.mermaid](#diagrams)

**Kong API Gateway Features:**

1. **Routing:**
   - Path-based routing
   - Header-based routing
   - Query parameter routing

2. **Security:**
   - OAuth 2.0 authentication
   - JWT validation
   - API key management
   - Rate limiting per client
   - IP whitelisting/blacklisting

3. **Traffic Management:**
   - Request/response transformation
   - Request validation
   - Response caching
   - Circuit breaker pattern
   - Retry logic

4. **Monitoring:**
   - Request logging
   - Analytics and metrics
   - Error tracking
   - Performance monitoring

### 5.2 Microservices Architecture

**Diagram Reference:** See [08_Microservices_Architecture.mermaid](#diagrams)

#### 5.2.1 Core Business Services

**1. Company Management Service**
- Company registration and onboarding
- Company profile management
- Company verification and approval workflow
- Company document management
- Company status tracking

**API Endpoints:**
```
POST   /api/v1/companies/register
GET    /api/v1/companies/{companyId}
PUT    /api/v1/companies/{companyId}
GET    /api/v1/companies/{companyId}/documents
POST   /api/v1/companies/{companyId}/verify
```

**Data Model:** See WCO Data Model - Party entity

**2. License & Permits Service**
- License application management
- Permit request processing
- OGA integration for approvals
- License renewal management
- Compliance checking

**API Endpoints:**
```
POST   /api/v1/licenses/apply
GET    /api/v1/licenses/{licenseId}
GET    /api/v1/licenses/company/{companyId}
PUT    /api/v1/licenses/{licenseId}/renew
POST   /api/v1/permits/request
```

**Workflow:** Camunda-based approval workflow with parallel OGA tasks

**3. Agent Nomination Service**
- Agent registration
- Agent-company relationships
- Power of attorney management
- Agent authorization tracking

**API Endpoints:**
```
POST   /api/v1/agents/nominate
GET    /api/v1/agents/company/{companyId}
PUT    /api/v1/agents/{agentId}/revoke
GET    /api/v1/agents/{agentId}/authorizations
```

**4. Declaration Management Service**
- Import/export declaration submission
- Declaration validation
- State machine management
- Amendment handling
- Declaration cancellation

**API Endpoints:**
```
POST   /api/v1/declarations/submit
GET    /api/v1/declarations/{declarationId}
PUT    /api/v1/declarations/{declarationId}/amend
GET    /api/v1/declarations/status/{declarationId}
POST   /api/v1/declarations/{declarationId}/cancel
```

**State Machine:** See [09_Declaration_State_Machine.mermaid](#diagrams)

**5. Document Management Service**
- Document upload and storage
- Document validation
- Version control
- Document retrieval
- Document lifecycle management

**Supported Formats:**
- PDF, JPEG, PNG for scanned documents
- XML, JSON, EDI for structured data
- Microsoft Office formats

**Storage:**
- Object storage (MinIO/S3 compatible)
- Document metadata in PostgreSQL
- Document indexing for search

**6. Track & Trace Service**
- Real-time cargo tracking
- Shipment status updates
- Event notification
- Historical tracking data
- Integration with JUP/TOS for container tracking

**Events Tracked:**
- Cargo arrival at port
- Container gate-in/gate-out
- Customs examination
- Duty payment
- Cargo release
- Delivery confirmation

**7. Payment & Billing Service**
- Invoice generation
- Payment processing
- Payment gateway integration
- Receipt management
- Accounting integration

**Payment Methods:**
- Bank transfer
- Credit/debit card
- Mobile money
- Digital wallets

**Integration:** BANSTA messages for bank status

**8. Master Data Management Service**
- HS Code management (WCO HS2017/HS2022)
- Port code management (UN/LOCODE)
- Country codes (ISO 3166)
- Currency codes (ISO 4217)
- Unit of measure codes
- IMDG (Dangerous goods codes)

**Data Sources:**
- WCO reference data
- UN reference data
- Local customizations

#### 5.2.2 Integration Services

**Diagram Reference:** See [10_Integration_Services_Architecture.mermaid](#diagrams)

**1. ASYCUDA Integration Service**
- Customs declaration submission
- Customs assessment status
- Duty calculation
- Clearance certificate retrieval

**Protocol:** SOAP/XML
**ICD Reference:** JUL-AGT Integration Control Document

**2. SINTECE Integration Service**
- Single window data exchange
- Certificate validation
- License verification

**Protocol:** REST/JSON
**ICD Reference:** JUL-SINTECE Integration Control Document

**3. JUP Integration Service**
- Port entry/exit declarations
- Container tracking
- Berth scheduling

**Protocol:** REST/JSON or SOAP/XML

**4. TOS Integration Service**
- Container gate-in/gate-out
- Container status
- Terminal charges

**Protocol:** REST/JSON

**5. OGA Integration Service**
- Multi-agency permit applications
- Certificate requests
- Approval status tracking

**Agencies:**
- ARCCLA (regulatory approvals)
- MINDCOM (commerce permits)
- ANTT (transport licenses)
- Health/Agriculture agencies (LPCO)

#### 5.2.3 Cross-Cutting Services

**1. Identity & Access Management Service**
**Diagram Reference:** See [11_IAM_Architecture.mermaid](#diagrams)

**Keycloak Implementation:**

- **Authentication:**
  - Username/password
  - Two-factor authentication (2FA)
  - Digital certificates
  - Social login (optional)

- **Authorization:**
  - Role-based access control (RBAC)
  - Attribute-based access control (ABAC)
  - Fine-grained permissions

- **User Management:**
  - User registration
  - Profile management
  - Password reset
  - Account activation/deactivation

**Roles:**
- System Administrator
- Company Administrator
- Company User
- Government Official (various agencies)
- Customs Officer
- Port Operator
- Support Staff

**Groups:**
- Company-based groups
- Agency-based groups
- Role-based groups

**2. Notification Service**
- Email notifications
- SMS notifications
- In-app notifications
- Push notifications (mobile)
- Alert management

**Notification Types:**
- Application status updates
- Payment confirmations
- Document expiry warnings
- System announcements
- Quota alerts
- Tariff change notifications

**3. Workflow Service (Camunda)**
- Business process orchestration
- Task management
- SLA monitoring
- Process analytics

**Key Workflows:**
- Company registration approval
- License application processing
- Declaration clearance process
- Payment verification
- Document approval chains

**4. Audit & Logging Service**
- Comprehensive audit trail
- User activity logging
- System event logging
- Compliance reporting

**Audit Events:**
- User login/logout
- Data modifications
- Document access
- Payment transactions
- Configuration changes
- API calls

**5. Reporting & Analytics Service**
- Pre-built reports
- Ad-hoc reporting
- Data visualization
- Business intelligence dashboards

**Report Categories:**
- Trade statistics
- Revenue reports
- Processing time reports
- User activity reports
- System performance reports

### 5.3 Business Logic Layer

**Diagram Reference:** See [12_Business_Logic_Architecture.mermaid](#diagrams)

**Business Domain Model:**

The business logic layer implements domain-driven design principles with the following aggregates:

1. **Company Aggregate:**
   - Company entity
   - Company documents
   - Company users
   - Company licenses
   - Company agents

2. **Declaration Aggregate:**
   - Declaration header
   - Declaration items
   - Supporting documents
   - Payment information
   - Status history

3. **License Aggregate:**
   - License application
   - Required documents
   - Approval workflow
   - License certificate
   - Renewal history

4. **Shipment Aggregate:**
   - Shipment header
   - Container information
   - Cargo items
   - Tracking events
   - Related declarations

**Business Rules Engine:**

Implemented using Drools for complex rule evaluation:

- Tariff calculation rules
- License eligibility rules
- Document requirement rules
- Validation rules
- Approval routing rules

**Process Flow Example - Import Declaration:**
**Diagram Reference:** See [13_Import_Declaration_Process.mermaid](#diagrams)

1. Trader submits import declaration via web portal
2. System validates declaration data
3. System checks required documents
4. System submits to ASYCUDA
5. Customs processes declaration
6. System receives assessment from ASYCUDA
7. System generates duty invoice
8. Trader makes payment
9. System confirms payment with bank
10. System requests clearance certificate
11. System notifies trader of clearance
12. Cargo can be released

### 5.4 Services and Integration Layer

**Diagram Reference:** See [14_Integration_Layer_Architecture.mermaid](#diagrams)

#### 5.4.1 Integration Patterns

**1. Synchronous Integration (REST/SOAP):**
- Request-reply pattern
- Used for: Real-time queries, validation services
- Timeout handling: 30 seconds default
- Retry logic: 3 attempts with exponential backoff

**2. Asynchronous Integration (Message Queue):**
- Publish-subscribe pattern
- Used for: Status updates, notifications, batch processing
- Message persistence for reliability
- Dead letter queue for failed messages

**3. File-based Integration (FTP/SFTP):**
- Used for: Bulk data exchange, reports
- Scheduled file pickup
- File validation and processing
- Archive strategy

**4. EDI Integration:**
- UN/EDIFACT messages
- Used for: Maritime declarations, cargo manifests
- Message types: CUSCAR, CUSDEC, BAPLIE, COPRAR
- Transformation to internal format

#### 5.4.2 Data Flow

**Diagram Reference:** See [15_Data_Flow_Diagram.mermaid](#diagrams)

**Critical Data Flows:**

| Use Case | Data Flow | Style | Source | Target | Frequency | Security |
|----------|-----------|-------|--------|--------|-----------|----------|
| Declaration Submission | Import Declaration | Request-Reply | JUL Portal | ASYCUDA | On-demand | TLS 1.3, JWT |
| Customs Assessment | Assessment Result | Notification | ASYCUDA | JUL | Real-time | TLS 1.3, Certificate |
| Payment Confirmation | Payment Status | Request-Reply | JUL | Bank Gateway | On-demand | TLS 1.3, Digital Signature |
| Container Tracking | Container Events | Subscribe | JUP/TOS | JUL | Real-time | TLS 1.3, API Key |
| License Approval | Approval Status | Notification | OGA Systems | JUL | Real-time | TLS 1.3, OAuth 2.0 |
| Manifest Data | Cargo Manifest | Publish | SINTECE | JUL | On arrival | TLS 1.3, Certificate |

**Data Specifications:**

All data exchanges follow:
- WCO Data Model 3.10 for customs data
- UN/EDIFACT for maritime messages
- JSON for REST APIs
- SOAP/XML for legacy integrations
- ISO standards for codes and identifiers

### 5.5 Data Access Layer

**Diagram Reference:** See [16_Data_Access_Layer.mermaid](#diagrams)

#### 5.5.1 Data Access Control

**Database Access Strategy:**

1. **Application-Level Access:**
   - Each microservice has dedicated database schema
   - Service accounts with minimal privileges
   - No direct database access from presentation layer

2. **Connection Management:**
   - Connection pooling (HikariCP)
   - Pool size: min=10, max=50 per service
   - Connection timeout: 30 seconds
   - Idle timeout: 10 minutes

3. **Query Optimization:**
   - Prepared statements for all queries
   - Query result caching where appropriate
   - Index optimization for frequent queries
   - Slow query logging and analysis

#### 5.5.2 Data Storage

**Primary Database (PostgreSQL):**

- **Configuration:**
  - Version: PostgreSQL 14+
  - Cluster: 3-node setup (1 primary, 2 replicas)
  - Replication: Streaming replication
  - Backup: Daily full backup, continuous WAL archiving

- **Schema Strategy:**
  - Separate schema per microservice
  - Shared reference data schema
  - Audit schema for all audit logs

- **Data Types:**
  - Unicode support (UTF-8 encoding)
  - JSONB for semi-structured data
  - Full-text search capabilities
  - PostGIS for geographic data

**Document Store (MongoDB):**

- **Configuration:**
  - Version: MongoDB 6+
  - Replica set: 3 nodes
  - Sharding for large collections

- **Usage:**
  - Uploaded documents metadata
  - Unstructured logs
  - Flexible schema data
  - Historical archives

**Cache Layer (Redis):**

- **Configuration:**
  - Version: Redis 7+
  - Cluster mode: 6 nodes (3 masters, 3 replicas)
  - Persistence: RDB + AOF

- **Usage:**
  - Session storage
  - API response caching
  - Rate limiting counters
  - Distributed locks
  - Real-time analytics

#### 5.5.3 Connection Pooling

**HikariCP Configuration:**

```yaml
hikaricp:
  pool-name: JUL-Pool
  minimum-idle: 10
  maximum-pool-size: 50
  connection-timeout: 30000
  idle-timeout: 600000
  max-lifetime: 1800000
  auto-commit: false
  connection-test-query: SELECT 1
```

**Benefits:**
- Reduced connection overhead
- Better resource utilization
- Improved performance
- Connection leak detection

#### 5.5.4 Concurrent Access and Object Locking

**Strategy: Optimistic Locking**

- Version number or timestamp on entities
- Check version on update
- Throw exception if version mismatch
- Application handles retry logic

**Implementation:**
```java
@Version
private Long version;
```

**Use Cases for Pessimistic Locking:**
- Financial transactions (payment processing)
- Critical counter updates
- Resource allocation

#### 5.5.5 Transactional Requirements

**Transaction Boundaries:**

1. **Service-Level Transactions:**
   - Database operations within single service are transactional
   - ACID properties enforced by database

2. **Distributed Transactions:**
   - Saga pattern for cross-service transactions
   - Compensating transactions for rollback
   - Event sourcing for audit trail

**Example Transaction Boundaries:**

- **Declaration Submission:**
  - Start transaction
  - Save declaration
  - Save items
  - Save documents references
  - Update status
  - Commit transaction

- **Payment Processing (Saga):**
  1. Reserve payment amount
  2. Call bank payment API
  3. If success: Confirm payment, update declaration
  4. If failure: Release reserved amount, notify user

#### 5.5.6 Persistence Strategy

**Entity Persistence Requirements:**

| Entity | Size | Volume | Duration | Update Frequency | Reliability |
|--------|------|--------|----------|------------------|-------------|
| Company | ~5 KB | 100,000 | Indefinite | Monthly | Critical |
| User | ~2 KB | 500,000 | Indefinite | Weekly | Critical |
| Declaration | ~50 KB | 10M/year | 7 years | Daily | Critical |
| Document | 1-5 MB | 50M/year | 7 years | Rarely | High |
| Transaction Log | ~1 KB | 100M/year | 3 years | Never | Critical |
| Audit Log | ~500 B | 500M/year | 5 years | Never | Critical |

**Archival Strategy:**

- Active data: 2 years in primary database
- Archive data: 2-7 years in archive database
- Cold storage: >7 years in object storage
- Automated archival process monthly

### 5.6 Performance Requirements

**Diagram Reference:** See [17_Performance_Architecture.mermaid](#diagrams)

#### Performance Targets

| Requirement | Use Case | Mechanism | Constraints |
|-------------|----------|-----------|-------------|
| Response time < 3s | Portal page load | CDN, caching, lazy loading | 95th percentile |
| Response time < 2s | API calls | Connection pooling, caching | 90th percentile |
| Response time < 5s | Report generation | Async processing, pre-aggregation | Large reports |
| Throughput 100 req/s | Declaration submission | Horizontal scaling, load balancing | Peak hours |
| Throughput 1000 req/s | Track & trace queries | Read replicas, caching | Normal operations |
| Concurrent users 10,000 | Portal access | Stateless architecture, CDN | Business hours |
| Database queries < 500ms | Complex queries | Indexing, query optimization | 95th percentile |

**Performance Optimization Strategies:**

1. **Caching Strategy:**
   - Browser caching for static assets
   - Redis caching for API responses
   - Database query result caching
   - CDN for geographic distribution

2. **Database Optimization:**
   - Read replicas for query load distribution
   - Partitioning for large tables (by date/region)
   - Materialized views for complex reports
   - Index optimization based on query patterns

3. **Application Optimization:**
   - Lazy loading of data
   - Pagination for large result sets
   - Async processing for heavy operations
   - Connection pooling
   - Database connection reuse

4. **Infrastructure Optimization:**
   - Kubernetes horizontal pod autoscaling
   - Load balancing across multiple instances
   - Geographic distribution of services
   - SSD storage for databases

### 5.7 Security Architecture

**Diagram Reference:** See [18_Security_Architecture.mermaid](#diagrams)

#### 5.7.1 Authentication

**Multi-Factor Authentication Strategy:**

1. **Primary Authentication (Username/Password):**
   - Minimum password requirements (12 characters, complexity)
   - Password hashing (bcrypt with salt)
   - Account lockout after 5 failed attempts
   - Password expiry (90 days for government users)

2. **Secondary Authentication (Optional 2FA):**
   - Time-based OTP (TOTP)
   - SMS-based OTP
   - Email verification code
   - Hardware tokens (for high-privilege users)

3. **Certificate-Based Authentication:**
   - Digital certificates for companies
   - Certificate validation against CA
   - Certificate revocation checking (CRL/OCSP)
   - Smart card integration

4. **SSO Integration:**
   - OpenID Connect protocol
   - SAML 2.0 for government systems
   - JWT tokens for API access
   - Session management in Redis

**Authentication Flow:**
**Diagram Reference:** See [19_Authentication_Flow.mermaid](#diagrams)

1. User enters credentials
2. System validates against Keycloak
3. If 2FA enabled, prompt for second factor
4. Validate second factor
5. Issue JWT access token
6. Issue refresh token
7. Store session in Redis
8. Return tokens to client

#### 5.7.2 Authorization

**Role-Based Access Control (RBAC):**

| Role | Description | Permissions |
|------|-------------|------------|
| system.admin | System Administrator | Full system access, user management, configuration |
| company.admin | Company Administrator | Company data, user management within company, declarations |
| company.user | Company User | Submit declarations, view company data, upload documents |
| company.viewer | Company Viewer | Read-only access to company data |
| trader.user | Trader | Import/export declarations, payment, tracking |
| agent.user | Shipping Agent | Agent nominations, declarations on behalf of clients |
| broker.user | Customs Broker | Clearance declarations, document submission |
| customs.officer | Customs Official | Declaration review, assessment, clearance approval |
| customs.supervisor | Customs Supervisor | Advanced clearance, risk assessment, reporting |
| port.operator | Port Operator | Container tracking, gate operations |
| government.officer | OGA Officer | License approval, permit issuance, inspection |
| auditor | System Auditor | Read-only access to audit logs, reports |
| support.staff | Support Staff | Limited user management, troubleshooting |

**Permission Matrix:**

| Resource | Create | Read | Update | Delete | Approve |
|----------|--------|------|--------|--------|---------|
| Company | company.admin | company.*, system.admin | company.admin | system.admin | government.officer |
| Declaration | trader.*, broker.* | trader.*, customs.* | trader.* | trader.* | customs.officer |
| License | company.admin | company.*, government.* | government.officer | system.admin | government.officer |
| User | company.admin, system.admin | company.admin, system.admin | same | system.admin | - |
| Payment | trader.* | trader.*, customs.* | - | system.admin | - |
| Report | - | customs.*, government.* | - | - | - |

**Attribute-Based Access Control (ABAC):**

- Access based on attributes (company, location, time)
- Dynamic policy evaluation
- Fine-grained access control

**Example Policy:**
```
ALLOW READ Declaration
WHERE user.company = declaration.company
OR user.role = "customs.officer"
AND declaration.status IN ["submitted", "assessed"]
```

#### 5.7.3 Access Request Process

**User Access Workflow:**

1. **Self-Registration (Traders/Agents):**
   - User registers on portal
   - Email verification required
   - Company admin approval required
   - Account activated

2. **Admin Creation (Government Users):**
   - Request submitted to system admin
   - Approval by department head
   - Role assignment by system admin
   - Credentials provided securely

3. **Role Change Request:**
   - User submits role change request
   - Manager approval required
   - System admin implements change
   - Audit log created

4. **Access Revocation:**
   - Immediate for security incidents
   - Upon termination/resignation
   - Certificate revocation
   - Session invalidation

#### 5.7.4 Encryption

**Data Encryption Strategy:**

1. **Data in Transit:**
   - TLS 1.3 for all communications
   - Certificate pinning for mobile apps
   - Perfect forward secrecy (PFS)
   - Strong cipher suites only

2. **Data at Rest:**
   - Database encryption (PostgreSQL TDE)
   - File storage encryption (AES-256)
   - Key management (HashiCorp Vault)
   - Encrypted backups

3. **Application-Level Encryption:**
   - Sensitive fields encrypted (PII, financial data)
   - Encryption at application layer before storage
   - Encryption keys rotated quarterly

4. **Key Management:**
   - Centralized key management (Vault)
   - Key rotation policy
   - Key backup and recovery
   - Hardware Security Module (HSM) for root keys

**Encryption Implementation:**

```java
// Field-level encryption example
@Convert(converter = EncryptedStringConverter.class)
private String taxIdentificationNumber;

@Convert(converter = EncryptedStringConverter.class)
private String bankAccountNumber;
```

#### 5.7.5 API Security

**API Security Measures:**

1. **Authentication:**
   - OAuth 2.0 for user APIs
   - API keys for system integrations
   - JWT tokens with expiration
   - Client certificate authentication for sensitive APIs

2. **Authorization:**
   - Scope-based access control
   - Resource-level permissions
   - Rate limiting per client

3. **Input Validation:**
   - Schema validation for all inputs
   - SQL injection prevention
   - XSS prevention
   - CSRF protection

4. **Output Encoding:**
   - Proper content type headers
   - JSON sanitization
   - No sensitive data in logs

**API Rate Limiting:**

| Client Type | Rate Limit | Burst Limit | Time Window |
|-------------|------------|-------------|-------------|
| Public Portal | 100 req/min | 200 | 1 minute |
| Mobile App | 50 req/min | 100 | 1 minute |
| Integration API | 1000 req/min | 2000 | 1 minute |
| Internal Service | Unlimited | - | - |
| Partner System | 500 req/min | 1000 | 1 minute |

### 5.8 Scalability

**Diagram Reference:** See [20_Scalability_Architecture.mermaid](#diagrams)

#### Horizontal Scaling Strategy

**Application Tier:**
- Stateless microservices enable unlimited horizontal scaling
- Kubernetes Horizontal Pod Autoscaler (HPA)
- Auto-scaling based on CPU/memory/custom metrics
- Min replicas: 2, Max replicas: 20 per service

**Database Tier:**
- Read replicas for query distribution
- Connection pooling to manage connections
- Database sharding for very large tables (future)
- Caching to reduce database load

**Cache Tier:**
- Redis cluster mode
- Horizontal scaling of cache nodes
- Partitioning of cache data

**Message Queue:**
- RabbitMQ/Kafka cluster
- Partition-based scaling
- Consumer groups for parallel processing

#### Vertical Scaling Considerations

**Resource Allocation Per Service:**

| Service | Min CPU | Min Memory | Max CPU | Max Memory |
|---------|---------|------------|---------|------------|
| API Gateway | 1 core | 2 GB | 4 cores | 8 GB |
| Company Service | 0.5 core | 1 GB | 2 cores | 4 GB |
| Declaration Service | 1 core | 2 GB | 4 cores | 8 GB |
| Document Service | 1 core | 2 GB | 4 cores | 16 GB |
| Payment Service | 0.5 core | 1 GB | 2 cores | 4 GB |
| Integration Service | 1 core | 2 GB | 4 cores | 8 GB |

#### Session Management

**Stateless Session Strategy:**
- JWT tokens contain session state
- No server-side session storage (except Redis for refresh tokens)
- Session data in Redis cache cluster
- Session replication across Redis nodes
- Session timeout: 30 minutes idle, 8 hours maximum

#### Future Scalability Considerations

**Geographic Distribution:**
- Multi-region deployment capability
- Data residency compliance
- CDN for static content
- Regional database replicas

**Database Scaling:**
- Table partitioning (by date, region)
- Archival of old data
- Separate analytics database
- Eventual consistency for non-critical data

### 5.9 Extensibility

**Microservices Extensibility:**

The architecture supports extensibility through:

1. **API Versioning:**
   - URL versioning (/api/v1/, /api/v2/)
   - Header-based versioning
   - Backward compatibility support

2. **Plugin Architecture:**
   - Custom modules can be added without core changes
   - Event-driven integration points
   - Webhook support for external integrations

3. **Feature Flags:**
   - Toggle features without deployment
   - A/B testing capability
   - Gradual rollout of new features

4. **Multi-Tenancy:**
   - Support for multiple countries/regions
   - Tenant-specific configurations
   - Shared infrastructure

**Extension Points:**

- Custom document validators
- Additional payment gateways
- New OGA integrations
- Custom report templates
- Additional authentication methods
- New notification channels

**Standards Compliance for Extensibility:**

- Open API specification for all APIs
- Standard data models (WCO, UN)
- Standard protocols (REST, SOAP, EDIFACT)
- Configurable business rules
- Externalized configuration

---

## 6. DATA CONVERSION AND MIGRATION

### 6.1 Migration Strategy

**Diagram Reference:** See [21_Data_Migration_Strategy.mermaid](#diagrams)

**Migration Approach:**

1. **Phased Migration:**
   - Phase 1: Master data and reference data
   - Phase 2: Company and user data
   - Phase 3: Historical declarations (last 2 years)
   - Phase 4: Older historical data (archive)

2. **Data Sources:**
   - Existing systems (if any)
   - Excel files and databases
   - Paper records (digitization)
   - External systems (ASYCUDA, etc.)

3. **Migration Tools:**
   - Apache Camel for ETL
   - Spring Batch for batch processing
   - Custom migration scripts
   - Data validation framework

### 6.2 Data Mapping

**Company Data Migration:**

| Module | Business Object | Source System | Source Table | Target Schema | Target Table | Validation Rules |
|--------|----------------|---------------|--------------|---------------|--------------|------------------|
| Company | Company | Excel/Legacy | companies | jul_company | companies | Tax ID unique, mandatory fields |
| Company | Company Document | File system | N/A | jul_document | company_documents | File format validation |
| Company | Company User | Excel/Legacy | users | jul_user | users | Email unique, company exists |
| License | License | Excel/OGA | licenses | jul_license | licenses | License number unique |
| License | License Type | Configuration | N/A | jul_master | license_types | Valid license type codes |

**Declaration Data Migration:**

| Module | Business Object | Source System | Constraints | Target Table | Interface Rule | Sequence |
|--------|----------------|---------------|-------------|--------------|----------------|----------|
| Declaration | Import Declaration | ASYCUDA | Last 2 years | declarations | Map to WCO DM 3.10 | 1 |
| Declaration | Declaration Items | ASYCUDA | Related to declaration | declaration_items | Preserve item sequence | 2 |
| Declaration | Declaration Parties | ASYCUDA | Declarant, consignee | declaration_parties | Map party roles | 3 |
| Declaration | Declaration Docs | ASYCUDA | Supporting documents | declaration_documents | Link to document store | 4 |
| Declaration | Declaration Payments | ASYCUDA | Duty payments | payments | Match with financial records | 5 |

### 6.3 Data Quality and Validation

**Validation Checks:**

1. **Completeness:**
   - Mandatory fields populated
   - Required relationships exist
   - No orphaned records

2. **Accuracy:**
   - Data types correct
   - Values within valid ranges
   - Code values valid in reference tables

3. **Consistency:**
   - Cross-field validation
   - Total amounts match detail
   - Status values logical

4. **Uniqueness:**
   - Primary keys unique
   - Business keys unique
   - No duplicate records

**Migration Quality Metrics:**

- Success rate: 95%+ records migrated successfully
- Error rate: <5% requiring manual intervention
- Data quality score: 90%+ passing all validations
- Performance: 10,000 records per hour minimum

### 6.4 Rollback Strategy

- Backup of source systems before migration
- Snapshot of target database before each phase
- Ability to rollback to previous phase
- Reconciliation reports after each phase
- Parallel run period for validation

---

## 7. REPORTING AND INFORMATION

### 7.1 Reporting Strategy

**Diagram Reference:** See [22_Reporting_Architecture.mermaid](#diagrams)

**Reporting Layers:**

1. **Operational Reports:**
   - Real-time dashboards
   - Daily transaction reports
   - User activity reports
   - System performance reports

2. **Analytical Reports:**
   - Trade statistics
   - Revenue analysis
   - Processing time analysis
   - Trend analysis

3. **Compliance Reports:**
   - Audit reports
   - Regulatory reports
   - WCO statistical reports
   - Financial reports

### 7.2 Report Catalog

| Use Case | Subject Domain | Business Object | Report Type | Description | Format |
|----------|----------------|-----------------|-------------|-------------|--------|
| Trade Statistics | Customs | Import/Export | Analytical | Monthly trade volumes by HS code | PDF, Excel |
| Revenue Collection | Finance | Duty Payments | Operational | Daily revenue collection summary | PDF, Excel |
| Processing Times | Operations | Declaration | Analytical | Average clearance times by type | Dashboard, PDF |
| User Activity | Security | User Actions | Operational | User login and activity log | Excel, CSV |
| License Approvals | Licensing | License | Operational | License approval status and timeline | PDF, Excel |
| Container Movements | Port Operations | Container | Operational | Container gate-in/out report | PDF, Excel |
| System Performance | Infrastructure | System Metrics | Technical | Server and application performance | Dashboard |
| Compliance Audit | Audit | All Entities | Compliance | Complete audit trail for period | PDF, Excel |
| OGA Statistics | Government | Permits/Licenses | Analytical | OGA processing times and volumes | Dashboard, PDF |

### 7.3 Report Generation Mechanism

**Technology Stack:**

- **JasperReports:** Template-based reports (PDF, Excel, CSV)
- **Grafana:** Real-time dashboards and visualizations
- **Kibana:** Log analysis and system monitoring reports
- **Custom Report Engine:** Ad-hoc queries and custom reports

**Report Scheduling:**

- Cron-based scheduling
- On-demand generation
- Automated email delivery
- Report archive (6 months online, 7 years archive)

**Performance Optimization:**

- Pre-aggregated data for common reports
- Materialized views for complex queries
- Report caching for frequently accessed reports
- Async report generation for large reports

---

## 8. DEPLOYMENT ARCHITECTURE

**Diagram Reference:** See [03_Deployment_Architecture.mermaid](#diagrams) (Referenced earlier)

### 8.1 Environment Specifications

#### Development Environment

**Infrastructure:**

| Component | Specification | Quantity | Location | Purpose |
|-----------|---------------|----------|----------|---------|
| K8s Master Nodes | 4 vCPU, 16GB RAM | 1 | On-premise DC | Control plane |
| K8s Worker Nodes | 8 vCPU, 32GB RAM | 3 | On-premise DC | Application workload |
| PostgreSQL | 4 vCPU, 16GB RAM, 500GB SSD | 1 | On-premise DC | Primary database |
| Redis | 2 vCPU, 8GB RAM | 1 | On-premise DC | Cache |
| Storage | NFS/SAN | 2 TB | On-premise DC | Document storage |

**Software:**
- Kubernetes 1.27
- Docker 24.x
- PostgreSQL 14
- Redis 7
- Keycloak 22

**Access:**
- VPN required
- Developer workstations
- CI/CD pipelines

#### Testing/UAT Environment

**Infrastructure:**

| Component | Specification | Quantity | Location | Purpose |
|-----------|---------------|----------|----------|---------|
| K8s Master Nodes | 8 vCPU, 32GB RAM | 3 | On-premise DC | Control plane (HA) |
| K8s Worker Nodes | 16 vCPU, 64GB RAM | 5 | On-premise DC | Application workload |
| PostgreSQL Cluster | 8 vCPU, 32GB RAM, 1TB SSD | 3 | On-premise DC | DB cluster (1 primary, 2 replicas) |
| MongoDB Cluster | 8 vCPU, 32GB RAM, 1TB SSD | 3 | On-premise DC | Document store |
| Redis Cluster | 4 vCPU, 16GB RAM | 6 | On-premise DC | Cache cluster |
| RabbitMQ Cluster | 4 vCPU, 16GB RAM | 3 | On-premise DC | Message broker |
| Storage | NFS/SAN | 10 TB | On-premise DC | Document storage |
| Load Balancer | 4 vCPU, 16GB RAM | 2 | DMZ | HA load balancer |

**Software:**
- Identical to production versions
- Test data loaded
- Integration endpoints configured

**Access:**
- Business users for UAT
- QA team
- Integration partners for testing

#### Production Environment

**Infrastructure:**

| Component | Specification | Quantity | Location | Costs | Admin & License |
|-----------|---------------|----------|----------|-------|-----------------|
| K8s Master Nodes | 16 vCPU, 64GB RAM | 3 | On-premise DC | $15K each | Kubernetes (Free) |
| K8s Worker Nodes | 32 vCPU, 128GB RAM, 1TB SSD | 10 | On-premise DC | $30K each | Kubernetes (Free) |
| PostgreSQL Cluster | 32 vCPU, 128GB RAM, 4TB NVMe | 3 | On-premise DC | $50K each | PostgreSQL (Free) |
| MongoDB Cluster | 32 vCPU, 128GB RAM, 4TB NVMe | 3 | On-premise DC | $50K each | MongoDB Community (Free) |
| Redis Cluster | 16 vCPU, 64GB RAM | 6 | On-premise DC | $20K each | Redis (Free) |
| RabbitMQ Cluster | 16 vCPU, 64GB RAM | 3 | On-premise DC | $20K each | RabbitMQ (Free) |
| Keycloak Cluster | 8 vCPU, 32GB RAM | 3 | On-premise DC | $15K each | Keycloak (Free) |
| Storage | NFS/SAN High-Performance | 50 TB | On-premise DC | $100K | NetApp/EMC license |
| Backup Storage | NFS/SAN | 100 TB | Backup DC | $80K | NetApp/EMC license |
| Load Balancer (External) | 16 vCPU, 64GB RAM | 2 | DMZ | $40K each | F5/HAProxy license |
| Firewall/WAF | Enterprise-grade | 2 | DMZ | $100K each | Fortinet/Palo Alto license |
| Monitoring Stack | 16 vCPU, 64GB RAM | 3 | Management Zone | $20K each | Prometheus/Grafana (Free) |
| Log Aggregation | 32 vCPU, 128GB RAM, 4TB SSD | 3 | Management Zone | $40K each | ELK Stack (Free) |

**Total Infrastructure Cost (CAPEX):** ~$1.5M
**Annual Maintenance (OPEX):** ~$300K (20% of CAPEX)
**Commercial Licenses:** ~$200K annually (Firewall, Storage, Backup software)

**Network Infrastructure:**

- 10 Gbps internal network
- 1 Gbps internet connectivity
- Redundant network paths
- VPN concentrators for secure access
- Network segmentation (VLANs)

**Power and Cooling:**

- Dual power supply for all critical equipment
- UPS with 30-minute runtime
- Generator backup
- Redundant cooling systems

### 8.2 Geographic Distribution

**Primary Data Center (Luanda):**
- All production systems
- Primary database
- Application servers
- Integration services

**Disaster Recovery Site (Secondary Location):**
- Standby database replica
- Cold standby application servers
- Backup systems
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 15 minutes

### 8.3 Deployment Process

**Continuous Integration/Continuous Deployment (CI/CD):**

**Diagram Reference:** See [23_CICD_Pipeline.mermaid](#diagrams)

1. **Code Commit:**
   - Developer commits code to GitLab
   - Triggers CI pipeline

2. **Build Stage:**
   - Compile code
   - Run unit tests
   - Code quality analysis (SonarQube)
   - Security scanning (OWASP Dependency Check)
   - Build Docker images
   - Push images to private registry

3. **Test Stage:**
   - Deploy to test environment
   - Run integration tests
   - Run API tests (Postman/Newman)
   - Performance tests (JMeter)
   - Security tests (OWASP ZAP)

4. **Staging Deployment:**
   - Deploy to staging environment
   - Smoke tests
   - UAT approval required

5. **Production Deployment:**
   - Approval workflow (change management)
   - Blue-green deployment strategy
   - Rolling updates with health checks
   - Automated rollback on failure
   - Post-deployment verification

**Deployment Tools:**

- GitLab CI/CD for pipelines
- Helm charts for Kubernetes deployments
- Terraform for infrastructure provisioning
- Ansible for configuration management

### 8.4 Monitoring and Alerting

**Monitoring Stack:**

1. **Infrastructure Monitoring (Prometheus + Grafana):**
   - CPU, memory, disk usage
   - Network metrics
   - Container metrics
   - Kubernetes cluster health

2. **Application Monitoring (Prometheus + Grafana):**
   - Request rates
   - Response times
   - Error rates
   - Business metrics (declarations submitted, payments processed)

3. **Log Aggregation (ELK Stack):**
   - Application logs
   - System logs
   - Audit logs
   - Security logs

4. **APM (Application Performance Monitoring):**
   - Distributed tracing (Jaeger)
   - Transaction monitoring
   - Bottleneck identification

**Alerting Rules:**

| Metric | Threshold | Severity | Action |
|--------|-----------|----------|--------|
| CPU Usage | >80% for 5 min | Warning | Scale up |
| Memory Usage | >85% for 5 min | Warning | Scale up |
| Disk Usage | >80% | Warning | Expand storage |
| API Error Rate | >5% | Critical | On-call notification |
| API Response Time | >3s (95th percentile) | Warning | Investigate |
| Database Connection Pool | >80% utilized | Warning | Increase pool size |
| Failed Logins | >10 in 5 min | Critical | Potential attack |
| Service Down | Any service unreachable | Critical | Immediate escalation |

---

## 9. INFRASTRUCTURE ARCHITECTURE DETAILS

### 9.1 Backup, Failover, and Recovery

**Diagram Reference:** See [24_Backup_Recovery_Architecture.mermaid](#diagrams)

#### 9.1.1 Backup Strategy

**Database Backup:**

1. **PostgreSQL:**
   - **Full Backup:** Daily at 2:00 AM
   - **Incremental Backup:** Every 6 hours
   - **WAL Archiving:** Continuous (every 5 minutes)
   - **Retention:** 30 days online, 1 year archive, 7 years tape
   - **Backup Tool:** pg_basebackup, pg_dump, Barman
   - **Backup Verification:** Weekly restore test

2. **MongoDB:**
   - **Full Backup:** Daily at 3:00 AM
   - **Incremental Backup:** Every 6 hours
   - **Oplog Backup:** Continuous
   - **Retention:** 30 days online, 6 months archive
   - **Backup Tool:** mongodump, MongoDB Ops Manager
   - **Backup Verification:** Weekly restore test

3. **Redis:**
   - **RDB Snapshot:** Every 6 hours
   - **AOF:** Continuous append-only file
   - **Retention:** 7 days
   - **Recovery:** Automatic from RDB + AOF

**Application Backup:**

- **Docker Images:** Stored in private registry with versioning
- **Configuration:** Backed up in Git repository
- **Kubernetes State:** etcd backup every 6 hours
- **Secrets:** Encrypted backup in Vault

**Document Storage Backup:**

- **Incremental Backup:** Daily
- **Full Backup:** Weekly
- **Retention:** 30 days online, 7 years archive
- **Replication:** 3 copies (primary, secondary, offsite)

#### 9.1.2 Failover Strategy

**Database Failover:**

**PostgreSQL:**
- **Primary-Replica Setup:** 1 primary, 2 replicas (streaming replication)
- **Automatic Failover:** Patroni for automatic failover
- **Failover Time:** <60 seconds
- **Promotion:** Replica promoted to primary automatically
- **Application Impact:** Connection retry logic handles failover

**MongoDB:**
- **Replica Set:** 3 members (1 primary, 2 secondaries)
- **Automatic Failover:** Built-in election mechanism
- **Failover Time:** <30 seconds
- **Application Impact:** Driver handles reconnection automatically

**Application Failover:**

- **Kubernetes Self-Healing:** Automatic pod restart on failure
- **Multi-Replica:** Minimum 2 replicas per service
- **Load Balancer:** Automatic traffic routing to healthy pods
- **Health Checks:** Liveness and readiness probes
- **Circuit Breaker:** Prevent cascade failures

**Infrastructure Failover:**

- **Load Balancer:** Active-passive HA pair
- **Network:** Redundant network paths
- **Power:** Dual power supply, UPS, generator
- **Storage:** RAID configuration, SAN replication

#### 9.1.3 Recovery Strategy

**Disaster Recovery Plan:**

**RPO (Recovery Point Objective):** 15 minutes
**RTO (Recovery Time Objective):** 4 hours

**Recovery Procedures:**

1. **Data Corruption/Loss:**
   - Restore from latest backup
   - Replay WAL/Oplog for point-in-time recovery
   - Validate data integrity
   - Resume operations

2. **Service Failure:**
   - Kubernetes automatic restart
   - Manual intervention if restart fails
   - Scale up resources if needed
   - Rollback deployment if new version caused failure

3. **Infrastructure Failure:**
   - Activate DR site if primary DC unavailable
   - Restore services from DR site
   - Point DNS to DR site
   - Sync data back to primary when restored

4. **Complete Site Failure:**
   - Activate DR site (secondary location)
   - Promote DR database to primary
   - Redirect traffic to DR site
   - Full operational mode in 4 hours

**Recovery Testing:**

- Quarterly DR drill
- Annual full DR exercise
- Monthly backup restore verification
- Documented recovery procedures
- Trained recovery team

### 9.2 Maintenance Windows

**Planned Maintenance:**

**Regular Maintenance Window:**
- **Schedule:** Every Saturday 2:00 AM - 6:00 AM (Angola time)
- **Frequency:** Weekly
- **Activities:**
  - Security patches
  - Minor updates
  - Database maintenance (VACUUM, REINDEX)
  - Log rotation
  - Certificate renewal

**Major Maintenance Window:**
- **Schedule:** Last Sunday of month 1:00 AM - 8:00 AM
- **Frequency:** Monthly
- **Activities:**
  - Major version upgrades
  - Infrastructure changes
  - Large data migrations
  - Comprehensive testing

**Emergency Maintenance:**
- **Trigger:** Critical security vulnerability, major outage
- **Approval:** Change Advisory Board (emergency approval)
- **Notification:** 4 hours notice (if possible)
- **Duration:** As required

**Maintenance Communication:**

- 7 days advance notice for regular maintenance
- 14 days advance notice for major maintenance
- Email notification to registered users
- System banner on portal
- Status page updates

**Zero-Downtime Deployments:**

For application updates (non-infrastructure):
- Blue-green deployment
- Rolling updates
- No maintenance window required
- Performed during business hours if needed

### 9.3 High Availability Configuration

**Service Level Agreement (SLA):**

- **Availability Target:** 99.9% (43.8 minutes downtime per month)
- **Planned Maintenance:** Excluded from SLA
- **Performance Target:** 95% of requests < 3 seconds
- **Support Response Time:**
  - Critical (P1): 15 minutes
  - High (P2): 1 hour
  - Medium (P3): 4 hours
  - Low (P4): 24 hours

**HA Components:**

| Component | HA Configuration | Redundancy Level |
|-----------|------------------|------------------|
| Load Balancer | Active-Passive pair | 2x |
| API Gateway | Active-Active (3+ pods) | 3x minimum |
| Application Services | Active-Active (2-10+ pods) | 2-10x |
| PostgreSQL | Primary + 2 replicas | 3x |
| MongoDB | 3-member replica set | 3x |
| Redis | 6-node cluster (3 masters, 3 replicas) | 2x per shard |
| RabbitMQ | 3-node cluster | 3x |
| Keycloak | 3-node cluster | 3x |
| Storage | RAID 10 + replication | 4x |

---

## 10. STANDARDS AND COMPLIANCE

### 10.1 WCO Data Model Compliance

The JUL system implements the World Customs Organization (WCO) Data Model Version 3.10 for all customs-related data exchanges.

**WCO Data Model Implementation:**

**Diagram Reference:** See [25_WCO_Data_Model_ER.mermaid](#diagrams)

**Core Entities:**

1. **Declaration:**
   - Declaration header information
   - Declaration type and procedure codes
   - Declaration currency and exchange rate
   - Customs office information
   - Reference to related declarations

2. **DeclarationGoodsItem:**
   - Item sequence number
   - HS code classification
   - Item description
   - Origin information
   - Valuation details
   - Quantity and unit of measure

3. **Party:**
   - Party identification
   - Party role (declarant, importer, exporter, agent)
   - Party address
   - Party communication details
   - Authorization information

4. **Transport:**
   - Transport mode
   - Transport means identification
   - Container information
   - Route information
   - Border crossing details

5. **Document:**
   - Document type code
   - Document reference
   - Document issue date
   - Document expiry date
   - Attachment information

6. **ValuationAdjustment:**
   - Customs valuation method
   - Adjustment amounts
   - Currency information
   - Related charges

**HS Code Management:**

- WCO HS2017 and HS2022 compliant
- Six-digit harmonization
- National extensions (8-10 digits)
- Regular updates from WCO
- Tariff rate application

### 10.2 UN/EDIFACT Compliance

**Supported Message Types:**

1. **CUSCAR (Cargo Report Message):**
   - Purpose: Cargo manifest submission
   - Usage: Pre-arrival cargo information
   - Frequency: Per vessel/flight arrival

2. **CUSDEC (Customs Declaration Message):**
   - Purpose: Goods declaration
   - Usage: Import/export declarations
   - Frequency: Per consignment

3. **CUSRES (Customs Response Message):**
   - Purpose: Customs response to declaration
   - Usage: Assessment, clearance status
   - Frequency: Per declaration response

4. **BAPLIE (Bayplan/Stowage Plan Message):**
   - Purpose: Container loading plan
   - Usage: Vessel bay planning
   - Frequency: Per vessel

5. **COPRAR (Container Discharge/Loading Order Message):**
   - Purpose: Container movement instructions
   - Usage: Terminal operations
   - Frequency: Per container move

6. **BANSTA (Banking Status Message):**
   - Purpose: Payment status
   - Usage: Payment confirmation
   - Frequency: Per payment transaction

**Message Transformation:**

- UN/EDIFACT to JSON/XML conversion
- Mapping to internal data model
- Validation against message syntax
- Error handling and rejection notifications

### 10.3 International Standards

**ISO Standards:**

1. **ISO 3166 (Country Codes):**
   - 2-letter country codes (ISO 3166-1 alpha-2)
   - 3-letter country codes (ISO 3166-1 alpha-3)
   - Subdivision codes (ISO 3166-2)

2. **ISO 4217 (Currency Codes):**
   - 3-letter currency codes
   - Currency numbers
   - Minor unit representation

3. **ISO 8601 (Date and Time):**
   - Standard date/time format
   - UTC timezone for storage
   - Local timezone for display

4. **UN/LOCODE (Location Codes):**
   - Port and location codes
   - Format: AOLAD (country + location)
   - Regular updates from UN

**IMDG (International Maritime Dangerous Goods Code):**

- Dangerous goods classification
- UN numbers
- Packing groups
- Special handling requirements

### 10.4 Regional Standards

**GCC (Gulf Cooperation Council) Standards:**

1. **GCC Common Customs Law:**
   - Customs procedures harmonization
   - Common external tariff
   - Rules of origin

2. **GCC Unified Guide for Customs Procedures:**
   - Standardized processes
   - Common documentation
   - Mutual recognition

**African Union Standards:**

1. **African Continental Free Trade Area (AfCFTA):**
   - Tariff preferences
   - Rules of origin
   - Trade facilitation measures

### 10.5 Security Standards

**Information Security:**

1. **ISO 27001 (Information Security Management):**
   - Security controls implementation
   - Risk assessment
   - Continuous improvement

2. **OWASP Top 10:**
   - Web application security
   - API security
   - Secure coding practices

3. **PCI DSS (Payment Card Industry Data Security Standard):**
   - Payment data protection
   - Cardholder data security
   - Network security

**Data Protection:**

1. **GDPR Principles (where applicable):**
   - Data minimization
   - Purpose limitation
   - Storage limitation
   - Data subject rights

2. **Local Data Protection Laws:**
   - Compliance with Angolan data protection regulations
   - Cross-border data transfer restrictions
   - Personal data handling procedures

### 10.6 Integration Standards

**API Standards:**

1. **REST API:**
   - RESTful design principles
   - HTTP methods (GET, POST, PUT, DELETE)
   - Status codes
   - JSON payload

2. **OpenAPI Specification 3.0:**
   - API documentation
   - Schema definition
   - Example payloads

3. **SOAP/WSDL:**
   - For legacy system integration
   - WS-Security for authentication
   - WS-ReliableMessaging for reliability

**Message Standards:**

1. **JSON Schema:**
   - Request/response validation
   - Data type enforcement
   - Required field validation

2. **XML Schema (XSD):**
   - For SOAP and EDI messages
   - Schema validation
   - Namespace management

3. **Avro/Protobuf:**
   - For high-performance messaging
   - Schema evolution
   - Backward compatibility

### 10.7 Compliance Monitoring

**Compliance Audit:**

- Quarterly compliance assessment
- Standards conformance testing
- Gap analysis
- Remediation planning

**Compliance Reporting:**

- Annual compliance report
- Standards version tracking
- Non-conformance register
- Corrective action tracking

---

## APPENDIX

### A. Glossary of Terms

| Term | Definition |
|------|------------|
| AGT | Administração Geral Tributária (Angolan Customs Authority) |
| ANTT | Agência Nacional de Transportes Terrestres (National Land Transport Agency) |
| ARCCLA | Autoridade Reguladora da Concorrência (Competition Regulatory Authority) |
| ASYCUDA | Automated System for Customs Data (UN system for customs automation) |
| CPE | Centro de Processamento Electrónico (Electronic Processing Center) |
| CUSDEC | Customs Declaration Message (UN/EDIFACT) |
| CUSCAR | Cargo Report Message (UN/EDIFACT) |
| DMZ | Demilitarized Zone |
| EDI | Electronic Data Interchange |
| ESB | Enterprise Service Bus |
| GCC | Gulf Cooperation Council |
| HS Code | Harmonized System Code for trade goods classification |
| IAM | Identity and Access Management |
| IMDG | International Maritime Dangerous Goods Code |
| JUL | Janela Única Logística (Logistics Single Window) |
| JUP | Janela Única Portuária (Port Single Window) |
| LPCO | Licenses, Permits, Certificates, and Other requirements |
| MINDCOM | Ministério do Comércio (Ministry of Commerce) |
| OGA | Other Government Agency |
| PICE | Portal de Importação e Exportação (Import/Export Portal) |
| RBAC | Role-Based Access Control |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SIGT | Sistema Integrado de Gestão de Transportes (Integrated Transport Management System) |
| SICOEX | Sistema de Comércio Exterior (Foreign Trade System) |
| SINTECE | Sistema Integrado do Comércio Exterior (Integrated Foreign Trade System) |
| SLA | Service Level Agreement |
| SSO | Single Sign-On |
| TOS | Terminal Operating System |
| UAT | User Acceptance Testing |
| UN/LOCODE | United Nations Code for Trade and Transport Locations |
| WCO | World Customs Organization |
| WCAG | Web Content Accessibility Guidelines |

### B. Acronyms

| Acronym | Full Form |
|---------|-----------|
| API | Application Programming Interface |
| BPM | Business Process Management |
| CA | Certificate Authority |
| CDN | Content Delivery Network |
| CI/CD | Continuous Integration/Continuous Deployment |
| CPU | Central Processing Unit |
| CSRF | Cross-Site Request Forgery |
| HA | High Availability |
| HLD | High Level Design |
| HTTPS | Hypertext Transfer Protocol Secure |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| K8s | Kubernetes |
| LDAP | Lightweight Directory Access Protocol |
| NAS | Network Attached Storage |
| OAuth | Open Authorization |
| OTP | One-Time Password |
| RAM | Random Access Memory |
| REST | Representational State Transfer |
| SAN | Storage Area Network |
| SAML | Security Assertion Markup Language |
| SMTP | Simple Mail Transfer Protocol |
| SOAP | Simple Object Access Protocol |
| SQL | Structured Query Language |
| SSD | Solid State Drive |
| TLS | Transport Layer Security |
| UML | Unified Modeling Language |
| VPN | Virtual Private Network |
| WAF | Web Application Firewall |
| WSDL | Web Services Description Language |
| XML | Extensible Markup Language |
| XSS | Cross-Site Scripting |

### C. Reference Documents

1. WCO Data Model Version 3.10 Specification
2. UN/EDIFACT Message Directory
3. ISO 3166 Country Codes
4. ISO 4217 Currency Codes
5. UN/LOCODE Location Codes
6. HS 2017 and HS 2022 Nomenclature
7. IMDG Code (International Maritime Dangerous Goods Code)
8. GCC Common Customs Law
9. JUL-SINTECE Integration Control Document
10. JUL-AGT Integration Control Document
11. JUL Solution Architecture Document
12. JUL User Management Architecture Document

### D. Diagram References

All diagrams are provided as separate Mermaid files:

1. [01_System_Context_Diagram.mermaid](#) - System context and external interfaces
2. [02_High_Level_Architecture.mermaid](#) - Overall system architecture
3. [03_Deployment_Architecture.mermaid](#) - Deployment topology
4. [04_Kubernetes_Architecture.mermaid](#) - Kubernetes cluster architecture
5. [05_Network_Architecture.mermaid](#) - Network zones and connectivity
6. [06_Layered_Architecture.mermaid](#) - Application layer structure
7. [07_API_Gateway_Architecture.mermaid](#) - API Gateway design
8. [08_Microservices_Architecture.mermaid](#) - Microservices overview
9. [09_Declaration_State_Machine.mermaid](#) - Declaration lifecycle
10. [10_Integration_Services_Architecture.mermaid](#) - Integration layer
11. [11_IAM_Architecture.mermaid](#) - Identity and Access Management
12. [12_Business_Logic_Architecture.mermaid](#) - Business domain model
13. [13_Import_Declaration_Process.mermaid](#) - Import process flow
14. [14_Integration_Layer_Architecture.mermaid](#) - Integration patterns
15. [15_Data_Flow_Diagram.mermaid](#) - Data flow between systems
16. [16_Data_Access_Layer.mermaid](#) - Database access architecture
17. [17_Performance_Architecture.mermaid](#) - Performance optimization
18. [18_Security_Architecture.mermaid](#) - Security layers
19. [19_Authentication_Flow.mermaid](#) - Authentication sequence
20. [20_Scalability_Architecture.mermaid](#) - Scalability strategy
21. [21_Data_Migration_Strategy.mermaid](#) - Migration approach
22. [22_Reporting_Architecture.mermaid](#) - Reporting infrastructure
23. [23_CICD_Pipeline.mermaid](#) - CI/CD workflow
24. [24_Backup_Recovery_Architecture.mermaid](#) - Backup and DR
25. [25_WCO_Data_Model_ER.mermaid](#) - WCO data model entities

---

## DOCUMENT APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| System Architect | | | |
| Technical Lead | | | |
| Project Manager | | | |
| Business Owner | | | |
| IT Manager | | | |

---

**END OF DOCUMENT**
