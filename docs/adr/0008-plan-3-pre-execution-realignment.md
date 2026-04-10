# ADR 0008 — Plan 3 Pre-Execution Realignment

**Date:** 2026-04-09
**Status:** Accepted
**Context:** Plan 3 (SSP Authoring) pre-execution realignment
**Predecessors:** 0001 (pre-flight), 0002 (Plan 1 complete), 0003 (RegScale install), 0004 (DefectDojo install), 0005 (PBS backup gap), 0006 (Plan 2 realignment), 0007 (Plan 2 complete)

## Decision

The 2026-04-07 Plan 3 plan (`docs/superpowers/plans/2026-04-07-homelab-fedramp-low-plan-3-ssp-authoring.md` in the parent workspace) was authored before Plan 1 and Plan 2 executed. Plan 2 execution (complete 2026-04-09, ADR 0007) discovered realignments that make the 2026-04-07 plan silently wrong in the same way ADR 0006 was wrong about Plan 2. This ADR is the Plan 3 analogue of ADR 0006 — the pre-execution realignment record that a reviewer can walk to see every decision made before Plan 3 authoring started.

The authoritative Plan 3 artifacts are:
- **Design spec:** `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`
- **Implementation plan:** `docs/superpowers/plans/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring.md`
- **This ADR** (pre-execution)
- **ADR 0009** (Plan 3 completion, filed at Gate 5)

The 2026-04-07 Plan 3 plan file is kept in the parent workspace as historical context. A SUPERSEDED banner at the top of that file points forward to the authoritative artifacts.

## Supersession deltas

| 2026-04-07 Plan 3 assumption | Post-Plan-2 reality |
|---|---|
| Tier 1 ~ 40 controls in AU/CM/IA/SC/SI/RA/IR | Tier 1 = 87 controls in AC/AU/CM/CP/IA/IR/RA/SC/SI. CA promoted to Tier-1-grade -> 97 effective detailed controls. Tier 2 = 59 controls after CA promotion. |
| Control markdown at `ssp/controls/<family>/<id>.md` with custom YAML (`control:` / `title:` / `baseline:` / `status:` / `origination:` / `responsible-role:`) and custom prose headings (`## Implementation Description` / `### What` / `### How` / `### Where` / `## Assessment Procedure` / `## Inheritance` / `## Related Controls`) | Trestle 4.0.1 `ssp-generate` produced `trestle-workspace/mss-ssp/<family>/<id>.md` with `x-trestle-add-props` / `x-trestle-set-params` / `x-trestle-global` YAML and prose section `## What is the solution and how is it implemented?` -> `### This System` -> `#### Implementation Status:`. 868 `<REPLACE_ME>` placeholders distributed across prose statements AND set-params. |
| Execution on `[wsl]` Ubuntu | Git Bash on Windows with Python 3.14 native per ADR 0006 Deviation 1 |
| `make ssp` / `make conmon` | `./pipelines.sh ssp-assemble` / `./pipelines.sh conmon` per ADR 0006 Deviation 2 |
| Trestle 3.4+ | Trestle 4.0.1 pinned per ADR 0006 Deviation 9; pydantic.v1 Python 3.16 tripwire documented in ADR 0006 Amendment Task 2 |
| Section 4.2 family table omits SR | FedRAMP Rev 5 Low includes 11 SR controls in the scaffold; Plan 3 authors them |

## Pre-execution decisions

1. **Authoring order:** CM -> AC -> AU -> IA -> SC -> SI -> RA -> IR -> CP -> CA (Tier 1 + CA promoted) -> AT -> MA -> MP -> PE -> PL -> PS -> SA -> SR (Tier 2).
2. **Two-control Gate 2 shape-check:** CM-2 (base) and IA-5(1) (enhancement). CM has zero enhancements; IA has 7 (the most of any family), making IA-5(1) the highest-coverage enhancement shape-check.
3. **Evidence policy:** catalog-first. Phase 1 dispatches 18 parallel subagents to build per-family catalogs under `docs/plan-3/evidence-catalog/`. Phase 2 authors from catalogs in main session.
4. **Gate 3 spot-check scope:** up to 10 random citations per family, all controls for families with <10 members. Actual total: 144 spot checks.
5. **Implementation Status rubric:** honest per-control. No `alternative`.
6. **Set-params policy:** filled inline with prose, per control. Baseline-mandated values use `inherited` origin; organization-defined use `organization`.
7. **Branch strategy:** direct commits to `main` per ADR 0006 Branch Strategy.
8. **No new pytest tests** (except a single unit test for `docs/plan-3/verify-family.py` per TDD — that test lives in `tests/` and is counted in the regression pass).

## Consequences

**Positive:**

- Plan 3 executes mechanically against the 2026-04-09 design spec and plan, with no mid-plan rediscovery of Plan 2 realignments.
- Every deviation from the 2026-04-07 plan is captured here with the reason, so a reviewer walking the repo chronologically sees the full supersession story.
- The Phase 1 / Phase 2 split gives Plan 3 a durable evidence artifact (the catalogs) independent of the prose, which a reviewer can audit separately from the SSP.

**Negative / accepted:**

- The 2026-04-07 Plan 3 plan file lingers in the parent workspace. The SUPERSEDED banner mitigates this. A cleaner repo would delete the file, but the user direction at Plan 3 kickoff was "leave it, document document document."
- Plan 3 scope is larger than the 2026-04-07 estimate (87 vs ~40 Tier 1). Context budget is correspondingly larger — Plan 3 is sliced into 4 sessions per design section 7.2.

**Risks going into Plan 3 authoring:**

- Trestle 4.0.1 `ssp-assemble` behavior against real control prose is untested. **Mitigation:** Gate 2 two-control shape-check (Task 2).
- Phase 1 subagents could hallucinate evidence paths. **Mitigation:** Gate 3 144-spot-check audit + user review checkpoint.
- FedRAMP-mandated parameter values could be overridden by "homelab cadence." **Mitigation:** Phase 1 subagent obligation to flag baseline-mandated vs organization-defined per parameter, enforced during Gate 3.
- Voice drift across Sessions B/C/D. **Mitigation:** canonical tool-name list + per-session re-read ritual.
- Control-enhancement files have a different frontmatter shape than base controls. **Mitigation:** IA-5(1) is the second of the two Gate 2 shape-check targets.

## Amendments

*(Further deviations discovered during Plan 3 execution that fit this ADR's scope rather than warranting a separate ADR are appended here with date + task reference.)*

(none yet)

---

**Next:** Plan 3 Task 2 (Gate 2 two-control shape-check on CM-2 + IA-5(1)).
