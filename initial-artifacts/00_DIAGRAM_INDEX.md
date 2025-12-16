# JUL High Level Design - Complete Diagram Set

## ✅ All 25 Diagrams Created Successfully!

All diagrams are in proper Mermaid format (without markdown code fences) and ready to render.

## Complete Diagram List

### 1. System Overview & Architecture (Diagrams 01-05)

**01_System_Context_Diagram.mermaid**
- Complete system context
- External actors: Traders, Agents, Forwarders, Brokers, Truckers
- JUL components: Portal, Mobile, API Gateway, Services, IAM
- External systems: ASYCUDA, SINTECE, PICE, SIGT, SICOEX, JUP, TOS, Banks, OGAs

**02_High_Level_Architecture.mermaid**
- Layered architecture overview
- Presentation Layer: Web Portal, Mobile Apps, API Console
- API Gateway: Kong
- Application Layer: Core Services (8), Integration Services (5), Cross-Cutting (5)
- Data Layer: PostgreSQL, MongoDB, Redis, RabbitMQ

**03_Deployment_Architecture.mermaid**
- Deployment topology
- Internet → DMZ (Load Balancer, WAF) → Kubernetes Cluster
- Data Zone: Database clusters, cache, storage
- Management: Monitoring, Logging, Backup
- DR Site: Standby DB and storage

**04_Kubernetes_Architecture.mermaid**
- Kubernetes cluster details
- Control Plane (3 nodes): API Server, etcd, Scheduler, Controller
- Worker Node Pool with Kubelet and Pods
- Namespaces: jul-production, jul-integration, jul-security, jul-data
- Add-ons: NGINX Ingress, CoreDNS, Metrics Server

**05_Network_Architecture.mermaid**
- Network topology and zones
- DMZ (172.16.1.0/24): Load Balancer, WAF, Firewall
- Application Zone (10.10.0.0/16): Kubernetes, API Gateway, Pods
- Data Zone (10.20.0.0/16): Database, Cache, Storage networks
- Management Zone (10.30.0.0/16): Bastion, Monitoring, Logging

### 2. Application Architecture (Diagrams 06-12)

**06_Layered_Architecture.mermaid**
- Multi-tier architecture
- Presentation: UI, Mobile UI
- API: REST, GraphQL, WebSocket
- Business Logic: Services, Domain Models, Rules Engine, Workflow
- Data Access: Repositories, ORM (JPA/Hibernate), Cache, Queue
- Data: PostgreSQL, Redis, RabbitMQ, Object Storage

**07_API_Gateway_Architecture.mermaid**
- Kong API Gateway details
- Authentication (OAuth 2.0/JWT)
- Rate Limiting
- Routing
- Request/Response Transformation
- Response Caching
- Logging & Metrics
- Backend service routing

**08_Microservices_Architecture.mermaid**
- All 18 microservices with ports
- Core Business: Company (8081), License (8082), Agent (8083), Declaration (8084), Document (8085), Track (8086), Payment (8087), Master Data (8088)
- Integration: ASYCUDA (9081), SINTECE (9082), JUP (9083), TOS (9084), OGA (9085)
- Cross-Cutting: IAM (8080), Notification (8089), Workflow (8090), Audit (8091), Reporting (8092)

**09_Declaration_State_Machine.mermaid**
- Complete declaration lifecycle
- States: Draft → Submitted → Validating → SentToCustoms → CustomsReceived → UnderAssessment → Assessed → PendingPayment → PaymentReceived → PaymentVerified → Cleared → Released
- Exception paths: ValidationFailed, InspectionRequired, Rejected
- Simplified Mermaid state diagram format

**10_Integration_Services_Architecture.mermaid**
- Integration layer components
- JUL Services: Declaration, Track, License
- Integration Layer: ESB, Protocol Adapters, Data Transformer
- External Systems: ASYCUDA (SOAP/XML), SINTECE (REST/JSON), JUP, TOS, Banks (BANSTA EDI)

**11_IAM_Architecture.mermaid**
- Keycloak-based Identity and Access Management
- Components: Login Service, Multi-Factor Auth, SSO, RBAC, Token Management, Session Management
- Identity Providers: LDAP/AD, Certificate Auth
- Data Stores: Keycloak DB, Session Cache (Redis)

**12_Business_Logic_Architecture.mermaid**
- Domain-Driven Design
- Domain Aggregates: Company, Declaration, License, Shipment
- Business Rules: Drools Engine, Tariff Rules, Validation Rules, Eligibility Rules
- Domain Services: Declaration, Payment, License

### 3. Integration & Data Flow (Diagrams 13-17)

**13_Import_Declaration_Process.mermaid**
- Sequence diagram for import process
- End-to-end flow from trader submission to cargo release
- 16 steps: Create → Submit → Validate → ASYCUDA → Assessment → Payment → Bank → Clearance
- Participants: Trader, Portal, API, Services, ASYCUDA, Payment, Bank

**14_Integration_Layer_Architecture.mermaid**
- Integration patterns
- Synchronous (Request-Reply)
- Asynchronous (Pub-Sub)
- File-Based (FTP/SFTP)
- EDI (UN/EDIFACT)
- Protocol Adapters: REST, SOAP, EDI, File
- Message Queue with Dead Letter Queue

**15_Data_Flow_Diagram.mermaid**
- Critical data flows
- User → Portal → API → Declaration Service → Database
- Declaration Service → ASYCUDA (CUSDEC/CUSRES)
- Payment flow: User → Payment Service → Bank (BANSTA)
- Data formats: JSON, XML, EDI

**16_Data_Access_Layer.mermaid**
- Data access architecture
- Application Services → Repositories
- Connection Pool (HikariCP), Cache Manager, Transaction Manager
- ORM Layer: JPA/Hibernate, Query Builder
- Data Stores: PostgreSQL Primary, Replicas, Redis Cache

**17_Performance_Architecture.mermaid**
- Performance optimization
- CDN for static content
- Load Balancer distribution
- Cache Layer (Redis)
- Read Replicas for query distribution
- Auto-Scaling (HPA) for application instances

### 4. Security & Operations (Diagrams 18-21)

**18_Security_Architecture.mermaid**
- Multi-layer security
- Perimeter: DDoS Protection, WAF, IDS
- Application: API Security (OAuth 2.0), Input Validation, Output Encoding
- Data: TLS 1.3 (transit), AES-256 (rest), Field Encryption, Key Vault
- IAM: Authentication (2FA), Authorization (RBAC)
- Monitoring: SIEM, Audit Logging

**19_Authentication_Flow.mermaid**
- Sequence diagram for authentication
- User login with 2FA
- JWT token generation
- Session management in Redis
- Subsequent API calls with token validation
- Token refresh flow

**20_Scalability_Architecture.mermaid**
- Scalability strategy
- Horizontal Pod Autoscaler (2-20 pods)
- Stateless services
- Database scaling: Primary + multiple replicas
- Connection pooling
- Redis cluster (6 nodes) with partitioning
- Load distribution: Round Robin, Least Connections

**21_Data_Migration_Strategy.mermaid**
- Migration approach
- Source Systems: Legacy, Excel, ASYCUDA
- ETL Process: Extract → Transform → Validate → Load
- Validation: Quality Checks, Reconciliation, Error Handling
- Target: JUL Database (Master Data, Company Data, Declaration Data)

### 5. Reporting & DevOps (Diagrams 22-24)

**22_Reporting_Architecture.mermaid**
- Reporting infrastructure
- Reporting Tools: JasperReports, Grafana, Kibana, Custom Engine
- Data Sources: OLTP (PostgreSQL), Analytics (DW), Logs (ES), Metrics (Prometheus)
- Report Types: Operational, Analytical, Compliance, Real-time Dashboards

**23_CICD_Pipeline.mermaid**
- Complete CI/CD workflow
- Development: Developer → GitLab
- CI Build: Trigger → Build → Unit Tests → Code Quality (SonarQube) → Security Scan (OWASP) → Docker Build
- CD Deploy: Test Env → Integration Tests → Staging → UAT → Production
- Verification: Health Checks → Smoke Tests → Rollback Decision

**24_Backup_Recovery_Architecture.mermaid**
- Backup and DR strategy
- Production: Applications, Primary DB, Storage
- Backup: Full (Daily 2AM), Incremental (6 hours), WAL (Continuous), Config
- Storage: Online (30 days), Archive (7 years), Offsite
- DR Site: Standby DB, DR Storage, Cold Standby Apps
- Recovery: Restore → Verify → Failover

### 6. Standards Compliance (Diagram 25)

**25_WCO_Data_Model_ER.mermaid**
- WCO Data Model 3.10 entity relationships
- Core entities: DECLARATION, GOODS_ITEM, COMMODITY, HS_CODE
- Parties: PARTY, DECLARATION_PARTY
- Transport: TRANSPORT, CONTAINER
- Financial: DUTY_TAX, PAYMENT
- Packaging: PACKAGING
- Complete relationships and foreign keys

## How to Use These Diagrams

### Rendering Diagrams

**Option 1: Mermaid Live Editor (Online)**
```
1. Go to https://mermaid.live/
2. Copy the content of any .mermaid file
3. Paste into the editor
4. Export as PNG or SVG
```

**Option 2: Mermaid CLI (Command Line)**
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Convert single diagram
mmdc -i 01_System_Context_Diagram.mermaid -o 01_System_Context_Diagram.png

# Convert all diagrams
for file in *.mermaid; do
    mmdc -i "$file" -o "${file%.mermaid}.png"
done
```

**Option 3: VS Code Extension**
```
1. Install "Mermaid Preview" extension in VS Code
2. Open any .mermaid file
3. Press Ctrl+Shift+P → "Mermaid: Preview"
4. Export/Save as image
```

**Option 4: Markdown Viewers**
Most modern markdown viewers support Mermaid:
- GitHub (renders automatically in README)
- GitLab (renders automatically)
- Confluence (with Mermaid plugin)
- Notion (paste as code block with language "mermaid")

### Embedding in Word Document

**Method 1: Convert to Images First**
```bash
# Convert all diagrams to PNG
for file in *.mermaid; do
    mmdc -i "$file" -o "${file%.mermaid}.png" -w 1200 -H 800
done

# Then insert images into Word at the appropriate sections
```

**Method 2: Using Pandoc**
```bash
# If you have mermaid-filter installed
pandoc ../JUL_High_Level_Design.md -o JUL_HLD.docx --filter mermaid-filter

# This will convert markdown + mermaid to Word with embedded diagrams
```

**Method 3: Manual Process**
```
1. Render each diagram to PNG using Mermaid Live Editor
2. Open JUL_High_Level_Design.md in Word (File → Open)
3. At each "Diagram Reference" location, insert the corresponding PNG image
4. Adjust image sizes as needed (recommend 6-7 inches wide)
5. Add captions below each diagram
```

### Diagram Naming Convention

All diagrams follow this pattern:
- `[NN]_[Description].mermaid`
- NN = Two-digit number (01-25)
- Description = Snake_case description
- Extension = .mermaid

### Diagram Types Used

- **graph TB/LR**: Flowcharts and architecture diagrams (Top-Bottom or Left-Right)
- **sequenceDiagram**: Sequence/interaction diagrams
- **stateDiagram-v2**: State machine diagrams
- **erDiagram**: Entity-Relationship diagrams

### Color Scheme

Consistent colors across all diagrams:
- **Blue (#4A90E2)**: Presentation layer, UI components, Core services
- **Green (#50C878)**: Application services, API Gateway, Success states
- **Red (#E74C3C, #E67E22)**: External systems, Security, Databases, Critical components
- **Purple (#9B59B6)**: Message queues, Async processing
- **Orange (#F39C12)**: Security, IAM, Monitoring, Warnings
- **Cyan (#1ABC9C, #27AE60)**: Financial systems, Payments, Completion
- **Gray (#95A5A6)**: Storage, Archives, External/Unknown

## Diagram Quality Checklist

✅ All 25 diagrams created
✅ No markdown code fences (pure Mermaid syntax)
✅ Consistent naming convention
✅ Consistent color scheme
✅ Readable labels with line breaks where appropriate
✅ Logical flow direction
✅ Clear relationships and connections
✅ Subgraphs for grouping related components
✅ Comments where helpful
✅ Referenced in HLD document

## Integration with HLD Document

Each diagram is referenced in the HLD document at the appropriate section:
- **"Diagram Reference: See [XX_Diagram_Name.mermaid]"**
- References appear before the detailed text explanation
- Diagrams provide visual representation of concepts explained in text

## Maintenance

When updating diagrams:
1. Edit the .mermaid file directly
2. Test rendering in Mermaid Live Editor
3. Update diagram version/date if tracking changes
4. Regenerate images if using image exports
5. Update HLD document if diagram structure changes significantly

## Support

For questions about:
- **Mermaid syntax**: https://mermaid.js.org/intro/
- **Diagram design**: Refer to HLD document sections
- **WCO standards**: https://www.wcoomd.org/
- **System architecture**: Contact JUL System Architecture Team

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Total Diagrams**: 25  
**Status**: ✅ Complete
