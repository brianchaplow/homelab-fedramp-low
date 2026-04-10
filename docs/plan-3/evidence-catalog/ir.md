# IR — Incident Response: Evidence Catalog

**Family:** IR (Incident Response)  
**FedRAMP Rev 5 Low controls:** IR-1, IR-2, IR-4, IR-5, IR-6, IR-7, IR-8  
**Catalog date:** 2026-04-09  
**Source:** homelab-fedramp-low repo — live homelab SOC on brisket + pitcrew + haccp  

---

## IR-1 — Incident Response Policy and Procedures

### Control Summary

Develop, document, and disseminate an incident response policy (purpose, scope, roles, responsibilities, management commitment, coordination, compliance) and implementing procedures. Designate an official to manage the IR policy. Review and update the policy and procedures at defined frequencies and following defined events.

**ODPs (all organization-defined):**

| ODP | ID | Meaning |
|-----|----|---------|
| Personnel/roles to receive policy | ir-01_odp.01 + ir-01_odp.02 | Who receives the policy |
| Review frequency — policy | ir-01_odp.03 | How often policy is reviewed |
| Triggering events — policy | ir-01_odp.04 | Events that trigger review |
| Review frequency — procedures | ir-01_odp.05 | How often procedures are reviewed |
| Triggering events — procedures | ir-01_odp.06 | Events that trigger procedure review |
| Designated official | ir-01_odp.07 | Role that manages IR policy |

All six ODPs are organization-defined (no FedRAMP-mandated fixed value). Values are set at authoring time in `trestle-workspace/mss-ssp/ir/ir-1.md`.

### Implementation Status

**partial**

An operational incident handling capability exists (Wazuh → Shuffle → TheHive pipeline, ADR 0005 real-incident record), but no standalone written IR policy document has been committed to this repo. The SSP authoring task (Plan 3) will constitute the formal policy documentation artifact.

### System Implementation

The homelab Managed SOC Service implements incident response governance at the system level. The system owner (Brian Chaplow) serves as the designated official for IR policy. The incident response policy is embedded in this SSP and in the operational runbooks committed to the `homelab-fedramp-low` repository. The policy covers:

- **Purpose:** Detect, contain, eradicate, and recover from security incidents affecting the in-boundary FedRAMP Low system (dojo, regscale, and their supporting infrastructure).
- **Scope:** All hosts enrolled as Wazuh agents, all services surfaced in the OSCAL component definition, and supporting infrastructure (Wazuh SIEM, Shuffle SOAR, TheHive, Velociraptor, ELK/Arkime on haccp).
- **Roles:** System owner (policy authority), SOC operator (detection and triage), DFIR operator (Velociraptor endpoint forensics).
- **Review cadence:** Policy reviewed annually and after any security incident that results in a new ADR or runbook update.
- **Triggering events:** Successful attack reaching in-boundary assets, significant vulnerability (CVSS ≥ 7) requiring remediation, PBS backup gap or comparable data-integrity incident (per ADR 0005 precedent).

Procedures are documented in `runbooks/monthly-conmon.md` and per-incident ADRs. The ADR series (0001–0008+) serves as the living procedure amendment record.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR policy statement (SSP) | `trestle-workspace/mss-ssp/ir/ir-1.md` | Prose filled during Plan 3 authoring |
| ADR series (procedure update record) | `docs/adr/0001-preflight-and-eula.md` through `docs/adr/0008-plan-3-pre-execution-realignment.md` | Each ADR amends or extends operational procedures |
| Monthly ConMon runbook | `runbooks/monthly-conmon.md` | Defines the recurring operational procedure |
| Restore runbook | `runbooks/restore-from-pbs.md` | Recovery procedure for in-boundary VMs |

### Parameter Values

| ODP | Value | Origin |
|-----|-------|--------|
| ir-01_odp.01 (personnel — policy) | system owner; SOC operator | organization |
| ir-01_odp.02 (personnel — procedures) | system owner; SOC operator | organization |
| ir-01_odp.03 (policy review frequency) | annually | organization |
| ir-01_odp.04 (policy review triggers) | security incident resulting in an ADR; significant regulatory change | organization |
| ir-01_odp.05 (procedure review frequency) | annually | organization |
| ir-01_odp.06 (procedure review triggers) | security incident; runbook gap discovery | organization |
| ir-01_odp.07 (designated official) | system owner (Brian Chaplow) | organization |

### Gaps / Notes

- No standalone IR policy PDF or Word document exists; the SSP prose plus the ADR series constitutes the policy body. This is adequate for a homelab portfolio but a 3PAO would expect a linked policy document for a production system.
- ADR 0005 (PBS backup gap) demonstrates the review-and-update mechanism is real: an incident triggered procedure hardening (fstab automount) and a runbook update.

---

## IR-2 — Incident Response Training

### Control Summary

Provide incident response training to system users consistent with assigned roles within a defined time period of assuming an IR role, when required by system changes, and at a defined frequency thereafter. Review and update IR training content at a defined frequency and following defined events.

**ODPs:**

| ODP | ID | Meaning |
|-----|----|---------|
| Time period for initial training | ir-02_odp.01 | How soon after role assumption |
| Frequency of recurring training | ir-02_odp.02 | How often thereafter |
| Frequency of content review | ir-02_odp.03 | How often training content is reviewed |
| Triggering events for content review | ir-02_odp.04 | Events that trigger review |

All four ODPs are organization-defined.

### Implementation Status

**partial**

The system owner and sole SOC operator is self-trained through construction and operation of the homelab SOC (Phases 1–15 in CLAUDE.md). No formal IR training records or a structured training program have been documented as a distinct artifact. Training content is embedded in the operational runbooks and ADR series.

### System Implementation

The Managed SOC Service is a single-operator homelab. The system owner maintains IR competency through:

- **Continuous hands-on operation** of the Wazuh → Shuffle → TheHive → Velociraptor incident pipeline (Phases 5–6, 14 execution).
- **Real incident handling** producing documented ADRs (ADR 0005: PBS backup gap — detection, investigation, containment, fix, verification cycle).
- **Caldera red-team exercises** (Phase 7) that validate detection and response: 4 Sandcat agents on smoker running adversary simulations against VLAN 40 targets, with Wazuh detection confirmed.
- **Velociraptor DFIR training** through enrollment of 7 clients and endpoint artifact collection walkthroughs.

Training content review is triggered by any new ADR that reveals a response procedure gap, or by Caldera simulation results showing detection failures.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR training record (SSP prose) | `trestle-workspace/mss-ssp/ir/ir-2.md` | Prose authored in Plan 3 |
| PBS backup gap incident (real IR exercise) | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | Demonstrates detection→investigation→remediation competency |
| Restore runbook (recovery procedure) | `runbooks/restore-from-pbs.md` | Documents the operator's recovery knowledge |
| Caldera configuration (VLAN 40 red-team) | `reference/` (parent repo, CLAUDE.md §v3 Migration Phase 7) | 4 Sandcat agents, Wazuh detection validated |

### Parameter Values

| ODP | Value | Origin |
|-----|-------|--------|
| ir-02_odp.01 (initial training time period) | within 30 days of assuming IR role | organization |
| ir-02_odp.02 (recurring frequency) | annually | organization |
| ir-02_odp.03 (content review frequency) | annually | organization |
| ir-02_odp.04 (content review triggers) | security incident; red-team exercise revealing detection gap | organization |

### Gaps / Notes

- No structured training curriculum document or training completion record exists. A 3PAO would expect signed training acknowledgments or course completion records.
- The homelab's single-operator model means "training" is the operator's own work product; this is a known limitation acceptable for a portfolio demonstration system.

---

## IR-4 — Incident Handling

### Control Summary

Implement an incident handling capability (preparation, detection and analysis, containment, eradication, recovery) consistent with the incident response plan. Coordinate with contingency planning. Incorporate lessons learned. Ensure rigor and consistency of handling activities.

**No ODPs** — all sub-elements are prescriptive (the phases of incident handling are NIST-defined).

### Implementation Status

**implemented**

The full NIST incident handling lifecycle is operationally implemented through the Wazuh → Shuffle WF1 → TheHive → Cortex → Velociraptor pipeline. ADR 0005 demonstrates a real end-to-end incident handled through this capability.

### System Implementation

The Managed SOC Service implements all five NIST incident handling phases:

**Preparation:**
- Wazuh SIEM (brisket, 15 enrolled agents) continuously monitors all in-boundary and supporting hosts.
- Shuffle SOAR WF1 v2 is deployed: webhook receives Wazuh alerts → AbuseIPDB enrichment → Cloudflare block (where applicable) → TheHive case creation → Discord notification via `$discord_webhook`.
- Velociraptor v0.75.3 (brisket) with 7 enrolled DFIR clients provides pre-staged endpoint forensics collection capability.
- PBS LXC 300 provides daily backups of in-boundary VMs (dojo VMID 201, regscale VMID 301, DC01 VMID 100, WS01 VMID 101, TheHive VMID 200) enabling recovery.

**Detection and Analysis:**
- Wazuh agents ship host events (syslog, auth, file-integrity, syscollector, vulnerability) to the Wazuh Indexer (OpenSearch) on brisket.
- Zeek on haccp span0 (USB 2.5GbE, promiscuous mode) produces JA3/JA4/community-id enriched JSON logs shipped via Filebeat → Logstash 5-stage enrichment pipeline to the ELK stack (haccp ES 8.17).
- ML Scorer (brisket:5002, XGBoost PR-AUC 0.9998) scores network flows for anomaly detection.
- Shuffle WF2 (cron 0600/1800) generates morning/evening digests; WF10 (cron 0530) produces nightly briefing via Ollama qwen3:8b.
- TheHive 4 + Cortex 3 (pitcrew LXC 200) with 5 analyzers provides structured case management and automated indicator analysis.

**Containment:**
- Shuffle WF1 v2 calls the Cloudflare API to block offending IPs at the CDN boundary.
- OPNsense firewall rules enforce VLAN segmentation (targets on VLAN 40 are isolated from VLAN 20/30 SOC infrastructure).
- MokerLink ACL provides hardware-level L3 segmentation between VLANs.

**Eradication:**
- Velociraptor hunts and artifact collection enable endpoint remediation: process termination, file removal, persistence mechanism identification across 7 enrolled clients.
- Wazuh active response can execute remediation scripts on enrolled agents.

**Recovery:**
- PBS snapshots provide same-day rollback capability (daily job at 02:00; verified via ADR 0005).
- Restore procedure documented in `runbooks/restore-from-pbs.md`.

**Lessons learned** are captured as ADRs after every real incident (ADR 0005 is the canonical example — PBS backup gap prompted fstab hardening and runbook update).

**Coordination with contingency planning:** The restore runbook cross-references CP controls; the monthly ConMon cycle (`runbooks/monthly-conmon.md`) coordinates IR outputs with the OSCAL POA&M update cycle.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR-4 SSP prose | `trestle-workspace/mss-ssp/ir/ir-4.md` | Authored in Plan 3 |
| PBS backup gap incident (real IR cycle) | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | Detection→analysis→containment→eradication→recovery demonstrated |
| Restore runbook (recovery) | `runbooks/restore-from-pbs.md` | Recovery SOP for in-boundary VMs |
| Monthly ConMon runbook (coordination) | `runbooks/monthly-conmon.md` | IR output feeds POA&M update |
| Wazuh agent enrollment (15 agents) | CLAUDE.md §Service Inventory — brisket Wazuh Manager | 15 agents: brisket, haccp, OPNsense syslog, dojo (016), regscale (017), etc. |
| Shuffle WF1 v2 (enrichment + block + case) | CLAUDE.md §Shuffle Workflow Variables | WF1: webhook → AbuseIPDB → Cloudflare → TheHive case |
| TheHive 4 + Cortex 3 (case management) | CLAUDE.md §pitcrew — TheHive LXC 200 | 5 Cortex analyzers |
| Velociraptor DFIR (7 clients) | CLAUDE.md §brisket — Velociraptor :8889 | Endpoint forensics collection |

### Parameter Values

IR-4 has no ODPs; all sub-elements are prescriptive per NIST SP 800-53 Rev 5.

### Gaps / Notes

- PBS backup-failure alerting (Wazuh → Discord) is deferred — the 5-day silent gap in ADR 0005 would have been caught earlier with this alert. Interim tripwire documented in `runbooks/monthly-conmon.md`. This gap is tracked as a Plan 1 Task 20 follow-up.
- Velociraptor hunt groups (post-migration item per CLAUDE.md) are not yet configured; endpoint forensics is available but not pre-staged with specific hunt profiles for the in-boundary VMs (dojo, regscale).
- Shuffle WF4 (Velociraptor automated triage) is pending (listed in CLAUDE.md post-migration items), so automated DFIR escalation is not yet wired end-to-end.

---

## IR-5 — Incident Monitoring

### Control Summary

Track and document incidents. (No ODPs — prescriptive.)

### Implementation Status

**implemented**

Incidents are tracked in TheHive cases (created automatically by Shuffle WF1) and documented in the ADR series. The PBS backup gap (ADR 0005) demonstrates the documentation chain from detection through resolution.

### System Implementation

The Managed SOC Service provides two complementary incident monitoring mechanisms:

**Automated incident tracking via TheHive 4:**
- Shuffle WF1 v2 automatically creates TheHive cases for Wazuh alerts that pass the enrichment and dedup filter. Each case captures: alert timestamp, source IP (enriched via AbuseIPDB), Cloudflare block status, Wazuh rule ID and description, and severity.
- TheHive case lifecycle (New → In Progress → Resolved) provides the audit trail for active incidents.
- Cortex 3 with 5 analyzers runs automated indicator analysis (IP reputation, hash lookup, etc.) and records results as case observables.

**Documented incident record via ADR series:**
- Significant incidents that affect operational posture, configuration, or procedures are captured as Architecture Decision Records in `docs/adr/`. This is the primary mechanism for incidents discovered outside the automated Wazuh alerting path (e.g., operational errors during plan execution).
- ADR 0005 (PBS backup gap): detected 2026-04-08 during Plan 1 Task 12 verification; documented root cause (boot-race NFS mount failure), 5-day backup gap, manual remediation, and preventive control (automount hardening).

**ELK/Zeek historical record:**
- Zeek network logs on haccp ES (`logs-zeek.haccp-default-*` data stream) provide a tamper-evident network event record for post-incident forensics.
- Arkime PCAP archive (Samsung 990 EVO Plus, `/opt/arkime/raw/`, daily SSH/rsync to smokehouse at 0300) provides full packet capture for retrospective analysis.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR-5 SSP prose | `trestle-workspace/mss-ssp/ir/ir-5.md` | Authored in Plan 3 |
| PBS backup gap incident record | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | Incident tracked + documented end-to-end |
| Shuffle WF1 v2 (auto case creation) | CLAUDE.md §Shuffle Workflow Variables — WF1 | TheHive case per alert |
| TheHive 4 case management | CLAUDE.md §pitcrew — TheHive LXC 200 | Case tracking platform |
| Zeek data stream | haccp ES `logs-zeek.haccp-default-*` | Network event audit trail |
| Arkime PCAP archive | haccp `/opt/arkime/raw/` → smokehouse NFS | Full PCAP retention |

### Parameter Values

IR-5 has no ODPs.

### Gaps / Notes

- TheHive cases created by Shuffle WF1 are not yet manually cross-referenced back to ADRs in a structured way; a 3PAO would look for traceability between case IDs and formal incident records.
- No formal incident register (spreadsheet or database) exists outside TheHive; the ADR series is the near-equivalent but is not structured as a formal incident log with mandatory fields (CVSS score at detection, containment SLA, etc.).
- Arkime PCAP retention policy is not yet formally documented (no defined retention period); the data accumulates until the 1.8TB Samsung 990 EVO Plus fills. A defined policy should be captured in the SSP prose.

---

## IR-6 — Incident Reporting

### Control Summary

Require personnel to report suspected incidents to the organizational IR capability within a defined time period. Report incident information to defined authorities.

**ODPs:**

| ODP | ID | Meaning |
|-----|----|---------|
| Reporting time period | ir-06_odp.01 | How quickly personnel must report |
| Reporting authorities | ir-06_odp.02 | Who receives incident reports |

Both ODPs are organization-defined.

### Implementation Status

**implemented**

The single-operator homelab model means the system owner is simultaneously the personnel required to report and the IR capability receiving the report. Discord alerting (`$discord_webhook` via Shuffle WF1) serves as the real-time notification mechanism. Formal reporting to external authorities (US-CERT/CISA) is not applicable at the homelab portfolio level but is acknowledged in the SSP.

### System Implementation

**Internal reporting (same-operator model):**
- Wazuh automatically forwards alerts to Shuffle WF1 via webhook; WF1 posts to Discord `#soc-alerts` and creates a TheHive case within minutes of detection. This satisfies "report to the organizational IR capability" for the single-operator system — the operator is notified via Discord within the response time.
- Infrastructure-layer alerts (e.g., GPU thermal, service down) route to `#infrastructure-alerts` via the Grafana alerting integration (`$discord_webhook_infra`).
- Nightly briefing (WF10 cron 0530 via `$discord_webhook_briefing`) posts to `#morning-briefing`, providing daily review even when no real-time alert fires.

**Reporting to external authorities:**
- This system is a homelab portfolio demonstration, not a federal information system subject to mandatory FISMA/CISA reporting. IR-6(b) is acknowledged but not operationally applicable at this scope.
- If this system were in production scope, US-CERT reporting within 1 hour of discovery of a significant incident would be required per FedRAMP ConMon requirements.

**Reporting time period:** Suspected incidents are surfaced to the operator via Discord within minutes of Wazuh detection (Shuffle WF1 latency). The operator self-reports to the IR capability (TheHive case) within 1 hour.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR-6 SSP prose | `trestle-workspace/mss-ssp/ir/ir-6.md` | Authored in Plan 3 |
| Shuffle WF1 (Discord notification) | CLAUDE.md §Shuffle Workflow Variables — `$discord_webhook` | SOC alert channel |
| Grafana GPU thermal alert | CLAUDE.md §Phase 14 thermal hardening — uid=dfihoiidr7k00c | Infrastructure alert via `$discord_webhook_infra` |
| PBS backup gap ADR (reporting record) | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | Demonstrates incident detection and documentation workflow |

### Parameter Values

| ODP | Value | Origin |
|-----|-------|--------|
| ir-06_odp.01 (reporting time period) | 1 hour of discovery | organization |
| ir-06_odp.02 (reporting authorities) | system owner (Brian Chaplow); US-CERT/CISA for production-scope incidents | organization |

### Gaps / Notes

- External reporting to US-CERT/CISA is not applicable at the current homelab portfolio scope; the SSP prose will document this explicitly as an organizational determination.
- There is no formal incident reporting form or template; the ADR serves as the report artifact. A mature program would use a standardized incident report template.

---

## IR-7 — Incident Response Assistance

### Control Summary

Provide an incident response support resource, integral to the organizational IR capability, that offers advice and assistance to users of the system for the handling and reporting of incidents. (No ODPs.)

### Implementation Status

**implemented**

TheHive 4 + Cortex 3 serve as the automated incident response support resource. Shuffle WF1 provides the initial enrichment and triage assistance. Velociraptor provides endpoint forensics assistance. Discord channels provide the real-time human-to-system notification channel.

### System Implementation

The Managed SOC Service provides the following IR support resources:

**TheHive 4 (pitcrew LXC 200, 10.10.30.22:9000):**
- Structured case management platform with case timeline, observable tracking, and task assignment.
- 5 Cortex 3 analyzers provide automated indicator analysis (IP reputation, file hash lookup, etc.) on demand from within any case.
- Functions as the "help desk" equivalent — every alert that clears the Shuffle dedup filter becomes a TheHive case that the operator can investigate with analyzer assistance.

**Shuffle SOAR WF1 v2 (brisket:3443/5001):**
- Provides pre-analysis advice for each alert: AbuseIPDB score, Cloudflare block status, Wazuh rule classification.
- Discord posting delivers the enriched alert summary directly to the operator's notification channel, reducing the investigation bootstrap time.

**Velociraptor v0.75.3 (brisket:8889):**
- Endpoint forensics assistance for 7 enrolled clients.
- Enables rapid artifact collection (process list, network connections, file system timeline, memory artifacts) to assist incident analysis.

**Ollama qwen3:8b (brisket:11434):**
- LLM-assisted classification in the Zeek enrichment pipeline (Logstash Stage 5 via the `zeek-enrichment.conf` rate-limited Ollama call).
- WF10 nightly briefing uses qwen3:8b to produce a narrative incident summary from the previous 24 hours of alerts.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR-7 SSP prose | `trestle-workspace/mss-ssp/ir/ir-7.md` | Authored in Plan 3 |
| TheHive 4 + Cortex 3 | CLAUDE.md §pitcrew — TheHive LXC 200 | Case management + 5 analyzers |
| Velociraptor DFIR | CLAUDE.md §brisket — Velociraptor :8889 | 7 enrolled clients |
| Shuffle WF1 (enrichment + Discord) | CLAUDE.md §Shuffle Workflow Variables | Enrichment advice per alert |
| Nightly briefing WF10 | CLAUDE.md §Shuffle Workflow Variables — WF10 cron 0530 | LLM narrative summary |

### Parameter Values

IR-7 has no ODPs.

### Gaps / Notes

- TheHive is accessible only on the internal VLAN 30 network (10.10.30.22:9000); there is no external-facing IR assistance interface. This is appropriate for a single-operator homelab but would limit assistance to remote operators if the system were multi-user.
- Cortex analyzers are limited to 5; a production system might integrate additional threat intelligence analyzers (VirusTotal, Shodan, etc.). OpenCTI integration with TheHive is not yet implemented.

---

## IR-8 — Incident Response Plan

### Control Summary

Develop, distribute, and maintain an incident response plan that provides a roadmap for implementing the IR capability, describes its structure and organization, defines reportable incidents, provides metrics, defines resource requirements, addresses information sharing, and is reviewed and approved by defined personnel at a defined frequency. Protect the plan from unauthorized disclosure and modification.

**ODPs:**

| ODP | ID | Meaning |
|-----|----|---------|
| Review/approval personnel or roles | ir-08_odp.01 | Who approves the IRP |
| Review frequency | ir-08_odp.02 | How often reviewed |
| Incident response personnel (distribution) | ir-08_odp.03 | Who receives the IRP |
| Organizational elements (distribution) | ir-08_odp.04 | Which org elements receive the IRP |
| Incident response personnel (changes) | ir-08_odp.05 | Who receives IRP change notices |
| Organizational elements (changes) | ir-08_odp.06 | Which org elements receive change notices |
| (aggregate: ir-8_prm_5) | ir-08_odp.05 + ir-08_odp.06 + ir-08_odp.07 | Change communication recipients |

### Implementation Status

**partial**

The incident response plan is distributed across multiple artifacts (SSP IR-4 prose, runbooks, ADRs) rather than as a single titled IRP document. The operational capability is fully implemented; the formal plan document consolidation is the Plan 3 SSP authoring deliverable.

### System Implementation

The Managed SOC Service's incident response plan is composed of the following artifacts, collectively providing the IRP elements required by NIST SP 800-53 IR-8:

**Roadmap and structure (IR-8a.1–a.4):**
- This SSP's IR family prose (IR-1 through IR-8) provides the organizational roadmap and structure for the IR capability.
- The Wazuh → Shuffle → TheHive → Cortex → Velociraptor pipeline defines the operational structure.

**Reportable incidents (IR-8a.5):**
- Any Wazuh alert that reaches Shuffle WF1 (passes dedup filter) is a reportable event.
- Incidents requiring an ADR: operational failures affecting in-boundary availability, confidentiality, or integrity; backup failures; service disruptions; successful adversary techniques confirmed by Caldera or real-world events.
- Thresholds: CVSS ≥ 7.0 vulns on in-boundary hosts generate POA&M entries; CVSS ≥ 9.0 generate immediate TheHive cases via WF1.

**Metrics (IR-8a.6):**
- Mean-time-to-detection (MTTD): measured as time from event occurrence to Wazuh alert timestamp.
- Mean-time-to-respond (MTTR): measured as time from TheHive case creation to case resolution.
- Open POA&M items by severity (tracked in `poam/POAM-2026-04.xlsx`, regenerated monthly by `./pipelines.sh conmon`).
- Monthly Wazuh alert count by rule group (surfaced via Wazuh Dashboard on brisket:5601).

**Resources and management support (IR-8a.7):**
- brisket (ThinkStation, Ultra 9 285, 64GB, RTX A1000): Wazuh Manager + Indexer, Shuffle SOAR, Velociraptor, ML Scorer, Ollama.
- pitcrew LXC 200: TheHive 4 + Cortex 3.
- haccp (ThinkStation P340 Tiny, 32GB): ELK 8.17 + Arkime + Zeek (span0).
- smoker LXC 300: PBS backup server with NFS mount to smokehouse 17TB.
- No additional management budget required — all resources are deployed.

**Information sharing (IR-8a.8):**
- Incident information is shared via Discord webhooks (immediate notification to operator), TheHive cases (structured incident record), and the ADR series (formal post-incident documentation committed to the public GitHub repo).
- External sharing: not applicable at homelab scope; production-scope systems would report to US-CERT/CISA.

**Review and approval (IR-8a.9):**
- IRP (as embodied by this SSP) is reviewed annually and following any incident that results in an ADR.
- Approved by the system owner (Brian Chaplow) as the sole organizational authority.

**Distribution (IR-8b):**
- IRP artifacts are committed to the homelab-fedramp-low GitHub repo (`github.com/brianchaplow/homelab-fedramp-low`), accessible to all authorized repository contributors.

**Protection (IR-8e):**
- The repo is version-controlled (git); history is immutable absent force-push.
- GitHub branch protection (if enabled on main) prevents unauthorized modification.
- `.env` files containing service credentials are gitignored and not included in the IRP artifacts.

### Evidence Paths

| Artifact | Path | Notes |
|----------|------|-------|
| IR-8 SSP prose (IRP narrative) | `trestle-workspace/mss-ssp/ir/ir-8.md` | Plan 3 authored IRP |
| ADR 0005 (incident record demonstrating IRP execution) | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | Real incident handled per IRP |
| Monthly ConMon runbook | `runbooks/monthly-conmon.md` | Metrics collection procedure |
| Restore runbook | `runbooks/restore-from-pbs.md` | Recovery SOP referenced by IRP |
| POA&M (metrics artifact) | `poam/POAM-2026-04.xlsx` | 8,473 open findings, severity-bucketed |
| OSCAL SSP (IRP distribution artifact) | `oscal/ssp.json` | Assembled SSP — Plan 3 delivery |
| Component definition (resource inventory) | `oscal/component-definition.json` | 7 in-boundary components |

### Parameter Values

| ODP | Value | Origin |
|-----|-------|--------|
| ir-08_odp.01 (review/approval personnel) | system owner (Brian Chaplow) | organization |
| ir-08_odp.02 (review frequency) | annually | organization |
| ir-08_odp.03 (distribution — IR personnel) | system owner; SOC operator | organization |
| ir-08_odp.04 (distribution — org elements) | homelab-fedramp-low GitHub repo (public) | organization |
| ir-08_odp.05 (change notice — IR personnel) | system owner; SOC operator | organization |
| ir-08_odp.06 (change notice — org elements) | homelab-fedramp-low GitHub repo (git commit notification) | organization |
| ir-08_odp.07 (change notice — additional) | Discord `#soc-alerts` channel | organization |

### Gaps / Notes

- No standalone IRP document (titled "Incident Response Plan") has been produced; the SSP IR family prose plus runbooks constitute the distributed IRP. This is a known portfolio trade-off.
- The ADR series serves as the IRP update history, but ADRs are not explicitly cross-referenced to IRP version numbers. A version-numbered IRP with a change log would be more auditable.
- GitHub branch protection status on the `main` branch is not confirmed in this repo's ADR record; the IRP protection claim (IR-8e) should be verified and the protection rules documented.
- Velociraptor hunt groups and WF4 (automated DFIR triage) remain pending per CLAUDE.md post-migration items; these would strengthen the resources section of the IRP once implemented.

---

## Coverage Summary

| Control | Status | Key Evidence |
|---------|--------|--------------|
| IR-1 | partial | ADR series as procedure record; no standalone IR policy document |
| IR-2 | partial | Hands-on operator training via homelab operation; no formal training records |
| IR-4 | implemented | Full PDRR cycle: Wazuh→Shuffle→TheHive→Velociraptor; ADR 0005 real incident |
| IR-5 | implemented | TheHive cases (automated) + ADR series (manual); ELK/Arkime network record |
| IR-6 | implemented | Discord via Shuffle WF1 (<1 hour notification); US-CERT not applicable at scope |
| IR-7 | implemented | TheHive 4 + Cortex 3 (5 analyzers) + Velociraptor + Ollama WF10 briefing |
| IR-8 | partial | Distributed IRP across SSP + runbooks + ADRs; no standalone IRP document |

**Notes for SSP authoring (Plan 3 Task 8 — IR family):**

1. IR-4 and IR-5 and IR-7 are the strongest controls — write detailed prose grounded in the Wazuh→Shuffle→TheHive pipeline and the ADR 0005 incident record.
2. IR-1, IR-2, and IR-8 are partial — prose should be honest about the distributed/informal nature of the policy, training, and plan documents while demonstrating the underlying operational maturity.
3. IR-6 external reporting: explicitly state this is a homelab portfolio system and US-CERT reporting is not applicable; do not claim implemented for the external-authorities sub-element.
4. All IR ODPs are organization-defined; no FedRAMP-mandated fixed values exist for this family. Values in the parameter table above are the proposed organizational values to be filled into `x-trestle-set-params` in each control's markdown source.
