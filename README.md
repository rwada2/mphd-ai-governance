# MPHD AI governance capstone

Design-stage demonstration for a hypothetical municipal public health department.
Only synthetic use cases are permitted. No resident, patient, agency, or vendor-confidential records belong here.

## Scope

This repository contains requirements, editable designs, and an executable reference classifier.
It is not a deployed intake application, clinical system, legal determination, or certified compliance product.

## Structure

- `src/`: deterministic reference classification code.
- `tests/`: synthetic rule, validation, and precedence checks.
- `data/`: fictional scenario fixtures.
- `docs/`: requirements, decisions, and collaboration guidance.
- `design/`: editable architecture diagram and rendered figure.

## Run

Python 3.11 or later; no third-party dependencies:

    python -m unittest discover -s tests -v

## Branches

`main` holds reviewed baselines. `development` holds proposed changes.
The initial demonstration is a single-author workflow; it does not claim independent peer review.
Before a future merge, update affected requirements, diagrams, rules, and tests together.

## Hosting

A remote URL and reviewer access must be established through the owner's GitHub or GitLab account.
Do not commit secrets, real intake submissions, credentials, or raw audit logs.
