# MPHD AI governance capstone

Core-logic prototype for a hypothetical municipal public health department.
Only synthetic use cases are permitted. No resident, patient, agency, or vendor-confidential records belong here.

## Scope

This repository contains requirements, editable designs, an executable reference classifier,
and isolated intake, routing, and review-decision modules.
It is not a deployed intake application, clinical system, legal determination, or certified compliance product.

## Structure

- `src/`: deterministic classification, intake, routing, and review validation.
- `tests/`: synthetic rule, validation, and precedence checks.
- `data/`: fictional scenario fixtures.
- `docs/`: requirements, decisions, and collaboration guidance.
- `design/`: editable architecture diagram and rendered figure.

## Run

Python 3.11 or later; no third-party dependencies:

    python -m unittest discover -s tests -v
    python demo_week5.py

The Week 5 suite has 40 test methods. The demo uses a fixed reference date of
2026-10-01 for reproducible review-date examples. Production callers should
leave the optional date argument unset to use the current date.

`docs/week5.md` documents the module boundaries, discovered validation defect,
and local evidence. `evidence/week5-unit-tests.txt` records successful execution.
The older Week 4 browser/SQLite demonstration remains in the course workspace;
its storage and HTTP behavior are not covered by these isolated module tests.

The [Week 5 traceability supplement](docs/week5-traceability.md) maps implemented
requirement slices to pinned source, named tests, passing results, and commits.
It is a later evidence improvement proposed through a pull request; it does not
change or replace the original Week 5 milestone.

## Branches

`main` holds reviewed baselines. `development` holds proposed changes.
The initial demonstration is a single-author workflow; it does not claim independent peer review.
Before a future merge, update affected requirements, diagrams, rules, and tests together.

## Hosting

Repository: [rwada2/mphd-ai-governance](https://github.com/rwada2/mphd-ai-governance).

Both `main` and `development` preserve the capstone's history across course units.
Viewing access should be verified before submitting the repository URL to the instructor.
Do not commit secrets, real intake submissions, credentials, or raw audit logs.

## Milestones

- `v0.1.1-design`: original requirements, classifier, tests, and architecture baseline.
- `v0.2.0-core-tested`: Week 5 core logic and 40 passing isolated unit tests.

Policy identifier `MPHD-0.1` remains unchanged because the illustrative risk rules
did not change. The application release version records implementation changes.
Typed reviewer names do not implement authentication or production authorization.
