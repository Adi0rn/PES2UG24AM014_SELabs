# Lab 3 - Component Modelling and Architectural Pattern Selection

**Adithya Ajith Pillai | PES2UG24AM014**  
**Problem Statement 12: Blood Bank Inventory and Emergency Donor Matcher**

Selected style: **Layered architecture**, deployed as a client-server web application. The layers are logical boundaries, not independently deployed microservices.

## Deliverables

| File | Purpose |
|---|---|
| Component_Diagram.png | UML component diagram export |
| Component_Diagram.pdf | Vector diagram export |
| Component_Diagram.drawio | Editable diagram source for diagrams.net |
| Architecture_Justification.docx | One-page Word justification |
| Architecture_Justification.pdf | One-page PDF justification |
| README.md | Architecture analysis, interface contracts and requirement traceability |

The diagram has **7 components** (6 internal and 1 external) and **8 named provided/required interfaces**. Squares show ports; balls show provided interfaces; sockets show required interfaces. Solid assembly connectors join consumers to providers. Data labels show request and result payloads. The gateway is marked external. Internal API calls are in-process unless explicitly labelled HTTPS.

## Scenario review

Blood banks need current usable stock, component expiry tracking and emergency notifications to compatible eligible donors near a shortage. The main actors are Emergency Requester and Blood Bank Manager. Donors are notification recipients whose eligibility is maintained through authorized management workflows. The design follows the assigned problem sheet and the derived Lab2 baseline in this repository.

Key challenges are concurrent reservations, excluding expired stock, component-specific compatibility, consent and eligibility filters, geographical search, restricted donor data and provider failure handling. The 10 km radius and 30-second alert-dispatch target come from the assigned problem statement; they are design targets, not measured results.

## Architectural style analysis

| Style | Scenario-specific strengths | Scenario-specific limitations | Decision |
|---|---|---|---|
| Layered | Shared transactions protect the bag ledger; rules and provider adapters are separated; modest deployment complexity | Shared database can bottleneck; coarse application scaling; module boundaries need discipline | Selected for the present scope |
| Microservices | Matching and notification services could scale and deploy independently | Cross-service reservation consistency and distributed failure handling increase complexity; network hops and operational overhead | Reconsider only after measured scaling or team needs justify it |
| Client-server | Centralized stock and access control; requester and manager clients share server state | Does not itself define internal responsibility boundaries; central infrastructure requires availability planning | Used as the deployment model, complemented by logical layers |

## Components

| Layer | Component | Responsibility |
|---|---|---|
| Presentation | Web Portal | Submit emergency requests, inventory management forms and permitted status views |
| Business | Emergency Coordinator | Authenticate and authorize, validate input, invoke inventory checks/reservations and coordinate shortage alerts |
| Business | Inventory and Shelf Life | Register and query usable units, enforce expiry rules and reserve units atomically |
| Business | Donor Matcher | Apply approved component-specific compatibility, current eligibility, consent and the 10 km radius |
| Infrastructure | Transactional Persistence | Shared relational ledger for units, requests, verified donors, audit entries and durable notification outbox |
| Infrastructure | Notification Adapter | Queue/dispatch alerts, resolve contact details, record provider results and retry without duplicate sends |
| External | SMS Gateway | Accept SMS requests and expose provider outcomes |

## Interface catalogue

| Interface | Required by consumer | Provided by supplier | Contract |
|---|---|---|---|
| IRequestAPI | Web Portal | Emergency Coordinator | HTTPS/JSON: authenticated request, stock view or request-status operation -> permitted result |
| IInventory | Emergency Coordinator | Inventory and Shelf Life | In-process API: group, component, quantity -> usable count or reservation outcome |
| IDonorMatch | Emergency Coordinator | Donor Matcher | In-process API: verified shortage, component and receiving location -> compatible eligible donor IDs within 10 km |
| IStockRepository | Inventory and Shelf Life | Transactional Persistence | SQL transaction: check and reserve specific usable units -> commit or concurrency conflict |
| INotificationQueue | Emergency Coordinator | Notification Adapter | In-process API: request ID and matched donor IDs -> durable queued job; no provider call in the stock transaction |
| IOutboxRepository | Notification Adapter | Transactional Persistence | SQL: enqueue/claim job, resolve authorized contact data and record attempt -> pending jobs or outcome |
| ISmsTransport | Notification Adapter | SMS Gateway | HTTPS: contact and message -> provider acceptance or failure; later delivery status if supplied |
| IDonorRepository | Donor Matcher | Transactional Persistence | Indexed SQL/spatial query: eligibility, consent and location conditions -> authorized donor records |

## Emergency data flow

1. The Web Portal invokes IRequestAPI. The coordinator checks identity, permissions and request fields.
2. IInventory checks available unexpired units and reserves them through IStockRepository. Transaction failure rolls back the reservation; concurrent requests cannot allocate the same unit. Stock mutations and their audit entries commit together.
3. If a shortage remains, IDonorMatch queries IDonorRepository for consenting, available, manager-approved eligible donors. Compatibility rules are component-specific; the software does not replace clinical approval.
4. INotificationQueue persists a deduplicated outbox job through the adapter and IOutboxRepository before reporting it queued. A logical key of request ID plus donor ID prevents duplicate jobs. The adapter can poll pending jobs in a background task within the layered application; a separate deployment is not required.
5. A short transaction claims a job, then releases database locks before ISmsTransport is called. The adapter records provider acceptance/failure and delivery updates when available. Retries reuse an idempotency key when supported. Provider acceptance does not prove handset delivery; provider-side idempotency is required to close timeout/retry ambiguity.
6. Requester views expose their own fulfilment status. Restricted contact/location records are used only by authorized server-side processing and are not returned to ordinary requester views.

## Requirement traceability

| Lab2 baseline | Components and interfaces |
|---|---|
| FR-001 Emergency matching and alerts | Coordinator, Inventory, Donor Matcher, Notification Adapter; IInventory, IDonorMatch, INotificationQueue, ISmsTransport |
| FR-002 Inventory management | Portal, Coordinator, Inventory, Persistence; IRequestAPI, IInventory, IStockRepository |
| FR-003 Shelf life monitoring | Inventory excludes expired units and flags near-expiry units through persisted expiry timestamps |
| FR-004 Donor records | Authorized management operations through IRequestAPI and coordinator delegation to Donor Matcher; IDonorRepository manages verified records |
| FR-005 Allocation and tracking | Coordinator and Inventory use shared persistence for request status, unit allocation and audit history |
| NFR-001 Transactional consistency | Atomic checks/reservations with row locking or conditional updates; rollback and uniqueness constraints protect each bag |
| NFR-002 Security and privacy | Coordinator access checks, server-only repository access, restricted donor fields, HTTPS and audit logging |

The diagram shows component dependencies rather than every method. IRequestAPI includes authorized management and status operations; IInventory and IDonorMatch include those domain operations in addition to the emergency path. IStockRepository and IDonorRepository also expose the request/record persistence operations needed by those modules. This is a proposed architecture, not a claim of implemented software or completed performance tests.

## Validation checklist

- [x] At least 5 components: 7 shown.
- [x] At least 4 interfaces: 8 named contracts shown.
- [x] Provided balls, required sockets, ports and solid assembly connectors.
- [x] Interaction and request/result data labels, including API, SQL and HTTPS.
- [x] Layered, microservices and client-server styles analysed.
- [x] Selected architecture, two scenario-specific reasons, security advantage and performance benefit.
- [x] One-page Word justification and PDF export.
- [x] PNG/PDF component diagram and editable draw.io source.

## Sources

- Lab_3_Architecture_Student_handout.pdf, pages 5-7: deliverables, notation and justification requirements. The coffee-kiosk scenario in the handout is an example; this submission uses the assigned blood-bank scenario.
- 12_SE_Lab1_SE_Problem_Statements-1.pdf: Problem Statement 12, Blood Bank Inventory and Emergency Donor Matcher.
- [Lab2](../Lab2): derived requirement IDs and blood-bank backlog used for traceability.
