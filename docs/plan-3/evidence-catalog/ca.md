# CA -- Assessment, Authorization, and Monitoring
## Evidence Catalog -- Plan 3 Phase 1

**Generated:** 2026-04-09
**Controls:** CA-1, CA-2, CA-2(1), CA-3, CA-5, CA-6, CA-7, CA-7(4), CA-8, CA-9
**Tier:** CA promoted to Tier-1-grade (ADR 0008 §Supersession deltas)
**Scaffold source:** `trestle-workspace/mss-ssp/ca/`

---

## CA-1 -- Policy and Procedures

### 1. Control Statement Summary

Develop, document, and disseminate an assessment, authorization, and monitoring policy to designated personnel; designate an official to manage that policy; and review/update the policy and associated procedures at defined frequencies and following defined events.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Personnel/roles for dissemination (a) | ca-01_odp.01 / ca-01_odp.02 | `<REPLACE_ME>` | System owner (Brian Chaplow) | organization |
| Designee (b) | ca-01_odp.03 | `<REPLACE_ME>` | System owner (Brian Chaplow) | organization |
| Policy review frequency (c.1) | ca-01_odp.04 | `<REPLACE_ME>` | Annually | organization |
| Policy trigger events (c.1) | ca-01_odp.05 | `<REPLACE_ME>` | Significant system change; security incident; regulatory update | organization |
| Procedure review frequency (c.2) | ca-01_odp.06 | `<REPLACE_ME>` | Annually | organization |
| Procedure trigger events (c.2) | ca-01_odp.07 / ca-01_odp.08 | `<REPLACE_ME>` | Significant system change; security incident | organization |

All values are organization-defined; no FedRAMP-mandated baseline value applies to CA-1 ODPs in the Rev 5 Low profile.

### 3. Implementation Evidence

- **This SSP** (`oscal/ssp.json`) serves as the system-level assessment, authorization, and monitoring policy document for the Managed SOC Service (MSS) homelab boundary. It addresses purpose (FedRAMP Low ConMon portfolio), scope (7 in-boundary components per `oscal/component-definition.json`), roles (system owner = Brian Chaplow), and compliance (FedRAMP Rev 5 Low baseline, NIST SP 800-53 Rev 5).
- **ADR series** (`docs/adr/0001` through `docs/adr/0008`) provides the change-event record: each ADR is filed at a significant system change or deviation discovery event, equivalent to the "following events" update trigger.
- **`runbooks/monthly-conmon.md`** documents the ConMon procedures for the ongoing monitoring cycle. Plan 3 SSP authoring constitutes the initial documentation event; annual review cadence starts from Plan 3 completion.
- **`docs/adr/0008-plan-3-pre-execution-realignment.md`** records the pre-execution critical read (2026-04-09) as the first documented policy review event.

### 4. Gaps / Open Items

CA-1 is partially implemented: the SSP prose and runbook are authored during Plan 3; formal annual review scheduling is not yet established. Status: **partial**.

### 5. Related Controls

CA-2, CA-5, CA-6, CA-7, PM-9, PM-10

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-1.md`

---

## CA-2 -- Control Assessments

### 1. Control Statement Summary

Select an assessor; develop an assessment plan covering scope, procedures, environment, and roles; get plan approved before assessment; assess controls at defined frequency to determine correct implementation and desired outcomes; produce an assessment report; provide results to defined personnel.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Assessment frequency (d) | ca-02_odp.01 | `<REPLACE_ME>` | Annually (aligned with FedRAMP ConMon annual assessment) | organization |
| Recipients of results (f) | ca-02_odp.02 | `<REPLACE_ME>` | System owner (Brian Chaplow) | organization |

No FedRAMP-mandated fixed values apply to CA-2 ODPs in the Rev 5 Low profile; "annually" aligns with OMB A-130 and FedRAMP ConMon guidance.

### 3. Implementation Evidence

- **Test suite** (130 passing tests at Plan 2 completion per ADR 0007; 136 after Plan 3 Task 3): located in `tests/` and exercised via `./pipelines.sh test`. The test suite is the mechanism by which control effectiveness is assessed on a per-pipeline-run basis. Each `./pipelines.sh conmon` invocation re-executes the pipeline and validates the output artifacts, providing ongoing evidence of correctness.
- **`pipelines/build/oscal_poam.py`**: SLA window logic (15/30/90/180 days, corrected from plan text per ADR 0006 Amendment Task 12) encodes the assessment finding → remediation timeline mapping per FedRAMP Low ConMon Strategy Guide.
- **`poam/POAM-2026-04.xlsx`** (4.9 MB, 8,473 items): the April 2026 assessment output. Each row is a finding produced by live Wazuh vulnerability scan against 5 in-boundary agents (brisket, haccp, smokehouse, dojo, regscale). This is the assessment report artifact for the initial ConMon cycle.
- **`docs/adr/0007-plan-2-complete.md`** §"Done criteria -- verified": documents the live end-to-end assessment run that validated all pipeline subcommands against live infrastructure on 2026-04-09.
- **DefectDojo** (`http://10.10.30.27:8080`): hosts the imported findings in 5 products (MSS Core - brisket, MSS Log Analytics - haccp, MSS Network Sensors - smokehouse, MSS GRC Tooling - dojo + regscale, MSS Boundary Protection - OPNsense). The per-product engagement "ConMon 2026-04" is the assessment scope artifact.
- **Assessor:** Brian Chaplow (system owner) serves as self-assessor for this homelab portfolio. CA-2(1) addresses the independence constraint.

### 4. Gaps / Open Items

Formal written assessment plan (distinct document) has not been produced -- the SSP and test suite together serve this function for the homelab scope. Frequency parameter not yet set in markdown. Status: **partial**.

### 5. Related Controls

CA-2(1), CA-5, CA-7, RA-5, SI-2

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-2.md`

---

## CA-2(1) -- Independent Assessors

### 1. Control Statement Summary

Employ independent assessors or assessment teams to conduct control assessments.

### 2. Parameters

No ODPs. No `x-trestle-set-params` block in scaffold (`trestle-workspace/mss-ssp/ca/ca-2.1.md`).

### 3. Implementation Evidence

- **Homelab scope context:** This is a single-person portfolio system owned and operated by Brian Chaplow. Full assessor independence (separate organizational entity) is not feasible for a homelab. The control is implemented at a commensurate level: the test suite in `tests/` provides automated, deterministic verification independent of manual operator judgment; Wazuh (brisket) runs the vulnerability scanner independently of the manual authoring workflow; DefectDojo SLA enforcement is automated and not subject to operator override without a code change.
- **Structural independence mechanisms:**
  - `pipelines/ingest/wazuh_vulns.py` ingests scan data directly from the Wazuh Indexer (OpenSearch at `https://10.10.20.30:9200`) without manual filtering -- the scanner result is authoritative.
  - `pipelines/push/defectdojo.py` pushes findings to DefectDojo as a separate system; findings cannot be deleted without DefectDojo API access (separate credential).
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §"Gate 3 spot-check scope" documents 144 planned spot-checks of evidence citations by the author against repo artifacts -- a self-review gate that catches hallucinated citations before SSP publication.
- **Accepted limitation:** True third-party independence is not implemented. This is the honest state; the portfolio treats CA-2(1) as partially implemented with the automated pipeline as the independence substitute.

### 4. Gaps / Open Items

Third-party or independent-role assessment not available for homelab scope. Automated pipeline provides the nearest feasible substitute. Status: **partial**.

### 5. Related Controls

CA-2, CA-7, CA-8

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-2.1.md`

---

## CA-3 -- Information Exchange

### 1. Control Statement Summary

Approve and manage information exchange with other systems using defined agreement types; document interface characteristics, security requirements, and impact level for each exchange; review and update agreements at defined frequency.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Agreement type(s) (a) | ca-03_odp.01 | `<REPLACE_ME>` | Information exchange security agreements (documented in SSP §external connections) | organization |
| Agreement documentation location (b) | ca-03_odp.02 | `<REPLACE_ME>` | This SSP §external connections; `CLAUDE.md` §"Network Quick Reference" | organization |
| Review frequency (c) | ca-03_odp.03 | `<REPLACE_ME>` | Annually; following significant system change | organization |

### 3. Implementation Evidence

The MSS homelab boundary has four categories of external information exchange, all documented in `CLAUDE.md` (the authoritative whole-project design reference):

**1. Tailscale overlay network (outbound/bidirectional)**
- Hosts with Tailscale: brisket (TS 100.124.139.56), smokehouse (TS 100.110.112.98), sear (TS 100.86.67.91), haccp (TS 100.74.16.82), smoker (TS 100.77.138.24), PITBOSS (TS 100.126.10.19), GCP VM (TS 100.125.40.97).
- Protocol: WireGuard-based mesh VPN. Traffic is encrypted in transit. No sensitive system data transits Tailscale except SSH management sessions and pipeline invocations from PITBOSS.
- Agreement type: implicit operator agreement with Tailscale, Inc. (SaaS). Interface documented in `CLAUDE.md` §"SSH Quick Reference."

**2. Wazuh agent → Wazuh Manager (in-boundary)**
- 15 agents report to brisket:1514/1515. dojo (016) and regscale (017) are on VLAN 30; their agent traffic crosses the VLAN 30 → VLAN 20 routed path via MokerLink L3 switch (10.10.10.2).
- Interface: Wazuh OSSEC protocol (encrypted). Documented in `CLAUDE.md` §"brisket service inventory."

**3. PBS NFS mount (smoker LXC 300 → smokehouse)**
- PBS LXC 300 (10.10.30.24) mounts smokehouse (10.10.20.10) NFS export `/pbs-datastore` over VLAN 20/30 routed path.
- Interface characteristics: NFSv3/v4 over TCP. Impact level: moderate (VM backup data including ConMom artifacts). Documented in `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (boot-race failure and automount fix).
- Current fstab hardening: `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30`.

**4. Wazuh agent → customer-deployed agents (out-of-boundary)**
- GCP VM (agent 009) reports to brisket Wazuh Manager from external IP. Interface documented in `CLAUDE.md` §"GCP VM."
- OPNsense syslog → Wazuh (514/UDP, in-boundary VLAN 10 → 20). Documented in `CLAUDE.md` §"brisket service inventory."

**5. Pipeline API calls (outbound during ConMon)**
- `pipelines/common/defectdojo.py` → DefectDojo at `http://10.10.30.27:8080` (VLAN 30, in-boundary).
- `pipelines/common/regscale.py` → RegScale CE at `http://10.10.30.28/` (VLAN 30, in-boundary).
- `pipelines/common/wazuh.py` + `pipelines/common/wazuh_indexer.py` → brisket Wazuh Manager/Indexer (in-boundary).
- All three are in-boundary connections; included here for completeness.

### 4. Gaps / Open Items

Formal written interconnection security agreements (ISAs) do not exist -- the SSP prose and CLAUDE.md serve as the agreement documentation for this homelab. HTTP-only posture for DefectDojo and RegScale is a known gap documented in ADR 0002 §"Operator action items" and ADR 0003; SC-8 addresses the mitigations in the SC family. Status: **partial**.

### 5. Related Controls

CA-9, SC-7, SC-8, AC-17, AC-20

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-3.md`

---

## CA-5 -- Plan of Action and Milestones

### 1. Control Statement Summary

Develop a POA&M documenting planned remediation of weaknesses and vulnerabilities; update existing POA&M at defined frequency based on assessment findings, audits, and continuous monitoring.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Update frequency (b) | ca-05_odp | `<REPLACE_ME>` | Monthly (each ConMon cycle) | organization |

FedRAMP ConMon Strategy Guide requires monthly POA&M updates; "monthly" is the correct organization-defined value here.

### 3. Implementation Evidence

- **`pipelines/build/oscal_poam.py`**: OSCAL POA&M builder. Reads DefectDojo findings via `DefectDojoClient.list_findings()`, maps each finding to an OSCAL POA&M item with FedRAMP Low SLA-based scheduled completion date (Critical=15 days, High=30, Medium/Moderate=90, Low=180). SLA windows corrected from plan text (30/90/180/365) to actual FedRAMP values per ADR 0006 Amendment Task 12.
- **`oscal/poam.json`** (gitignored, regenerated monthly): OSCAL 1.1.2 POA&M JSON, 16.8 MB, 8,473 items from the April 2026 ConMon cycle. Source of truth for the rendered spreadsheet.
- **`poam/POAM-2026-04.xlsx`** (4.9 MB, 8,473 rows): April 2026 POA&M in FedRAMP Rev 5 POA&M template format (`templates/FedRAMP-POAM-Template-Rev5.xlsx`). Data in "Open POA&M Items" sheet starting at row 8. Internal `Medium` severity mapped to `Moderate` for the template dropdown. `False Positive` state sets the FP column to Yes.
- **`pipelines/render/poam.py`**: POA&M xlsx renderer. Writes into the FedRAMP template format with correct column mapping.
- **`./pipelines.sh conmon`** (`pipelines/cli.py` `conmon` command): runs the full monthly cycle -- ingest-findings → oscal → render-iiw → render-poam -- producing updated POA&M artifacts from live Wazuh scan data on each invocation.
- **DefectDojo SLA enforcement** (`http://10.10.30.27:8080`): the 5 MSS products have FedRAMP Low ConMon SLA configurations applied via `deploy/defectdojo/post-install.sh` (idempotent seed script). DefectDojo flags findings approaching or past SLA, providing the early-warning mechanism for the monthly POA&M update.
- **`docs/adr/0007-plan-2-complete.md`** §"Done criteria": documents the live April 2026 run that produced the first POA&M.

### 4. Gaps / Open Items

POA&M is implemented and live. The update frequency parameter needs to be set in the scaffold markdown. Monthly update cadence is established by `./pipelines.sh conmon` but is not yet a scheduled/automated cron -- operator runs it manually. Status: **implemented** (the artifact and pipeline exist; cron automation is a future enhancement, not a control gap).

### 5. Related Controls

CA-2, CA-7, RA-5, SI-2, PM-4

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-5.md`

---

## CA-6 -- Authorization

### 1. Control Statement Summary

Assign a senior official as the authorizing official (AO) for the system and for common controls; ensure AO accepts common controls and authorizes the system to operate before commencing; ensure common control AO authorizes controls for inheritance; update authorizations at defined frequency.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Authorization update frequency (e) | ca-06_odp | `<REPLACE_ME>` | Annually; following significant security change | organization |

### 3. Implementation Evidence

- **Authorizing Official:** Brian Chaplow (system owner and sole operator) serves as the AO for this homelab system. This is the maximum independence feasible for a single-person portfolio system.
- **This SSP** (`oscal/ssp.json`, assembled from `trestle-workspace/mss-ssp/`): constitutes the authorization package. The SSP documents the system boundary, controls, and implementation status. Plan 3 SSP authoring is the authorization event -- a completed SSP with realistic implementation prose represents the ATO artifact for portfolio purposes.
- **ADR 0009** (planned, to be filed at Plan 3 Gate 5): will serve as the self-authorization decision record. ADR 0008 §"Authoritative Plan 3 artifacts" explicitly identifies ADR 0009 as the "Plan 3 completion" ADR filed at Gate 5. This is the authorization record that a reviewer can walk to confirm the AO accepted the risk and authorized the system.
- **Common controls:** No inherited common controls from a shared services provider in this homelab. The system is standalone; all controls are system-specific or organization-defined.
- **FedRAMP Low context:** A real FedRAMP authorization requires a federally-delegated AO and a FedRAMP-authorized 3PAO. This homelab treats the system owner as AO and the automated test suite + SSP as the equivalent of a 3PAO assessment package, per the explicit portfolio scope documented in `README.md`.

### 4. Gaps / Open Items

ADR 0009 has not been filed yet (pending Plan 3 Gate 5). Authorization update frequency parameter not set in markdown. Status: **planned** (authorization event will occur at Plan 3 completion; the artifact trail is being built now).

### 5. Related Controls

CA-2, CA-7, PL-2, PM-10

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-6.md`

---

## CA-7 -- Continuous Monitoring

### 1. Control Statement Summary

Develop a system-level ConMon strategy and implement continuous monitoring per the organization-level strategy. Strategy must include: system-level metrics; monitoring and assessment frequencies; ongoing control assessments; ongoing metric monitoring; correlation and analysis; response actions; and security/privacy status reporting to defined personnel at defined frequency.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| System-level metrics (a) | ca-07_odp.01 | `<REPLACE_ME>` | Vulnerability counts by severity (per Wazuh/DefectDojo); POA&M SLA adherence rate; agent connectivity (15 agents); backup job success (PBS daily); GPU thermal headroom (brisket RTX A1000) | organization |
| Monitoring frequencies (b) | ca-07_odp.02 | `<REPLACE_ME>` | Continuous (Wazuh real-time); daily (PBS backup tripwire); monthly (ConMon cycle) | organization |
| Assessment of control effectiveness frequency (b) | ca-07_odp.03 | `<REPLACE_ME>` | Monthly (each `./pipelines.sh conmon` run); annually (full SSP review) | organization |
| Security status report recipients (g) | ca-07_odp.04 / ca-07_odp.06 | `<REPLACE_ME>` | System owner (Brian Chaplow) | organization |
| Security status report frequency (g) | ca-07_odp.05 / ca-07_odp.07 | `<REPLACE_ME>` | Monthly (ConMon cycle output); daily (Wazuh/Discord alerts) | organization |

Note: `ca-7_prm_4` aggregates `ca-07_odp.04` + `ca-07_odp.06` (security + privacy report recipients); `ca-7_prm_5` aggregates `ca-07_odp.05` + `ca-07_odp.07` (security + privacy report frequencies).

### 3. Implementation Evidence

CA-7 is the hero control for the CA family. The entire Plan 2 pipeline is the CA-7 implementation.

**ConMon orchestration:**
- **`./pipelines.sh conmon`** (`pipelines/cli.py` `conmon` command): single command executes the full monthly cycle -- ingest-findings → inventory → build-poam → render-iiw → render-poam. Verified live against the homelab SOC on 2026-04-09 per ADR 0007.
- **`runbooks/monthly-conmon.md`**: ConMon procedure runbook. Stub during Plan 1; procedure fills in as Plan 2/3 pipeline matures.

**Ongoing monitoring -- real-time:**
- **Wazuh SIEM** (brisket, 10.10.20.30): 15 agents active (brisket, haccp, smokehouse, sear, PITBOSS, DC01, WS01, DVWA/Juice Shop, Metasploitable 3 Linux and Win, WordPress, crAPI, vsftpd, dojo, regscale, OPNsense syslog). Zeek pipeline (7 indices: `zeek-*` on Wazuh Indexer). Wazuh Dashboard at brisket:5601.
- **ELK Stack** (haccp, 10.10.30.25): Elasticsearch 8.17 + Kibana + Fleet + Logstash in Docker (`/opt/elk/docker-compose.yml`). 4 Fleet agents. 214 detection rules. `logs-zeek.haccp-default-*` data stream from Phase 14 Zeek pipeline. Kibana at haccp:5601.
- **OpenCTI** (brisket:8080): Threat intelligence platform v7, 6 connectors, IOC sync to Wazuh CDB lists every 6 hours (`0 */6 * * *`) and to haccp `opencti-threat-intel` index every 6 hours (`15 */6 * * *`).
- **Grafana** (brisket:3000): SOC v3 Overview dashboard + Grafana alert "GPU Thermal Critical -- Brisket Above 90C" (uid=dfihoiidr7k00c, 2m window) routing to #infrastructure-alerts via Discord.
- **Shuffle SOAR** (brisket:3443): 10 active workflows including WF10 (nightly briefing, 0530 EST) and WF9 (5-min polling). Real-time alert routing to Discord.

**Ongoing monitoring -- vulnerability scanning:**
- **`pipelines/ingest/wazuh_vulns.py`**: reads `wazuh-states-vulnerabilities-*` index via `WazuhIndexerClient` with `search_after` pagination. Live run: 8,471 findings across 5 in-boundary agents (brisket 2804, haccp 1899, regscale 1861, dojo 1861, smokehouse 46). Per ADR 0007 Task 10.
- **`pipelines/push/defectdojo.py`**: pushes normalized findings to DefectDojo, creating monthly engagement "ConMon YYYY-MM" per product.

**Control effectiveness assessment:**
- **`pipelines/build/oscal_poam.py`** + **`poam/POAM-2026-04.xlsx`**: assessment output artifact (8,473 items with FedRAMP SLA due dates).
- **`inventory/IIW-2026-04.xlsx`** (178 KB, 7 rows): Inventory of Interfaces and Weaknesses in FedRAMP Rev 5 template format (`templates/FedRAMP-IIW-Template-Rev5.xlsx`). Produced by `pipelines/render/iiw.py` from `oscal/component-definition.json`.
- **Test suite** (130+ tests in `tests/`): regression safety net for control effectiveness -- every pipeline module tested per ADR 0007 §"Test suite."

**Correlation and analysis:**
- Phase 14 Logstash enrichment pipeline on haccp: 5-stage pipeline (de-dot → OpenCTI TI lookups → novel-entity tracking in `haccp-entities-seen` → tier routing → Ollama classification on brisket qwen3:8b with token-bucket rate limit, 10/min cap after thermal hardening on 2026-04-08). Output: `logs-zeek.haccp-default-*`.
- Wazuh ML anomaly detection: Elastic ML trial license on haccp analyzing DC01/WS01 Windows Security events.

**Response actions:**
- Shuffle WF1 v2: webhook-triggered enrichment + OPNsense block + dedup via Cloudflare and AbuseIPDB.
- DefectDojo SLA clock: findings approaching SLA surfaced in monthly POA&M review.

**Status reporting:**
- Discord #morning-briefing: Shuffle WF10 (0530 EST) nightly briefing from Phase 14 pipeline.
- Discord #soc-alerts: real-time Wazuh/Shuffle alert routing.
- `poam/POAM-2026-04.xlsx`: monthly status report artifact.

### 4. Gaps / Open Items

CA-7 is implemented. All ODP parameters need to be set in the markdown scaffold. Monitoring frequency and metric ODPs planned values above. Status: **implemented**.

### 5. Related Controls

CA-2, CA-5, CA-7(4), CA-8, RA-5, SI-4, AU-6, PM-6

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-7.md`

---

## CA-7(4) -- Risk Monitoring

### 1. Control Statement Summary

Ensure risk monitoring is an integral part of the continuous monitoring strategy, including: effectiveness monitoring, compliance monitoring, and change monitoring.

### 2. Parameters

No ODPs. No `x-trestle-set-params` block in scaffold (`trestle-workspace/mss-ssp/ca/ca-7.4.md`).

### 3. Implementation Evidence

CA-7(4) is fully covered by the CA-7 evidence above, extended to the three monitoring dimensions:

**Effectiveness monitoring:**
- Wazuh 15 agents provide continuous real-time telemetry. Agent connectivity gaps surface in Wazuh Dashboard (brisket:5601) within minutes of failure.
- `./pipelines.sh conmon` re-ingests all open findings each cycle and recomputes SLA due dates in `pipelines/build/oscal_poam.py` -- findings that were "open" and have passed their SLA window are automatically identified in `poam/POAM-2026-04.xlsx`.
- Test suite (130+ tests): automated effectiveness check on every pipeline invocation. A regression in any pipeline module causes a test failure before the POA&M is published.
- Grafana alerting (brisket:3000): GPU thermal, agent health, and service-level metrics provide effectiveness signal for infrastructure controls.

**Compliance monitoring:**
- DefectDojo SLA engine: FedRAMP Low ConMon SLA windows (Critical=15, High=30, Medium=90, Low=180 days per `pipelines/build/oscal_poam.py` `SLA_DAYS`) enforce compliance with the FedRAMP Continuous Monitoring Strategy Guide. Per `deploy/defectdojo/post-install.sh`, SLA configurations are seeded into all 5 MSS products idempotently.
- FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`): 156 `<with-id>` references define the compliance boundary. Each `./pipelines.sh ssp-assemble` run validates that authored control prose maps to a defined FedRAMP Low control.
- OSCAL 1.1.2 schema validation: `trestle validate` run against all 5 OSCAL artifacts (catalog, profile, component-definition, SSP, POA&M) per ADR 0007. Schema validity is the compliance check for the ConMon artifact set.

**Change monitoring:**
- ADR series (`docs/adr/`): every significant system change generates an ADR. ADRs 0001-0008 cover infrastructure deployment (Plan 1), OSCAL pipeline build (Plan 2), and Plan 3 pre-execution realignment. The ADR trail is the change log.
- Wazuh syscollector: hardware and OS inventory data for all 15 agents stored in `wazuh-states-*` indices. Changes in OS version, installed packages, or hardware configuration surface on next agent check-in.
- Wazuh `wazuh-states-vulnerabilities-*` index: per-CVE vulnerability state tracked per agent. New CVEs appearing in the index since the last `./pipelines.sh ingest-findings` run represent change events.
- PBS daily backups (smoker LXC 300 → smokehouse NFS, `10.10.20.10:/pbs-datastore`): backup success/failure is a change indicator for VM availability. ADR 0005 documents the boot-race change event that caused a 5-day gap, and the fstab automount hardening that closes the monitoring gap.
- Git commit log: every pipeline code change is tracked in `github.com/brianchaplow/homelab-fedramp-low`. Direct commits to `main` per ADR 0006 Branch Strategy.

### 4. Gaps / Open Items

CA-7(4) is implemented via the same mechanisms as CA-7. No additional gaps beyond CA-7. Status: **implemented**.

### 5. Related Controls

CA-7, RA-3, PM-9, PM-28, SI-4

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-7.4.md`

---

## CA-8 -- Penetration Testing

### 1. Control Statement Summary

Conduct penetration testing at a defined frequency on defined system components.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| Frequency (a) | ca-08_odp.01 | `<REPLACE_ME>` | Annually; ad hoc following significant system change | organization |
| Target systems/components (b) | ca-08_odp.02 | `<REPLACE_ME>` | VLAN 40 target segment (10.10.40.0/24): DVWA + Juice Shop (10.10.40.10), Metasploitable 3 Linux (10.10.40.20), Metasploitable 3 Win (10.10.40.21), WordPress (10.10.40.30), crAPI (10.10.40.31) | organization |

FedRAMP Low does not mandate CA-8 as a baseline requirement; however, the homelab implements it as a core SOC capability.

### 3. Implementation Evidence

- **sear** (10.10.20.20, Kali Linux, 32GB, GTX 1650 Ti): dedicated attack box for penetration testing. Contains Kali toolset updated per fleet patch 2026-03-31 (documented in memory `fleet_update_2026-03-31.md`). SSH: `butcher@10.10.20.20` (Tailscale: `butcher@100.86.67.91`).
- **Caldera v5.3.0** (smoker:8888, 10.10.30.21): adversary emulation platform with 4 Sandcat agents enrolled. Red (Caldera `red` account) and Blue (Caldera `blue` account) teams configured. Shuffle WF3 integrates Caldera via `$caldera_url` and `$caldera_api_key` workflow variables.
- **Attack discipline:** All attacks target VLAN 40 only (10.10.40.0/24) per `CLAUDE.md` §"Conventions." The `./run_attack.sh` wrapper provides ground-truth logging for each penetration test session.
- **Wazuh detection validation:** Caldera red-team exercises validated Wazuh detection rules (Phase 7 complete per `CLAUDE.md` §v3 Migration Status, row Phase 7). Detection validation is the penetration testing feedback loop.
- **VLAN isolation:** MokerLink L3 switch (10.10.10.2) enforces VLAN 40 isolation via ACL. OPNsense (10.10.10.1) enforces inter-VLAN firewall rules. sear (VLAN 20) cannot route to VLAN 40 except through the attack path; this prevents lateral movement from the tester to production infrastructure.
- **Test coverage:** Targets include DVWA + Juice Shop (web application), Metasploitable 3 Linux and Win (multi-service), WordPress (WPScan), crAPI (REST API), vsftpd (FTP), SMTP relay, and SNMPd -- all on VLAN 40.

### 4. Gaps / Open Items

No formal penetration test report artifact currently exists in the repo. `./run_attack.sh` logs exist on sear but are not committed. A formal pen-test report artifact is a Plan 4 writeup item. Status: **partial** (capability fully operational; formal report artifact pending).

### 5. Related Controls

CA-2, CA-7, RA-5, SI-4, IR-4

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-8.md`

---

## CA-9 -- Internal System Connections

### 1. Control Statement Summary

Authorize internal connections of defined system components; document interface characteristics, security requirements, privacy requirements, and nature of information communicated for each; terminate connections after defined conditions; review the need for each connection at defined frequency.

### 2. Parameters

| ODP | Identifier | Profile default | Planned value | Origin |
|-----|------------|-----------------|---------------|--------|
| System components authorized for internal connection (a) | ca-09_odp.01 | `<REPLACE_ME>` | All VLAN 20 + VLAN 30 components listed in `CLAUDE.md` §"All Hosts" | organization |
| Termination conditions (c) | ca-09_odp.02 | `<REPLACE_ME>` | Component decommission; security incident requiring isolation; unauthorized connection detected | organization |
| Review frequency (d) | ca-09_odp.03 | `<REPLACE_ME>` | Annually; following significant network or component change | organization |

### 3. Implementation Evidence

**Authorization and documentation mechanism:**
- **`CLAUDE.md` §"All Hosts" table**: authoritative inventory of all in-boundary and connected hosts, including IP, VLAN, and role. Every host listed is an authorized internal connection.
- **`CLAUDE.md` §"VLANs" table**: defines the VLAN architecture that partitions connections by trust level (VLAN 10 Management, VLAN 20 SOC, VLAN 30 Lab/Proxmox/AD, VLAN 40 Targets -- ISOLATED).
- **`CLAUDE.md` §"Network Quick Reference" → `reference/network.md`**: detailed topology, OPNsense interfaces, firewall rules, and MokerLink ACL table. The MokerLink ACL table is the authorization record for inter-VLAN connections.
- **`oscal/component-definition.json`** (16 KB, 7 components): OSCAL-format inventory of in-boundary components (brisket, haccp, smokehouse, dojo, regscale, opnsense, mokerlink) produced by `pipelines/build/oscal_component.py` from live Wazuh syscollector data + `inventory/overlay.yaml`.

**Key internal connections and authorization status:**

| Connection | Interface | Information | VLAN path | Authorization |
|------------|-----------|-------------|-----------|---------------|
| Wazuh agents (15) → Manager (brisket:1514/1515) | OSSEC protocol (encrypted) | Security events, syscollector, vuln scan | VLAN 20/30/10 → VLAN 20 | Authorized by Wazuh Manager enrollment |
| Filebeat (smokehouse) → Logstash (brisket:5044) | Beat protocol | Zeek logs | VLAN 20 | Authorized per Phase 2 Zeek pipeline |
| Fleet agents (haccp) → Elasticsearch (haccp:9200) | HTTPS | ELK telemetry | VLAN 30 (local) | Authorized per Phase 10 ELK migration |
| Logstash (haccp) → OpenCTI (brisket:8080) | HTTP/REST | TI lookups | VLAN 30 → VLAN 20 | Authorized per Phase 14 enrichment pipeline |
| Logstash (haccp) → Ollama (brisket:11434) | HTTP | LLM classification | VLAN 30 → VLAN 20 | Authorized per Phase 14 (token-bucket rate limit) |
| PBS LXC 300 (10.10.30.24) → smokehouse NFS (10.10.20.10) | NFSv3/v4 | VM backup data | VLAN 30 → VLAN 20 | Authorized per Phase 11; fstab automount hardened per ADR 0005 |
| dojo (10.10.30.27) → brisket Wazuh (agent 016) | OSSEC | Security events | VLAN 30 → VLAN 20 | Authorized per Plan 1 (ADR 0002) |
| regscale (10.10.30.28) → brisket Wazuh (agent 017) | OSSEC | Security events | VLAN 30 → VLAN 20 | Authorized per Plan 1 (ADR 0002) |
| PITBOSS (10.10.10.100) → pipelines endpoint | SSH/Git Bash | Pipeline invocations | VLAN 10 → VLAN 20 | Authorized per management VLAN design |

**Enforcement mechanism:**
- **MokerLink L3 switch** (10.10.10.2): ACL table enforces authorized inter-VLAN routing. VLAN 40 targets are isolated -- no routing path from target segment to production VLANs except through OPNsense firewall rules explicitly permitting the Caldera C2 path.
- **OPNsense firewall** (10.10.10.1): inter-VLAN rules enforce the connection policy. Firewall rules documented in `reference/network.md`.
- **MokerLink mirror sessions 1+2** (TE1-TE9 → TE10/TE11): SPAN configuration feeds haccp `span0` USB 2.5GbE (Arkime capture) and smokehouse sensor -- authorized read-only mirror, not a routable connection.

**Termination conditions:**
- Component decommission: OpenCTI LXC 202 (10.10.30.26) is a documented example -- decommissioned after Phase 12 migration to brisket Docker; autostart disabled; connection terminated.
- Security incident: Shuffle WF1 v2 can trigger OPNsense block via `$cf_api_token` and `$cf_account_id` Cloudflare workflow variables -- immediate connection termination path exists.

### 4. Gaps / Open Items

The internal connection inventory is documented in `CLAUDE.md` and `oscal/component-definition.json` but no single structured CA-9 authorization table exists in the repo as a standalone artifact. The SSP prose (this control) will serve as that artifact. Review frequency parameter not yet set in markdown. Status: **implemented** (connections authorized and documented; formal review scheduling pending).

### 5. Related Controls

CA-3, SC-7, AC-4, AC-17, CM-8

### 6. Scaffold File

`trestle-workspace/mss-ssp/ca/ca-9.md`

---

## Summary Table

| Control | Scaffold File | Status | Key Evidence |
|---------|--------------|--------|--------------|
| CA-1 | `ca/ca-1.md` | partial | This SSP; ADR series; `runbooks/monthly-conmon.md` |
| CA-2 | `ca/ca-2.md` | partial | `tests/` (130 tests); `poam/POAM-2026-04.xlsx` (8,473 items); DefectDojo products; ADR 0007 |
| CA-2(1) | `ca/ca-2.1.md` | partial | Automated pipeline independence; `pipelines/ingest/wazuh_vulns.py`; Gate 3 144-spot-check |
| CA-3 | `ca/ca-3.md` | partial | Tailscale mesh; PBS NFS (ADR 0005); Wazuh agent-manager paths; `CLAUDE.md` §external connections |
| CA-5 | `ca/ca-5.md` | implemented | `pipelines/build/oscal_poam.py`; `poam/POAM-2026-04.xlsx`; `./pipelines.sh conmon`; DefectDojo SLA |
| CA-6 | `ca/ca-6.md` | planned | This SSP as ATO artifact; ADR 0009 (pending Gate 5) |
| CA-7 | `ca/ca-7.md` | implemented | `./pipelines.sh conmon`; Wazuh 15 agents; ELK; OpenCTI; Grafana; Shuffle; Phase 14 enrichment pipeline |
| CA-7(4) | `ca/ca-7.4.md` | implemented | Effectiveness: test suite + Grafana; Compliance: DefectDojo SLA + OSCAL validation; Change: ADR trail + Wazuh syscollector + git log |
| CA-8 | `ca/ca-8.md` | partial | sear Kali; Caldera v5.3.0; VLAN 40 targets; `./run_attack.sh`; Wazuh detection validation |
| CA-9 | `ca/ca-9.md` | implemented | MokerLink ACL; OPNsense firewall; `oscal/component-definition.json`; `CLAUDE.md` §All Hosts; SPAN mirror sessions |

**Param fill notes:**
- All CA ODPs are organization-defined; no FedRAMP Low baseline mandates a fixed value for any CA parameter.
- Planned values above represent the homelab cadence: annual review, monthly ConMon cycle, 15/30/90/180 SLA days.
- The `ca-7_prm_4` / `ca-7_prm_5` aggregated params (security+privacy reporting recipients/frequency) will be identical values since this system has a single stakeholder.

**Evidence paths verified as of 2026-04-09:**
- `trestle-workspace/mss-ssp/ca/ca-*.md` -- confirmed via `ls trestle-workspace/mss-ssp/ca/` (10 files)
- `pipelines/build/oscal_poam.py` -- confirmed via file enumeration; `SLA_DAYS` dict read at lines 49-54
- `pipelines/cli.py` -- confirmed; `conmon` command at line 272
- `pipelines/render/poam.py`, `pipelines/render/iiw.py` -- confirmed via Glob
- `pipelines/ingest/wazuh_vulns.py` -- confirmed via Glob
- `pipelines/push/defectdojo.py` -- confirmed via Glob
- `pipelines/build/oscal_component.py` -- confirmed via Glob
- `docs/adr/0002-deployment-complete.md` through `docs/adr/0008-plan-3-pre-execution-realignment.md` -- confirmed via Read
- `runbooks/monthly-conmon.md` -- confirmed via Read
- `tests/smoke/check_defectdojo.sh`, `tests/smoke/check_regscale.sh` -- confirmed via Glob
- `templates/FedRAMP-POAM-Template-Rev5.xlsx`, `templates/FedRAMP-IIW-Template-Rev5.xlsx` -- confirmed via Glob
- `deploy/defectdojo/post-install.sh` -- confirmed via Glob
- `oscal/ssp.json`, `oscal/component-definition.json` -- documented in ADR 0007 final artifact inventory
- `poam/POAM-2026-04.xlsx`, `inventory/IIW-2026-04.xlsx` -- documented in ADR 0007 final artifact inventory
- `docs/adr/0009-plan-3-complete.md` -- does not yet exist (pending Plan 3 Gate 5; referenced as planned)
