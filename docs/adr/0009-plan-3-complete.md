# ADR 0009 -- Plan 3 SSP Authoring Complete

**Date:** 2026-04-10
**Status:** Accepted
**Plan:** Plan 3 SSP Authoring (design spec at `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`, implementation plan at `docs/superpowers/plans/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring.md`)
**Predecessors:** ADR 0001-0008. ADR 0008 is the Plan 3 pre-execution realignment record.

## Decision

Plan 3 (SSP Authoring) is **complete**. Every done criterion from the design spec section 2 goal state is verified. The `plan-3-complete` tag is on this commit.

## Done criteria -- verified

- [x] `./pipelines.sh ssp-assemble` succeeds and writes `oscal/ssp.json`.
- [x] `grep -c REPLACE_ME oscal/ssp.json` returns **0**.
- [x] `grep -rc REPLACE_ME trestle-workspace/mss-ssp/` returns **0** across all files.
- [x] `grep -rn "Add implementation prose for the main This System component for control" trestle-workspace/mss-ssp/` returns **0 matches**.
- [x] `verify-family.py` returns exit 0 for all 18 families (156 controls, 0 empty).
- [x] 136 pytest tests pass (130 Plan 2 baseline + 6 verify-family tests from Plan 3 Task 3).
- [x] SSP-level metadata (title, version, system-name, description, authorization-boundary, information-type, component description) filled with real values -- no REPLACE_ME anywhere in the assembled JSON.

## Final artifact inventory

| Artifact | Path | Content |
|---|---|---|
| Assembled OSCAL SSP | `oscal/ssp.json` | 156 implemented_requirements, 0 REPLACE_ME, 0 placeholder prose |
| Authored scaffold | `trestle-workspace/mss-ssp/` | 156 control markdown files with evidence-anchored prose + filled set-params + honest Impl Status |
| SSP metadata | `trestle-workspace/system-security-plans/mss-ssp/system-security-plan.json` | Title, system-name, boundary description, info-type filled |
| Evidence catalog | `docs/plan-3/evidence-catalog/` | 18 family files mapping every control to mechanism + verified evidence paths |
| Gate 2 log | `docs/plan-3/SHAPE-CHECK-LOG.md` | CM-2 + IA-5(1) shape-check observations |
| Gate 3 log | `docs/plan-3/GATE-3-AUDIT.md` | 148 spot-check verifications |
| Gate 4 helper | `docs/plan-3/verify-family.py` | Per-family by-components emptiness verifier |
| Gate 4 tests | `tests/test_verify_family.py` | 6 pytest tests for the verifier |

## Statistics

| Metric | Value |
|---|---|
| Total controls authored | 156 |
| Tier 1 controls (AC, AU, CM, CP, IA, IR, RA, SC, SI) | 87 |
| CA promoted to Tier 1-grade | 10 |
| Tier 2 controls (AT, MA, MP, PE, PL, PS, SA, SR) | 59 |
| Control enhancements authored | 21 |
| Pytest tests passing | 136 |
| Phase 1 subagents dispatched | 18 (parallel) |
| Gate 3 spot checks performed | 148 |
| Gate 3 corrections | 3 (parent workspace path prefix, all in RA/SA) |
| YAML parse fixes during authoring | 2 (ia-5 colon, sa-9 colon -- unquoted colons in set-param values) |

## Gate 2 shape-check findings (ADR 0008 Amendment)

Four Trestle 4.0.1 structural findings discovered during Task 2 and captured in ADR 0008 Amendment:

1. Prose assembles into `by-components[].description`, not `statements[].description`
2. `x-trestle-set-params` values do not appear as `set-parameters` in the assembled JSON
3. SSP-level metadata had 9 REPLACE_ME strings (filled in Task 23)
4. Enhancement files are structurally identical to base controls

These findings changed the verify-family.py design (checks by-components emptiness instead of REPLACE_ME in statements) and added the SSP metadata fill step to Task 23.

## Supersession of 2026-04-07 Plan 3 plan

ADR 0008 documents the supersession in full. The 2026-04-07 Plan 3 plan file remains in the parent workspace with a SUPERSEDED banner. The authoritative Plan 3 artifacts are the 2026-04-09 design spec, the 2026-04-09 implementation plan, ADR 0008, and this ADR.

## Consequences

**Positive:**

- The assembled SSP is a 3PAO-readable artifact with zero placeholder content anywhere. A FedRAMP reviewer can read any control implementation end-to-end and find evidence-anchored prose citing specific homelab mechanisms.
- The evidence catalog (`docs/plan-3/evidence-catalog/`) is a durable secondary artifact -- a reviewer can audit the SSP against the catalog to confirm every claim has a traceable mechanism.
- The whole-project design section 1.4 Question 3 ("Show me one control implementation end-to-end") is now answerable for any of the 156 controls.
- Every Plan 2 deliverable (POA&M pipeline, IIW, component-definition, monthly ConMon rhythm) is cited from the CA family's control-implementation prose, with CA-7 as the hero control.
- Implementation statuses are honest: `implemented` where the mechanism runs, `partial` where there are real gaps (MFA, formal policy documents, HR processes), `planned` where a capability is roadmapped, `not-applicable` where controls genuinely don't apply to a single-operator homelab.

**Negative / accepted:**

- The POA&M-from-SSP-planned-controls linkage described in whole-project design section 4.6 is NOT implemented. Controls with `planned` status document their gap in prose paragraph 2 but do not generate POA&M items. Deferred to Plan 4.
- Some Tier 2 controls have N/A justifications a strict 3PAO might challenge (PS family especially). Every N/A is backed by the single-operator boundary.
- Two YAML parse fixes were needed during authoring (unquoted colons in set-param values). Future authoring should quote any set-param value containing colons.
- RegScale OSCAL push is still a manual runbook (ADR 0006 Deviation 7).

**Risks going into Plan 4:**

- DefectDojo findings pile-up (ADR 0007 Plan 3 Risk #2 carried forward).
- POA&M-from-SSP-planned linkage deferred.
- OSCAL schema drift tripwire remains `tests/test_oscal_roundtrip.py`.

## Next

Plan 4 -- ConMon Writeups and Portfolio Integration.
