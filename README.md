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

Repository: [rwada2/Week3_Detailed_Design](https://github.com/rwada2/Week3_Detailed_Design).

Both `main` and `development` are published for the Unit 3 version-control demonstration.
Viewing access should be verified before submitting the repository URL to the instructor.
Do not commit secrets, real intake submissions, credentials, or raw audit logs.
