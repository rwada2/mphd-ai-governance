# Collaboration protocol

1. Open a change request naming the requirement ID and expected behavior.
2. Work on development or a short feature branch.
3. Update code, synthetic tests, requirements, and diagram together where affected.
4. Run the documented unittest command and review the diff.
5. Request independent review when a real collaborator is available; never fabricate approval.
6. Merge to main, tag the baseline, and retain decision reasons.

Recommended message format: `type(scope): requirement and concrete change`.
Examples: `docs(FR01): define controlled intake fields`; `test(FR02): reject conflicting automation answers`.

Hosted branch protection and reviewer invitations remain account-owner configuration work until verified.
