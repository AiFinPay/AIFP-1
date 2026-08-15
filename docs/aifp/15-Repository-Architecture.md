# AIFP-1 Repository Architecture

**Document:** AIFP-DOC-15  
**Status:** Active architecture guidance

This document describes **source-of-truth responsibilities**, not a promise that every conceptual repository/package in older drafts exists. Current repository names, package releases, and default branches must be verified from the actual AiFinPay GitHub organization/package registries.

## 1. Principle: One Source Of Truth Per Concern

A payment system must not have multiple competing "canonical" copies of the same deployment, economics, ABI/IDL, or SDK behavior.

Recommended ownership:

| Concern | Canonical home |
|---|---|
| AIFP-1 normative protocol | This repository's AIFP-1 RFC + accepted AIPs |
| Current AIFP-1 economics | `docs/economics.md` + RFC; implementation must match |
| OpenAPI contract | `docs/aifp/08-OpenAPI-3.1-Specification.yaml` |
| AIFP-1 JSON object shapes | `docs/aifp/10-JSON-Schemas.md` / generated schema artifacts |
| Examples | Derived from the canonical protocol/API/schema surfaces |
| SDK implementation | Actual SDK repository/package source |
| Hosted backend implementation | Actual backend/service repository |
| Smart contracts/programs | Chain-specific canonical source repositories |
| Deployment addresses/provenance | Canonical deployment registry/evidence source used by SDK/backend |
| Production release state | Release/deployment evidence, not this docs repository |

## 2. Current Protocol Boundaries

This repository's primary subject is **AIFP-1 merchant AI-traffic/resource monetization**.

```text
AIFP-1 → merchant monetization → 100/0
AIFP-2/x402 → separate agent payment route → 0/0
AIFP-3 → identity / Agent Passport
```

Do not duplicate AIFP-2 or AIFP-3 normative specifications into AIFP-1 merely because SDKs may integrate all of them.

## 3. Economics Synchronization

Current AIFP-1 reference economics:

```text
standard: $0.0005/action
complex:  $0.002/action
premium:  $0.005/action
treasuryBps: 100
creatorBps:  0
```

Any economics change must update all affected current surfaces in one coordinated change:

1. RFC/economics;
2. OpenAPI;
3. schemas;
4. Postman/examples;
5. SDK policy/registry;
6. backend quote/verifier policy;
7. contract/deployment profile;
8. tests/conformance;
9. developer docs/changelog.

Legacy values may remain only in explicitly historical material.

## 4. Implementation Repository Requirements

A payment implementation repository should provide enough context to establish:

- what it implements;
- which protocol/route versions it supports;
- build/test commands;
- security reporting process;
- current deployment/registry source where applicable;
- CI/release workflow;
- source ownership/maintainers;
- known legacy/deprecated paths.

High-risk payment and smart-contract repositories should also document the independent review/release gate.

## 5. Contract Source Provenance

A chain/program address must have one identified canonical source/version relationship.

If two source trees claim the same deployed program/address but differ materially:

1. neither should be cited as canonical by assumption;
2. establish reproducible build/runtime/source evidence;
3. select/record the winning canonical source;
4. archive/gravestone the losing duplicate or clearly label it historical;
5. regenerate ABI/IDL from the canonical source;
6. update SDK/backend registry and tests.

This avoids audit responses citing the wrong source tree.

## 6. Default Branch / Production Source

Every active implementation repository should define one canonical default/main integration branch.

Avoid long-lived situations where:

- GitHub default branch is `main`;
- active product development is merged to `master`;
- production deploys from another branch;
- security remediation lives on a fourth long-lived branch.

If temporary release branches are required, the production SHA and branch relationship must be explicit and reconciled back to the canonical branch.

## 7. Deployment Registry

A payment-target registry should distinguish at least:

- chain/network ID;
- contract/program address;
- implementation version;
- runtime/source provenance;
- supported payment entrypoint;
- supported assets and decimals;
- active economic profile;
- verifier support;
- activation status;
- legacy/superseded status.

A current SDK/backend should consume or generate from one canonical registry rather than hand-maintaining independent address tables.

## 8. Network Status Vocabulary

Do not use a raw network count as a release status.

Use explicit states such as:

- `deployed`;
- `source verified`;
- `canonical target`;
- `verifier ready`;
- `SDK ready`;
- `E2E verified`;
- `payment-live`;
- `legacy`.

A network can be deployed but not payment-live under the current AIFP-1 profile.

## 9. SDK And Package Documentation

This protocol repository may link real packages but should not invent packages/releases from an aspirational language matrix.

For each package link, verify:

- exact package name;
- current version;
- source repository;
- current protocol routes;
- supported chains/assets;
- published installation command.

Planned SDKs should be labeled planned.

## 10. CI / Conformance Expectations

Relevant repositories should automate as much of the following as practical:

- build/lint;
- unit/integration tests;
- protocol/economic regression tests;
- ABI/IDL/schema drift checks;
- deployment-registry drift checks;
- dependency/security scanning;
- secrets scanning;
- replay/idempotency tests;
- low-value/decimal tests;
- route isolation tests.

For AIFP-1, conformance should assert `100/0` and current reference prices. For AIFP-2, conformance should assert `0/0` separately.

## 11. Pull Request Traceability

High-value implementation changes should maintain a traceability chain:

```text
Requirement / Jira
→ implementation branch
→ PR
→ exact head SHA
→ CI/tests
→ independent review where required
→ deployment/release approval
→ deployed SHA/address/version
→ E2E evidence
```

A PR title or "CI green" alone is not production approval.

## 12. Documentation Repository Layout

Within this AIFP-1 repository:

```text
/
├── README.md
├── aips/                 # governance proposals
├── docs/
│   ├── economics.md
│   ├── architecture.md
│   ├── quickstart/
│   └── aifp/             # canonical documentation package
├── examples/
├── schemas/
├── sdk/                  # protocol-facing SDK design notes, not necessarily implementation
├── scripts/
├── tests/
└── .github/
```

Documentation stubs under `sdk/` or `tests/` must not be described as production implementations unless real code/tests exist there.

## 13. Archive / Legacy Policy

Keep historical repositories when they provide deployment/audit evidence, but archive or clearly mark them when they are no longer active sources of truth.

An archived repository should point to its successor when one exists. Do not merge current product updates into an obsolete duplicate merely to keep both copies looking current.

## 14. Current Release Principle

For payment infrastructure, prefer:

**one canonical source + one canonical registry + one reviewed release path**

over
**many partially synchronized repositories/branches claiming the same behavior**.

That principle is part of AIFP-1 operational correctness because stale source/registry/economic data can lead directly to incorrect payments.
