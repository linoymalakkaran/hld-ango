# JUL Architecture Diagrams Index
## Janela Única Logística - Visual Architecture Guide

**Version:** 2.0  
**Date:** December 2025  
**Purpose:** Complete index and navigation guide for all architectural diagrams

---

## Table of Contents

1. [Overview](#overview)
2. [Diagram Categories](#diagram-categories)
3. [Viewing Instructions](#viewing-instructions)
4. [Diagram Dependency Map](#diagram-dependency-map)
5. [Technical Conventions](#technical-conventions)
6. [Category Details](#category-details)
7. [Integration Guidelines](#integration-guidelines)

---

## Overview

This document provides a comprehensive index of all architectural diagrams for the JUL (Janela Única Logística) system. The 18 diagrams provide complete visual documentation of the system architecture, from high-level context through detailed implementation specifications.

### Diagram Summary
- **Total Diagrams**: 18
- **Format**: Mermaid (.mermaid files)
- **Rendering**: Compatible with GitHub, VS Code, Mermaid Live Editor
- **Style**: Professional corporate theme with consistent color scheme
- **Purpose**: Technical documentation supporting HLD document

---

## Diagram Categories

### 🏛️ **System Context & Overview** (3 diagrams)
High-level system boundaries and architectural overview
- Context boundaries and external entities
- Complete system architecture overview
- Infrastructure deployment patterns

### 🏗️ **Infrastructure & Deployment** (3 diagrams)
Physical and virtual infrastructure architecture
- Kubernetes orchestration and containers
- Network topology and security zones
- Backup and disaster recovery strategies

### 💻 **Application Architecture** (4 diagrams)
Software architecture and service design
- Application layer organization
- API gateway and routing patterns
- Microservices communication and boundaries
- Business logic organization

### 🔄 **Business Processes** (2 diagrams)
Workflow and process automation
- Customs declaration state management
- End-to-end import process flows

### 🔗 **Integration & Data** (4 diagrams)
External connectivity and data management
- External system integration patterns
- Service integration layer design
- Data flow between system components
- Database access and persistence patterns

### 🔐 **Security & Identity** (3 diagrams)
Security architecture and access control
- Identity and access management
- Comprehensive security controls
- Authentication and authorization flows

### 📊 **Operations & Monitoring** (3 diagrams)
System operations and DevOps
- Performance monitoring and observability
- Auto-scaling and load balancing
- CI/CD pipeline and deployment automation

### 📈 **Data & Reporting** (2 diagrams)
Data modeling and business intelligence
- Reporting and analytics architecture
- WCO Data Model 3.10 entity relationships

---

## Viewing Instructions

### Recommended Tools
1. **VS Code** with Mermaid Preview extension
2. **GitHub** - Direct rendering in repository view
3. **Mermaid Live Editor** - https://mermaid.live
4. **IntelliJ/WebStorm** with Mermaid plugins

### Rendering Commands
```bash
# VS Code: Open Command Palette (Ctrl+Shift+P)
> Mermaid: Preview

# Browser-based viewing
# Visit: https://mermaid.live
# Copy diagram content and paste

# CLI rendering (with mermaid-cli)
mmdc -i diagram.mermaid -o diagram.png -w 1920 -H 1080
```

### Print Settings
- **Format**: A3 landscape for complex diagrams
- **Resolution**: 300 DPI minimum for technical documentation
- **Color**: Full color recommended, grayscale compatible
- **Font Size**: Minimum 8pt for readability

---

## Diagram Dependency Map

### Primary Flow (Recommended Reading Order)
```
01_System_Context
    ↓
02_High_Level_Architecture
    ↓
03_Deployment_Architecture
    ↓
[Branch to specialized views]
```

### Infrastructure Path
```
04_Kubernetes_Architecture
    ↓
05_Network_Architecture
    ↓
24_Backup_Recovery_Architecture
```

### Application Path
```
06_Layered_Architecture
    ↓
07_API_Gateway_Architecture
    ↓
08_Microservices_Architecture
    ↓
12_Business_Logic_Architecture
```

### Process Path
```
09_Declaration_State_Machine
    ↓
13_Import_Declaration_Process
```

### Integration Path
```
10_Integration_Services_Architecture
    ↓
14_Integration_Layer_Architecture
    ↓
15_Data_Flow_Diagram
    ↓
16_Data_Access_Layer
```

### Security Path
```
11_IAM_Architecture
    ↓
18_Security_Architecture
    ↓
19_Authentication_Flow
```

### Operations Path
```
17_Performance_Architecture
    ↓
20_Scalability_Architecture
    ↓
23_CICD_Pipeline
```

### Data Path
```
25_WCO_Data_Model_ER
    ↓
22_Reporting_Architecture
    ↓
21_Data_Migration_Strategy
```

---

## Technical Conventions

### Color Scheme
- **Primary Blue**: #2E86AB (Main services and components)
- **Secondary Blue**: #A23B72 (Supporting services)
- **Gray**: #F18F01 (External systems)
- **Green**: #C73E1D (Databases and storage)
- **Orange**: #4CAF50 (Success states and positive flows)
- **Red**: #FF5722 (Error states and security boundaries)

### Shape Conventions
| Shape | Meaning | Usage |
|-------|---------|-------|
| Rectangle | Service/Component | Microservices, applications |
| Rounded Rectangle | External System | ASYCUDA, SINTECE, OGA |
| Cylinder | Database | PostgreSQL instances |
| Cloud | Cloud Service | External cloud providers |
| Diamond | Decision Point | Workflow branches |
| Circle | Start/End | Process initiation/completion |

### Line Conventions
| Line Style | Meaning | Usage |
|------------|---------|-------|
| Solid | Synchronous Call | REST API, gRPC |
| Dashed | Asynchronous | Message queues, events |
| Thick Solid | Primary Flow | Main business processes |
| Dotted | Configuration | Config files, environment |

### Label Conventions
- **Services**: PascalCase (e.g., DeclarationService)
- **Ports**: Numbers in parentheses (e.g., :8080)
- **Protocols**: Uppercase abbreviations (e.g., HTTPS, gRPC)
- **Databases**: snake_case suffixed with _db (e.g., company_db)

---

## Category Details

### 01. System Context Diagram
**File**: `01_System_Context_Diagram.mermaid`  
**Purpose**: Defines system boundaries and external entities  
**Key Elements**:
- JUL system boundary
- External stakeholders (importers, customs officers, brokers)
- Government systems (ASYCUDA, SINTECE)
- Other government agencies (OGAs)

**Use Cases**:
- Stakeholder identification
- Scope definition
- Integration planning
- Business context understanding

---

### 02. High Level Architecture
**File**: `02_High_Level_Architecture.mermaid`  
**Purpose**: Complete system architectural overview  
**Key Elements**:
- 11 microservices with clear boundaries
- Frontend Angular application
- Keycloak authentication
- Database cluster organization
- External system connections

**Use Cases**:
- Solution architecture review
- Technical planning
- Service boundary definition
- Technology stack overview

---

### 03. Deployment Architecture
**File**: `03_Deployment_Architecture.mermaid`  
**Purpose**: Infrastructure and deployment patterns  
**Key Elements**:
- Kubernetes cluster structure
- Docker containerization
- Load balancers and networking
- Storage and database deployment

**Use Cases**:
- Infrastructure planning
- DevOps implementation
- Capacity planning
- Environment setup

---

### 04. Kubernetes Architecture
**File**: `04_Kubernetes_Architecture.mermaid`  
**Purpose**: Detailed Kubernetes orchestration  
**Key Elements**:
- Namespaces organization (production, staging, monitoring)
- Pod and service definitions
- Ingress controllers and routing
- ConfigMaps and secrets management

**Use Cases**:
- Container orchestration
- Resource allocation
- Service mesh planning
- Operations automation

---

### 05. Network Architecture
**File**: `05_Network_Architecture.mermaid`  
**Purpose**: Network topology and security zones  
**Key Elements**:
- DMZ and internal network zones
- Firewall rules and security groups
- VPN connections for external integrations
- Load balancer configurations

**Use Cases**:
- Network security planning
- Firewall configuration
- VPN setup
- Traffic flow analysis

---

### 06. Layered Architecture
**File**: `06_Layered_Architecture.mermaid`  
**Purpose**: Application layer organization  
**Key Elements**:
- Presentation layer (Angular frontend)
- API layer (Kong gateway)
- Business logic layer (microservices)
- Data access layer (repositories)
- Infrastructure layer (databases, storage)

**Use Cases**:
- Code organization
- Separation of concerns
- Development team structure
- Testing strategy

---

### 07. API Gateway Architecture
**File**: `07_API_Gateway_Architecture.mermaid`  
**Purpose**: Kong gateway configuration and routing  
**Key Elements**:
- Route definitions and upstream services
- Authentication and authorization plugins
- Rate limiting and security policies
- Load balancing strategies

**Use Cases**:
- API management
- Security policy implementation
- Traffic routing
- Performance optimization

---

### 08. Microservices Architecture
**File**: `08_Microservices_Architecture.mermaid`  
**Purpose**: Detailed microservices design  
**Key Elements**:
- 11 microservices with ports and protocols
- Service-to-service communication patterns
- Database-per-service implementation
- Cross-cutting concerns (logging, monitoring)

**Use Cases**:
- Service development
- Inter-service communication
- Data management strategy
- Development team coordination

---

### 09. Declaration State Machine
**File**: `09_Declaration_State_Machine.mermaid`  
**Purpose**: Customs declaration workflow  
**Key Elements**:
- Declaration lifecycle states
- State transition triggers and conditions
- Integration points with external systems
- Error handling and retry logic

**Use Cases**:
- Business process implementation
- Workflow engine configuration
- User interface design
- Business rule validation

---

### 10. Integration Services Architecture
**File**: `10_Integration_Services_Architecture.mermaid`  
**Purpose**: External system integration patterns  
**Key Elements**:
- ASYCUDA SOAP/XML integration
- SINTECE REST/JSON integration
- OGA REST/JSON integration
- Message queuing and transformation

**Use Cases**:
- Integration development
- Data transformation mapping
- Error handling strategies
- Performance optimization

---

### 11. IAM Architecture
**File**: `11_IAM_Architecture.mermaid`  
**Purpose**: Identity and access management  
**Key Elements**:
- Keycloak configuration and realms
- User authentication flows
- Role-based access control (RBAC)
- Single sign-on (SSO) implementation

**Use Cases**:
- Security implementation
- User management
- Authorization policies
- SSO configuration

---

### 12. Business Logic Architecture
**File**: `12_Business_Logic_Architecture.mermaid`  
**Purpose**: Core business logic organization  
**Key Elements**:
- Business rule engines
- Validation services
- Calculation engines
- Workflow orchestration

**Use Cases**:
- Business rule implementation
- Validation strategy
- Calculation algorithms
- Process automation

---

### 13. Import Declaration Process
**File**: `13_Import_Declaration_Process.mermaid`  
**Purpose**: End-to-end import process flow  
**Key Elements**:
- User journey from submission to clearance
- System interactions and validations
- Document management workflow
- Payment and clearance processes

**Use Cases**:
- User experience design
- Process optimization
- Training material development
- Business process documentation

---

### 14. Integration Layer Architecture
**File**: `14_Integration_Layer_Architecture.mermaid`  
**Purpose**: Detailed integration layer design  
**Key Elements**:
- Message transformation services
- Protocol adapters and converters
- Error handling and retry mechanisms
- Monitoring and logging integration

**Use Cases**:
- Integration implementation
- Message transformation
- Error recovery planning
- Performance monitoring

---

### 15. Data Flow Diagram
**File**: `15_Data_Flow_Diagram.mermaid`  
**Purpose**: Information flow between services  
**Key Elements**:
- Data sources and destinations
- Transformation points and rules
- Data validation and quality checks
- Real-time vs. batch processing flows

**Use Cases**:
- Data architecture planning
- ETL process design
- Data quality implementation
- Performance optimization

---

### 16. Data Access Layer
**File**: `16_Data_Access_Layer.mermaid`  
**Purpose**: Database access patterns  
**Key Elements**:
- Repository pattern implementation
- Database connection pooling
- Transaction management
- Data caching strategies

**Use Cases**:
- Data access implementation
- Performance optimization
- Transaction design
- Caching strategy

---

### 17. Performance Architecture
**File**: `17_Performance_Architecture.mermaid`  
**Purpose**: Monitoring and observability  
**Key Elements**:
- Prometheus metrics collection
- Grafana dashboards and alerting
- Application performance monitoring (APM)
- Log aggregation with ELK stack

**Use Cases**:
- Performance monitoring
- Alerting configuration
- Troubleshooting procedures
- Capacity planning

---

### 18. Security Architecture
**File**: `18_Security_Architecture.mermaid`  
**Purpose**: Comprehensive security controls  
**Key Elements**:
- Defense in depth strategy
- Encryption at rest and in transit
- Security scanning and vulnerability management
- Incident response procedures

**Use Cases**:
- Security implementation
- Compliance validation
- Risk assessment
- Security operations

---

### 19. Authentication Flow
**File**: `19_Authentication_Flow.mermaid`  
**Purpose**: Login and token management  
**Key Elements**:
- OAuth 2.0 and SAML flows
- Multi-factor authentication (MFA)
- Token lifecycle management
- Session management

**Use Cases**:
- Authentication implementation
- Security configuration
- User experience design
- Integration testing

---

### 20. Scalability Architecture
**File**: `20_Scalability_Architecture.mermaid`  
**Purpose**: Auto-scaling and load balancing  
**Key Elements**:
- Horizontal and vertical scaling strategies
- Load balancing algorithms
- Auto-scaling triggers and policies
- Performance thresholds and metrics

**Use Cases**:
- Capacity planning
- Auto-scaling configuration
- Performance optimization
- Cost management

---

### 21. Data Migration Strategy
**File**: `21_Data_Migration_Strategy.mermaid`  
**Purpose**: Migration approach and phases  
**Key Elements**:
- Migration phases and timelines
- Data extraction and transformation
- Validation and testing procedures
- Rollback and recovery plans

**Use Cases**:
- Migration planning
- Risk mitigation
- Testing strategy
- Change management

---

### 22. Reporting Architecture
**File**: `22_Reporting_Architecture.mermaid`  
**Purpose**: Business intelligence and reporting  
**Key Elements**:
- Data warehouse design
- ETL processes for reporting
- Dashboard and report generation
- Real-time analytics capabilities

**Use Cases**:
- BI implementation
- Report development
- Analytics planning
- Business intelligence strategy

---

### 23. CI/CD Pipeline
**File**: `23_CICD_Pipeline.mermaid`  
**Purpose**: Build and deployment automation  
**Key Elements**:
- Source code management
- Build and test automation
- Deployment strategies
- Environment promotion workflow

**Use Cases**:
- DevOps implementation
- Deployment automation
- Quality assurance
- Release management

---

### 24. Backup Recovery Architecture
**File**: `24_Backup_Recovery_Architecture.mermaid`  
**Purpose**: Disaster recovery strategies  
**Key Elements**:
- Backup schedules and retention
- Recovery time and point objectives
- Disaster recovery procedures
- Business continuity planning

**Use Cases**:
- DR planning
- Backup implementation
- Business continuity
- Risk management

---

### 25. WCO Data Model ER
**File**: `25_WCO_Data_Model_ER.mermaid`  
**Purpose**: WCO 3.10 entity relationships  
**Key Elements**:
- WCO data model entities
- Relationship mappings
- Data validation rules
- Compliance requirements

**Use Cases**:
- Data model implementation
- Compliance validation
- Database design
- Integration mapping

---

## Integration Guidelines

### For Technical Documentation
1. **Include in README**: Link to this index from project README
2. **Architecture Reviews**: Use diagrams in technical design reviews
3. **Developer Onboarding**: Sequential reading path for new team members
4. **Stakeholder Communication**: Select relevant diagrams for audience

### For Development Teams
1. **Service Development**: Reference microservices architecture (08)
2. **API Implementation**: Follow API gateway patterns (07)
3. **Database Design**: Use data access layer patterns (16)
4. **Integration Work**: Study integration layer design (14)

### For Operations Teams
1. **Deployment**: Use Kubernetes architecture (04) for container orchestration
2. **Monitoring**: Implement performance architecture (17) patterns
3. **Security**: Follow security architecture (18) guidelines
4. **CI/CD**: Configure pipeline based on diagram 23

### For Business Analysts
1. **Process Design**: Use declaration state machine (09) for workflows
2. **User Journey**: Reference import declaration process (13)
3. **Requirements**: Map to system context diagram (01)
4. **Reporting**: Design based on reporting architecture (22)

---

**Document Control**  
**Version**: 2.0  
**Diagrams**: 18 total  
**Last Updated**: December 2025  
**Next Review**: March 2026  
**Owner**: JUL Architecture Team