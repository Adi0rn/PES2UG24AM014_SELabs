# Lab 2 - Agile Backlog Creation and Sprint Simulation

**Adithya Ajith Pillai | PES2UG24AM014**

**Problem statement 12: Blood Bank Inventory and Emergency Donor Matcher**

4 epics, 10 stories, 48 Fibonacci story points. Two one-week sprints of 24 points each.

## Status

Backlog, acceptance criteria, sprint plans, reflection answers and local simulation visuals are prepared. **Authentic Jira screenshots are pending.** No Jira sprint completion or feature implementation is claimed. `simulation_visuals/` contains labelled local illustrations, not Jira evidence.

## Files

| File | Content |
|---|---|
| Lab2_Submission.pdf | Main report with backlog, stories, sprint plans, four reflection answers and simulation visuals |
| Lab2_Submission.docx | Editable report |
| Jira_Backlog_Import.csv | Four epics and ten stories with descriptions, estimates, requirements and acceptance criteria |
| Sprint_Simulation.csv | Daily simulated completions and burndown values |
| Jira_Setup_and_Evidence.md | Import mapping, sprint workflow and authentic evidence checklist |
| screenshots/README.md | Required screenshot names and current evidence status |
| simulation_visuals/ | Backlog, board and two burndown illustrations |

## Backlog

| Story | Epic | Summary | Requirements | Priority | Points | Sprint |
|---|---|---|---|---|---:|---|
| US-01 | E1 | Register blood component units | FR-002 | High | 5 | 1 |
| US-02 | E1 | View current usable stock | FR-002; FR-003 | High | 3 | 1 |
| US-03 | E1 | Flag expiry and exclude expired units | FR-003 | High | 3 | 1 |
| US-04 | E2 | Submit an emergency blood request | FR-001; FR-005 | High | 5 | 1 |
| US-05 | E2 | Reserve units without double allocation | FR-005; NFR-001 | High | 8 | 1 |
| US-06 | E3 | Maintain eligible donor records | FR-004 | High | 3 | 2 |
| US-07 | E3 | Find compatible donors within 10 km | FR-001; FR-004 | High | 8 | 2 |
| US-08 | E3 | Dispatch emergency SMS notifications | FR-001 | High | 5 | 2 |
| US-09 | E4 | Track fulfilment and alert outcomes | FR-005 | Medium | 3 | 2 |
| US-10 | E4 | Enforce roles and audit sensitive actions | NFR-002 | High | 5 | 2 |

## Sprint goals

**Sprint 1 - 24 points:** Create and validate usable inventory, submit an emergency request and reserve units without double allocation.
**Sprint 2 - 24 points:** Manage eligible donors, enforce access controls, match nearby candidates and dispatch and track emergency alerts.

## Requirement baseline

The supplied problem sheet defines the emergency cross-reference and 10 km SMS guideline and the no-double-allocation constraint. Other requirements below are an explicit derived Lab 2 baseline, not a claimed copy of an existing Lab 1 submission.

| ID | Requirement | Interpretation |
|---|---|---|
| FR-001 | Emergency matching and alerts | Cross-reference emergency requests with current usable inventory; notify compatible eligible donors within 10 km when stock is insufficient. Target notification dispatch within 30 seconds. |
| FR-002 | Inventory management | Register uniquely identified blood component units and show current available stock by blood group and component. |
| FR-003 | Shelf life monitoring | Track each component unit expiry timestamp; exclude expired, quarantined and reserved units from available stock and flag units nearing expiry. |
| FR-004 | Donor records | Maintain consent, verified blood group, location, availability and manager-approved eligibility information for potential donors. |
| FR-005 | Allocation and tracking | Reserve usable units against a request and record its status and allocation history. |
| NFR-001 | Transactional consistency | Prevent simultaneous allocation of the same blood bag through atomic reservation and concurrency control. |
| NFR-002 | Security and privacy | Enforce authenticated role-based access; restrict donor contact and location details to authorized staff and record sensitive changes in an audit log. |

## Reflection

### Q1. How did you turn the requirements into epics and user stories?

The problem has four connected goals: maintain usable inventory, process emergency requests, reach suitable donors and control access to sensitive records. These goals define the four epics. Requirements were split into small actor-focused outcomes, such as adding a bag, checking current stock and reserving units. Each story uses the As a role, I want a goal, so that a benefit format, with acceptance criteria and requirement links. FR-001 is split across request submission, donor matching and SMS dispatch because each outcome can be reviewed separately.

### Q2. How did you estimate story points?

The backlog uses relative Fibonacci estimates of 3, 5 and 8 points. Viewing usable stock is the 3-point baseline. Request validation and notification dispatch are 5-point stories because they have more integration and failure handling. Atomic reservation and geographical donor matching are 8 points because concurrency, transaction rollback, eligibility filtering and boundary cases introduce greater uncertainty. Points represent relative effort and uncertainty; they are not hours or a measured team velocity.

### Q3. How did you decide what goes into each sprint?

Sprint 1 establishes the inventory-to-reservation path: register units, show available stock, exclude expired units, accept a request and reserve stock safely. Sprint 2 adds donor records, access control, nearby matching, SMS dispatch and request tracking. The second sprint begins with donor records and access control so later stories can use them. Both sprints have an assumed planning capacity of 24 points over five working days. Sprint 1 is an isolated lab increment using synthetic data; it is not deployable with real donor data before security is complete.

### Q4. What did you learn from running the sprints in Jira?

The local sprint simulation shows why a burndown should count points only when a story meets its Definition of Done. In Sprint 1, the 8-point reservation story burns down on the final day, so a flat period does not necessarily mean no work occurred. Requirement links reveal coverage gaps, while dependency ordering prevents starting SMS dispatch before matching and access control are ready. These observations come from the supplied simulation data. A live Jira sprint has not been executed for this submission; the Jira setup guide explains how to reproduce the workflow and capture authentic evidence.

## Reference

The submission structure and reflection questions follow [the reference Lab 2 folder](https://github.com/Dhruvjagadeesh/SOFTWARE-ENGINEERING-LAB-SUBMISSIONS/tree/main/Lab2_Agile-Backlog-and-Sprint-Simulation). Stories, acceptance criteria and simulated progress are adapted to Problem Statement 12.
