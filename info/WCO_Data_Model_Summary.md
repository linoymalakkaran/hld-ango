# WCO Standard Data Model – ER Summary (Derived from JUL–AGT Integration Control Document)

## Executive Summary
- Purpose: Consolidate the data artifacts, actors, flows, and lifecycle states required to model a WCO-compliant Customs Declaration data domain based on JUL–AGT integration.
- Scope: End-to-end Declaration process including registration, validation, risk assessment, examination, assessment, payment, release, and integrations (ASYCUDA, SINTECE, IAM/Keycloak, DMS/MinIO).
- Outcome: A normalized entity-relationship set aligned to WCO Data Model concepts (Declaration, Consignment, Goods Item, Trader Parties, Transport Means, Duty/Tax Lines, Payments, Documents, etc.), ready for ER diagramming.

## Data Domains
- Declaration Domain: Core declaration, goods items, customs procedures, status model.
- Consignment & Transport Domain: Shipment-level structures, packages, containers, means of transport, routes.
- Trader & Parties Domain: Importer/Exporter, declarant, representatives, contact and address data.
- Assessment & Payment Domain: Duties/taxes/fees, valuation, assessments, guarantees, payments and receipts.
- Risk & Control Domain: Risk scores, selectivity results, inspections/examinations and outcomes.
- Document & Attachment Domain: Supporting documents, evidence, digital storage references (MinIO), metadata.
- Integration Domain: External system message exchanges (ASYCUDA, SINTECE), status sync and audit.
- Security & IAM Domain: User identities, roles, audit trails, authorization (Keycloak).

## Core Entities (WCO-Aligned)
- Declaration: Unique customs declaration with procedure, regime, statuses, timestamps.
- Consignment: Shipment-level grouping tied to the declaration; route and transport context.
- GoodsItem: Line items in the declaration, HS codes, quantities, valuation.
- TraderParty: Importer, Exporter, Declarant, Agent; legal identifiers and addresses.
- TransportMeans: Vessel/flight/truck details, mode, carrier, voyage/flight numbers.
- Container/Equipment: Container IDs, seals, equipment references.
- Package: Packaging types, counts, marks.
- CustomsOffice: Lodgment, clearance, exit/entry offices.
- Procedure: Customs procedure codes and regulatory regimes.
- Document: Attached/supporting docs (invoices, BL/AWB, certificates) with DMS linkage.
- DutyTaxFee (AssessmentLine): Duty/tax/fee lines with base, rates, amounts, currency.
- Valuation: CIF/FOB values, exchange rates, charges.
- Payment: Payment records, methods, references, receipts.
- Guarantee: Bond/guarantee references, amounts, validity.
- RiskAssessment: Risk indicators, selectivity channel, scores.
- Examination: Inspection orders, findings, results.
- IntegrationMessage: Outbound/inbound messages to ASYCUDA/SINTECE with statuses.
- UserIdentity: IAM linkage to Keycloak users and roles.
- AuditEvent: Change logs, status transitions, external sync outcomes.

## Key Relationships
- Declaration 1—N GoodsItem: Each declaration has multiple goods items.
- Declaration 1—1 Consignment: One primary consignment per declaration (or 1—N if multi-consignment).
- Declaration N—N TraderParty: Role-based associations (Importer, Exporter, Declarant, Agent).
- Consignment 1—N TransportMeans: Primary means with possible legs (route segments).
- Consignment 1—N Container/Equipment: Containers linked to the shipment.
- GoodsItem 1—N Package: Packaging per line item.
- Declaration 1—N Document: Supporting documents stored in DMS (MinIO ref).
- Declaration 1—N DutyTaxFee: Assessment lines per declaration.
- Declaration 1—1 Valuation: Overall valuation snapshot; may also have item-level valuation.
- Declaration 1—N Payment: Payments against assessed amounts (partial/combined allowed).
- Declaration 0—N Guarantee: Guarantees attached when required by procedure/regime.
- Declaration 0—N RiskAssessment: Risk outcomes over time.
- Declaration 0—N Examination: Inspections tied to risk/controls.
- Declaration 0—N IntegrationMessage: External exchange log (ASYCUDA/SINTECE).
- UserIdentity 0—N AuditEvent: Actions by users recorded for traceability.

## Declaration Lifecycle (Typical States)
- Draft → Submitted → Validated → RiskAssessed → ExaminationOrdered → Examined → Assessed → PaymentPending → Paid → Released.
- Exception paths: Rejected, Amended, Cancelled, Suspended, Re-assessed.
- Each transition captured in `AuditEvent`; integration sync reflected in `IntegrationMessage`.

## Identifiers & Keys
- Declaration: System-generated `DeclarationId`; external references (ASYCUDA TxnId, SINTECE MsgId), MRN/Tracking.
- GoodsItem: `GoodsItemId` scoped to `DeclarationId` with item sequence.
- Consignment: `ConsignmentId` with transport and route references.
- TraderParty: `TraderId` with legal identifiers (TIN/EORI/CRN), role-type.
- TransportMeans: `TransportId` with IMO/flight/truck identifiers.
- Container: `ContainerId` (ISO), seals.
- Document: `DocumentId` + DMS object key (MinIO bucket/key) and checksum.
- DutyTaxFee: `AssessmentLineId` tied to `DeclarationId` and line sequence.
- Payment: `PaymentId` with external gateway reference and receipt number.
- Guarantee: `GuaranteeId` (bond number, issuer).
- IntegrationMessage: `MessageId`, channel (ASYCUDA/SINTECE), correlation IDs.
- AuditEvent: `AuditId` with actor, timestamp, action, entity reference.

## Attribute Highlights (Per Entity)
- Declaration: Type, regime/procedure codes, office, dates, trader roles, status.
- GoodsItem: HS code, description, origin, quantity/weight, value, packages.
- Consignment: Departure/arrival countries/offices, route legs, carrier.
- TransportMeans: Mode, identifiers (IMO/flight/vehicle), voyage/flight dates.
- TraderParty: Names, legal IDs, addresses, contacts, role.
- DutyTaxFee: Basis, rate, amount, currency, tax/duty code.
- Valuation: Customs value, method, exchange rate, charges.
- Payment: Method, amount, currency, reference, status, timestamp.
- Document: Type, issuer, date, reference number, DMS link, checksum.
- RiskAssessment: Profile hits, selectivity result (green/yellow/red), score.
- Examination: Instruction, findings, result, officer, date.
- IntegrationMessage: Direction, message type, status, timestamps, payload ref.
- AuditEvent: Actor (UserIdentity), action, before/after, timestamp, entity.

## Integration Considerations
- ASYCUDA: Map core declaration fields and item details to exchange format; track external transaction ID and sync statuses.
- SINTECE: Align message segments for trade/transport data; store inbound/outbound message references and outcomes.
- IAM/Keycloak: Persist `UserIdentity` with role-based access; enforce authorization on sensitive transitions.
- DMS/MinIO: Store document binaries externally; keep normalized `Document` metadata and DMS object key.
- Messaging & Retry: `IntegrationMessage` to capture delivery attempts, retries, failures, and reconciliation.

## Compliance & Security
- Data Minimization: Store only necessary personal/commercial data.
- Auditability: Full lifecycle with `AuditEvent` and immutable key transitions.
- Access Control: Role-based authorization (Keycloak) for declaration edits, assessments, releases.
- Integrity: Checksums for documents; validation for identifiers and codes.

## ER Modeling Notes
- Normalize trader parties; model role assignment via associative table to `Declaration`.
- Keep `DutyTaxFee` and `Valuation` separate; allow item-level extension if needed.
- Model `IntegrationMessage` as log with polymorphic linkage if messages relate to multiple entities.
- Consider route modeling via `ConsignmentLeg` for multi-leg transport.
- Use strong typing for code lists (HS, procedure codes, offices, document types).

## Open Questions (To Confirm Before Diagramming)
- Single vs multi-consignment per declaration in JUL–AGT context?
- Item-level valuation granularity required or only declaration-level?
- Guarantee details per declaration or per consignment?
- SINTECE message granularity: declaration-level, consignment-level, or both?
- Required code lists and authoritative sources (HS version, procedure codes, office codes)?

## Next Steps
- Build ER diagram using the entities and relationships above.
- Validate field-level mappings against WCO Data Model segments and local regulatory requirements.
- Confirm integration payload schemas and correlation IDs.

---

## Gap Analysis Updates (JUL – Gap Analysis – Draft V3 – 2025-11-22)

### Summary of Key Gaps
- Code Lists: Partial/inconsistent use of WCO-aligned lists (procedure codes, document types, customs office codes, HS version, currency, UN/Locode).
- Identifiers: Missing or inconsistent `MRN`, correlation IDs for external systems, and standardized party ID types (TIN/EORI/CRN).
- Valuation & Duties: Limited valuation method capture, exchange rate tracking, and item-level duty/tax breakdowns.
- Trader Roles: Declarant capacity and role assignments not uniformly modeled across declarations.
- Transport & Consignment: Route leg granularity (multi-leg), places of loading/unloading, and container seal details incomplete.
- Documents: Document type codification and DMS metadata (checksum, hash, mime) not consistently captured.
- Risk & Control: Selectivity channel codes and risk indicator provenance need normalization.
- Audit & Status: Lifecycle status codes diverge from WCO/Regulatory naming; audit trail fields missing for some transitions.
- Integration: Message typing, retry/reconciliation tracking, and correlation with declaration/consignment insufficient.

### Model Updates Applied (ER Summary Adjustments)
- Declaration:
	- Added attributes: `MRN`, `DeclarationType`, `DeclarantCapacity`, `Incoterms`, `OfficeOfLodgment`, `OfficeOfExit/Entry`, `RegistrationNumber`, `RegistrationDate`.
	- Status codes aligned to standard lifecycle; normalized code list references.
- GoodsItem:
	- Added `HSVersion`, `PreferenceCode`, `OriginCriteria`, `StatisticalValue`, `SupplementaryUnits`, `ItemValuationMethod`, `PackageMarksNumbers`.
	- Noted optional item-level `DutyTaxFee` linkage for granular assessments.
- Consignment:
	- Introduced `ConsignmentLeg` to model multi-leg routes with `PlaceOfLoading`/`PlaceOfUnloading` (UN/Locode).
	- Extended container details with `SealNumber`, `SealStatus`.
- TransportMeans:
	- Extended with `CarrierCode`, `ModeCode`, `IMO/Flight/VehicleId`, `Voyage/FlightDates` standardization.
- TraderParty:
	- Standardized identification types (TIN/EORI/CRN) and role assignments via associative linkage to `Declaration` with `RoleType` and `DeclarantCapacity`.
- Document:
	- Enforced WCO document type codes; added `MimeType`, `Checksum/HashAlgo`, `IssueDate`, and `Issuer`.
- Valuation:
	- Captures `ValuationMethod`, `ExchangeRateSource`, `ChargesBreakdown` (freight/insurance/other).
- DutyTaxFee:
	- Clarified `TaxTypeCode`, `Basis`, `Rate`, `Amount`, `Currency` with code list alignment; supports declaration- or item-level association.
- Payment:
	- Added `PaymentGatewayRef`, `ReceiptNumber`, `PaymentStatus`, `PaymentTimestamp`.
- RiskAssessment:
	- Standardized `SelectivityChannel` (green/yellow/red), `RiskScore`, and `ProfileId` provenance.
- IntegrationMessage:
	- Added `MessageType`, `Direction`, `CorrelationId`, `RetryCount`, `LastAttempt`, `Outcome`, and polymorphic entity references.
- AuditEvent:
	- Ensured `ActorId`, `Action`, `Before/AfterSnapshotRef`, `Timestamp`, and reason/comments.

### WCO Segment Mapping (Indicative)
- DEC: `Declaration`
- GOO: `GoodsItem`
- CON: `Consignment`, `ConsignmentLeg`
- PAR: `TraderParty` (+ role association to DEC)
- TRN: `TransportMeans`
- DOC: `Document`
- DTF: `DutyTaxFee`
- VAL: `Valuation`
- PAY: `Payment`
- GUA: `Guarantee`
- RSK: `RiskAssessment`
- AUD: `AuditEvent`
- INT: `IntegrationMessage`

### Code Lists to Adopt/Confirm
- HS Version: Target version in use and effective date.
- UN/Locode: Places of loading/unloading and customs offices (if applicable).
- Procedure/Regime Codes: WCO-aligned or national variants; mapping table required.
- Document Types: WCO document codes; local extensions via controlled vocabulary.
- Currency: ISO 4217; exchange rate source references.
- Mode of Transport: Standardized codes (UNECE/IMO/ICAO as applicable).

### Remaining Open Items
- Multi-consignment per declaration: confirm cardinality for JUL–AGT.
- Item-level valuation: mandated vs optional; scope of charges breakdown.
- Guarantees: per declaration vs per consignment and required attributes.
- SINTECE granularity: declaration-level vs consignment-level messaging and required correlation.
- MRN generation: source system, uniqueness constraints, and format specifications.

### Actions
- Implement code list services and references for the entities above.
- Define correlation ID strategy across integration flows (ASYCUDA/SINTECE).
- Update lifecycle status catalog and ensure audit coverage on all transitions.
- Validate attribute sets against current regulatory requirements and WCO Data Model.

## WCO DM v3.x Attribute Mapping (Indicative, Element IDs to Confirm)

| Local Entity.Attribute | WCO Segment | WCO Element Name | Element ID (public?) | Notes / Code List | Source URL |
| --- | --- | --- | --- | --- | --- |
| Declaration.declaration_id | DEC | Declaration Identifier | Not public (DMOS) | System PK, internal | https://datamodel.wcoomd.org/
| Declaration.functional_reference_id | DEC | Functional Reference ID (LRN) | WCO: D026 | External reference | https://eucdm.softdev.eu.com/
| Declaration.MRN | DEC | Movement Reference Number | EUCDM: 2/6 | Official MRN format rules | https://ec.europa.eu/taxation_customs/dds2/mrn/mrn_home.jsp
| Declaration.declaration_type_code | DEC | Declaration Type Code | WCO: D018 | WCO/EU code lists | https://eucdm.softdev.eu.com/
| Declaration.declaration_office_id | DEC | Customs Office of Lodgment | WCO: D014 | UN/Locode/national | https://eucdm.softdev.eu.com/
| Declaration.goods_location_code | DEC | Goods Location Code | EUCDM: 5/23 | Location codes | https://eucdm.softdev.eu.com/
| Declaration.declarant_party_id | PAR | Declarant Identification | Not public (DMOS) | TIN/EORI/CRN | https://taxation-customs.ec.europa.eu/economic-operators-registration-and-identification-eori_en
| Declaration.representative_party_id | PAR | Representative Identification | Not public (DMOS) | Agent ID/EORI | https://taxation-customs.ec.europa.eu/economic-operators-registration-and-identification-eori_en
| Declaration.border_transport_means | TRN | Border Transport Means | Not public (DMOS) | Snapshot of TRN | https://unece.org/trade/uncefact/rec19
| Declaration.created_datetime | DEC | Creation Date/Time | Not public (DMOS) | ISO timestamp | https://eucdm.softdev.eu.com/
| Declaration.submission_datetime | DEC | Submission Date/Time | Not public (DMOS) | ISO timestamp | https://eucdm.softdev.eu.com/
| Declaration.acceptance_datetime | DEC | Acceptance Date/Time | Not public (DMOS) | ISO timestamp | https://eucdm.softdev.eu.com/
| Declaration.status | DEC | Declaration Status Code | Not public (DMOS) | Normalized lifecycle | https://eucdm.softdev.eu.com/
| Declaration.total_invoice_amount | DEC | Total Invoice Amount | Not public (DMOS) | Sum of item values | https://eucdm.softdev.eu.com/
| Declaration.invoice_currency_code | DEC | Invoice Currency Code | Not public (DMOS) | ISO 4217 | https://www.iso.org/iso-4217-currency-codes.html
| GoodsItem.goods_item_id | GOO | Goods Item Identifier | Not public (DMOS) | Internal PK | https://datamodel.wcoomd.org/
| GoodsItem.sequence_numeric | GOO | Line Number | WCO: G037 | Item sequence | https://eucdm.softdev.eu.com/
| GoodsItem.commodity_code | GOO | Commodity Code | WCO: G054 | HS code | https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx
| GoodsItem.commodity_code_list_id | GOO | Commodity Code List Id | Not public (DMOS) | HS version | https://www.wcotradetools.org/en
| GoodsItem.customs_value_amount | VAL | Customs Value Amount | Not public (DMOS) | Valuation | https://www.wcoomd.org/en/topics/valuation/overview.aspx
| GoodsItem.customs_value_currency_id | VAL | Currency Code | Not public (DMOS) | ISO 4217 | https://www.iso.org/iso-4217-currency-codes.html
| GoodsItem.statistical_value_amount | GOO | Statistical Value Amount | WCO: G042 |  | https://eucdm.softdev.eu.com/
| GoodsItem.net_weight_measure | GOO | Net Mass | WCO: D057 | kg | https://eucdm.softdev.eu.com/
| GoodsItem.gross_weight_measure | GOO | Gross Mass | WCO: D056 | kg | https://eucdm.softdev.eu.com/
| GoodsItem.supplementary_unit_quantity | GOO | Supplementary Units | Not public (DMOS) | UoM | http://service.unece.org/trade/untdid/d16b/tred/tred7065.htm
| GoodsItem.origin_country_code | GOO | Country of Origin | Not public (DMOS) | ISO 3166-1 | https://www.iso.org/obp/ui/#search/code/
| GoodsItem.export_country_code | GOO | Country of Export | Not public (DMOS) | ISO 3166-1 | https://www.iso.org/obp/ui/#search/code/
| GoodsItem.destination_country_code | GOO | Country of Destination | Not public (DMOS) | ISO 3166-1 | https://www.iso.org/obp/ui/#search/code/
| GoodsItem.goods_description | GOO | Goods Description | Not public (DMOS) | Text | https://eucdm.softdev.eu.com/
| GoodsItem.packaging_type_code | GOO | Package Type Code | WCO: D103 | UNECE 7065 | http://service.unece.org/trade/untdid/d16b/tred/tred7065.htm
| GoodsItem.package_quantity | GOO | Number of Packages | WCO: D102 | Integer | https://eucdm.softdev.eu.com/
| Party.party_id | PAR | Party Identifier | Not public (DMOS) | Internal PK | https://datamodel.wcoomd.org/
| Party.party_identification | PAR | Party Identification | Not public (DMOS) | TIN/EORI/CRN | https://taxation-customs.ec.europa.eu/economic-operators-registration-and-identification-eori_en
| Party.party_name | PAR | Party Name | Not public (DMOS) |  | https://eucdm.softdev.eu.com/
| Party.party_type_code | PAR | Party Type Code | Not public (DMOS) | Importer/Exporter/Declarant | https://eucdm.softdev.eu.com/
| Party.party_role_code | PAR | Party Role Code | Not public (DMOS) | Role in declaration | https://eucdm.softdev.eu.com/
| Company.company_id | PAR | Economic Operator Identifier | Not public (DMOS) | Internal PK | https://datamodel.wcoomd.org/
| Company.registration_number | PAR | Registration Number | Not public (DMOS) | National registry | https://eucdm.softdev.eu.com/
| HSCode.hs_code | GOO | Commodity Code | Not public (DMOS) | HS code | https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx
| HSCode.version | GOO | Code List Version | Not public (DMOS) | HS version | https://www.wcotradetools.org/en
| TariffSchedule.duty_rate_percent | DTF | Duty Rate | Not public (DMOS) | Duty code | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| TariffSchedule.vat_rate_percent | DTF | VAT Rate | Not public (DMOS) | Tax code | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| TariffSchedule.excise_rate_percent | DTF | Excise Rate | Not public (DMOS) | Tax code | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| Payment.total_amount | PAY | Payment Amount | Not public (DMOS) | Amount paid | https://eucdm.softdev.eu.com/
| Payment.currency_code | PAY | Currency Code | Not public (DMOS) | ISO 4217 | https://www.iso.org/iso-4217-currency-codes.html
| Payment.payment_method | PAY | Payment Method | Not public (DMOS) |  | https://eucdm.softdev.eu.com/
| Payment.transaction_reference | PAY | Payment Reference | Not public (DMOS) | External gateway ref | https://eucdm.softdev.eu.com/
| DutyCalculation.calculation_basis | DTF | Calculation Basis | Not public (DMOS) | Method or basis | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| DutyCalculation.calculated_duty | DTF | Duty Amount | Not public (DMOS) |  | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| DutyCalculation.calculated_vat | DTF | VAT Amount | Not public (DMOS) |  | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| DutyCalculation.calculated_excise | DTF | Excise Amount | Not public (DMOS) |  | https://taxation-customs.ec.europa.eu/customs-4/customs-tariff/taric_en
| Document.document_id | DOC | Document Identifier | Not public (DMOS) | Internal PK | https://datamodel.wcoomd.org/
| Document.document_category | DOC | Document Type Code | EUCDM: 2/3 | WCO/UNECE codes | http://service.unece.org/trade/untdid/d16b/tred/tred1001.htm
| Document.content_type | DOC | MIME Type | Not public (DMOS) |  | IANA MIME registry
| Document.minio_object_key | DOC | Document Reference | Not public (DMOS) | Storage key reference | 
| Document.checksum_sha256 | DOC | Checksum | Not public (DMOS) | Integrity check | 
| DocumentReference.reference_type | DOC | Document Usage Type | Not public (DMOS) | Required/optional | http://service.unece.org/trade/untdid/d16b/tred/tred1001.htm
| TransportMeans.mode_code | TRN | Mode of Transport Code | Not public (DMOS) | UNECE Rec 19 | https://unece.org/trade/uncefact/rec19
| TransportMeans.carrier_code | TRN | Carrier Identifier | Not public (DMOS) | EORI/national | https://taxation-customs.ec.europa.eu/economic-operators-registration-and-identification-eori_en
| ConsignmentLeg.place_of_loading | CON | Place of Loading | Not public (DMOS) | UN/Locode | https://unece.org/trade/uncefact/unlocode
| ConsignmentLeg.place_of_unloading | CON | Place of Unloading | Not public (DMOS) | UN/Locode | https://unece.org/trade/uncefact/unlocode
| RiskAssessment.selectivity_channel | RSK | Selectivity Result | Not public (DMOS) | Green/Yellow/Red | https://rmc.wcoomd.org/
| IntegrationMessage.correlation_id | INT | Message Correlation Id | Not public (DMOS) | SBDH correlation | https://uncefact.github.io/format-sbdh
| AuditEvent.action | AUD | Action Type | Not public (DMOS) | Lifecycle event | https://datamodel.wcoomd.org/
| AuditEvent.timestamp | AUD | Event Date/Time | Not public (DMOS) | ISO timestamp | https://datamodel.wcoomd.org/
### Public Sources and Licensing Note
- Detailed WCO DM element identifiers and full data dictionary are provided via DMOS for licensed users and WCO Members: https://datamodel.wcoomd.org/
- EUCDM publicly confirms alignment to WCO DM and exposes element names used operationally: https://taxation-customs.ec.europa.eu/eu-customs-data-model-eucdm_en
- Code lists: HS (WCO), ISO 4217 (currency), ISO 3166-1 (country), UN/LOCODE (locations), UNECE Rec 19 (mode of transport), UN/EDIFACT 1001 (document types).

## DMOS Segment Codes (Document Section Codes)
Indicative mapping of segment codes/classes from WCO DM v3.x (sample):

| Segment Code | Class Name |
|--------------|------------|
| 42A | Declaration |
| 43A | GoodsShipment |
| 67A | GovernmentAgencyGoodsItem |
| 08A | BorderTransportMeans |
| 39A | TransportMeans |
| 14A | Consignment |
| 54A | GoodsLocation |
| 55A | GoodsMeasure |
| 32A | Packaging |
| 45A | Document |
| 47A | DutyTaxFee |
| 49A | ValuationAdjustment |
| 66A | AdditionalDocument |
| 68A | AdditionalInformation |

Note: Full segment dictionaries are available via DMOS licensing.

Notes:
- Element IDs marked “TBD” should be populated from the licensed WCO DM v3.x reference. Segment names reflect common WCO structures (DEC, GOO, PAR, TRN, CON, DOC, DTF, VAL, PAY, RSK, AUD, INT).
- Code lists to enforce: HS version, ISO 4217 currency, ISO 3166-1 country, UN/Locode, mode of transport, document type codes, procedure codes.
