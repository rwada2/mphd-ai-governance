# Baseline requirements

FR01 Intake: validate structured metadata; no patient attachments; hold incomplete or contradictory submissions.
FR02 Classification: apply all versioned rules; preserve fired rule IDs; choose the highest applicable tier.
FR03 Routing: low to supervisor; moderate to security/data governance; high to committee with privacy/legal; unacceptable blocks activation with appeal.
FR04 Inventory: maintain owner, tool, tier, status, conditions, and next review date.
FR05 Monitoring: schedule re-reviews; record incidents; calculate overdue review counts.
FR06 Access and audit: enforce role and record-level permissions; record privileged and approval actions.

NFR01 Performance: proposed p95 classification under two seconds with 50 simultaneous requests and 10,000 registry entries.
NFR02 Usability: proposed 90% unassisted completion of a synthetic intake task; WCAG 2.2 AA target.
NFR03 Reliability: proposed 99.5% monthly availability, RPO 24 hours, RTO eight hours; failed rules or audit writes hold approval.
NFR04 Security: MFA, default-deny access, encryption, connector restrictions, and no self-approval.
NFR05 Maintainability: reviewed versioned rules, documented schema, automated tests, and reversible releases.

All NFR values are proposed pilot acceptance targets, not achieved measurements.
