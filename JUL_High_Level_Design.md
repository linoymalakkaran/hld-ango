# HIGH LEVEL DESIGN DOCUMENT
## JUL (Janela Única Logística) - Angola National Logistics Single Window

**Document Version:** 2.0  
**Date:** December 2025  
**Status:** Production Ready

---

## DOCUMENT CONTROL

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 2.0 | December 2025 | System Architect | ICRMS Format - Production Ready |

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Application Architecture](#2-application-architecture)
3. [User Interfaces](#3-user-interfaces)
4. [Infrastructure Architecture](#4-infrastructure-architecture)
5. [Data Architecture](#5-data-architecture)
6. [Integration and APIs](#6-integration-and-apis)
7. [Use Cases](#7-use-cases)
8. [Compliance and Regulations](#8-compliance-and-regulations)

---

# 1. Introduction

## 1.1 Purpose of the Document

This High Level Design (HLD) document provides a comprehensive architectural blueprint for the JUL (Janela Única Logística) - Angola's National Logistics Single Window System. The document follows the ICRMS format structure and outlines the technical architecture, design decisions, and implementation approach for a modern, scalable trade facilitation platform.

The JUL system serves as a central hub for customs clearance and regulatory compliance, integrating multiple government agencies and private sector stakeholders to streamline trade processes, reduce clearance times, and enhance transparency in logistics operations.

**Key Objectives:**
- Provide single-point submission for trade-related documents
- Enable real-time tracking of shipments and cargo
- Facilitate seamless integration with customs and regulatory agencies
- Ensure compliance with World Customs Organization (WCO) standards
- Support concurrent users up to 10,000 with 99.9% system availability
- Process transactions with response time < 3 seconds (95th percentile)

## 1.2 Overview of the System

The JUL system is a comprehensive trade facilitation platform built on modern microservices architecture, deployed on-premises using Kubernetes orchestration. The system integrates with three primary external systems: ASYCUDA (Angola Customs Authority - AGT), SINTECE (Angola Single Window), and multiple Other Government Agencies (OGAs).

**System Context:**  
**Diagram Reference:** [diagrams/01_System_Context_Diagram.mermaid](diagrams/01_System_Context_Diagram.mermaid)

**Primary Stakeholders:**
- **Traders** (Importers/Exporters): Submit declarations, track shipments, obtain clearances
- **Customs Brokers**: Process customs declarations on behalf of traders
- **Freight Forwarders**: Manage cargo logistics and documentation
- **Customs Officers** (AGT): Process declarations, conduct examinations, issue clearances
- **Government Officials** (OGAs): Issue licenses, permits, and regulatory approvals

**Core Capabilities:**
- Company registration and onboarding with verification workflows
- Digital license and permit application processing (CNCA certificates)
- Customs broker/agent nomination and authorization management  
- Customs declaration (DU - Declaração Única) submission and processing
- Document management with secure storage and validation
- Master data synchronization from Angola government systems
- Multi-language support (Portuguese, English)
- Comprehensive audit trail and compliance reporting

**Technology Foundation:**
- **Frontend**: Angular 17+ with Module Federation micro-frontend architecture
- **Backend**: ASP.NET Core 8.0 microservices (11 services total)
- **Authentication**: Keycloak 23+ with OAuth 2.0/OpenID Connect/SAML 2.0
- **Database**: PostgreSQL 15+ with database-per-microservice pattern
- **Document Storage**: MinIO S3-compatible object storage
- **Message Queue**: RabbitMQ 3.12+ for asynchronous processing
- **Deployment**: On-premises Kubernetes cluster with Docker containers

---

# 2. Application Architecture

## 2.1 Architecture Overview

The JUL system employs a microservices architecture consisting of 11 specialized services, grouped into three categories: Core Business Services, Integration Services, and Cross-Cutting Services. This architecture provides scalability, maintainability, and independent deployability while ensuring high availability and performance.

**High-Level Architecture:**  
**Diagram Reference:** [diagrams/02_High_Level_Architecture.mermaid](diagrams/02_High_Level_Architecture.mermaid)

**Architecture Layers:**
1. **Presentation Layer**: Angular micro-frontends with Module Federation
2. **API Gateway Layer**: Kong API Gateway for unified API management
3. **Application Layer**: 11 microservices with business logic
4. **Data Layer**: PostgreSQL databases, Redis cache, MinIO storage, RabbitMQ messaging
5. **Security Layer**: Keycloak authentication and authorization

## 2.2 High-Level Application Architecture

The application architecture follows Domain-Driven Design (DDD) principles with clear bounded contexts for each microservice. Each service owns its data and communicates through well-defined APIs and asynchronous messaging.

**Service Communication Patterns:**
- **Synchronous**: REST APIs for real-time operations
- **Asynchronous**: RabbitMQ messaging for event-driven processing
- **External Integration**: SOAP/XML for ASYCUDA, REST/JSON for SINTECE and OGAs

**Data Management Strategy:**
- Database-per-microservice pattern
- Event sourcing for audit requirements
- CQRS (Command Query Responsibility Segregation) for complex read scenarios
- Master data distribution through nightly batch synchronization

## 2.3 Application Components (Microservices)

**Microservices Architecture:**  
**Diagram Reference:** [diagrams/06_Microservices_Architecture.mermaid](diagrams/06_Microservices_Architecture.mermaid)

### Core Business Services (6 Services)

#### 1. Company Management Service (Port 8081)
**Purpose**: Handles company registration, profile management, and verification workflows
- Company registration and onboarding
- Company profile management and updates
- User-company relationship management
- Integration with Keycloak for user provisioning
- Company verification and approval workflows
- **Database**: company_db (PostgreSQL)

#### 2. License & Permits Service (Port 8082)
**Purpose**: Manages license applications and permit processing, including CNCA certificates
- License application management (CNCA - Certificado Nacional de Capacidade Aduaneira)
- Permit request processing and approval workflows
- Integration with SINTECE for license verification
- License renewal and compliance tracking
- Multi-agency permit coordination
- **Database**: license_db (PostgreSQL)

#### 3. Agent Nomination Service (Port 8083)
**Purpose**: Manages customs broker/agent nominations and authorizations
- Customs broker/agent nomination processing
- Agent authorization and delegation management
- Power of attorney (procuração) management
- Agent-company relationship tracking
- Authorization validity monitoring
- **Database**: agent_db (PostgreSQL)

#### 4. Declaration Management Service (Port 8084)
**Purpose**: Core customs declaration processing with integrated payment functionality
- DU (Declaração Única) creation, validation, and submission
- Declaration lifecycle management and state transitions
- Integration with ASYCUDA for customs processing
- **Integrated payment processing** (consolidated from separate Payment Service)
- **Integrated tracking functionality** (consolidated from Track & Trace Service)
- Workflow management via Camunda integration
- **Database**: declaration_db (PostgreSQL)

#### 5. Document Management Service (Port 8085)
**Purpose**: Secure document storage and management with MinIO integration
- Document upload, storage, and retrieval
- Document validation and format verification
- **MinIO integration** for secure object storage
- Document metadata management in PostgreSQL
- Support for PDF, images, XML, JSON, and Microsoft Office formats
- Document lifecycle and retention management
- **Database**: document_metadata_db (PostgreSQL)
- **Storage**: MinIO object storage cluster

#### 6. Master Data Management Service (Port 8086)
**Purpose**: Centralized reference data synchronization and distribution
- **Nightly batch synchronization** from Angola government systems
- HS Code management (WCO HS2017/HS2022 classification)
- Port code management (UN/LOCODE standards)
- Country codes (ISO 3166), Currency codes (ISO 4217)
- Unit of measure codes and IMDG dangerous goods codes
- Master data distribution to all microservices
- **Database**: masterdata_db (PostgreSQL)

### Integration Services (3 Services)

#### 7. ASYCUDA Integration Service (Port 9081)
**Purpose**: Integration with Angola Customs Authority (AGT) ASYCUDA system
- SOAP/XML message handling for CUSDEC (customs declaration) and CUSRES (customs response)
- Declaration submission and status tracking with ASYCUDA
- Duty calculation and assessment result processing
- Clearance certificate retrieval and management
- **Protocol**: SOAP/XML - Synchronous communication
- **Reference**: JUL-AGT Integration Control Document
- **Integration Flow**: [diagrams/10_ASYCUDA_Integration_Flow.mermaid](diagrams/10_ASYCUDA_Integration_Flow.mermaid)

#### 8. SINTECE Integration Service (Port 9082)
**Purpose**: Integration with Angola SINTECE Single Window system
- REST/JSON API integration for license and permit verification
- Certificate validation and authenticity checking
- Single window data exchange and synchronization
- Regulatory compliance status verification
- **Protocol**: REST/JSON - Synchronous communication
- **Reference**: JUL-SINTECE Integration Control Document
- **Integration Flow**: [diagrams/11_SINTECE_Integration_Flow.mermaid](diagrams/11_SINTECE_Integration_Flow.mermaid)

#### 9. OGA Integration Service (Port 9083)
**Purpose**: Integration with multiple Other Government Agencies
- REST/JSON API integration with health, agriculture, standards agencies
- Multi-agency permit applications and approval tracking
- Regulatory certificate requests and status monitoring
- **Protocol**: REST/JSON - Asynchronous via message queue
- Agency coordination for LPCO (License, Permit, Certificate, Others) requirements

### Cross-Cutting Services (5 Services)

#### 10. IAM Service - Keycloak (Port 8080)
**Purpose**: Comprehensive identity and access management
- **Keycloak 23+ implementation** for authentication and authorization
- OAuth 2.0, OpenID Connect, and SAML 2.0 support
- **Multi-Factor Authentication (MFA)** mandatory for customs officers
- **Role-Based Access Control (RBAC)** with fine-grained permissions
- Single Sign-On (SSO) across all applications
- Company-user relationship management
- **Database**: keycloak_db (PostgreSQL)
- **Architecture**: [diagrams/12_IAM_Keycloak_Architecture.mermaid](diagrams/12_IAM_Keycloak_Architecture.mermaid)

#### 11. Notification Service (Port 8089)
**Purpose**: Multi-channel notification and alerting system
- Email notifications for status updates and alerts
- SMS notifications for critical events
- In-app notifications and real-time alerts
- Push notifications for mobile applications
- Notification templates and personalization
- **Database**: notification_db (PostgreSQL)

#### 12. Workflow Service - Camunda (Port 8090)
**Purpose**: Business process management and orchestration
- **Camunda 8 BPM** for workflow orchestration
- Declaration approval and processing workflows
- License application approval chains
- Task management and SLA monitoring
- Process analytics and optimization
- **Database**: camunda_db (PostgreSQL)

#### 13. Audit & Logging Service (Port 8091)
**Purpose**: Comprehensive audit trail and compliance logging
- Complete audit trail for all transactions and user activities
- User activity logging with detailed event tracking
- System event logging and error tracking
- Compliance reporting and regulatory audit support
- Data retention management (7 years minimum)
- **Database**: audit_db (PostgreSQL)

#### 14. Reporting Service (Port 8092)
**Purpose**: Operational and compliance reporting
- Operational reports for trade statistics and performance metrics
- Statistical reports for government and business intelligence
- Compliance reports for regulatory requirements
- Dashboard data aggregation and visualization
- Custom report generation and scheduling
- **Database**: reporting_db (PostgreSQL)

## 2.4 Technology Stack

### Frontend Technologies
- **Angular 17+** with TypeScript for web applications
- **Module Federation** for micro-frontend architecture
- **Angular Material UI** for consistent user interface components
- **Responsive Design** supporting web and mobile web access
- **PWA (Progressive Web App)** capabilities for offline functionality

### Backend Technologies
- **ASP.NET Core 8.0** with C# for all microservices
- **RESTful APIs** for service communication
- **gRPC** for high-performance inter-service communication (optional)
- **Entity Framework Core** for database access and ORM

### Authentication & Authorization
- **Keycloak 23+** for comprehensive identity management
- **OAuth 2.0 / OpenID Connect** for secure API access
- **SAML 2.0** for enterprise single sign-on
- **Multi-Factor Authentication (MFA)** with TOTP/SMS support

### Databases & Storage
- **PostgreSQL 15+** as primary relational database (database-per-service)
- **MinIO** for S3-compatible object storage (documents and attachments)
- **Redis 7+** for caching and session management
- **RabbitMQ 3.12+** for asynchronous messaging and event processing

### API Management & Integration
- **Kong API Gateway** for unified API management, security, and routing
- **Apache Kafka 3.6** (alternative to RabbitMQ) for high-throughput messaging

### Workflow & BPM
- **Camunda 8** for business process management and orchestration

### Deployment & Infrastructure
- **Kubernetes** on-premises cluster for container orchestration
- **Docker** containers for all services and applications
- **Helm Charts** for Kubernetes package management and deployment
- **NGINX Ingress Controller** for load balancing and SSL termination

### Monitoring & Logging
- **Prometheus + Grafana** for metrics collection and visualization
- **ELK Stack** (Elasticsearch, Logstash, Kibana) for centralized logging
- **Jaeger** for distributed tracing and performance monitoring

## 2.5 Example Workflow

**Declaration Processing Workflow:**  
**Diagram Reference:** [diagrams/07_Declaration_Lifecycle_State_Machine.mermaid](diagrams/07_Declaration_Lifecycle_State_Machine.mermaid)

### Sample DU (Declaração Única) Processing Flow:

1. **Declaration Creation**: Trader creates customs declaration via Angular web portal
2. **Document Validation**: System validates declaration data and required documents
3. **Document Storage**: Documents uploaded to MinIO with metadata in PostgreSQL
4. **Declaration Submission**: Declaration submitted to Declaration Management Service
5. **ASYCUDA Integration**: Declaration forwarded to AGT ASYCUDA via SOAP/XML CUSDEC message
6. **Customs Assessment**: ASYCUDA processes declaration and returns CUSRES with duty calculation
7. **Payment Processing**: System generates invoice and processes payment (integrated in Declaration Service)
8. **Clearance Certificate**: Upon payment confirmation, clearance certificate is issued
9. **Notification**: Trader notified via email/SMS of clearance completion
10. **Audit Trail**: Complete transaction logged for compliance and audit purposes

**Performance Targets:**
- **Response Time**: < 3 seconds (95th percentile)
- **Throughput**: 100 declarations per second
- **Availability**: 99.9% uptime
- **Concurrent Users**: 10,000 simultaneous users

---

# 3. User Interfaces

## 3.1 English User Interface

The JUL system provides a comprehensive web-based user interface built with Angular 17+ and Module Federation architecture, supporting responsive design for both desktop and mobile web access.

### Web Portal Features

**Main Dashboard:**
- Personalized dashboard with role-based information display
- Real-time status updates for declarations, licenses, and permits
- Quick action buttons for common tasks (submit declaration, check status)
- Notification center with alerts and system announcements
- Performance metrics and analytics (for authorized users)

**Company Management Interface:**
- Company registration wizard with document upload
- Company profile management with verification status
- User invitation and role assignment interface
- Company document library with version control

**Declaration Management Interface:**
- Declaration creation wizard with step-by-step guidance
- Document attachment interface with drag-and-drop functionality
- Declaration status tracking with timeline visualization
- Amendment and cancellation workflows
- Payment integration with multiple payment methods

**License & Permits Interface:**
- License application forms for different permit types (CNCA, etc.)
- OGA permit coordination dashboard
- License renewal notifications and processing
- Compliance status tracking and reporting

**Agent Nomination Interface:**
- Agent search and selection interface
- Power of attorney document management
- Authorization tracking and renewal alerts
- Agent performance and activity reporting

**Document Management Interface:**
- Secure document upload with format validation
- Document viewer with annotation capabilities
- Document sharing and collaboration features
- Advanced search with metadata filtering
- Document retention and archival management

**Reporting Interface:**
- Pre-built report templates for common scenarios
- Custom report builder with drag-and-drop interface
- Data visualization with charts and graphs
- Export capabilities (PDF, Excel, CSV)
- Scheduled report delivery via email

### Mobile Web Experience

**Responsive Design Features:**
- Touch-optimized interface with gesture support
- Simplified navigation for mobile screens
- Offline capability for essential functions
- Push notifications for status updates
- Camera integration for document capture

**Mobile-Specific Functionalities:**
- Quick status check for declarations and shipments
- Mobile-optimized document upload
- GPS integration for location-based services
- Barcode/QR code scanning for tracking
- Emergency contact and support access

### Accessibility Features

**WCAG 2.1 AA Compliance:**
- Screen reader compatibility
- Keyboard navigation support
- High contrast mode
- Adjustable font sizes
- Alternative text for images and icons

## 3.2 Portuguese User Interface

The primary user interface is designed for Portuguese-speaking users in Angola, with full localization and cultural adaptation.

### Localization Features

**Language Support:**
- **Portuguese (Primary)**: Complete interface translation with Angolan Portuguese conventions
- **English (Secondary)**: Full English interface for international users
- Dynamic language switching without session loss
- Localized date, time, and number formats
- Currency display in Angolan Kwanza (AOA)

**Cultural Adaptation:**
- Angola-specific terminology and legal references
- Local business process workflows
- Integration with Angolan government systems terminology
- Culturally appropriate color schemes and imagery
- Local contact information and support channels

### Portuguese Interface Components

**Navigation Elements:**
- "Painel Principal" (Main Dashboard)
- "Declarações" (Declarations)
- "Licenças e Autorizações" (Licenses and Permits)
- "Documentos" (Documents)
- "Relatórios" (Reports)
- "Configurações" (Settings)

**Form Labels and Instructions:**
- Complete Portuguese translation of all form fields
- Context-sensitive help in Portuguese
- Validation messages in Portuguese
- Angola-specific field formats (NIB, NIF, etc.)
- Local address and contact formats

**User Roles in Portuguese:**
- "Comerciante" (Trader)
- "Despachante" (Customs Broker)
- "Agente de Carga" (Freight Forwarder)
- "Funcionário Aduaneiro" (Customs Officer)
- "Administrador do Sistema" (System Administrator)

### User Experience Optimization

**Performance Optimizations:**
- Lazy loading of interface components
- Optimized bundle sizes for faster loading
- Progressive enhancement for slower connections
- Cached static resources for repeat visits
- Compressed image assets and icons

**User Assistance:**
- Contextual help system in Portuguese
- Interactive tutorials for new users
- Comprehensive FAQ section
- Live chat support during business hours
- Video tutorials for complex processes

---

# 4. Infrastructure Architecture

## 4.1 Server Architecture

The JUL system is deployed on a robust on-premises infrastructure designed for high availability, scalability, and performance. The architecture supports three distinct environments with graduated resource allocation.

**Deployment Architecture:**  
**Diagram Reference:** [diagrams/03_Deployment_Architecture.mermaid](diagrams/03_Deployment_Architecture.mermaid)

### 4.1.1 Scalability and High Availability

**Kubernetes Cluster Architecture:**  
**Diagram Reference:** [diagrams/04_Kubernetes_Architecture.mermaid](diagrams/04_Kubernetes_Architecture.mermaid)

#### Production Environment Specifications
- **Kubernetes Worker Nodes**: 10+ nodes for high availability
- **Node Specifications**: 32 vCPU, 128 GB RAM per node
- **Control Plane**: 3 master nodes for cluster management redundancy
- **Ingress Controller**: NGINX with SSL termination and load balancing
- **Namespaces**: jul-production, jul-monitoring, jul-security, jul-backup

#### Staging Environment Specifications  
- **Kubernetes Worker Nodes**: 5 nodes for production-like testing
- **Node Specifications**: 16 vCPU, 64 GB RAM per node
- **Control Plane**: 3 master nodes
- **Namespaces**: jul-staging, jul-integration, jul-testing

#### Development Environment Specifications
- **Kubernetes Worker Nodes**: 3 nodes for development and testing
- **Node Specifications**: 8 vCPU, 32 GB RAM per node
- **Control Plane**: Single master node (non-HA acceptable for dev)
- **Namespaces**: jul-development, jul-feature, jul-sandbox

#### High Availability Features
- **Pod Replication**: Minimum 2 replicas per service in production
- **Node Affinity Rules**: Spread replicas across different nodes
- **Resource Limits**: CPU and memory limits to prevent resource contention
- **Health Checks**: Liveness and readiness probes for all services
- **Auto-scaling**: Horizontal Pod Autoscaler (HPA) based on CPU/memory metrics

### 4.1.2 Database Options

#### PostgreSQL High Availability Configuration
- **Production**: Primary + 2 read replicas with automatic failover
- **Staging**: Primary + 1 replica for testing failover scenarios  
- **Development**: Single instance with regular backups

#### Database-per-Microservice Pattern
Each microservice maintains its own PostgreSQL database:
- **company_db**: Company and user management data
- **license_db**: License and permit information
- **agent_db**: Agent nomination and authorization data
- **declaration_db**: Declaration and payment transaction data
- **document_metadata_db**: Document metadata and indexing
- **masterdata_db**: Reference data and HS codes
- **keycloak_db**: Authentication and authorization data
- **camunda_db**: Workflow and process data
- **notification_db**: Notification templates and logs
- **audit_db**: Comprehensive audit trail
- **reporting_db**: Aggregated reporting data

#### MinIO Object Storage Cluster
- **Production**: Distributed deployment with 6+ nodes for redundancy
- **Data Protection**: Erasure coding with configurable redundancy levels
- **Backup Strategy**: Cross-site replication for disaster recovery
- **Access Control**: Integration with Keycloak for authentication
- **Encryption**: Server-side encryption for data at rest

## 4.2 Network & Security

**Network Architecture:**  
**Diagram Reference:** [diagrams/05_Network_Architecture.mermaid](diagrams/05_Network_Architecture.mermaid)

### Network Zones and Segmentation

#### DMZ Zone (172.16.1.0/24)
- **Load Balancer**: HAProxy or NGINX for traffic distribution
- **Web Application Firewall (WAF)**: ModSecurity for application-layer protection
- **Firewall**: iptables/pfSense for network-level security
- **DDoS Protection**: Rate limiting and traffic shaping
- **SSL Termination**: TLS 1.3 encryption with modern cipher suites

#### Application Zone (10.10.0.0/16)
- **Kubernetes Cluster**: All application services and pods
- **Kong API Gateway**: Centralized API management and security
- **Internal Load Balancing**: Service mesh for inter-service communication
- **Container Network Interface (CNI)**: Calico or Flannel for pod networking

#### Data Zone (10.20.0.0/16)
- **PostgreSQL Clusters**: Database servers with replication
- **MinIO Object Storage**: Distributed storage cluster
- **Redis Cluster**: Caching and session storage
- **RabbitMQ Cluster**: Message queuing and event processing

#### Management Zone (10.30.0.0/16)
- **Bastion Host**: Secure administrative access point
- **Monitoring Stack**: Prometheus, Grafana, ELK Stack
- **Backup Services**: Database and file system backup systems
- **Configuration Management**: Ansible or similar for infrastructure automation

### Security Architecture
**Security Architecture:**  
**Diagram Reference:** [diagrams/15_Security_Architecture.mermaid](diagrams/15_Security_Architecture.mermaid)

#### Multi-Layer Security Model

**Perimeter Security:**
- **Firewall Rules**: Strict ingress/egress traffic controls
- **Intrusion Detection System (IDS)**: Real-time threat monitoring
- **VPN Access**: Secure remote access for administrators
- **Network Segmentation**: VLAN isolation between zones

**Application Security:**
- **API Gateway Security**: OAuth 2.0, rate limiting, request validation
- **Service Mesh Security**: mTLS between microservices
- **Container Security**: Image scanning, runtime protection
- **Secrets Management**: Kubernetes secrets with encryption at rest

**Data Security:**
- **Encryption in Transit**: TLS 1.3 for all communications
- **Encryption at Rest**: AES-256 encryption for databases and files
- **Field-Level Encryption**: Additional encryption for sensitive data
- **Key Management**: Hardware Security Module (HSM) or software-based KMS

## 4.3 Virtual Resources

### 4.3.1 Dev Environment
**Purpose**: Development and initial testing of new features

**Infrastructure Specifications:**
- **Total Nodes**: 3 Kubernetes worker nodes + 1 master
- **Computing Resources**: 24 vCPU total, 96 GB RAM total
- **Storage**: 2 TB NVMe SSD for fast development iterations
- **Database**: Single PostgreSQL instance per service
- **MinIO**: Single-node deployment with local storage
- **Redis**: Single instance without clustering

**Development Tools:**
- **GitLab CE**: Source code management and CI/CD pipelines
- **Harbor Registry**: Private container image registry
- **SonarQube**: Code quality analysis and security scanning
- **Development Certificates**: Self-signed certificates for HTTPS testing

### 4.3.2 Staging Environment  
**Purpose**: Production-like testing and user acceptance testing

**Infrastructure Specifications:**
- **Total Nodes**: 5 Kubernetes worker nodes + 3 masters
- **Computing Resources**: 80 vCPU total, 320 GB RAM total  
- **Storage**: 5 TB enterprise SSD with replication
- **Database**: PostgreSQL with primary + 1 replica per service
- **MinIO**: 3-node distributed deployment
- **Redis**: 3-node cluster with sentinel

**Testing Capabilities:**
- **Load Testing**: Performance testing with realistic data volumes
- **Integration Testing**: Full external system integration validation
- **Security Testing**: Penetration testing and vulnerability assessment
- **User Acceptance Testing**: Business user validation environment

### 4.3.3 Production Environment
**Purpose**: Live system serving actual business operations

**Infrastructure Specifications:**
- **Total Nodes**: 10+ Kubernetes worker nodes + 3 masters
- **Computing Resources**: 320+ vCPU total, 1.28+ TB RAM total
- **Storage**: 20+ TB enterprise NVMe with redundancy
- **Database**: PostgreSQL HA with primary + 2 replicas per service
- **MinIO**: 6+ node distributed deployment with erasure coding
- **Redis**: 6-node cluster with automatic failover

**Production Features:**
- **24/7 Monitoring**: Comprehensive monitoring with alerting
- **Automated Backups**: Multiple backup strategies with offsite storage
- **Disaster Recovery**: Full DR site with RTO < 4 hours, RPO < 1 hour
- **Performance Monitoring**: APM tools for application performance tracking
- **Compliance Logging**: Audit-grade logging for regulatory requirements

**Service Level Agreements:**
- **Availability**: 99.9% uptime (8.76 hours downtime/year maximum)
- **Response Time**: < 3 seconds for 95th percentile of API calls
- **Throughput**: 100 transactions per second sustained load
- **Data Retention**: 7 years for compliance requirements
- **Backup Recovery**: 15-minute RTO for database recovery

---

# 5. Data Architecture

## 5.1 Data Model Conforming to the WCO

The JUL system implements a comprehensive data model that fully conforms to the **World Customs Organization (WCO) Data Model Version 3.10**, ensuring international compatibility and standardization for customs and trade facilitation processes.

**WCO Data Model Implementation:**  
**Diagram Reference:** [diagrams/18_WCO_Data_Model_ER.mermaid](diagrams/18_WCO_Data_Model_ER.mermaid)

### Core WCO Entities Implementation

#### Declaration Entity
Implements WCO Declaration structure for customs processing:
```sql
-- Core Declaration Structure (WCO Compliant)
CREATE TABLE declarations (
    declaration_id UUID PRIMARY KEY,
    functional_reference_id VARCHAR(35) NOT NULL, -- WCO requirement
    declaration_type_code VARCHAR(3), -- Import/Export/Transit
    declaration_office_id VARCHAR(8), -- Customs office code
    goods_location_code VARCHAR(17), -- UN/LOCODE format
    declarant_party_id UUID REFERENCES parties(party_id),
    representative_party_id UUID REFERENCES parties(party_id),
    border_transport_means JSONB, -- WCO transport details
    created_datetime TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    submission_datetime TIMESTAMP WITH TIME ZONE,
    acceptance_datetime TIMESTAMP WITH TIME ZONE,
    wco_data_model_version VARCHAR(10) DEFAULT '3.10'
);
```

#### Goods Item Entity  
WCO-compliant goods item structure with HS classification:
```sql
CREATE TABLE goods_items (
    goods_item_id UUID PRIMARY KEY,
    declaration_id UUID REFERENCES declarations(declaration_id),
    sequence_numeric INTEGER NOT NULL,
    commodity_code VARCHAR(22), -- HS 2017/2022 codes
    commodity_code_list_id VARCHAR(3) DEFAULT 'HS', -- WCO standard
    customs_value_amount DECIMAL(18,2),
    customs_value_currency_id VARCHAR(3), -- ISO 4217
    statistical_value_amount DECIMAL(18,2),
    net_weight_measure DECIMAL(16,6),
    gross_weight_measure DECIMAL(16,6),
    supplementary_unit_quantity DECIMAL(16,6),
    origin_country_code VARCHAR(2), -- ISO 3166-1 alpha-2
    export_country_code VARCHAR(2),
    destination_country_code VARCHAR(2)
);
```

#### Party Entity
Comprehensive party management following WCO Party model:
```sql  
CREATE TABLE parties (
    party_id UUID PRIMARY KEY,
    party_identification VARCHAR(35) NOT NULL,
    party_name VARCHAR(70) NOT NULL,
    party_type_code VARCHAR(3), -- WCO party types
    party_role_code VARCHAR(3), -- Declarant, Representative, etc.
    communication_id VARCHAR(512), -- Contact information
    address JSONB, -- WCO Address structure
    tax_id VARCHAR(20), -- NIF in Angola
    economic_operator_id VARCHAR(17), -- EORI equivalent
    authorization_id VARCHAR(35) -- Various authorizations
);
```

### WCO Data Standards Integration

#### HS Code Classification (HS 2017/2022)
- **Harmonized System Codes**: Complete HS 2017 and HS 2022 nomenclature
- **Tariff Integration**: Integrated tariff schedules with duty rates
- **Classification Rules**: Automated classification assistance based on WCO guidelines
- **Updates**: Regular synchronization with WCO updates and Angola-specific modifications

#### UN/EDIFACT Message Support
- **CUSDEC**: Customs Declaration message for ASYCUDA integration
- **CUSRES**: Customs Response message for processing results  
- **CUSCAR**: Customs Cargo Report for manifest processing
- **BANSTA**: Bank Statement message for payment confirmations
- **Message Validation**: Schema validation against UN/EDIFACT standards

#### ISO Standard Implementation
- **ISO 3166**: Country codes for origin, export, and destination countries
- **ISO 4217**: Currency codes for all monetary values
- **ISO 8601**: Date and time formats with timezone support
- **UN/LOCODE**: Location codes for ports, airports, and inland terminals

## 5.2 High Level Data Ecosystem

The data ecosystem supports the complete trade facilitation lifecycle with multiple data sources, processing layers, and integration points.

**Data Flow Architecture:**  
**Diagram Reference:** [diagrams/09_Data_Flow_Declaration_Process.mermaid](diagrams/09_Data_Flow_Declaration_Process.mermaid)

### Data Sources and Flows

#### Internal Data Sources
- **User Input**: Web portal and mobile applications
- **System Generated**: Workflow events, audit logs, notifications
- **Calculated Data**: Duty calculations, statistical summaries, performance metrics

#### External Data Sources  
- **ASYCUDA (AGT)**: Customs assessment results, clearance certificates
- **SINTECE**: License validations, permit verifications
- **OGA Systems**: Regulatory approvals, certificate issuances
- **Master Data Sources**: HS codes, exchange rates, regulatory updates

#### Data Processing Layers
1. **Ingestion Layer**: Real-time and batch data ingestion from multiple sources
2. **Validation Layer**: Data quality checks, business rule validation
3. **Transformation Layer**: Format conversion, enrichment, standardization
4. **Storage Layer**: Transactional databases, data warehouse, object storage
5. **Analytics Layer**: Reporting, dashboards, business intelligence

### Master Data Synchronization
**Master Data Sync:**  
**Diagram Reference:** [diagrams/14_Master_Data_Sync.mermaid](diagrams/14_Master_Data_Sync.mermaid)

#### Nightly Batch Synchronization Process
- **Schedule**: Daily at 02:00 AM WAT (West Africa Time)
- **Duration**: Maximum 2 hours processing window
- **Data Sources**: Angola Customs Authority, SINTECE, OGA systems
- **Distribution**: Push updates to all microservice databases
- **Validation**: Data integrity checks and conflict resolution
- **Rollback**: Automated rollback capability for failed synchronizations

## 5.3 Reference Data

### Primary Reference Data Sets

#### HS Code Management
- **HS 2017 Classification**: Complete 6-digit HS codes with Angola-specific extensions
- **HS 2022 Migration**: Transition support for updated classification
- **Tariff Schedules**: Import duty rates, VAT rates, excise duties
- **Seasonal Tariffs**: Time-based duty variations for agricultural products
- **Preferential Tariffs**: SADC, EU, and other trade agreement rates

#### Geographic and Administrative Codes
- **Country Codes**: ISO 3166-1 alpha-2 and alpha-3 codes
- **Currency Codes**: ISO 4217 with real-time exchange rates
- **Port Codes**: UN/LOCODE for all Angola ports and international locations
- **Customs Offices**: Angola customs office codes and operating hours
- **Administrative Divisions**: Angola provinces, municipalities, communes

#### Regulatory Reference Data
- **License Types**: CNCA, import/export permits, OGA-specific licenses
- **Document Types**: Required documents per commodity and country
- **Prohibited/Restricted Goods**: Dynamic lists per origin/destination
- **Quota Management**: Import/export quotas with real-time balances

## 5.4 Transactional Data

### Core Transaction Entities

#### Declaration Transactions
- **Declaration Lifecycle**: Complete audit trail from creation to clearance
- **State Transitions**: Timestamped state changes with user attribution
- **Amendment History**: Complete change history for modified declarations
- **Payment Transactions**: Integrated payment processing with bank reconciliation

#### Document Transactions
- **Document Storage**: MinIO object storage with PostgreSQL metadata
- **Version Control**: Document versioning with change tracking
- **Access Logs**: Complete audit trail of document access and modifications
- **Retention Management**: Automated archival and deletion based on retention policies

#### Integration Transactions
- **ASYCUDA Messages**: Complete CUSDEC/CUSRES message exchange logs
- **SINTECE Interactions**: License verification and certificate validation logs
- **OGA Communications**: Multi-agency interaction tracking and response management

### Document Management Architecture
**Document Management:**  
**Diagram Reference:** [diagrams/13_Document_Management_MinIO.mermaid](diagrams/13_Document_Management_MinIO.mermaid)

#### MinIO Object Storage Implementation
- **Bucket Structure**: Organized by document type, year, and access level
- **Metadata Storage**: Document metadata in PostgreSQL for searchability
- **Security**: Server-side encryption with Keycloak authentication
- **Backup**: Cross-site replication for disaster recovery
- **CDN Integration**: Content delivery optimization for large documents

## 5.5 Data Management

### Data Governance Framework

#### Data Quality Management
- **Validation Rules**: Business rule engine for data quality enforcement
- **Data Cleansing**: Automated correction of common data entry errors
- **Duplicate Detection**: Advanced algorithms for duplicate record identification
- **Data Profiling**: Regular analysis of data quality metrics

#### Data Security and Privacy
- **Encryption Standards**: AES-256 encryption for data at rest
- **Access Controls**: Role-based access with field-level permissions
- **Data Masking**: PII protection in non-production environments
- **Audit Logging**: Complete data access and modification audit trail

#### Backup and Recovery Strategy
- **Backup Frequency**: 
  - Transaction logs: Every 15 minutes
  - Database backups: Every 6 hours  
  - Full system backups: Daily
- **Retention Policy**: 
  - Active backups: 30 days
  - Archive backups: 7 years (compliance requirement)
- **Recovery Testing**: Monthly disaster recovery testing
- **Cross-site Replication**: Real-time replication to DR site

#### Performance Optimization
- **Database Indexing**: Optimized indexes for common query patterns
- **Query Optimization**: Regular query performance analysis and tuning
- **Caching Strategy**: Multi-level caching with Redis for frequently accessed data
- **Archival Strategy**: Automated data archival for improved performance

---

# 6. Integration and APIs

## 6.1 Integrations Overview

The JUL system integrates with three primary external systems to provide comprehensive trade facilitation services. All integrations are designed for high availability, error handling, and comprehensive audit logging.

**Integration Architecture:**  
**Diagram Reference:** [diagrams/08_Integration_Architecture.mermaid](diagrams/08_Integration_Architecture.mermaid)

### External Integration Summary

| System | Protocol | Pattern | Purpose | SLA |
|---------|----------|---------|---------|-----|
| ASYCUDA (AGT) | SOAP/XML | Synchronous | Customs declaration processing | < 30 seconds response |
| SINTECE | REST/JSON | Synchronous | License/permit verification | < 10 seconds response |
| OGAs | REST/JSON | Asynchronous | Regulatory approvals | < 24 hours processing |

### Integration Principles

#### Design Patterns
- **Circuit Breaker**: Prevent cascade failures with configurable thresholds
- **Retry Logic**: Exponential backoff for transient failures
- **Dead Letter Queue**: Failed message handling and investigation
- **Idempotency**: Safe retry operations for all integration calls
- **Timeout Management**: Configurable timeouts per integration endpoint

#### Error Handling Strategy
- **Graceful Degradation**: System continues operating when external systems are unavailable
- **Error Classification**: Systematic categorization of integration errors
- **Alerting**: Real-time notifications for critical integration failures
- **Fallback Mechanisms**: Alternative processing paths for essential operations

## 6.2 Application Integration Approach

### 6.2.1 Internal Integrations

#### Microservice Communication Patterns

**Service-to-Service Communication:**
- **Synchronous APIs**: REST APIs for real-time operations requiring immediate response
- **Asynchronous Messaging**: RabbitMQ for event-driven processing and loose coupling
- **Service Discovery**: Kubernetes DNS-based service discovery
- **Load Balancing**: Kubernetes service load balancing with session affinity

**API Gateway Integration (Kong):**
- **Unified API Entry Point**: Single entry point for all client applications
- **Authentication**: OAuth 2.0 token validation with Keycloak integration
- **Rate Limiting**: Configurable rate limits per client/API
- **Request/Response Transformation**: Protocol mediation and data transformation
- **Caching**: Response caching for frequently accessed data
- **Analytics**: API usage metrics and performance monitoring

#### Event-Driven Architecture

**Domain Events:**
- **Declaration Events**: Declaration submitted, validated, approved, rejected
- **Payment Events**: Payment initiated, completed, failed, refunded
- **Document Events**: Document uploaded, validated, approved, expired
- **License Events**: License applied, approved, renewed, revoked

**Event Publishing:**
- **Event Sourcing**: Complete event history for audit and replay capabilities
- **Event Store**: PostgreSQL-based event store with partitioning
- **Message Schema**: JSON schema validation for all events
- **Event Versioning**: Backward-compatible event schema evolution

### 6.2.2 External Integrations

#### 1. ASYCUDA (AGT) Integration

**Integration Details:**
- **System**: Angola Customs Authority (Administração Geral Tributária)
- **Protocol**: SOAP/XML over HTTPS
- **Authentication**: Certificate-based mutual authentication
- **Message Format**: UN/EDIFACT CUSDEC/CUSRES messages
- **Integration Control Document**: JUL-AGT Integration Control Document - Draft - V2

**ASYCUDA Integration Flow:**  
**Diagram Reference:** [diagrams/10_ASYCUDA_Integration_Flow.mermaid](diagrams/10_ASYCUDA_Integration_Flow.mermaid)

**Key Messages:**
- **CUSDEC (Customs Declaration)**: Submit declaration for customs processing
  - Declaration header with declarant and representative information
  - Goods items with HS codes, values, and quantities
  - Supporting document references and attachments
  - Transport and logistics information

- **CUSRES (Customs Response)**: Receive customs assessment and decisions
  - Assessment results with calculated duties and taxes
  - Inspection requirements and procedures
  - Payment instructions and deadlines
  - Clearance authorization or rejection reasons

**Integration Features:**
- **Real-time Processing**: Synchronous request/response for immediate feedback
- **Message Validation**: Schema validation against UN/EDIFACT standards
- **Error Handling**: Comprehensive error code mapping and user-friendly messages
- **Retry Logic**: Automated retry for transient network failures
- **Message Archival**: Complete message history for audit and troubleshooting

#### 2. SINTECE Integration

**Integration Details:**
- **System**: Angola Single Window for Trade (Sistema Nacional de Troca Electrónica de Dados)
- **Protocol**: REST/JSON over HTTPS
- **Authentication**: OAuth 2.0 with client credentials
- **Integration Control Document**: JUL-SINTECE Integration Control Document - Draft - v2

**SINTECE Integration Flow:**  
**Diagram Reference:** [diagrams/11_SINTECE_Integration_Flow.mermaid](diagrams/11_SINTECE_Integration_Flow.mermaid)

**Key Operations:**
- **License Verification**: Validate CNCA and other license authenticity
  - License number verification
  - Validity period confirmation
  - Scope and limitation checks
  - Renewal status verification

- **Certificate Validation**: Authenticate regulatory certificates
  - Certificate authenticity verification
  - Issuing authority validation
  - Expiration status checks
  - Revocation list verification

- **Permit Status Check**: Real-time permit status inquiries
  - Application status tracking
  - Approval workflow progress
  - Document requirement verification
  - Fee payment confirmation

**Integration Features:**
- **RESTful API**: Modern REST API with JSON payloads
- **Real-time Verification**: Immediate license and certificate validation
- **Bulk Operations**: Batch verification for multiple licenses
- **Status Webhooks**: Optional webhook notifications for status changes

#### 3. OGA (Other Government Agencies) Integration

**Integration Details:**
- **Agencies**: Multiple government agencies (health, agriculture, standards, commerce)
- **Protocol**: REST/JSON over HTTPS (standardized interface)
- **Authentication**: OAuth 2.0 or API key-based per agency
- **Pattern**: Asynchronous processing via message queue

**Supported Government Agencies:**
- **Ministry of Health**: Food and pharmaceutical import permits
- **Ministry of Agriculture**: Plant and animal import permits  
- **Angola Bureau of Standards**: Product conformity certificates
- **Ministry of Commerce**: Import/export quotas and restrictions
- **Ministry of Environment**: Environmental impact permits

**OGA Integration Features:**
- **Unified Interface**: Standardized API contract for all OGA integrations
- **Asynchronous Processing**: Non-blocking permit applications with status tracking
- **Multi-Agency Coordination**: Parallel processing of multiple permit requirements
- **Document Submission**: Secure document upload for permit applications
- **Status Notifications**: Real-time updates on permit application progress
- **SLA Tracking**: Service level agreement monitoring per agency

**Common OGA Operations:**
- **Permit Application**: Submit permit requests with required documentation
- **Status Inquiry**: Check application status and processing progress  
- **Document Submission**: Upload additional documents requested by agencies
- **Fee Payment**: Process permit fees through integrated payment system
- **Certificate Retrieval**: Download approved permits and certificates

#### Integration Security

**Security Standards:**
- **TLS 1.3**: All external communications encrypted with modern TLS
- **Certificate Authentication**: Mutual TLS for high-security integrations
- **API Rate Limiting**: Protection against abuse and DoS attacks
- **Request Signing**: Digital signatures for critical transactions
- **Audit Logging**: Complete integration audit trail for compliance

**Monitoring and Alerting:**
- **Health Checks**: Continuous monitoring of external system availability
- **Performance Metrics**: Response time and throughput monitoring
- **Error Rate Tracking**: Integration failure rate monitoring with alerting
- **Business Metrics**: Transaction success rates and processing volumes
- **SLA Monitoring**: Automatic SLA breach detection and notification

---

# 7. Use Cases

## 7.1 Core Use Cases

### UC-001: Company Registration and Onboarding

**Primary Actor**: New Trading Company  
**Scope**: Complete company registration process with verification

**Main Success Scenario:**
1. Company representative accesses JUL web portal
2. Completes company registration form with business details
3. Uploads required documentation (business license, tax certificate, etc.)
4. Submits application for review
5. System validates documents and business information
6. Government officials review and verify company credentials
7. System sends approval notification via email/SMS
8. Company receives login credentials and can begin operations

**Extensions:**
- **3a**: Document validation fails - system provides specific error messages
- **6a**: Additional documentation required - automated request sent to company
- **6b**: Application rejected - detailed rejection reasons provided

**Business Value**: Streamlined company onboarding reduces time from 15 days to 3 days

### UC-002: CNCA License Application

**Primary Actor**: Trading Company  
**Scope**: Application for Certificado Nacional de Capacidade Aduaneira (National Customs Capacity Certificate)

**Main Success Scenario:**
1. Registered company accesses license application portal
2. Selects CNCA license type and completes application form
3. Uploads required documentation (financial statements, staff qualifications)
4. Pays application fee through integrated payment system
5. System validates application completeness
6. Workflow routes application to appropriate government reviewers
7. Reviewers evaluate application against CNCA criteria
8. System generates digital CNCA certificate upon approval
9. Company notified and can download certificate immediately

**Business Value**: Reduces CNCA processing time from 30 days to 7 days

### UC-003: Customs Declaration (DU) Processing

**Primary Actor**: Customs Broker/Trader  
**Scope**: Complete import/export declaration submission and processing

**Main Success Scenario:**
1. User creates new customs declaration (DU) in the system
2. Enters cargo details with HS codes, values, and quantities
3. Uploads supporting documents (invoice, packing list, certificates)
4. System validates declaration against business rules
5. Declaration submitted to ASYCUDA via CUSDEC message
6. ASYCUDA processes declaration and calculates duties
7. System receives CUSRES with assessment results
8. User processes payment for calculated duties and fees
9. System confirms payment with banking integration
10. Clearance certificate generated and made available for download
11. Cargo release notification sent to all relevant parties

**Extensions:**
- **5a**: ASYCUDA system unavailable - declaration queued for later processing
- **6a**: Inspection required - system schedules inspection appointment
- **8a**: Payment fails - alternative payment methods offered

**Business Value**: Reduces declaration processing time from 3 days to 4 hours

### UC-004: Multi-Agency Permit Coordination

**Primary Actor**: Importer requiring multiple permits  
**Scope**: Coordinated application for permits from multiple government agencies

**Main Success Scenario:**
1. Importer initiates permit application for regulated goods
2. System identifies required permits based on HS code and origin country
3. Creates coordinated application for all required agencies (health, agriculture, standards)
4. Submits applications to relevant OGAs simultaneously
5. Tracks progress across all agencies with unified status dashboard
6. Sends notifications as individual permits are approved/rejected
7. Provides consolidated view when all permits are complete
8. Enables import declaration submission once all permits obtained

**Business Value**: Eliminates duplicate data entry and reduces permit processing time by 50%

### UC-005: Real-time Cargo Tracking

**Primary Actor**: Trader/Freight Forwarder  
**Scope**: End-to-end visibility of cargo movement and status

**Main Success Scenario:**
1. User searches for shipment using container number or declaration reference
2. System displays real-time cargo status and location
3. Shows key milestones: arrival, customs clearance, inspection, release
4. Provides estimated delivery timeline based on current status
5. Sends proactive notifications for status changes
6. Displays any delays or issues requiring attention
7. Enables document download (clearance certificate, delivery order)

**Business Value**: Improves supply chain visibility and reduces cargo dwell time

## 7.2 Additional Use Cases

### UC-006: Agent Nomination and Authorization

**Primary Actor**: Trading Company  
**Scope**: Appointment of customs broker with proper authorization

**Main Success Scenario:**
1. Company searches for qualified customs brokers in system
2. Reviews broker qualifications, ratings, and service areas
3. Initiates nomination request with power of attorney upload
4. System validates broker credentials and authorization status
5. Broker accepts nomination and confirms service agreement
6. System establishes authorized relationship with defined scope
7. Company can assign declarations to nominated broker
8. All broker actions performed with proper audit trail

### UC-007: Automated Duty Calculation

**Primary Actor**: Declaration Service (System)  
**Scope**: Accurate duty and tax calculation for imports

**Main Success Scenario:**
1. System receives validated declaration with HS codes and values
2. Retrieves current tariff rates from master data
3. Applies preferential rates based on origin country agreements
4. Calculates import duties, VAT, excise taxes, and fees
5. Applies any quota limitations or seasonal adjustments
6. Generates detailed duty calculation breakdown
7. Presents calculation to user for review and payment

### UC-008: Document Digitization and Management

**Primary Actor**: Document Management Service  
**Scope**: Secure upload, storage, and retrieval of trade documents

**Main Success Scenario:**
1. User uploads document through web interface or mobile app
2. System validates file format and size limitations
3. Extracts metadata and performs OCR for searchability
4. Stores document in MinIO with encryption
5. Creates searchable index in PostgreSQL database
6. Applies retention policies based on document type
7. Enables secure sharing with authorized parties

### UC-009: Compliance Reporting and Analytics

**Primary Actor**: Government Official/Supervisor  
**Scope**: Generate compliance and operational reports

**Main Success Scenario:**
1. Authorized user accesses reporting dashboard
2. Selects from pre-configured report templates or creates custom report
3. Defines parameters (date range, commodity codes, countries)
4. System aggregates data from multiple microservices
5. Generates report with visualizations and export options
6. Schedules recurring reports for regular distribution
7. Archives reports for historical reference and audit

### UC-010: System Monitoring and Health Checks

**Primary Actor**: System Administrator  
**Scope**: Proactive monitoring and maintenance of system health

**Main Success Scenario:**
1. Monitoring system continuously checks service health
2. Validates external system connectivity and response times
3. Monitors resource utilization and performance metrics
4. Detects anomalies and potential issues before user impact
5. Sends automated alerts to operations team
6. Triggers auto-scaling when resource thresholds exceeded
7. Provides real-time dashboard for system status overview

### UC-011: Master Data Synchronization

**Primary Actor**: Master Data Management Service  
**Scope**: Nightly synchronization of reference data from government sources

**Main Success Scenario:**
1. Automated job triggers at 2:00 AM daily
2. Connects to external government data sources
3. Downloads updated HS codes, tariffs, and regulatory data
4. Validates data integrity and consistency
5. Transforms data to internal format standards
6. Distributes updates to all microservice databases
7. Sends notification summary of changes to administrators
8. Archives previous versions for audit and rollback capability

### UC-012: Multi-Factor Authentication

**Primary Actor**: Customs Officer  
**Scope**: Secure login with enhanced authentication

**Main Success Scenario:**
1. User enters username and password at login screen
2. Keycloak validates credentials against user database
3. System determines MFA requirement based on user role
4. Sends SMS or authenticator app code to registered device
5. User enters MFA code within time limit
6. System validates code and grants session access
7. Establishes secure session with appropriate role permissions

**Business Value**: Enhanced security for sensitive customs operations while maintaining user experience

---

# 8. Compliance and Regulations

## 8.1 Regulatory Compliance Requirements

The JUL system must comply with multiple layers of regulatory requirements, from international standards to Angola-specific customs and trade regulations.

### Angola National Regulations

#### Customs Code of Angola
- **Legal Framework**: Compliance with Angola Customs Code and related regulations
- **Declaration Requirements**: Mandatory fields and validation rules for customs declarations
- **Documentation Standards**: Required documents for different types of imports/exports
- **Penalty Framework**: System support for penalty calculation and appeals process

#### Tax and Financial Regulations
- **VAT Compliance**: Proper VAT calculation and reporting for imported goods
- **Import Duty Regulations**: Accurate duty calculation based on official tariff schedules
- **Exchange Control**: Foreign exchange regulations for international payments
- **Anti-Money Laundering (AML)**: Transaction monitoring and suspicious activity reporting

#### Data Protection and Privacy
- **Personal Data Protection**: Angola data protection laws for individual privacy
- **Data Localization**: Requirements for data storage within Angola territory
- **Cross-border Data Transfer**: Regulations for data sharing with international systems
- **Audit Rights**: Government rights to audit system data and processes

### International Standards Compliance

#### World Customs Organization (WCO) Standards
- **WCO Data Model 3.10**: Complete implementation of WCO standardized data structures
- **SAFE Framework**: Security and trade facilitation standards
- **Time Release Study**: Metrics collection for customs processing time measurement
- **Authorized Economic Operator (AEO)**: Support for trusted trader programs

#### United Nations Standards
- **UN/EDIFACT**: Electronic Data Interchange standards for customs messages
- **UN/CEFACT Modeling Methodology**: Business process modeling standards
- **UN Trade Facilitation Implementation Guide**: Implementation of trade facilitation measures
- **UN/LOCODE**: Location codes for ports and terminals

### Security and Compliance Framework

#### Information Security Standards
- **ISO 27001**: Information Security Management System implementation
- **ISO 27002**: Security controls for information systems
- **NIST Cybersecurity Framework**: Comprehensive cybersecurity risk management
- **PCI DSS**: Payment card industry data security standards (for payment processing)

#### Audit and Compliance Monitoring
- **Audit Trails**: Complete audit logging for all system transactions
- **Compliance Reporting**: Automated generation of regulatory compliance reports
- **Risk Assessment**: Regular security and compliance risk assessments
- **Incident Response**: Defined procedures for security incidents and breaches

## 8.2 Data Model Standards

### WCO Data Model 3.10 Implementation

#### Core Data Elements
The system implements all mandatory WCO Data Model 3.10 elements:

**Declaration-Level Data:**
- Declaration functional reference identifier
- Declaration type code (import/export/transit)
- Submitter identification and authentication
- Declarant and representative party information
- Goods location and customs office codes
- Currency codes (ISO 4217) and exchange rates

**Goods Item-Level Data:**
- Sequential numbering for goods items
- HS commodity codes (6-digit minimum, 8-10 digit where applicable)
- Commercial and statistical values
- Weights (net and gross) with standard units
- Country of origin, export, and destination codes
- Previous administrative references

**Party Information:**
- Party identification numbers (tax IDs, business registration)
- Party names and addresses in standard format
- Communication details (phone, email, fax)
- Party roles and authorization levels
- Economic operator registration numbers

#### Data Validation Rules

**HS Code Validation:**
- Verification against current HS 2017/2022 classification
- Cross-validation with tariff schedules
- Validation of commodity description consistency
- Check for prohibited/restricted goods based on HS codes

**Value and Quantity Validation:**
- Consistency between commercial invoice and declared values
- Reasonable value ranges based on commodity type
- Quantity unit validation against HS code requirements
- Currency conversion using official exchange rates

**Geographic Code Validation:**
- Country code validation against ISO 3166-1
- Port and location code validation against UN/LOCODE
- Route validation for transit declarations
- Customs office code validation

### Data Quality Standards

#### Master Data Governance
- **Data Stewardship**: Designated data stewards for each data domain
- **Data Quality Metrics**: Continuous monitoring of data completeness, accuracy, and consistency
- **Data Lineage**: Complete tracking of data sources and transformations
- **Data Standardization**: Consistent formats and values across all systems

#### Data Synchronization Standards
- **Source System Integration**: Authoritative data sources for each data element
- **Update Frequency**: Real-time for critical data, daily batch for reference data
- **Conflict Resolution**: Defined rules for resolving data conflicts
- **Change Management**: Controlled process for master data updates

## 8.3 Additional Standards

### Technical Standards

#### Web Standards and Accessibility
- **WCAG 2.1 AA**: Web Content Accessibility Guidelines for inclusive design
- **HTML5/CSS3**: Modern web standards for responsive interfaces
- **REST API Standards**: OpenAPI 3.0 specifications for all APIs
- **JSON Schema**: Validation schemas for all API payloads

#### Integration Standards
- **OAuth 2.0 / OpenID Connect**: Secure authentication and authorization
- **SAML 2.0**: Enterprise single sign-on integration
- **SOAP 1.1/1.2**: Legacy system integration (ASYCUDA)
- **TLS 1.3**: Secure communication protocols

#### Container and Deployment Standards
- **OCI Container Standards**: Open Container Initiative specifications
- **Kubernetes Standards**: Cloud Native Computing Foundation standards
- **Helm Chart Standards**: Package management best practices
- **Docker Security**: Container security scanning and hardening

### Operational Standards

#### Service Level Agreements (SLA)
- **Availability**: 99.9% uptime (maximum 8.76 hours downtime per year)
- **Performance**: 95% of API calls complete within 3 seconds
- **Throughput**: System handles 100 transactions per second sustained load
- **Recovery**: 4-hour Recovery Time Objective (RTO) for disaster scenarios

#### Business Continuity Standards
- **Backup and Recovery**: Daily backups with 7-year retention
- **Disaster Recovery**: Offsite backup facility with 4-hour RTO
- **Business Continuity Planning**: Defined procedures for system outages
- **Change Management**: ITIL-based change control processes

### Environmental and Sustainability Standards

#### Green IT Practices
- **Energy Efficiency**: Optimized infrastructure for reduced power consumption
- **Virtualization**: High consolidation ratios to minimize hardware footprint
- **Paperless Operations**: Digital-first processes to reduce paper usage
- **Carbon Footprint**: Monitoring and reduction of system environmental impact

#### Sustainable Development Goals (SDG)
- **SDG 9**: Industry, Innovation and Infrastructure support
- **SDG 16**: Peace, Justice and Strong Institutions through transparent trade
- **SDG 17**: Partnerships for sustainable development through trade facilitation

### Quality Management Standards

#### ISO 9001 Quality Management
- **Process Documentation**: Comprehensive documentation of all business processes
- **Continuous Improvement**: Regular review and optimization of system processes
- **Customer Satisfaction**: User feedback collection and response mechanisms
- **Risk Management**: Systematic identification and mitigation of operational risks

#### Performance Monitoring
- **Key Performance Indicators (KPI)**: Defined metrics for system and business performance
- **Service Monitoring**: Real-time monitoring of all critical services
- **User Experience Monitoring**: Application performance monitoring from user perspective
- **Business Intelligence**: Analytics and reporting for continuous improvement

---

## APPENDICES

### Appendix A: Diagram References

All architectural diagrams are maintained in the `/diagrams/` directory:

- [System Context Diagram](diagrams/01_System_Context_Diagram.mermaid)
- [High Level Architecture](diagrams/02_High_Level_Architecture.mermaid)
- [Deployment Architecture](diagrams/03_Deployment_Architecture.mermaid)
- [Kubernetes Architecture](diagrams/04_Kubernetes_Architecture.mermaid)
- [Network Architecture](diagrams/05_Network_Architecture.mermaid)
- [Microservices Architecture](diagrams/06_Microservices_Architecture.mermaid)
- [Declaration Lifecycle State Machine](diagrams/07_Declaration_Lifecycle_State_Machine.mermaid)
- [Integration Architecture](diagrams/08_Integration_Architecture.mermaid)
- [Data Flow Declaration Process](diagrams/09_Data_Flow_Declaration_Process.mermaid)
- [ASYCUDA Integration Flow](diagrams/10_ASYCUDA_Integration_Flow.mermaid)
- [SINTECE Integration Flow](diagrams/11_SINTECE_Integration_Flow.mermaid)
- [IAM Keycloak Architecture](diagrams/12_IAM_Keycloak_Architecture.mermaid)
- [Document Management MinIO](diagrams/13_Document_Management_MinIO.mermaid)
- [Master Data Sync](diagrams/14_Master_Data_Sync.mermaid)
- [Security Architecture](diagrams/15_Security_Architecture.mermaid)
- [CI/CD Pipeline](diagrams/16_CICD_Pipeline.mermaid)
- [Monitoring Architecture](diagrams/17_Monitoring_Architecture.mermaid)
- [WCO Data Model ER](diagrams/18_WCO_Data_Model_ER.mermaid)

### Appendix B: Reference Documents

- JUL-AGT Integration Control Document - Draft - V2 (ASYCUDA integration specifications)
- JUL-SINTECE Integration Control Document - Draft - v2 (SINTECE integration specifications)  
- JUL System User Management Architecture (Keycloak implementation details)
- WCO Data Model Version 3.10 (World Customs Organization standards)
- UN/EDIFACT Message Standards (Electronic data interchange specifications)

### Appendix C: Glossary

**AGT**: Administração Geral Tributária (Angola Customs Authority)  
**ASYCUDA**: Automated System for Customs Data (UN customs system)  
**CNCA**: Certificado Nacional de Capacidade Aduaneira (National Customs Capacity Certificate)  
**CUSDEC**: Customs Declaration Message (UN/EDIFACT)  
**CUSRES**: Customs Response Message (UN/EDIFACT)  
**DU**: Declaração Única (Single Declaration for customs)  
**HS**: Harmonized System (commodity classification)  
**JUL**: Janela Única Logística (Angola National Logistics Single Window)  
**OGA**: Other Government Agencies  
**SINTECE**: Sistema Nacional de Troca Electrónica de Dados (Angola Single Window)  
**WCO**: World Customs Organization

---

**Document Status**: Production Ready  
**Last Updated**: December 2025  
**Next Review**: June 2026