# ADR 0007 — Plan 2 Pipelines Complete

**Date:** 2026-04-09
**Status:** Accepted
**Plan:** [2026-04-07 Plan 2 — OSCAL Foundation + Pipelines](../superpowers/plans/2026-04-07-homelab-fedramp-low-plan-2-oscal-pipelines.md)
**Predecessors:** ADR 0001 (pre-flight), 0002 (Plan 1 deployment), 0003
(RegScale install), 0004 (DefectDojo install), 0005 (PBS backup gap),
0006 (Plan 2 environment + API realignment — the authoritative
deviation record for this plan)

## Decision

Plan 2 (OSCAL Foundation + Pipelines) is **complete**. Every done
criterion from the plan has a verified implementation, a passing
test, and a live end-to-end run against the homelab SOC. The repo
tags the milestone as `plan-2-complete` and the next phase (Plan 3 —
SSP Authoring) is unblocked.

## Done criteria — verified

- [x] **NIST 800-53 Rev 5 catalog** imported via Trestle
  (`trestle-workspace/catalogs/nist-800-53-rev5/catalog.json`, 10.7 MB)
  and mirrored to `oscal/catalog/`. `trestle validate` VALID. Plan 2
  Task 2.
- [x] **FedRAMP Rev 5 Low profile** bootstrapped from the
  `compliance-trestle-fedramp` plugin XML (the upstream
  `GSA/fedramp-automation` repo was deleted before Plan 2 executed —
  see ADR 0006 Deviation 11) and committed at
  `trestle-workspace/profiles/fedramp-rev5-low/profile.json`. 156
  `<with-id>` references preserved, VALID. Plan 2 Task 3.
- [x] **SSP markdown scaffold** generated with 156 control files
  under `trestle-workspace/mss-ssp/` (top-level dir, not nested
  under `system-security-plans/` — see ADR 0006 Amendment 2026-04-09
  Task 4). Mirrored to `ssp/controls/` for public-repo visibility.
  Plan 2 Task 4.
- [x] **Common pipeline modules** (`pipelines/common/config.py`,
  `logging.py`, `schemas.py`) per ADR 0006 Deviations 3 + 4.
  Hybrid env var strategy: architectural constants in code,
  secrets required from `.env`. HTTPS validator scoped to Wazuh
  endpoints only. Plan 2 Task 5.
- [x] **Wazuh REST client** (`pipelines/common/wazuh.py`) without
  `get_vulnerabilities()` — Wazuh 4.8 removed that endpoint per
  ADR 0006 Deviation 5. Plan 2 Task 6.
- [x] **Wazuh Indexer (OpenSearch) client**
  (`pipelines/common/wazuh_indexer.py`) — new module per ADR 0006
  Deviation 5. Pages through
  `wazuh-states-vulnerabilities-*` via `search_after` with `_id`
  tiebreaker (ADR 0006 Amendment Task 6b). Plan 2 Task 6b.
- [x] **Inventory ingestion** (`pipelines/ingest/inventory.py`):
  Wazuh syscollector + `inventory/overlay.yaml` → list of
  `InventoryComponent`. Live run produces 7 in-boundary components
  (5 Wazuh agents + opnsense + mokerlink). Plan 2 Task 7.
- [x] **OSCAL component-definition builder**
  (`pipelines/build/oscal_component.py`): emits every
  `InventoryComponent` field as an OSCAL prop (empty-string props
  omitted to satisfy the `^\S(.*\S)?$` schema regex) and maps
  `asset_type` + `is_virtual` to OSCAL component type
  (`hardware` / `software` / `network`). Plan 2 Task 8.
- [x] **IIW xlsx renderer** (`pipelines/render/iiw.py`): column
  layout verified against live Rev 5 template row 2 on 2026-04-09.
  Data lands in the `Inventory` sheet starting at row 13 (after
  the header + guidance + example rows). Booleans coerced to
  Yes/No. First April 2026 IIW committed at
  `inventory/IIW-2026-04.xlsx` (178 KB, 7 rows). Plan 2 Task 9.
- [x] **Wazuh vulnerability ingest**
  (`pipelines/ingest/wazuh_vulns.py`): reads the indexer via
  `WazuhIndexerClient.search_vulnerabilities` and emits normalized
  `Finding` records. Live run: 8,471 findings across 5 agents
  (brisket 2804, haccp 1899, regscale 1861, dojo 1861, smokehouse
  46). Severity resolution prefers Wazuh's own label and falls
  back to `severity_from_cvss` when missing. Every finding links
  to RA-5 + SI-2. Plan 2 Task 10.
- [x] **DefectDojo client + push pipeline**
  (`pipelines/common/defectdojo.py`,
  `pipelines/push/defectdojo.py`): Token-header auth, auto-paginated
  `list_findings` (1000-row page cap), auto-create engagement per
  product. `findings_to_generic_format` sends the affected host
  through the `endpoints` list — DefectDojo Generic Findings Import
  rejects a top-level `host` field (probed live 2026-04-09, returned
  "Not allowed fields are present: ['host']"). Live end-to-end:
  8,471 findings pushed to 4 products with zero skipped. Plan 2 Task 11.
- [x] **OSCAL POA&M builder** (`pipelines/build/oscal_poam.py`):
  FedRAMP Low ConMon SLA windows corrected from the plan text's
  wrong values (30/90/180/365) to the real values from the FedRAMP
  ConMon Strategy Guide (15/30/90/180). See ADR 0006 Amendment
  2026-04-09 Task 12. State mapping priority order: false-positive
  > risk-accepted > mitigated > active > closed. Plan 2 Task 12.
- [x] **POA&M xlsx renderer** (`pipelines/render/poam.py`): writes
  into the `Open POA&M Items` sheet starting at row 8. Internal
  `Medium` severity maps to `Moderate` for the template's
  Original Risk Rating dropdown. poam-state `False Positive` flips
  the False Positive column to Yes. Live April POA&M committed at
  `poam/POAM-2026-04.xlsx` (4.9 MB, 8,473 items). Plan 2 Task 13.
- [x] **End-to-end orchestration via `pipelines.sh` passthrough**
  (`pipelines/cli.py`, `pipelines.sh`, Task 14): Click CLI with
  seven subcommands + two composites (`oscal`, `conmon`). Unknown
  `pipelines.sh` commands forward to `pipelines.cli` via a
  passthrough arm per ADR 0006 Deviation 2 — the Makefile stays a
  thin alias from Plan 1, not rewritten. `HOST_TO_PRODUCT` uses
  ASCII hyphens and 6 entries including `opnsense → MSS Boundary
  Protection - OPNsense` per ADR 0006 Amendment 2026-04-09 Task 1.
  All Unicode arrows replaced with ASCII `->` to avoid Windows
  cp1252 encode errors on Python 3.14.
- [x] **Trestle `ssp-assemble` wrapper**
  (`pipelines/build/oscal_ssp.py`): subprocess call with
  absolute-path `trestle.exe` discovery (Git Bash on Windows does
  not have the venv on PATH). Live assembly against the empty
  156-control scaffold produced a syntactically valid
  SystemSecurityPlan with 156 `implemented_requirements` all
  carrying `REPLACE_ME` placeholders. Plan 3 can fill them
  incrementally. Output at `oscal/ssp.json` (69 KB). Plan 2 Task 15.
- [x] **RegScale CE OSCAL push (best-effort)**
  (`pipelines/common/regscale.py`, `pipelines/push/regscale.py`):
  JWT client per ADR 0006 Deviation 7. Swagger probe 2026-04-09
  confirmed CE has **no generic OSCAL import endpoints** — the 13
  OSCAL-prefixed paths are all export or validation.
  `OSCAL_IMPORT_PATHS` is therefore empty today and every push
  returns `status="manual-required"` pointing at
  `runbooks/regscale-manual-import.md`. When a future CE release
  ships generic import endpoints, populating the dict switches the
  pipeline automatically. Plan 2 Task 16.
- [x] **Done-criteria smoke and ADR** (this document). Every
  pipeline subcommand was exercised against live infrastructure
  during Plan 2 execution; the test suite is 130 passed; all 5
  OSCAL artifacts validate via `trestle.oscal.*.oscal_read`. Plan 2
  Task 17.

## Final artifact inventory

| Artifact | Path | Size | Items |
|----------|------|------|-------|
| NIST 800-53 Rev 5 catalog | `trestle-workspace/catalogs/nist-800-53-rev5/catalog.json` | 10.7 MB | ~1,100 controls |
| FedRAMP Rev 5 Low profile | `trestle-workspace/profiles/fedramp-rev5-low/profile.json` | 4.6 KB | 156 controls |
| Component-definition | `oscal/component-definition.json` | 16 KB | 7 components |
| IIW xlsx | `inventory/IIW-2026-04.xlsx` | 178 KB | 7 rows |
| SSP (scaffold) | `oscal/ssp.json` | 70 KB | 156 controls (placeholders) |
| POA&M | `oscal/poam.json` (gitignored) | 16.8 MB | 8,473 items |
| POA&M xlsx | `poam/POAM-2026-04.xlsx` | 4.9 MB | 8,473 rows |

Test suite: **130 passed** across 16 test files (config, logging,
schemas, wazuh client, wazuh indexer, inventory ingest, OSCAL
component, OSCAL POA&M, OSCAL SSP, IIW render, POA&M render,
DefectDojo client/push, RegScale client/push, CLI).

## Commits on main for Plan 2

- 8847706 Plan 2 Task 1: verify Plan 1 done state + interim PBS tripwire
- 7718629 Plan 2 Task 2: import NIST SP 800-53 Rev 5.2.0 catalog
- 8d12090 Plan 2 Task 3: bootstrap FedRAMP Rev 5 Low profile
- 6a74d59 Plan 2 Task 4: generate 156-control SSP markdown scaffold
- dfff17e docs: ADR 0006 amendments from Tasks 2-4
- 0de9071 Plan 2 Task 5: common pipeline modules
- e1e10bb Plan 2 Task 6: Wazuh API REST client (no vuln methods)
- c421437 Plan 2 Task 6b: Wazuh Indexer (OpenSearch) client
- (Task 7)  Plan 2 Task 7: inventory ingestion
- 30c2969 Plan 2 Task 8: OSCAL component-definition builder
- b379c9e Plan 2 Task 9: IIW xlsx renderer
- 4703274 Plan 2 Task 10: Wazuh vulnerability ingest via indexer
- (Task 11) Plan 2 Task 11: DefectDojo client + push pipeline
- fe3e4c9 Plan 2 Task 12: OSCAL POA&M builder
- 43862d7 Plan 2 Task 13: POA&M xlsx renderer
- d99e0da Plan 2 Task 14: end-to-end orchestration via pipelines.sh passthrough
- 217e1e1 Plan 2 Task 15: Trestle ssp-assemble wrapper
- (Task 16) Plan 2 Task 16: RegScale CE OSCAL push + manual runbook
- (this ADR) Plan 2 Task 17: done-criteria smoke + ADR 0007

## Live deliverables vs. Plan 2 scope

Plan 2 is bounded — it lays the pipeline rails without filling the
SSP control prose. Specifically:

- The SSP is a 156-control skeleton with `REPLACE_ME` placeholders.
  Plan 3 fills the prose (Tier 1 ~40 detailed control
  implementations, Tier 2 ~116 stubs).
- The POA&M represents every open Wazuh finding on in-boundary
  hosts. A real 3PAO-ready POA&M would deduplicate per-CVE across
  hosts, resolve vendor dependencies, and include remediation
  plans — all Plan 3/4 work.
- RegScale ingestion is a manual runbook today because CE exposes
  no generic OSCAL import. A future CE upgrade unlocks the
  automated push path.
- The FedRAMP submission scrub (delete rows 3-12 + col A from the
  IIW, for example) is a documented manual step. Plan 4 can add an
  automated scrub step if the portfolio demo warrants it.

None of these are regressions — they are intentional scope edges
called out in ADR 0006 and in the module docstrings.

## Next

**Plan 3 — SSP Authoring.** Populate the 156 control markdown
files under `trestle-workspace/mss-ssp/` with prose grounded in
the live homelab implementation. Tier 1 priority families per
ADR 0006 roadmap: AC, AU, CM, CP, IA, IR, RA, SC, SI. Tier 2 is
stub prose for the remaining families. The goal state is a
`trestle author ssp-assemble` run that produces an SSP JSON a
3PAO would read without immediately flagging placeholder content.

## Consequences

**Positive:**

- The monthly ConMon cycle is now a single `./pipelines.sh conmon`
  command. Every artifact a 3PAO asks for is generated from live
  homelab state — no manual data entry.
- Every deviation from the plan text is captured in ADR 0006 with
  live-probe evidence, so a reviewer walking the repo
  chronologically can reconstruct the exact decisions made during
  execution.
- The test suite is a real regression safety net. Every pipeline
  module has pytest coverage of both the happy path and the failure
  modes discovered during live smoke (Wazuh `vulnerability.id`
  keyword quirk, DefectDojo `host` field rejection, RegScale
  `username` field name, etc.).

**Negative / accepted:**

- Plan 2 is significantly larger than the plan text suggested.
  The ADR 0006 realignment added Task 6b, grew Task 8's prop list,
  added pagination to `list_findings`, flipped the SLA windows, and
  built a manual runbook fallback for RegScale. The net is
  ~130 tests instead of the ~20 the plan text implied.
- The POA&M JSON is 16.8 MB, gitignored, regenerated per cycle.
  The rendered xlsx (4.9 MB) is the shippable portfolio artifact.
- Windows + Python 3.14 required three compatibility fixes not in
  the plan text: cp1252 arrow replacement, `trestle.exe` absolute
  path discovery, and pydantic.v1 compat warnings (cosmetic, but a
  Python 3.16 tripwire is documented in ADR 0006 Task 2 amendment).

**Risks going into Plan 3:**

- Trestle 4.0.1 `ssp-assemble` behavior with real control prose
  (as opposed to `REPLACE_ME` placeholders) is untested — Plan 3
  Task 1 should run an early assembly against a single filled
  control to catch any shape surprises.
- DefectDojo findings pile up per run because the import-scan
  endpoint creates a new Test each time, not a dedup-merge. Plan 3
  or Plan 4 should add a pre-import cleanup or switch to
  reimport-scan.
- OSCAL schema drift if Trestle upgrades; the OSCAL round-trip
  test in `tests/test_oscal_roundtrip.py` is the early-warning
  tripwire.
