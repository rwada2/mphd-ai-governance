# Week 5 implementation and verification

## Objectives and module boundaries

FR01 intake checks required textual metadata and declared classification fields.
FR02 evaluates all applicable rules, retains rule IDs, and selects the highest tier.
FR03 maps that tier to a suggested reviewer and checks conditional approval rules.
These pure functions return immutable result objects without using a browser,
database, network, or real agency records. The architecture remains layered;
this milestone implements and tests business logic, not a new deployment layer.

`src/workflow.py` adapts the Week 4 prototype's validation and review conditions
into independently testable functions. Persistence and browser integration remain
separate. No claim is made that these tests verify the Week 4 HTTP/SQLite adapter,
authenticated separation of duties, audit protection, performance, or usability.

## Reproduce

From the repository root, using Python 3.11 or later:

    python -m unittest discover -s tests -v
    python demo_week5.py

The suite contains 17 original classifier checks, five new classifier input-contract
methods, eight intake methods, and ten review methods: 40 methods in total.
Some methods use multiple subtests; the unittest summary counts the methods.
No external testing package or account is required.

## Defect found and corrected

The original classifier called `.get` before checking that the input was a mapping
and tested membership in a set before validating enum value types. Non-object
inputs raised AttributeError; lists/dictionaries in enum fields raised TypeError.
A focused five-method regression run reported 11 subtest errors before the fix.

The correction validates the mapping and string types first and raises ValueError
consistently for invalid inputs. The seven policy conditions and fallback rule are
unchanged. The complete suite passes after the correction. Raw pre-fix local paths
are omitted from the public repository; the report explains the observed failure.

## Test design

Black-box checks assert specified outputs for synthetic input scenarios.
White-box-informed checks target rule precedence, retained rule identifiers, and
explicit validation branches. Boundary checks cover title lengths 200/201 and
review dates today/tomorrow. Negative checks cover invalid enums, boolean types,
missing fields, blocked approval, and matching owner/reviewer names. Regression
checks preserve the original eight scenario classifications and nine invariants.
No numerical branch-coverage claim is made.

Review tests inject 2026-10-01 so they are repeatable regardless of execution date.
The demonstration intentionally uses this same fixed reference date. The module's
default behavior uses the real current date when no override is supplied.

## Release scope

Development is the working branch; main is the checked milestone baseline.
After the relevant tests and diff review, merge development into main and tag
v0.2.0-core-tested. Publish it as a GitHub prerelease because the application is
a synthetic governance prototype. This is a single-author workflow, not a claim
of independent peer review or configured branch protection.
