# ADR 0011 -- Plan 4 Complete: Portfolio Ready for Application

**Date:** 2026-04-10
**Status:** Accepted
**Predecessors:** ADRs 0001-0010 (0010 = Plan 4 realignment)
**Supersedes:** none

## Decision

Plan 4 (ConMon writeups + portfolio integration) is complete. The
`homelab-fedramp-low` repository is portfolio-ready for the Rapid7 US
Public Sector Trust, Risk, and Compliance Analyst application. This
ADR captures the done state, the deliverables, and the 10-question
success criteria check from the whole-project design spec Section 1.4.

## Deliverables

### Session 1: ConMon cycles + DRs + SCR (2026-04-10)

- **April 2026 submission package** at `conmon-submissions/2026-04/`:
  16,944 POA&M items (16,944 Open, 72 Critical / 3,254 High / 7,622 Medium
  / 5,996 Low), 7 IIW components (5 Wazuh-agent hosts + OPNsense + MokerLink),
  Wazuh indexer scan evidence for all 5 in-boundary agents, submission README
  with data source attribution.
- **Three Deviation Requests** in `deviation-requests/`:
  - **RA-0001** Grafana exposure risk adjustment (CVSS re-rating with SC-7 /
    AC-3 / IA-2 / AU-2 compensating controls, references real POA&M item UUID
    e19cafa0-bab).
  - **FP-0001** Ubuntu ESM CVE tracker lag false positive (class-based DR
    covering all findings matching the NVD-vs-ESM timing gap pattern).
  - **OR-0001** Shared-tenancy compute on brisket (seven compensating
    controls including the Phase 14 GPU power cap, 6-month review cadence,
    future-state migration plan).
  - Plus a DR README explaining the three FedRAMP DR categories and the
    DR lifecycle.
- **May 2026 submission package** at `conmon-submissions/2026-05/`:
  25,416 POA&M items with **25,414 Open + 1 Completed + 1 Deviated** showing
  three intentionally staged state transitions (finding id=5 mitigated,
  finding id=2 risk-accepted via risk_acceptance id=1, finding id=16945
  synthetic CVE-2026-99999 created). Full diff-vs-April README with honest
  "staged vs organic" callout.
- **SCR-0001** at `significant-changes/SCR-0001-capitol-signals-boundary.md`:
  Three-alternative analysis (status quo / separate host / expand boundary),
  risk delta table, 5 control extensions (AC-3, SC-7, SC-13, AU-2, CM-8).
- **Pipeline enhancement:** `CONMON_MONTH` env var override added to
  `pipelines/cli.py` `_current_month()` for out-of-calendar-month staging.
  Minimal 15-line change, preserves default behavior, validates YYYY-MM
  format. Tests still 136/136 passing.

### Session 2: Diagrams + main writeup (2026-04-10)

- **Boundary diagram** at `docs/diagrams/boundary.mmd` + rendered PNG at
  `docs/diagrams/rendered/boundary.png`. Shows in-boundary (green) vs
  out-of-boundary (tan dashed) components with data flows: customer
  telemetry ingress, admin access path, co-tenant shared compute (OR-0001),
  external backup egress.
- **Pipeline diagram** at `docs/diagrams/pipeline.mmd` + rendered PNG at
  `docs/diagrams/rendered/pipeline.png`. Shows the 5-stage OSCAL-first
  pipeline: ingest -> DefectDojo push -> OSCAL build -> xlsx render ->
  RegScale push.
- **Writeup #1** at `writeups/01-building-fedramp-low-conmon-homelab.md`
  (3,229 words). Uses SI-4 as the hero control (5-layer detection stack,
  ADR 0008 thermal incident as proof of monitoring working under load).
  Includes the April->May diff narrative with all three staged transitions
  called out honestly, explicit "what's real, what's notional" table, and
  a "scope I did not implement" section for transparency.

### Session 3: Paramify comparison + README polish (2026-04-10)

- **Writeup #2** at `writeups/02-paramify-vs-diy.md` (1,805 words).
  Covers Paramify's March 6, 2026 FedRAMP 20x Moderate Authorization (first
  GRC tool to achieve it) and a fair feature comparison vs the
  homelab-fedramp-low pipeline. Honest about what commercial GRC wins
  (multi-user workflow, guided intake, eMASS export, FedRAMP auth as a
  vendor reference, vendor support) and what DIY wins (data ownership,
  learning depth, OSCAL-native from day one). All Paramify facts sourced
  from public paramify.com blog posts and the FedRAMP Marketplace listing.
- **Polished public README** with the 60-second recruiter test structure:
  boundary diagram hero image, what's-real-vs-notional table, 12-row quick
  tour, tooling inventory (including the three not-evaluated commercial
  platforms called out for honesty), three reading paths
  (60s / 10min / technical reviewer), writeups section, pipeline
  architecture diagram, ADR chain pointer. Scrubbed Unicode em dash from
  previous Plan 1 stub per feedback rule.

### Session 4: Final validation (2026-04-10)

- **This ADR (0011)** capturing Plan 4 completion.
- **Git tag** `plan-4-complete` on the final commit.

Note: job-application materials (resume bullet, cover letter paragraph,
LinkedIn copy) were authored during Plan 4 but kept private. They live
outside this public repo.

## 10-question success criteria (from whole-project design Section 1.4)

A GRC-literate reviewer should be able to answer each of these from the
repo alone in under 10 minutes:

1. **What's the authorization boundary?**
   `docs/diagrams/rendered/boundary.png` (embedded in README) plus
   SSP Section 9. Green = in, tan dashed = out. Seven mentions of the GCP VM
   across SSP sections, zero IIW rows, is the boundary working correctly.

2. **What baseline and why?**
   FedRAMP Low (156 controls from NIST 800-53 Rev 5). FIPS 199 rationale
   in the design spec Section 2.1: no PII/PHI/CUI/financial data processed,
   advisory-only telemetry, 99% monthly availability target.

3. **Show me one control implementation end-to-end.**
   `trestle-workspace/mss-ssp/si/si-4.md` (the writeup hero control, full
   5-layer detection stack) or `trestle-workspace/mss-ssp/au/au-2.md` (the
   simpler worked example).

4. **How does a finding become a POA&M item?**
   Plan 2 pipeline flow: `pipelines/ingest/wazuh_vulns.py` (Wazuh Indexer
   -> normalized Finding) -> `pipelines/push/defectdojo.py` (DefectDojo
   import-scan) -> `pipelines/build/oscal_poam.py` (DefectDojo findings ->
   OSCAL POA&M JSON) -> `pipelines/render/poam.py` (OSCAL -> FedRAMP Rev 5
   xlsx). Schema-validated at every stage.

5. **What happens when you can't fix something?**
   `deviation-requests/` has samples of all three FedRAMP DR categories:
   RA-0001 (Risk Adjustment), FP-0001 (False Positive), OR-0001
   (Operational Requirement).

6. **How do you know a POA&M item is really closed?**
   Verify-before-close discipline documented in the May submission README
   and the main writeup. A POA&M item is Completed when `is_mitigated=True`
   in DefectDojo; the OSCAL POA&M builder emits `poam-state: Completed` only
   if the next scan confirms the finding is absent.

7. **What's your OSCAL output?**
   `oscal/` directory: catalog (NIST imported), profile (FedRAMP Rev 5 Low),
   component-definition.json (7 components), poam.json (25,416 items),
   ssp.json (156 controls). The assembled SSP passes
   `trestle validate -f system-security-plans/mss-ssp/system-security-plan.json`.
   POA&M and component-definition are hand-built by the pipeline and are
   valid OSCAL 1.1.2 JSON.

8. **What's missing / would you do differently?**
   Called out explicitly in the main writeup "Scope I did not implement"
   section: POA&M-from-SSP-planned-controls linkage (deferred), the
   import-scan pile-up cross-engagement dedup (documented in May submission
   README as a structural pipeline change deferred to next ConMon milestone),
   3PAO simulation (theatrical), ServiceNow GRC and Onspring (not evaluated),
   AWS scale-out (one-paragraph appendix in the design spec).

9. **Where's the monthly rhythm?**
   `conmon-submissions/2026-04/` and `conmon-submissions/2026-05/` with
   full README diff narrative. Three intentional state transitions visible
   in the OSCAL output via the `poam-state` prop.

10. **How would this scale to Moderate or multi-system?**
    SCR-0001 demonstrates boundary evolution (proposing to add Capitol
    Signals API as a second in-scope service). The whole-project design
    Section 1.5 explicitly scopes out Moderate and High baselines. The
    Paramify comparison writeup discusses the multi-system management
    gap as a commercial-platform strength.

All 10 questions are answerable from the repo. Project is done.

## Final validation check

- **Test suite:** 136 passed (unchanged from Plan 3; `CONMON_MONTH` addition
  preserved all existing test assertions)
- **Trestle ssp-assemble:** OK, produces `oscal/ssp.json` successfully
- **Trestle validate on assembled SSP:** VALID
  (`system-security-plans/mss-ssp/system-security-plan.json`)
- **OSCAL artifact integrity:** all 3 OSCAL JSON files are valid JSON
  with correct OSCAL metadata containers (SSP 1.2.1,
  component-definition 1.1.2, POA&M 1.1.2)
- **Secret scan:** no hardcoded credentials in committed files; `.env.example`
  contains only empty placeholders; scan-evidence JSON matches are CVE
  description text, not secrets
- **Em dash check:** no Unicode U+2014 in any authored file (writeups, DRs,
  SCR, READMEs, application materials, this ADR) per feedback rule

## Open follow-ups (intentionally deferred from Plan 4)

These are documented here rather than addressed inside the plan, because
they were out of scope for the portfolio-ready milestone:

1. **Import-scan pile-up fix:** structural pipeline change to use a single
   rolling engagement per product instead of per-month engagements. Deferred
   to the next ConMon milestone; the May submission README documents the
   limitation honestly.
2. **POA&M from SSP Planned controls:** the current POA&M pipeline sources
   only from DefectDojo findings. SSP controls marked `Planned` do not flow
   into the POA&M as distinct items. Documented as a scope boundary in the
   main writeup Section 9.
3. **Screenshots for writeup illustration** (Task 11 of Plan 4): requires
   manual browser interaction and is blocked on subagent/Bash environment
   limitations on Windows. Deferred to operator. The Mermaid diagrams
   (boundary + pipeline) provide the core visual evidence that the writeups
   reference.
4. **Astro cross-posts** (Task 16 of Plan 4): `brianchaplow-astro` and
   `bytesbourbonbbq-astro` are separate repos. The writeup markdown is
   committed in this repo; the cross-post step is a copy-and-frontmatter
   operation that the operator will perform outside Plan 4.

## Public artifacts

- **Repo:** [github.com/brianchaplow/homelab-fedramp-low](https://github.com/brianchaplow/homelab-fedramp-low)
- **Main writeup:** `writeups/01-building-fedramp-low-conmon-homelab.md` (3,229 words)
- **Paramify comparison:** `writeups/02-paramify-vs-diy.md` (1,805 words)

## Application target

Rapid7 US Public Sector Trust, Risk, and Compliance Analyst (Continuous
Monitoring and POA&M role). Five named GRC platforms in the job
description: RegScale (deployed), DefectDojo (deployed), Paramify
(comparison post), ServiceNow GRC (acknowledged not evaluated), Onspring
(acknowledged not evaluated).

## Notes

- Every plan (1, 2, 3, 4) ran in a single execution session, which is the
  intended cadence for the pilot. The full ADR chain captures every
  execution decision and deviation from the original plans.
- The "what's real, what's notional" transparency pattern is load-bearing.
  Undisclosed staging would undermine the entire portfolio; disclosed
  staging strengthens it.
- This is the final ADR of Plan 4. The next ADR (0012 or later) will
  belong to post-portfolio work (e.g. the actual job application
  post-mortem, or a next-milestone plan).
