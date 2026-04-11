# RA -- Risk Assessment Evidence Catalog

**Family:** Risk Assessment (RA)
**Controls in FedRAMP Rev 5 Low baseline:** 8 (ra-1, ra-2, ra-3, ra-3.1, ra-5, ra-5.2, ra-5.11, ra-7)
**Scaffold files verified:** `trestle-workspace/mss-ssp/ra/` -- all 8 files confirmed present
**Catalog produced:** 2026-04-09 (Plan 3 Phase 1)
**Subagent:** ra-catalog

---

## RA-1 Risk Assessment Policy and Procedures

- **Status:** partial
- **Primary mechanism:** The homelab FedRAMP Low ConMon program operates under an informal risk assessment policy embodied across the ADR chain (ADRs 0001–0008) and the Plan design specs. ADR 0008 establishes the pre-execution policy that governs the SSP authoring phase; ADR 0006 establishes the ConMon pipeline policy. No formal signed policy document exists -- this is a single-operator personal system with no HR or formal organizational approval chain.
- **Supporting mechanisms:** The `pipelines.sh conmon` orchestration script codifies the monthly review cadence. The Makefile thin-alias pattern preserves the single-entry-point invariant established in Plan 1. ADRs serve as the de-facto policy record: each documents a decision, rationale, and consequence in a format a GRC reviewer can follow.
- **Evidence paths:**
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (risk assessment policy and ConMon approach)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` (authoring policy, parameter fill policy, status rubric)
  - `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` §3 (four content decisions = policy)
  - `runbooks/monthly-conmon.md` (operational procedure for monthly ConMon cycle)
  - `pipelines.sh` (orchestration entry point -- one-command conmon policy execution)
- **Set-params (proposed values):**
  - `ra-01_odp.01` (personnel or roles to disseminate policy to): `["Brian Chaplow (system owner, sole operator)"]`, `organization` -- single-operator system; no additional personnel
  - `ra-01_odp.02` (personnel or roles to disseminate procedures to): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `ra-01_odp.03` (policy review frequency): `annually`, `organization` -- aligns with the annual ConMon review cycle
  - `ra-01_odp.04` (policy review triggering events): `"following a significant architecture change, phase completion, or security incident as documented in an ADR"`, `organization`
  - `ra-01_odp.05` (procedure review frequency): `annually`, `organization`
  - `ra-01_odp.06` (procedure review triggering events): `"following a significant architecture change, phase completion, or security incident as documented in an ADR"`, `organization`
  - `ra-01_odp.07` (policy scope selection): `"system-level"`, `organization` -- homelab is a single system; no mission/business-process-level structure
  - `ra-01_odp.08` (official to manage policy): `"Brian Chaplow (system owner, sole operator)"`, `organization`
- **Authoring notes:** Lead with ADR chain as the de-facto policy mechanism. Explicitly acknowledge the partial status: no formal signed policy document, no HR/approval chain. Paragraph 2 can reference that the ADR pattern meets the spirit of RA-1 for a single-operator lab posture. Use "system-level" for the selection parameter -- the homelab has no organizational or mission/business-process tier.

---

## RA-2 Security Categorization

- **Status:** implemented
- **Primary mechanism:** The Managed SOC Service (MSS) homelab is categorized as **FIPS 199 Low** across all three security objectives (Confidentiality Low, Integrity Low, Availability Low). This categorization is consistent with the system's purpose: a portfolio-demonstration ConMon environment with no PII, no production customer data, and no life-safety functions. The FedRAMP Low baseline was explicitly selected at project inception and documented in ADR 0001.
- **Supporting mechanisms:** The FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) anchors the categorization -- it selects exactly 156 controls appropriate for Low-impact systems. The OSCAL SSP (`oscal/ssp.json`) carries the system-id `managed-soc-service` throughout. The IIW (`inventory/IIW-2026-04.xlsx`) records 7 in-boundary components all classified as Low-impact assets.
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (FedRAMP Low baseline selection decision)
  - `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (156 Low controls -- the categorization artifact)
  - `oscal/ssp.json` (system-id `managed-soc-service`, SSP scaffold)
  - `inventory/IIW-2026-04.xlsx` (7 in-boundary components, all Low-impact)
  - `inventory/overlay.yaml` (asset classification and boundary definition -- in/out-of-boundary)
- **Set-params (proposed values):**
  - RA-2 has no `x-trestle-set-params` in the scaffold -- no ODPs to fill.
- **Authoring notes:** This is a clean `implemented` -- the Low categorization is explicit and documented. Lead with FIPS 199 Low across C/I/A. Cite ADR 0001 as the categorization decision point. Note that the FedRAMP Low profile (156 controls) is the operationalized artifact of the categorization. Single paragraph is sufficient.

---

## RA-3 Risk Assessment

- **Status:** partial
- **Primary mechanism:** The monthly ConMon cycle (`./pipelines.sh conmon`) produces a continuously updated risk picture: Wazuh reads 12,949 vulnerability-state documents from the `wazuh-states-vulnerabilities-*` OpenSearch index on brisket (5 in-boundary agents), normalizes them into 8,471 findings with CVE, CVSS score, severity, and affected host, and pushes them to DefectDojo 2.57.0 on dojo (10.10.30.27:8080). The resulting DefectDojo finding inventory is the operational risk register. FedRAMP Low SLA windows (Critical 15d, High 30d, Medium 90d, Low 180d) are applied per finding as due-date tags, which constitutes the likelihood-and-magnitude assessment per severity.
- **Supporting mechanisms:** The OSCAL POA&M (`poam/POAM-2026-04.xlsx`, 8,473 rows) is the formal risk documentation artifact. OpenCTI v7 on brisket (port 8080) provides threat intel context via 6 connectors, with IOC sync to Wazuh CDB lists every 6 hours -- this feeds the threat identification component of RA-3a.1. Zeek on haccp span0 and Suricata on smokehouse eth4 provide network-level threat surface visibility. The gap: there is no formal written risk assessment report or risk assessment board review -- this is a single-operator system. The POA&M and ConMon pipeline serve as the documented risk output.
- **Evidence paths:**
  - `pipelines/ingest/wazuh_vulns.py` (vulnerability ingestion from `wazuh-states-vulnerabilities-*`, 12,949 docs)
  - `pipelines/build/oscal_poam.py` (SLA window application: Critical 15d, High 30d, Medium 90d, Low 180d per ADR 0006 Amendment Task 12)
  - `pipelines/common/wazuh_indexer.py` (WazuhIndexerClient, VULN_INDEX_PATTERN)
  - `pipelines/cli.py` (`conmon` composite command, `IN_BOUNDARY_WAZUH_AGENTS` tuple)
  - `poam/POAM-2026-04.xlsx` (April 2026 POA&M, 8,473 rows -- the risk documentation artifact)
  - `docs/adr/0007-plan-2-complete.md` (live run: 8,471 findings across 5 agents)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Amendment Task 12: SLA window correction)
- **Set-params (proposed values):**
  - `ra-03_odp.01` (risk assessment document type selection): `"risk assessment report"`, `organization` -- the POAM-2026-04.xlsx + oscal/poam.json serve as the risk assessment report output
  - `ra-03_odp.02` (risk assessment review frequency): `monthly`, `organization` -- matches the ConMon cycle cadence
  - `ra-03_odp.03` (risk assessment update frequency): `monthly`, `organization` -- `./pipelines.sh conmon` regenerates the risk picture each cycle
  - `ra-03_odp.04` (risk assessment update triggering events): `"when a new vulnerability is discovered with CVSS >= 7.0 (High/Critical), when a new phase adds in-boundary infrastructure, or when an ADR records a significant change to the system"`, `organization`
  - `ra-03_odp.05` (personnel or roles to disseminate results to): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
- **Authoring notes:** Lead paragraph on the ConMon pipeline as the continuous risk assessment mechanism. Name the Wazuh indexer index, DefectDojo finding count, and SLA window enforcement. Paragraph 2: acknowledge the partial gap (no formal risk assessment board, no written RA report separate from the POA&M -- acceptable for a single-operator portfolio system). Cite ADR 0006 Amendment Task 12 explicitly for the SLA correction from wrong values (30/90/180/365) to correct FedRAMP Low values (15/30/90/180).

---

## RA-3.1 Supply Chain Risk Assessment

- **Status:** partial
- **Primary mechanism:** Supply chain risk for the MSS homelab is assessed informally through the hardware procurement and software version-pinning practices documented in the ADR chain. Hardware: all 5 in-boundary hosts are Lenovo ThinkStation P340 Tiny or equivalent commercial off-the-shelf (COTS) hardware from a US vendor (Lenovo). Software: Trestle 4.0.1 is pinned (ADR 0006 Deviation 9); Wazuh 4.14.4, ELK 8.17, and Zeek versions are tracked via the inventory syscollector data in the `wazuh-states-vulnerabilities-*` index. DefectDojo 2.57.0 and RegScale CE are pinned by Proxmox VM snapshots and ADR 0003/0004 deployment records.
- **Supporting mechanisms:** The `inventory/overlay.yaml` records hardware model, end-of-life dates (brisket 2029-04, haccp 2028-04, smokehouse 2027-12), and asset tags for all 5 in-boundary hosts -- this is the supply chain component inventory. No formal third-party risk assessment process exists: the lab has no vendor contracts, no supply chain attestation process, and no hardware SBOM. The partial status reflects honest scope: this is a portfolio demo system, not a federal production CSP.
- **Evidence paths:**
  - `inventory/overlay.yaml` (hardware models, end-of-life dates, asset tags for all in-boundary components)
  - `docs/adr/0001-preflight-and-eula.md` (system boundary and COTS hardware acknowledgment)
  - `docs/adr/0003-regscale-install-deviation.md` (RegScale CE version pin -- supply chain traceability)
  - `docs/adr/0004-defectdojo-install-deviation.md` (DefectDojo 2.57.0 version pin -- supply chain traceability)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Deviation 9: Trestle 4.0.1 pin -- supply chain traceability)
- **Set-params (proposed values):**
  - `ra-03.01_odp.01` (systems/components/services to assess): `"all 5 in-boundary hardware assets (brisket, haccp, smokehouse, dojo VM, regscale VM) and all open-source software stacks (Wazuh 4.14.4, ELK 8.17, DefectDojo 2.57.0, RegScale CE, Trestle 4.0.1)"`, `organization`
  - `ra-03.01_odp.02` (supply chain risk assessment update frequency): `annually`, `organization` -- aligns with hardware end-of-life review cadence in overlay.yaml
- **Authoring notes:** Lead with hardware COTS provenance and software version-pinning as the available supply chain controls. Acknowledge partial explicitly: no vendor contracts, no SBOM, no third-party attestation -- appropriate for a single-operator lab. Cite overlay.yaml end-of-life dates as the closest artifact to a supply chain review cadence.

---

## RA-5 Vulnerability Monitoring and Scanning

- **Status:** implemented
- **Primary mechanism:** Wazuh 4.14.4 on brisket provides continuous vulnerability monitoring for all 5 in-boundary agents via its built-in vulnerability detector module. The detector cross-references installed package versions (collected by syscollector) against the National Vulnerability Database (NVD) and vendor advisories, storing results in the `wazuh-states-vulnerabilities-*` index on the Wazuh OpenSearch indexer (brisket:9200). A live probe on 2026-04-09 confirmed 12,949 documents across 5 agents: brisket 2,804, haccp 1,899, regscale 1,861, dojo 1,861, smokehouse 46. Each document carries CVE identifier, CVSS base score (v2/v3/v4), Wazuh severity label (Critical/High/Medium/Low), detected_at timestamp, affected package name and version, and NVD reference URLs -- satisfying RA-5b's interoperability and enumeration requirements.
- **Supporting mechanisms:** The Plan 2 vulnerability pipeline (`pipelines/ingest/wazuh_vulns.py`) normalizes every indexer hit into a `Finding` schema (`pipelines/common/schemas.py`) and pushes findings to DefectDojo 2.57.0 on dojo via `pipelines/push/defectdojo.py`. DefectDojo applies FedRAMP Low SLA windows (Critical 15d, High 30d, Medium 90d, Low 180d) and tracks remediation state per finding. Zeek on haccp span0 and Suricata on smokehouse eth4 provide complementary network-level vulnerability surface detection -- detecting active exploitation attempts, lateral movement, and misconfigured services that host-based scanners miss. OpenCTI v7 syncs threat indicators to Wazuh CDB lists every 6 hours, enabling RA-5f (updating vulnerabilities to be scanned) for IOC-based detections.
- **Evidence paths:**
  - `pipelines/ingest/wazuh_vulns.py` (vulnerability ingestion, field mapping from `wazuh-states-vulnerabilities-*`, severity resolution, control tags RA-5+SI-2)
  - `pipelines/common/wazuh_indexer.py` (WazuhIndexerClient, `VULN_INDEX_PATTERN = "wazuh-states-vulnerabilities-*"`, search_after paging, 12,949-document live probe)
  - `pipelines/common/schemas.py` (Finding model: cve, cvss_score, severity, affected_host, affected_package, related_controls)
  - `pipelines/push/defectdojo.py` (DefectDojo push pipeline, SLA tracking)
  - `pipelines/build/oscal_poam.py` (`SLA_DAYS = {Critical: 15, High: 30, Medium: 90, Low: 180}`, remediation timeline enforcement)
  - `pipelines/cli.py` (`IN_BOUNDARY_WAZUH_AGENTS`, `ingest-findings` command, `conmon` composite)
  - `poam/POAM-2026-04.xlsx` (8,473 POA&M rows -- the vulnerability scan report artifact)
  - `inventory/IIW-2026-04.xlsx` (7 in-boundary components with authenticated-scan status)
  - `docs/adr/0007-plan-2-complete.md` (live end-to-end run: 8,471 findings pushed to 4 DefectDojo products)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Deviation 5: Wazuh 4.8 REST endpoint removal → indexer-based approach; Amendment Task 12: SLA window correction)
- **Set-params (proposed values):**
  - `ra-05_odp.01` (vulnerability monitoring/scanning frequency): `"continuously (Wazuh vulnerability detector runs on agent check-in) and monthly (full ConMon pipeline via ./pipelines.sh conmon)"`, `organization`
  - `ra-05_odp.02` (vulnerability monitoring/scanning process): `"Wazuh syscollector collects package inventory on agent check-in; the vulnerability detector cross-references NVD; results are stored in wazuh-states-vulnerabilities-* and ingested monthly via pipelines/ingest/wazuh_vulns.py"`, `organization`
  - `ra-05_odp.03` (response times for remediation): `"Critical: 15 days; High: 30 days; Medium: 90 days; Low: 180 days -- per FedRAMP Low ConMon Strategy Guide SLA windows, enforced in pipelines/build/oscal_poam.py SLA_DAYS dict"`, `organization`
  - `ra-05_odp.04` (personnel or roles to share vulnerability information with): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
- **Authoring notes:** This is the anchor control for the RA family -- give it full two-paragraph treatment. Paragraph 1: Wazuh vulnerability detector as the SCAP-aligned scanner (NVD cross-reference, CVE/CVSS enumeration satisfies RA-5b). Paragraph 2: the Plan 2 pipeline (wazuh_vulns.py → DefectDojo → POAM) as the analysis and remediation tracking mechanism (RA-5c and RA-5d). Cite the live finding counts and SLA windows. Mention Zeek/Suricata as network-layer complement. Note OpenCTI IOC sync as the RA-5f mechanism.

---

## RA-5.2 Update Vulnerabilities to Be Scanned

- **Status:** implemented
- **Primary mechanism:** Wazuh's vulnerability detector automatically updates its NVD feed and vendor-specific advisories on a regular basis as part of the Wazuh manager's built-in feed management. When Wazuh 4.14.4 detects a new CVE relevant to an in-boundary package version, it creates a new document in `wazuh-states-vulnerabilities-*` on the next agent check-in -- no operator action required. OpenCTI v7 on brisket syncs fresh IOCs from 6 connectors to Wazuh CDB lists every 6 hours (cron `0 */6 * * *`), extending the scanner's IOC awareness automatically.
- **Supporting mechanisms:** The monthly `./pipelines.sh ingest-findings` pull captures any new vulnerability documents that appeared since the last run. The DefectDojo engagement auto-create logic (`_engagement_name()` returns `ConMon YYYY-MM`) ensures new monthly scans produce a fresh engagement rather than silently accumulating into a stale one. The `wazuh-states-vulnerabilities-*` index pattern covers all future index shards without operator intervention.
- **Evidence paths:**
  - `pipelines/common/wazuh_indexer.py` (`VULN_INDEX_PATTERN = "wazuh-states-vulnerabilities-*"` -- wildcard covers new shards automatically)
  - `pipelines/cli.py` (`ingest-findings` command, `_engagement_name()` monthly engagement auto-create)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Deviation 5: indexer-based approach -- inherits Wazuh's built-in NVD update pipeline)
  - `C:/Projects/CLAUDE.md` OpenCTI section (cron `0 */6 * * *` -- IOC sync to Wazuh CDB lists, every 6 hours)
- **Set-params (proposed values):**
  - `ra-05.02_odp.01` (update frequency selection): `"prior to a new scan; when new vulnerabilities are identified and reported"`, `organization` -- Wazuh auto-updates before each agent check-in evaluation; the monthly pipeline run also captures any new NVD entries since the prior run
  - `ra-05.02_odp.02` (update frequency): `"monthly (ConMon pipeline run) and continuously (Wazuh NVD feed refresh)"`, `organization`
- **Authoring notes:** Keep to one paragraph -- this is a narrow enhancement. Lead with Wazuh's automatic NVD feed update as the primary mechanism. Second sentence on OpenCTI IOC sync as the IOC-based complement. Cite VULN_INDEX_PATTERN wildcard as the technical artifact showing future-proof coverage. Status is implemented because Wazuh's built-in feed management satisfies the requirement without manual operator action.

---

## RA-5.11 Public Disclosure Program

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. The Managed SOC Service is a single-operator personal portfolio system, not a publicly accessible service. There is no public-facing attack surface to which external researchers would report vulnerabilities, no public-facing web application, no bug bounty scope, and no mechanism for receiving external vulnerability reports. The system is entirely hosted on a private homelab network (VLAN 20/30, 10.10.x.x) with access restricted to the operator via Tailscale VPN.
- **Supporting mechanisms:** OPNsense on the perimeter firewall (10.10.10.1) blocks all inbound connections from the internet by default. No public IP addresses are assigned to in-boundary MSS hosts. The operator's GCP VM (external, Tailscale 100.125.40.97) hosts public websites (brianchaplow.com, bytesbourbonbbq.com) but those are out-of-boundary assets and are not part of the MSS system boundary per `inventory/overlay.yaml`.
- **Evidence paths:**
  - `inventory/overlay.yaml` (out_of_boundary list includes gcp-vm with reason "Customer asset on GCP")
  - `C:/Projects/CLAUDE.md` network section (VLAN 20/30 private addressing, OPNsense perimeter, Tailscale-only remote access)
  - `docs/adr/0001-preflight-and-eula.md` (system boundary definition -- private homelab, no public-facing MSS surface)
- **Set-params (proposed values):**
  - RA-5.11 has no `x-trestle-set-params` in the scaffold -- no ODPs to fill.
- **Authoring notes:** One sentence justification is sufficient for not-applicable: "The MSS homelab has no public-facing attack surface; all in-boundary hosts are on private VLAN 20/30 with no inbound internet access. A public disclosure channel would have no mechanism to receive reports." Do not leave the N/A undefended.

---

## RA-7 Risk Response

- **Status:** implemented
- **Primary mechanism:** Risk findings are responded to through a structured pipeline: Wazuh identifies vulnerabilities → `pipelines/ingest/wazuh_vulns.py` normalizes them into `Finding` records with FedRAMP SLA due-dates → DefectDojo 2.57.0 on dojo tracks remediation state (Open, In Progress, Completed, False Positive, Deviated) → `pipelines/build/oscal_poam.py` builds the OSCAL POA&M with SLA-driven scheduled-completion dates → `poam/POAM-2026-04.xlsx` is the formal risk response record. Each DefectDojo finding's state change (active → mitigated, active → risk-accepted/Deviated) constitutes a documented risk response decision. The state mapping priority (`false-positive > risk-accepted > mitigated > active > closed`) in `_finding_state()` implements the organization's risk tolerance decision tree.
- **Supporting mechanisms:** ADR 0005 is the archetypal risk response record: a PBS backup gap was discovered via monitoring, the threat was assessed (5-day gap, no data loss, acceptable risk for the ConMon cycle), a fix was implemented (NFS automount hardening), and a follow-up TODO was captured (PBS Wazuh/Discord alert). ADR 0006 Amendment Task 12 is another: the SLA window values were wrong (30/90/180/365), the risk was assessed (incorrect due-dates in the POA&M), and the response was immediate correction to FedRAMP-correct values (15/30/90/180). The monthly ConMon cycle (`./pipelines.sh conmon`) is the recurring risk response mechanism -- it closes the loop between identification and documented response.
- **Evidence paths:**
  - `pipelines/build/oscal_poam.py` (`_finding_state()` state mapping, SLA due-date computation -- the risk response logic)
  - `pipelines/push/defectdojo.py` (DefectDojo push -- finding state tracking)
  - `pipelines/cli.py` (`conmon` composite -- full risk response cycle)
  - `poam/POAM-2026-04.xlsx` (8,473 rows with remediation state -- the formal risk response artifact)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (live risk response example: gap identified → assessed → fixed → follow-up captured)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Amendment Task 12: SLA correction as risk response to wrong baseline values)
  - `runbooks/monthly-conmon.md` (operational procedure for recurring risk response cycle)
- **Set-params (proposed values):**
  - RA-7 has no `x-trestle-set-params` in the scaffold -- no ODPs to fill.
- **Authoring notes:** Lead with the ConMon pipeline as the systematic risk response mechanism: Wazuh → DefectDojo state → POA&M. Use ADR 0005 as the concrete example of RA-7 in action (finding → assessment → response → documentation). Paragraph 2 can call out the DefectDojo state machine (Open/Deviated/False Positive/Completed) as the organization's formalized risk response taxonomy. Status is implemented: every open finding has a documented SLA due-date and state, which satisfies RA-7's "respond in accordance with organizational risk tolerance" requirement.

---

## Verification Summary

| Control | Scaffold file verified | Status | Set-params count | Evidence paths verified |
|---------|----------------------|--------|------------------|------------------------|
| RA-1 | `trestle-workspace/mss-ssp/ra/ra-1.md` | partial | 8 ODPs | 5 |
| RA-2 | `trestle-workspace/mss-ssp/ra/ra-2.md` | implemented | 0 (no ODPs) | 5 |
| RA-3 | `trestle-workspace/mss-ssp/ra/ra-3.md` | partial | 5 ODPs | 7 |
| RA-3.1 | `trestle-workspace/mss-ssp/ra/ra-3.1.md` | partial | 2 ODPs | 5 |
| RA-5 | `trestle-workspace/mss-ssp/ra/ra-5.md` | implemented | 4 ODPs | 10 |
| RA-5.2 | `trestle-workspace/mss-ssp/ra/ra-5.2.md` | implemented | 2 ODPs | 4 |
| RA-5.11 | `trestle-workspace/mss-ssp/ra/ra-5.11.md` | not-applicable | 0 (no ODPs) | 3 |
| RA-7 | `trestle-workspace/mss-ssp/ra/ra-7.md` | implemented | 0 (no ODPs) | 7 |

**Controls cataloged:** 8
**Grep verifications performed:** 46 (all evidence paths confirmed present via Read/Grep/ls before inclusion)
**Cites to parent CLAUDE.md:** 2 (RA-5.2 OpenCTI IOC sync schedule; RA-5.11 network topology)
**Cites to ADRs:** 14 (ADRs 0001, 0003, 0004, 0005, 0006, 0006 Amendment Task 12, 0007, 0008)
**Unresolved questions:**
- RA-1 has no formal signed policy document -- the ADR chain is the de-facto policy. Authoring should explicitly acknowledge this and mark `partial` rather than claiming `implemented`. A reviewer may push back that even for a lab, a one-page policy document signed by the operator would satisfy RA-1 cleanly -- this is a known gap to defend.
- RA-3.1 supply chain assessment is genuinely thin for a lab: hardware SBOM and vendor-specific SLAs do not exist. The `partial` status is honest; prose should not overstate the control.
- FedRAMP profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `modify.set-parameters` section -- confirmed on read. All RA parameters are organization-defined with no baseline-mandated values to inherit. Every ODP value in this catalog uses `organization` origin.
