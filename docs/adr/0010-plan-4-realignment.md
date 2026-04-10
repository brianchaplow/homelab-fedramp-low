# ADR 0010 -- Plan 4 Lightweight Realignment

**Date:** 2026-04-10
**Status:** Accepted
**Context:** Plan 4 (ConMon Writeups + Portfolio Integration) pre-execution realignment
**Predecessors:** ADR 0001-0009. ADR 0009 is the Plan 3 completion record.

## Decision

The 2026-04-07 Plan 4 plan (`docs/superpowers/plans/2026-04-07-homelab-fedramp-low-plan-4-conmon-writeups-portfolio.md` in the parent workspace) is structurally sound but has the same mechanical staleness as every pre-execution plan in this project (WSL refs, make refs, stale paths). Unlike Plan 3's full supersession (ADR 0008), Plan 4's scope is correct -- only environmental references need updating. This ADR applies the corrections without a new plan file.

The whole-project design `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` sections 6 and 8 remain the authoritative spec for Plan 4.

## Mechanical substitutions (same as ADR 0006)

| Plan 4 text | Actual |
|---|---|
| `[wsl]` | `[gitbash]` -- Git Bash on Windows, Python 3.14 native |
| `make <target>` | `./pipelines.sh <target>` |
| `ssp/controls/` | `trestle-workspace/mss-ssp/` |
| `.venv/bin/python` | `.venv/Scripts/python.exe` |
| `.venv/bin/pytest` | `.venv/Scripts/pytest.exe` |
| `~/homelab-fedramp-low/` | `/c/Projects/homelab-fedramp-low` |
| Test baseline: 130 | Test baseline: **136** (Plan 3 added 6 verify-family tests) |

## Scope decisions (from Plan 4 brainstorming 2026-04-10)

### 1. May ConMon cycle: manually staged transitions

The May 2026 cycle uses manually staged state transitions in DefectDojo before running `./pipelines.sh conmon`:
- **Close one finding:** mark a specific DefectDojo finding as mitigated (e.g., a patched CVE on one host)
- **Introduce one finding:** create a synthetic finding (e.g., a new CVE discovered on a package)
- **Deviate one finding:** risk-accept a finding for the OR-0001 shared-tenancy DR

Then run the pipeline to produce the May submission package from the staged state. The April-to-May diff is controlled and narratively clean for the writeup.

### 2. Priority order

1. ConMon cycles + DRs + SCR (artifacts a GRC reviewer reads first)
2. Writeup #1: "Building a FedRAMP Low ConMon Program in a Homelab" (~2500-3500 words)
3. Writeup #2: "Paramify vs. DIY" (~1500 words, requires WebSearch for Paramify public docs)
4. README overhaul + resume bullet + LinkedIn + cover letter paragraph

### 3. Paramify writeup: must-have, full treatment

The Paramify comparison is in scope with full WebSearch research. It is the lowest-priority deliverable but a must-have for the application (job listing references 5 GRC platforms). Written last -- if a session boundary hits, the main writeup + ConMon package is already a complete application.

## Deferred items from Plan 3 addressed in Plan 4

- **DefectDojo import-scan pile-up (ADR 0007 Risk #2):** investigate during May cycle staging. If `reimport-scan` works, switch. Otherwise document as a known limitation.
- **POA&M-from-SSP-planned-controls:** document as a known scope boundary in the main writeup section 9, not implement as code. The current POA&M pipeline sources from DefectDojo findings only.

## Consequences

**Positive:**
- Plan 4 executes immediately from the existing plan with this ADR's corrections applied. No new plan file, no supersession banner, no blocked session on design/planning.
- Every scope decision is captured with rationale, continuing the transparency pattern from ADRs 0006-0009.

**Negative / accepted:**
- The 2026-04-07 Plan 4 plan has stale environmental references that a reader must mentally substitute. This ADR is the substitution key.
- The manually staged May cycle is honest (documented as staged) but not purely organic. The writeup will call this out per the design spec's "what's real, what's notional" section.

---

**Next:** Plan 4 Task 1 (verify Plan 3 done state, then begin April submission package assembly).
