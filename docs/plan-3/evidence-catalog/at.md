# AT — Awareness and Training Evidence Catalog

**Family:** AT (Awareness and Training)
**Controls cataloged:** 5 (AT-1, AT-2, AT-2(2), AT-3, AT-4)
**Produced:** 2026-04-09 (Plan 3 Phase 1 subagent)
**Profile baseline:** FedRAMP Rev 5 Low (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`)

---

> **Single-operator context:** MSS is a personal homelab with one operator (Brian Chaplow). There is no organizational workforce, no HR function, and no second user with system access. This context is the primary determinant of status for every AT control. Where a control has a meaningful homelab analog, that analog is documented honestly. Where no analog exists, the status is `not-applicable` with a justification sentence rather than an unsupported claim.

---

## AT-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** This SSP (`trestle-workspace/mss-ssp/`) functions as the system-level awareness and training policy document for the MSS homelab. The SSP establishes the scope, purpose, and operator responsibilities for the single-person system. No separate awareness-and-training policy document exists, and none is needed given the single-operator model; the SSP + the `homelab-fedramp-low` git history serve as the combined policy and procedure record. The operator (Brian Chaplow) is explicitly designated as the sole person responsible for development, documentation, and dissemination of all awareness and training material, which in this context is self-authored.
- **Supporting mechanisms:** The `homelab-fedramp-low` git repository on `main` records every policy decision and deviation via ADRs (`docs/adr/0001–0008`). ADR 0008 explicitly captures the Plan 3 authoring decisions that govern how this SSP is reviewed and updated. The `runbooks/monthly-conmon.md` defines the review cadence tied to the monthly ConMon cycle.
- **Evidence paths:**
  - `homelab-fedramp-low/trestle-workspace/mss-ssp/at/at-1.md` (scaffold with `x-trestle-set-params` — Plan 3 fills prose)
  - `homelab-fedramp-low/docs/adr/0008-plan-3-pre-execution-realignment.md` (pre-execution decision log — serves as update trigger record)
  - `homelab-fedramp-low/runbooks/monthly-conmon.md` (review cadence anchor; ConMon cycle = policy review frequency)
  - `C:/Projects/CLAUDE.md` lines 1–10 (owner, last-updated date — policy metadata)
  - `homelab-fedramp-low/README.md` (public-facing policy statement and scope narrative)
- **Set-params (proposed values):**
  - `at-01_odp.01` (personnel/roles for dissemination): `["Brian Chaplow (system owner, sole operator)"]`, `organization` — single operator, self-disseminated
  - `at-01_odp.02` (personnel/roles for dissemination, procedures): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `at-01_odp.03` (official designated to manage): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `at-01_odp.04` (policy review frequency): `annually or when a new ADR records a scope or architecture change`, `organization` — no baseline-mandated frequency in FedRAMP Low profile; organization-defined
  - `at-01_odp.05` (events triggering policy update): `"new ADR filing, phase completion, or architecture change"`, `organization`
  - `at-01_odp.06` (procedures review frequency): `annually or when a new ADR records a scope or architecture change`, `organization`
  - `at-01_odp.07` (events triggering procedures update): `"new ADR filing, phase completion, or architecture change"`, `organization`
  - `at-01_odp.08` (policy level — org/mission/system): `system-level`, `organization` — single-system personal homelab; no org-level or mission-level program applicable
- **Authoring notes:** Status is `partial` rather than `implemented` because the AT policy is embedded in the SSP rather than a standalone policy document. The gap is honest and defensible: NIST guidance acknowledges that policy can be part of the general security plan. Lead paragraph on SSP-as-policy; second paragraph citing the ADR chain as the update procedure record. Reference `C:/Projects/CLAUDE.md` "Updated: 2026-04-08" as the observable last-review date.

---

## AT-2 Literacy Training and Awareness

- **Status:** partial
- **Primary mechanism:** The operator maintains continuous security literacy through active operation of the homelab SOC — a working Wazuh SIEM, OpenCTI v7 threat intelligence platform (6 connectors ingesting MITRE ATT&CK, AbuseIPDB, and threat-feed data), ELK threat-intel dashboards, Shuffle SOAR workflows, and a Phase 14 Logstash enrichment pipeline that surfaces novel entities and TI matches daily. This operational exposure constitutes continuous informal literacy training: every Wazuh alert reviewed, every OpenCTI indicator enriched, and every ADR authored requires applying and updating security knowledge. The WF10 morning briefing (Shuffle cron 0530 EST, posting to `#morning-briefing` via `$discord_webhook_briefing`) delivers a nightly threat summary derived from the `logs-zeek.haccp-default-*` data stream, reviewed each day by the operator.
- **Supporting mechanisms:** OpenCTI IOC sync cron (`0 */6 * * *`) pushes threat indicators to Wazuh CDB lists and to the haccp `opencti-threat-intel` ELK index, maintaining live awareness of current threat actor IOCs. The Grafana SOC v3 Overview dashboard and the `build-threat-intel-soc.py` Grafana dashboard expose threat-intel match rates for daily review. No formal training course exists; no annual completion record is generated. The gap is that awareness is continuous and operationally driven, not time-bounded with a completion attestation.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` lines 29–34 (Phase 14 nightly briefing at 0515, WF10 morning briefing, OpenCTI v7 6 connectors)
  - `C:/Projects/CLAUDE.md` lines 127–133 (OpenCTI IOC sync crons, WF10 cron schedule)
  - `C:/Projects/brisket-setup/monitoring/build-threat-intel-soc.py` (Grafana threat-intel dashboard — `DASHBOARD_UID = "threat-intel-soc"`, queries `opencti-threat-intel` index — verified present)
  - `homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` (RegScale EULA review — example of operator reading and acting on policy/advisory material)
  - `homelab-fedramp-low/runbooks/monthly-conmon.md` (ConMon cycle = scheduled review event; interim daily PBS tripwire as awareness habit)
  - `homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (live incident: operator discovered, diagnosed, and fixed a security-relevant configuration failure — applied literacy)
- **Set-params (proposed values):**
  - `at-02_odp.01` (frequency for recurring training): `"continuous — operator reviews WF10 morning briefing daily and reviews Wazuh/OpenCTI alerts as part of normal SOC operations"`, `organization` — no baseline-mandated frequency in FedRAMP Low profile
  - `at-02_odp.02` (personnel/roles receiving training): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `at-02_odp.03` (events triggering training): `"new phase completion, significant security incident, new CVE class introduced to the environment"`, `organization`
  - `at-02_odp.04` (personnel/roles for event-based training): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `at-02_odp.05` (awareness techniques): `"daily WF10 morning briefing (Discord #morning-briefing), OpenCTI IOC sync every 6 hours, Grafana threat-intel dashboard review, ADR authoring as incident-learning record"`, `organization`
  - `at-02_odp.06` (content update frequency): `"updated continuously via OpenCTI connector feeds and ADR filings"`, `organization`
  - `at-02_odp.07` (events triggering content update): `"new security incident, new phase adding in-boundary components, significant CVE advisory"`, `organization`
- **Authoring notes:** Status is `partial` because the awareness mechanism is real and live but there is no formal attestation-style training completion record or scheduled course. Lead paragraph makes the operational-exposure argument explicitly. Second paragraph names the gap (no annual completion attestation) and connects to AT-4 (git history as surrogate record). Cite ADR 0005 as a concrete incident that demonstrates the operator applied security awareness to identify and fix a configuration failure.

---

## AT-2(2) Insider Threat

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. The MSS homelab is a single-operator personal system. Insider threat as a control concept presupposes a multi-person workforce where one member could act against organizational interests without detection by others. With exactly one operator who is also the system owner, the ISSO, and the AO-equivalent, there is no distinct insider-versus-organization dynamic. No training program on recognizing insider-threat indicators is meaningful in this context.
- **Supporting mechanisms:** N/A
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` lines 71–81 (host inventory — confirms single operator with no other personnel having system access)
  - `homelab-fedramp-low/README.md` (author statement: "I'm a 27-year veteran… building FedRAMP-specific ConMon fluency")
- **Set-params (proposed values):**
  - No ODP parameters in scaffold (`at-2.2` has no `x-trestle-set-params` frontmatter — verified in `trestle-workspace/mss-ssp/at/at-2.2.md`)
- **Authoring notes:** One clean sentence: N/A because single-operator system eliminates the insider-versus-organization threat model. Do not overexplain. The README and CLAUDE.md host inventory are the supporting evidence that only one person has access.

---

## AT-3 Role-Based Training

- **Status:** partial
- **Primary mechanism:** All roles that exist in the MSS homelab — system owner, ISSO, system administrator, SOC analyst, incident responder, vulnerability manager, and assessment coordinator — are held by a single person: Brian Chaplow. Role-based training is fulfilled through operational mastery and self-directed study specific to each role. As system administrator, the operator maintains 15 Wazuh agents, manages Proxmox VMs, and resolves infrastructure failures (e.g., ADR 0005 PBS automount, ADR 0003 RegScale install deviation). As SOC analyst, the operator reviews Wazuh alerts, tunes detection rules, and operates the Shuffle SOAR pipeline daily. As ISSO and assessment coordinator, the operator authored this SSP, built the OSCAL ConMon pipelines (Plan 2), and executed the FedRAMP Low ConMon program. The depth of homelab build — 15 phases of live infrastructure completed — is the auditable record of role-specific competence.
- **Supporting mechanisms:** The Phase 14 Zeek + Logstash enrichment pipeline, Velociraptor DFIR enrollment of 7 clients, Caldera v5.3.0 adversary simulation, and ML pipeline (XGBoost PR-AUC 0.9998) each represent role-specific training artifacts for the SOC analyst and DFIR responder roles. The `homelab-fedramp-low` git history and ADR chain (0001–0008) document role-specific decisions made under real operational conditions. No third-party course completion certificate exists; the homelab build record is the training artifact.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` lines 15–30 (v3 Migration Status table — 14 phases complete; each phase = role-based competency exercise)
  - `homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` (ISSO / AO role: EULA review, pre-flight verification)
  - `homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (sysadmin role: infrastructure failure detection and fix)
  - `homelab-fedramp-low/docs/adr/0006-plan-2-environment-and-api-realignment.md` (assessment coordinator role: ConMon pipeline realignment)
  - `homelab-fedramp-low/docs/adr/0007-plan-2-complete.md` (full pipeline authorship — SOC analyst + OSCAL engineer roles evidenced)
  - `C:/Projects/reference/phase14/zeek/local.zeek` (SOC analyst / network analyst role: Zeek configuration — verified present)
- **Set-params (proposed values):**
  - `at-03_odp.01` (roles/responsibilities receiving training): `["Brian Chaplow — system owner, ISSO, system administrator, SOC analyst, incident responder, vulnerability manager, assessment coordinator (all roles held by sole operator)"]`, `organization`
  - `at-03_odp.02` (personnel/roles for training): `["Brian Chaplow (sole operator)"]`, `organization`
  - `at-03_odp.03` (frequency for recurring role-based training): `"continuous — operational homelab activity serves as ongoing role-based training"`, `organization` — no baseline-mandated frequency in FedRAMP Low profile
  - `at-03_odp.04` (training content update frequency): `"updated with each new phase completion or ADR filing"`, `organization`
  - `at-03_odp.05` (events triggering content update): `"new phase, new in-boundary component, security incident requiring new role skill"`, `organization`
- **Authoring notes:** Status is `partial` rather than `implemented` because there is no pre-access role-based training attestation (the control says "before authorizing access"). The operator self-authorizes; there is no distinct authorization event. Lead paragraph on single-operator role consolidation; second paragraph on the ADR + phase-completion chain as the training record. Cite ADR 0005 as the sysadmin-role training example where a real infrastructure failure was independently identified and resolved.

---

## AT-4 Training Records

- **Status:** partial
- **Primary mechanism:** The `homelab-fedramp-low` git repository on GitHub (`github.com/brianchaplow/homelab-fedramp-low`) is the training record for this system. Every ADR filed documents a learning event: a deviation discovered, a technology researched, a decision made under real operational conditions. The git commit log provides immutable, timestamped evidence of when each learning event occurred and what decision followed. This is the single-operator equivalent of a training completion database: rather than course completion records in an LMS, the repo contains 8 ADRs filed between 2026-04-08 and 2026-04-09, each recording the operator's applied decision-making under the relevant role. The `C:/Projects/CLAUDE.md` project ledger (updated 2026-04-08) records phase completion dates as additional time-stamped training milestones.
- **Supporting mechanisms:** The `homelab-soc-portfolio/` repo (referenced in `C:/Projects/CLAUDE.md`) provides additional public portfolio evidence of training artifact retention across Phases 1–14 (configs, workflow descriptions, model cards). No centralized training management system (TMS/LMS) exists; git is the durable record. Retention is indefinite while the repository exists on GitHub; no data-retention cutoff applies in a personal homelab context.
- **Evidence paths:**
  - `homelab-fedramp-low/docs/adr/` directory (8 ADR files, all timestamped — verified with `ls docs/adr/`)
    - `docs/adr/0001-preflight-and-eula.md` (2026-04-08)
    - `docs/adr/0002-deployment-complete.md` (2026-04-08)
    - `docs/adr/0003-regscale-install-deviation.md` (2026-04-08)
    - `docs/adr/0004-defectdojo-install-deviation.md` (2026-04-08)
    - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (2026-04-08)
    - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (2026-04-09)
    - `docs/adr/0007-plan-2-complete.md` (2026-04-09)
    - `docs/adr/0008-plan-3-pre-execution-realignment.md` (2026-04-09)
  - `C:/Projects/CLAUDE.md` lines 15–30 (phase-completion dates as milestone timestamps)
  - `homelab-fedramp-low/README.md` (identifies Brian Chaplow as sole operator — establishes whose record this is)
- **Set-params (proposed values):**
  - `at-04_odp` (retention period): `"indefinitely while the GitHub repository is active — git history is immutable and retained at github.com/brianchaplow/homelab-fedramp-low"`, `organization` — no baseline-mandated retention period in FedRAMP Low profile; organization-defined
- **Authoring notes:** Status is `partial` rather than `implemented` because there is no dedicated training monitoring mechanism that generates alerts on overdue training (e.g., a cron that flags if no ADR has been filed in N days). The control says "document AND monitor." The git history satisfies "document"; monitoring is manual. Lead paragraph on git-as-training-record; second paragraph naming the monitoring gap explicitly. The `at-04_odp` retention parameter should use a concrete statement tied to repository lifetime rather than a duration.

---

*End of AT evidence catalog.*
