# Architecture decisions

ADR01: Prefer a layered modular design over microservices for this small design-stage project.
ADR02: Select Dataverse as the provisional low-code data store; validate licensing and cumulative role permissions before pilot approval.
ADR03: Preserve a framework-neutral Python rule demonstrator to make the policy logic reviewable and portable.
ADR04: Classifications describe review intensity, not permission to use regulated data or evidence that an AI model is safe.
ADR05: External AI services are reviewed assets, not execution dependencies of this registry.

## Evidence limits

The classifier has no UI, persistence, authentication, approval implementation, or production audit protection.
Synthetic rule tests provide evidence only for reference classification behavior.
