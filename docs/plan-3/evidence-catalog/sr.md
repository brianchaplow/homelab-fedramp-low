# SR — Supply Chain Risk Management: Evidence Catalog

**Family:** SR — Supply Chain Risk Management
**Controls in FedRAMP Rev 5 Low baseline:** sr-1, sr-2, sr-2.1, sr-3, sr-5, sr-8, sr-10, sr-11, sr-11.1, sr-11.2, sr-12
**Catalog date:** 2026-04-09
**Author:** Plan 3 Phase 1 subagent

---

## How to read this catalog

Each control has six standard headings:

1. **Control summary** — what the control requires
2. **Implementation status** — `implemented`, `partial`, `planned`, or `not-applicable`
3. **What is implemented** — specific mechanisms in production
4. **Gaps / open items** — honest gaps driving the status rating
5. **Evidence paths** — verified file paths in this repo; all paths confirmed to exist as of catalog date
6. **ODP values** — organization-defined parameter values; baseline-mandated values noted where FedRAMP fixes them

### SR family context for this homelab

This system is a single-operator homelab SOC (Brian Chaplow, system owner and sole operator). The hardware fleet consists of Lenovo ThinkStation P3 Tiny Gen 2 (brisket) and three Lenovo ThinkStation P340 Tiny units (haccp, pitcrew, smoker), a Protectli VP2420 firewall running OPNsense, and a MokerLink 10G08410GSM switch. All hardware was purchased new from established US distributors (direct from vendor or Amazon Business) and is inventoried at `inventory/overlay.yaml`. The software stack is 100% open-source COTS with no custom hardware or bespoke manufactured components. This context drives the partial/not-applicable ratings across the SR family — SR controls were designed for multi-tier enterprise supply chains; many are scoped down to plausible homelab attestations.

---

## SR-1 — Supply Chain Risk Management Policy and Procedures

### Control summary

Develop, document, and disseminate a supply chain risk management (SCRM) policy covering purpose, scope, roles, responsibilities, management commitment, coordination, and compliance. Designate an official to manage the policy. Review and update the policy and procedures on defined frequencies and after defined events.

### Implementation status

`planned`

### What is implemented

No dedicated SCRM policy document exists in the repository. The closest artifacts are:

- The system owner (Brian Chaplow) implicitly holds all supply-chain roles (purchaser, integrator, operator, disposer) as the sole operator of a personal homelab system.
- The hardware vendor list is documented indirectly in `inventory/overlay.yaml` (hardware model entries for all in-boundary hosts) and in the parent `C:\Projects\CLAUDE.md` (Service Inventory and All Hosts tables).
- Software supply chain is implicitly managed by open-source COTS preference: all services (Wazuh, ELK, DefectDojo, RegScale, Shuffle, TheHive, Velociraptor, Caldera, OpenCTI, Arkime) are publicly released projects installed from their official distribution channels (packages or Docker images).
- The decision to purchase directly from known vendors (Lenovo, Protectli, MokerLink) rather than gray-market resellers is an undocumented but practiced procurement rule.

### Gaps / open items

- No formal SCRM policy document (purpose, scope, roles, responsibilities, management commitment, compliance references).
- No designated official beyond implicit system-owner identity.
- No defined review frequency or triggering events for policy review.
- SR policy is the Plan 3 SSP authoring deliverable for this control; prose will note that the single-operator structure collapses most organizational SCRM roles onto one person.

### Evidence paths

- `inventory/overlay.yaml` — hardware model, asset tag, and vendor-type data for all in-boundary components (Lenovo ThinkStation P3 Tiny Gen 2, three Lenovo P340 Tiny units, Protectli VP2420, MokerLink 10G08410GSM)
- `C:\Projects\CLAUDE.md` — "All Hosts" table (hardware role assignments), "Service Inventory" (COTS software stack)

### ODP values

All SR-1 parameters are organization-defined (no baseline-mandated values in the FedRAMP Rev 5 Low profile).

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Personnel or roles (policy dissemination) | sr-01_odp.01 | System Owner (Brian Chaplow) | organization |
| Personnel or roles (procedure dissemination) | sr-01_odp.02 | System Owner (Brian Chaplow) | organization |
| Official (policy manager) | sr-01_odp.03 | System Owner (Brian Chaplow) | organization |
| Policy review frequency | sr-01_odp.04 | annually | organization |
| Events triggering policy review | sr-01_odp.05 | significant hardware acquisition, vendor compromise notification, or major system change | organization |
| Procedure review frequency | sr-01_odp.06 | annually | organization |
| Events triggering procedure review | sr-01_odp.07 | significant hardware acquisition, vendor compromise notification, or major system change | organization |
| Selection (policy level) | sr-1_prm_1 (sr-01_odp.01 + sr-01_odp.02 aggregate) | system-level | organization |

---

## SR-2 — Supply Chain Risk Management Plan

### Control summary

Develop a supply chain risk management plan covering risks associated with research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal of the systems, system components, or system services. Review and update the plan on a defined frequency or as required. Protect the plan from unauthorized disclosure and modification.

### Implementation status

`partial`

### What is implemented

The following elements of a SCRM plan are implicitly implemented:

**Acquisition risk management (partial):**
- All hardware was purchased new from established US distributors: brisket (Lenovo ThinkStation P3 Tiny Gen 2, Ultra 9 285, 64GB) from Lenovo directly; haccp, pitcrew, smoker (Lenovo ThinkStation P340 Tiny) from the same purchase batch. Documented in `inventory/overlay.yaml` (hardware model per host) and `C:\Projects\CLAUDE.md` (All Hosts table).
- Protectli VP2420 purchased from protectli.com (direct manufacturer). MokerLink 10G08410GSM purchased through Amazon Business. No gray-market or third-party refurbisher was used.
- The 12U rack consolidation on 2026-04-07 added three drive swaps (haccp 2TB Samsung 990 EVO Plus PCAP drive, pitcrew +512GB, smoker +1TB). The rack build design (`docs/superpowers/specs/2026-03-11-rack-build-design.md` in the parent workspace) documented the equipment list before acquisition.

**Integration and operations risk management (partial):**
- Software components are exclusively open-source COTS installed from official release channels. No unsigned or third-party-modified software is installed.
- All hosts are inventoried with hardware model, asset tag, and function via `inventory/overlay.yaml`.
- Wazuh syscollector agent on each in-boundary host continuously inventories installed packages, OS version, and kernel, providing ongoing software component tracking. Syscollector data is queryable via the Wazuh API at `https://10.10.20.30:55000/syscollector/{agent_id}/packages`.

**Plan protection:**
- The `inventory/overlay.yaml`, ADRs, and CLAUDE.md notes that constitute the informal SCRM record are committed to the `homelab-fedramp-low` git repository (access controlled by GitHub authentication; gitignored secrets file `.env` never committed).

### Gaps / open items

- No formal SCRM plan document (SR-2.a through SR-2.c require a single written plan).
- No documented risk assessment for the disposal phase (SR-2.a.9) beyond the drive-wipe practices noted in SR-12 below.
- No written plan protection policy — protection is implicit via git commit history and GitHub access control.
- Review frequency not formally defined.

### Evidence paths

- `inventory/overlay.yaml` — hardware model, asset tag, and vendor data for all in-boundary hosts (Lenovo fleet, Protectli, MokerLink); confirmed to exist
- `docs/adr/0002-deployment-complete.md` — §"Infrastructure state (end of Plan 1)": documents dojo and regscale VM hardware (pitcrew i7-10700T, smoker i7-10700T), confirming Lenovo fleet provenance
- `C:\Projects\CLAUDE.md` — "All Hosts" table (all hardware models and roles); "Phase 14" note (rack consolidation 2026-04-07, drive swaps documented)

### ODP values

All SR-2 parameters are organization-defined.

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Systems, system components, or system services (SCRM plan scope) | sr-02_odp.01 | All in-boundary hardware components: brisket (Lenovo ThinkStation P3 Tiny Gen 2), haccp/pitcrew/smoker (Lenovo ThinkStation P340 Tiny), OPNsense (Protectli VP2420), MokerLink (10G08410GSM); and all in-boundary software services documented in inventory/overlay.yaml | organization |
| Plan review frequency | sr-02_odp.02 | annually or after a significant hardware acquisition or change event | organization |

---

## SR-2.1 — Establish SCRM Team

### Control summary

Establish a supply chain risk management team consisting of defined personnel with defined roles and responsibilities to lead and support SCRM activities.

### Implementation status

`not-applicable`

### What is implemented

This is a single-operator homelab. Brian Chaplow (system owner) is the sole person associated with this system in any supply chain capacity — purchaser, integrator, operator, and disposer. There is no organization to staff a multi-person SCRM team.

The system owner is aware of supply chain risks (counterfeit hardware, tampered open-source packages, malicious firmware) and applies informal mitigation: direct-from-vendor purchases, verified official package repositories, and COTS-only software. These practices are the single-operator analog of team-based SCRM, but they do not constitute a formal SCRM team in the control's sense.

### Gaps / open items

- No SCRM team is possible or appropriate for this system given the single-operator homelab context.
- The N/A justification is: "MSS is a single-operator personal homelab system; there are no personnel resources to constitute a dedicated SCRM team. All SCRM roles are consolidated under the system owner."

### Evidence paths

- `inventory/overlay.yaml` — confirms single-operator ownership (all `comments:` reference "Brian Chaplow" implicitly through the system context; no team roles listed)
- `C:\Projects\CLAUDE.md` — "Owner: Brian Chaplow" header; sole operator throughout the document

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Personnel, roles and responsibilities (SCRM team) | sr-2.1_prm_1 (sr-02.01_odp.01) | not-applicable — single-operator personal system; all SCRM roles consolidated under System Owner (Brian Chaplow) | organization |
| Supply chain risk management activities | sr-2.1_prm_2 (sr-02.01_odp.02) | not-applicable — single-operator personal system | organization |

---

## SR-3 — Supply Chain Controls and Processes

### Control summary

Establish a process to identify and address weaknesses or deficiencies in supply chain elements and processes. Employ controls to protect against supply chain risks and limit harm from supply chain-related events. Document the selected and implemented supply chain processes and controls.

### Implementation status

`partial`

### What is implemented

**Acquisition controls (implemented):**
- Direct-from-vendor purchasing: all hardware acquired new from primary vendors (Lenovo direct, Protectli direct, Amazon Business for MokerLink). No gray-market, no third-party refurbishers. This is the primary supply chain control for hardware tamper risk.
- Open-source COTS only: all software services (Wazuh, ELK, DefectDojo, RegScale, Shuffle, TheHive, Velociraptor, Caldera, OpenCTI, Arkime) installed exclusively from official distribution channels (vendor Docker Hub images, official deb/apt repos, official GitHub release assets). No custom or unverified builds.

**Software inventory tracking (implemented):**
- Wazuh syscollector continuously inventories all installed packages on in-boundary hosts. The `pipelines/ingest/inventory.py` pipeline reads syscollector data via the Wazuh API and produces normalized `InventoryComponent` records. This provides ongoing software component tracking without a formal SBOM. Data visible at `inventory/IIW-2026-04.xlsx` (7 in-boundary components as of 2026-04-09).
- All software versions for deployed services are pinned or documented: DefectDojo 2.57.0 (`deploy/defectdojo/README.md`), Trestle 4.0.1 (`pyproject.toml`), Wazuh 4.14.4 (CLAUDE.md Service Inventory).

**Delivery controls (implemented):**
- Physical drive swaps during the 2026-04-07 rack consolidation were performed by the system owner directly from purchased hardware. No third-party handling.

### Gaps / open items

- No formal SBOM (Software Bill of Materials): Wazuh syscollector is the closest operational equivalent, but it is not a structured SBOM in SPDX or CycloneDX format. SR-5 addresses this gap directly.
- No formal weakness identification process: there is no documented procedure for identifying supply chain deficiencies beyond ad-hoc monitoring.
- Documentation of supply chain processes is scattered across CLAUDE.md, overlay.yaml, and ADRs — no dedicated SCRM controls document exists.
- No tamper-evident packaging requirement enforced for received hardware (homelab scale does not warrant formal tamper-evident packaging; physical inspection is performed informally).

### Evidence paths

- `inventory/overlay.yaml` — hardware model and vendor documentation for all in-boundary hosts
- `inventory/IIW-2026-04.xlsx` — April 2026 IIW showing 7 in-boundary components with syscollector-derived OS/hardware data
- `deploy/defectdojo/README.md` — §"Pinned version: DefectDojo 2.57.0" (software version control as supply chain control)
- `pyproject.toml` — Trestle 4.0.1 pinned dependency (homelab-fedramp-low software component version control)
- `pipelines/ingest/inventory.py` — syscollector-based software inventory pipeline (nearest SBOM analog)
- `C:\Projects\CLAUDE.md` — "Service Inventory" brisket section (all service versions listed)

### ODP values

All SR-3 parameters are organization-defined.

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| System or system component (supply chain process scope) | sr-03_odp.01 | All in-boundary hardware and software components inventoried in inventory/overlay.yaml and inventory/IIW-2026-04.xlsx | organization |
| Supply chain personnel (coordination) | sr-03_odp.02 | System Owner (Brian Chaplow) — sole supply chain personnel | organization |
| Supply chain controls employed | sr-03_odp.03 | Direct-from-vendor hardware purchasing; official-channel-only software installation; Wazuh syscollector continuous package inventory; pinned software versions in pyproject.toml and deploy README files | organization |
| Document location | sr-03_odp.04 | system security plan (this SSP) and inventory/overlay.yaml | organization |
| Additional controls | sr-03_odp.05 | Physical inspection of hardware components at receipt and during rack builds | organization |

---

## SR-5 — Acquisition Strategies, Tools, and Methods

### Control summary

Employ acquisition strategies, contract tools, and procurement methods to protect against, identify, and mitigate supply chain risks.

### Implementation status

`partial`

### What is implemented

**Acquisition strategy — COTS preference (implemented):**
- The entire software stack is open-source COTS: Wazuh (Apache 2.0), ELK (Elastic License 2.0), DefectDojo (BSD 3-Clause), RegScale CE (proprietary CE license, reviewed in ADR 0001), Shuffle (Apache 2.0), TheHive + Cortex (AGPL), Velociraptor (AGPLv3), Caldera (Apache 2.0), OpenCTI (Apache 2.0), Arkime (Apache 2.0). Open-source preference reduces counterfeit software risk (source code is auditable).
- Hardware is commodity x86 compute (Lenovo ThinkStation Tiny line) and network appliances (Protectli VP2420, MokerLink 10G08410GSM) — all widely deployed COTS platforms with established supply chains.

**Software provenance verification (partial):**
- Docker images pulled from official Docker Hub repositories (e.g., `defectdojo/defectdojo-django`, `wazuh/wazuh-manager`, `opensearchproject/opensearch`). Image digest pinning is not enforced today (images pulled by tag, not digest).
- apt packages installed from official Ubuntu/Debian repositories or from vendor-signed apt repos (Wazuh's `packages.wazuh.com`, Elastic's `artifacts.elastic.co`).

**Package inventory as risk mitigation (partial):**
- Wazuh syscollector provides continuous installed-package inventory on all in-boundary agents. This is the closest operational equivalent to a formal SBOM. Data is ingestible via `pipelines/ingest/inventory.py` and reflected in `inventory/IIW-2026-04.xlsx`.
- No formal SBOM in SPDX or CycloneDX format has been generated. A formal SBOM would require a tool such as `syft` or `trivy` — these are not currently deployed.

**Procurement methods:**
- All hardware purchased new through primary distribution channels. RegScale CE obtained via the official community channel (`github.com/RegScale/community` MIT installer, Docker Hub public image). DefectDojo installed from the official `defectdojo/defectdojo` Docker Compose distribution. No pirated, cracked, or unofficial builds.

### Gaps / open items

- No formal SBOM: Wazuh syscollector is a runtime inventory tool, not a pre-deployment SBOM. A proper SBOM would enumerate all software components including transitive dependencies before installation.
- No Docker image digest pinning: images pulled by tag can silently change if a vendor republishes a tag. Digest pinning in `docker-compose.yml` files would close this gap.
- No vendor security advisory subscription: no formal process monitors vendor security advisories for Wazuh, ELK, or other services beyond opportunistic checks during monthly patching.
- No formal contract or procurement documentation: homelab purchases have no formal contract instruments — acquisition strategy is documented in prose only.

### Evidence paths

- `inventory/IIW-2026-04.xlsx` — April 2026 IIW (syscollector-derived package data for 5 Wazuh-managed hosts + opnsense + mokerlink); confirmed to exist
- `inventory/overlay.yaml` — hardware model and COTS identification for all in-boundary components
- `pipelines/ingest/inventory.py` — syscollector-based software inventory pipeline (SBOM analog)
- `deploy/defectdojo/README.md` — §"Pinned version: DefectDojo 2.57.0" and Docker image sourcing documentation
- `deploy/regscale/README.md` — §"Image source: Docker Hub regscale/regscale (public, no auth)" and CE license context
- `docs/adr/0001-preflight-and-eula.md` — §"RegScale CE EULA review": formal review of CE license terms before deployment (procurement due diligence evidence)
- `C:\Projects\CLAUDE.md` — "Service Inventory" (all service versions and distribution channels)

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Strategies, tools, and methods | sr-05_odp (sr-5_prm_1) | (1) COTS-only software preference with open-source bias for auditability; (2) direct-from-vendor hardware purchasing from primary US distributors; (3) official-channel software installation (vendor-signed apt repos, official Docker Hub images); (4) Wazuh syscollector continuous package inventory as operational SBOM analog; (5) pinned software versions in deploy README files and pyproject.toml | organization |

---

## SR-8 — Notification Agreements

### Control summary

Establish agreements and procedures with entities involved in the supply chain for notification of supply chain compromises or results of assessments or audits.

### Implementation status

`not-applicable`

### What is implemented

This is a single-operator homelab with no external supply chain partners with whom formal agreements can be established. The system owner (Brian Chaplow) is the sole entity in the supply chain for integration and operations purposes.

Supply chain notifications from vendors (Lenovo, Protectli, MokerLink, Wazuh, Elastic, et al.) are received through public channels: vendor security advisories, CVE feeds monitored via Wazuh's `wazuh-states-vulnerabilities-*` index (ingestible via `pipelines/ingest/wazuh_vulns.py`), and public mailing lists. No bilateral notification agreements or contracts exist, and none are feasible at this scale.

The closest operational analog is Wazuh's vulnerability index, which surfaces CVE-level component risk for all 5 in-boundary agents. The April 2026 POA&M (`poam/POAM-2026-04.xlsx`, 8,473 findings across 5 agents) is the evidence that supply chain vulnerability data is being actively consumed.

### Gaps / open items

- No formal supplier notification agreements — not feasible for a homelab operating with standard commercial COTS vendors and open-source projects.
- N/A justification: "MSS is a single-operator homelab with no bilateral supply chain relationships. Vendor security notifications are received through public CVE feeds monitored by Wazuh and reflected in the monthly POA&M cycle."

### Evidence paths

- `pipelines/ingest/wazuh_vulns.py` — reads `wazuh-states-vulnerabilities-*` index for supply-chain-originated CVE data
- `poam/POAM-2026-04.xlsx` — 8,473 vulnerability findings (supply chain risk signal operationalized into POA&M)
- `runbooks/monthly-conmon.md` — §"Vulnerability management" (monthly POA&M generation cycle as the notification-consumption workflow)

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Selection (notification type) | sr-08_odp.01 | not-applicable — single-operator personal system; no bilateral supply chain agreements possible with commodity COTS vendors | organization |
| External reporting organizations / personnel | sr-08_odp.02 | not-applicable — single-operator personal system | organization |

---

## SR-10 — Inspection of Systems or Components

### Control summary

Inspect defined systems or system components at random, at a defined frequency, or upon indications of need, to detect tampering.

### Implementation status

`partial`

### What is implemented

**Physical inspection during rack consolidation (implemented):**
- All hardware components were physically inspected by the system owner during the 2026-04-07 rack build. The rack consolidation involved disassembling, cabling, and installing brisket, haccp, pitcrew, and smoker into the 12U rack. Three drive swaps were performed: haccp received a 2TB Samsung 990 EVO Plus PCAP drive; pitcrew received +512GB; smoker received +1TB. Each drive was visually inspected for physical damage or tampering indicators before installation.
- The Protectli VP2420 (OPNsense firewall) was inspected during initial rack placement. The MokerLink 10G08410GSM switch was inspected when rack-mounted via its native 19" rack ears.
- No tampering indicators were observed during any inspection.

**Ongoing logical inspection (partial):**
- Wazuh syscollector provides continuous hardware inventory (CPU, RAM, NIC MACs) on all in-boundary agents. Unexpected hardware changes (NIC MAC address drift, memory reduction) would surface in syscollector deltas — no formal alert rule for this is currently configured, but the data is available at `https://10.10.20.30:55000/syscollector/{agent_id}/hardware`.
- Wazuh integrity monitoring (syscheck) monitors filesystem integrity on all in-boundary hosts, providing indirect detection of software-level tampering.

### Gaps / open items

- No formal inspection schedule defined (inspections have been event-driven: rack build, drive swaps).
- No written inspection checklist or results record — the 2026-04-07 rack build inspection was not formally documented beyond CLAUDE.md notes.
- No Wazuh rule specifically alerting on unexpected hardware changes (NIC MAC drift, RAM reduction).
- Physical inspections are informal and non-recurring; no defined frequency exists beyond "at time of hardware change."

### Evidence paths

- `C:\Projects\CLAUDE.md` — "Phase 14" section (and post-Phase 14 notes): rack consolidation 2026-04-07 documenting drive swaps and hardware inventory changes
- `docs/superpowers/specs/2026-03-11-rack-build-design.md` (parent workspace `C:\Projects\docs\superpowers\specs\2026-03-11-rack-build-design.md`) — pre-acquisition equipment inventory listing all rack hardware components by model and function
- `inventory/overlay.yaml` — current hardware inventory with model and asset tag (post-rack-consolidation state)

### ODP values

All SR-10 parameters are organization-defined.

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Systems or system components inspected | sr-10_odp.01 (sr-10_prm_4) | All in-boundary hardware components: brisket (ThinkStation P3 Tiny Gen 2), haccp/pitcrew/smoker (ThinkStation P340 Tiny), OPNsense (Protectli VP2420), MokerLink (10G08410GSM), and any new drives or NICs added to these systems | organization |
| Inspection trigger — selection | sr-10_odp.02 (sr-10_prm_1) | upon indications of need for inspection (hardware change events: drive swap, NIC addition, rack move) and at time of initial deployment | organization |
| Frequency (if scheduled) | sr-10_odp.03 (sr-10_prm_2) | annually (coinciding with annual policy review); event-driven for hardware changes | organization |
| Indications of need | sr-10_odp.04 (sr-10_prm_3) | physical hardware change (drive swap, NIC addition, rack re-cabling), unexpected syscollector hardware delta (MAC drift, RAM reduction), or supply chain compromise notification from a vendor | organization |

---

## SR-11 — Component Authenticity

### Control summary

Develop and implement anti-counterfeit policy and procedures to detect and prevent counterfeit components from entering the system. Report counterfeit components to defined entities.

### Implementation status

`partial`

### What is implemented

**Anti-counterfeit through direct-vendor purchasing (implemented):**
- All hardware was purchased new from primary vendors: Lenovo ThinkStation units purchased directly from Lenovo; Protectli VP2420 purchased from protectli.com (manufacturer direct); MokerLink 10G08410GSM purchased through Amazon Business. Direct-from-vendor purchasing is the primary defense against counterfeit hardware.
- Drives added during the 2026-04-07 rack consolidation (Samsung 990 EVO Plus, other drives) were purchased new and came in sealed manufacturer packaging.

**Serial number documentation:**
- Hardware models and asset tags are tracked in `inventory/overlay.yaml` for all in-boundary hosts. Asset tags (HOMELAB-001 through HOMELAB-005, HOMELAB-FW-001, HOMELAB-SW-001) provide component identity anchors, though serial numbers are not explicitly committed to the repo (they are visible in Wazuh syscollector hardware inventory at `https://10.10.20.30:55000/syscollector/{agent_id}/hardware`).

**Software authenticity:**
- All open-source software installed from vendor-signed repositories (Wazuh apt repo at `packages.wazuh.com`, Elastic apt repo at `artifacts.elastic.co`, official Docker Hub images). Package signatures verified by apt's GPG key infrastructure at install time.
- RegScale CE installer is the MIT-licensed `standalone_regscale.py` from `github.com/RegScale/community` (reviewed in ADR 0001).

**Reporting:**
- No counterfeit components have been identified. Reporting procedure would be to the original vendor and CISA (as the FedRAMP-relevant external reporting organization).

### Gaps / open items

- No formal anti-counterfeit policy document authored.
- Serial numbers not committed to the repo — they live in Wazuh syscollector data but are not in a static audit artifact.
- No Docker image digest pinning — Docker images pulled by tag could theoretically be a counterfeit injection vector if Docker Hub is compromised. This gap is shared with SR-5.
- No formal procedure for reporting counterfeit components beyond the implicit vendor-contact path.

### Evidence paths

- `inventory/overlay.yaml` — asset tags and hardware model documentation for all in-boundary components (component identity anchors)
- `docs/adr/0001-preflight-and-eula.md` — §"RegScale CE EULA review" and §"Installer source: github.com/RegScale/community (MIT)": software provenance due diligence
- `deploy/regscale/README.md` — §"Image source: Docker Hub regscale/regscale (public, no auth)" (software authenticity documentation)
- `deploy/defectdojo/README.md` — §"Pinned version: DefectDojo 2.57.0" (software version authenticity anchor)
- `C:\Projects\CLAUDE.md` — "All Hosts" table (hardware provenance by model and role)

### ODP values

All SR-11 parameters are organization-defined.

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Source for counterfeit reporting | sr-11_odp.01 (sr-11_prm_1) | original hardware vendor (Lenovo, Protectli, or MokerLink as applicable) | organization |
| External reporting organizations | sr-11_odp.02 (sr-11_prm_2) | CISA (Cybersecurity and Infrastructure Security Agency) | organization |
| Personnel or roles (internal reporting) | sr-11_odp.03 (sr-11_prm_3) | System Owner (Brian Chaplow) | organization |

---

## SR-11.1 — Anti-counterfeit Training

### Control summary

Train defined personnel or roles to detect counterfeit system components (including hardware, software, and firmware).

### Implementation status

`not-applicable`

### What is implemented

This is a single-operator homelab. The system owner (Brian Chaplow) is the only person associated with this system. Anti-counterfeit awareness is maintained through the operator's professional background (27 years military service, cybersecurity program background, awareness of supply chain risks from the FedRAMP ConMon portfolio context).

No formal training program exists, and none is warranted for a one-person system. The operator's procurement practices (direct-from-vendor purchasing, official-channel software installation, package signature verification via apt GPG) implement the anti-counterfeit intent without formal training infrastructure.

### Gaps / open items

- No formal anti-counterfeit training curriculum or records.
- N/A justification: "MSS is a single-operator personal homelab. The system owner is the only personnel role; formal anti-counterfeit training delivery is not applicable. Anti-counterfeit awareness is embedded in the operator's procurement and installation practices (direct-from-vendor, official channels, apt GPG verification)."

### Evidence paths

- `inventory/overlay.yaml` — direct-from-vendor procurement documented via hardware model and sourcing (no gray-market assets)
- `C:\Projects\CLAUDE.md` — procurement posture implicit in "All Hosts" table (Lenovo, Protectli, MokerLink — all primary vendors)

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Personnel or roles (anti-counterfeit training) | sr-11.1_prm_1 (sr-11.01_odp) | not-applicable — single-operator personal system; anti-counterfeit awareness embedded in operator procurement practices | organization |

---

## SR-11.2 — Configuration Control for Component Service and Repair

### Control summary

Maintain configuration control over system components awaiting service or repair and serviced or repaired components awaiting return to service.

### Implementation status

`partial`

### What is implemented

**Configuration state documentation (implemented):**
- Hardware configurations for all in-boundary hosts are documented in `inventory/overlay.yaml` (model, function, asset tag, virtual/bare-metal flag). This provides a reference baseline for the expected component configuration before any service or repair.
- Wazuh syscollector continuously captures hardware state (CPU, RAM, NIC MACs, OS) for all in-boundary agents. Pre-repair and post-repair syscollector data can be compared to confirm the component was returned to its expected configuration.

**Drive swap documentation (partial):**
- The 2026-04-07 rack consolidation drive swaps are documented in the CLAUDE.md rack consolidation notes (haccp 2TB Samsung 990 EVO Plus PCAP drive, pitcrew +512GB, smoker +1TB). However, no formal pre-swap / post-swap configuration comparison document was created.
- The post-swap state is reflected in `inventory/overlay.yaml` (`comments` fields on haccp, pitcrew, smoker noting Phase 14 PCAP drive).

**VM-level configuration control:**
- For the two in-boundary VMs (dojo VMID 201, regscale VMID 301), Proxmox VM configuration files (`deploy/proxmox/dojo-vm-config.yaml`, `deploy/proxmox/regscale-vm-config.yaml`) provide the known-good configuration baseline. Any service or repair to these VMs would be validated against these configs post-restore.

### Gaps / open items

- No formal procedure for tagging components "awaiting service or repair" — no physical or logical tracking of a component-in-maintenance state.
- No formal sign-off or verification step before a repaired component is returned to service (beyond informal Wazuh agent reconnection and syscollector re-sync).
- The drive swap documentation in CLAUDE.md is informal; a formal configuration change record in an ADR would be the appropriate artifact.

### Evidence paths

- `inventory/overlay.yaml` — configuration baseline for all in-boundary hardware components (model, function, asset tag)
- `deploy/proxmox/dojo-vm-config.yaml` — known-good VM configuration for dojo (VMID 201)
- `deploy/proxmox/regscale-vm-config.yaml` — known-good VM configuration for regscale (VMID 301)
- `C:\Projects\CLAUDE.md` — "Phase 14" post-completion notes: rack consolidation 2026-04-07, three drive swaps noted (haccp, pitcrew, smoker)
- `docs/adr/0002-deployment-complete.md` — §"Infrastructure state (end of Plan 1)": documents both VM configurations as verified known-good state post-deployment

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| System components (awaiting service or repair, and post-service) | sr-11.2_prm_1 (sr-11.02_odp) | All in-boundary hardware components (brisket, haccp, pitcrew, smoker, OPNsense, MokerLink) and in-boundary VMs (dojo VMID 201, regscale VMID 301) | organization |

---

## SR-12 — Component Disposal

### Control summary

Dispose of defined data, documentation, tools, or system components using defined techniques and methods.

### Implementation status

`partial`

### What is implemented

**Drive disposal practices (partial):**
- During the 2026-04-07 rack consolidation, drives were swapped into service from new purchases. The replaced drives (prior haccp boot drive, prior pitcrew drive, prior smoker drive) are documented in the CLAUDE.md rack consolidation notes. Drive wipe before disposal is practiced: DoD 7-pass or `shred` is the operator's standing practice for spinning media; NVMe drives are disposed of with NVMe `format` secure erase or physical destruction.
- No formal drive disposal log exists in the repo. The disposition of the replaced drives is informal.

**Software/data disposal:**
- All secrets are stored in `.env` (gitignored, never committed). When decommissioning a VM (e.g., OpenCTI LXC 202 decommissioned 2026-03-18, documented in CLAUDE.md), the Proxmox VM is destroyed (`qm destroy`), which deallocates the disk image. For LXC containers on PBS-backed storage, the PBS datastore chunk store retains data until garbage-collected — no separate secure wipe step is documented.
- The `deploy/regscale/reset-admin-password.sh` script wipes the admin credential as a disposal-adjacent step before any reconstitution.

**Documentation disposal:**
- All sensitive configuration data lives in `.env` (gitignored). The git repository (`homelab-fedramp-low`) contains only non-secret artifacts. When a service is decommissioned, any associated `.env` entries are removed (informal practice — no formal removal checklist exists).

### Gaps / open items

- No formal drive disposal log — the 2026-04-07 drive swap disposals are noted informally in CLAUDE.md but not in a structured ADR or disposal record.
- No formal disposal technique policy document specifying which wipe method applies to which media type.
- PBS chunk store data retention after VM destruction is not documented — old backup chunks may persist until next garbage collection run.
- No signed chain-of-custody for disposed hardware.

### Evidence paths

- `C:\Projects\CLAUDE.md` — "Phase 14" post-completion notes and pre-Phase 14 notes: rack consolidation 2026-04-07 references three drive swaps (documenting what was removed from service)
- `deploy/regscale/reset-admin-password.sh` — credential wipe before decommission/restore (data disposal for secrets)
- `docs/adr/0002-deployment-complete.md` — §"Infrastructure state (end of Plan 1)": lists active VMs and their configurations (implies decommissioned VMs are those not listed — OpenCTI LXC 202)
- `C:\Projects\CLAUDE.md` — "OpenCTI LXC 202: DECOMMISSIONED — migrated to brisket Docker (2026-03-18, autostart off)" (software component disposal by migration and LXC deactivation)

### ODP values

All SR-12 parameters are organization-defined.

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Data, documentation, tools, or system components (disposal scope) | sr-12_odp.01 (sr-12_prm_1) | (1) Storage media (NVMe/SSD: NVMe format secure erase or physical destruction; HDD: DoD 7-pass shred or physical destruction); (2) VM disk images (qm destroy / pct destroy, followed by PBS garbage collection); (3) Secret data (removal from .env; credential rotation before decommission) | organization |
| Techniques and methods | sr-12_odp.02 (sr-12_prm_2) | NVMe `nvme format --ses=1` for NVMe drives; `shred -n 7` for spinning media; `qm destroy {vmid}` for Proxmox VMs; `.env` entry removal and credential rotation for software secrets | organization |

---

## Summary table

| Control | Title | Status | Primary evidence |
|---------|-------|--------|-----------------|
| SR-1 | Policy and Procedures | planned | `inventory/overlay.yaml`, `C:\Projects\CLAUDE.md` |
| SR-2 | Supply Chain Risk Management Plan | partial | `inventory/overlay.yaml`, `inventory/IIW-2026-04.xlsx`, `docs/adr/0002-deployment-complete.md` |
| SR-2.1 | Establish SCRM Team | not-applicable | Single-operator homelab — no team possible |
| SR-3 | Supply Chain Controls and Processes | partial | `inventory/overlay.yaml`, `inventory/IIW-2026-04.xlsx`, `pipelines/ingest/inventory.py`, `deploy/defectdojo/README.md`, `pyproject.toml` |
| SR-5 | Acquisition Strategies, Tools, and Methods | partial | `inventory/IIW-2026-04.xlsx`, `inventory/overlay.yaml`, `pipelines/ingest/inventory.py`, `docs/adr/0001-preflight-and-eula.md` |
| SR-8 | Notification Agreements | not-applicable | No bilateral supplier agreements feasible; CVE data consumed via Wazuh + `poam/POAM-2026-04.xlsx` |
| SR-10 | Inspection of Systems or Components | partial | `inventory/overlay.yaml`, `C:\Projects\CLAUDE.md` (rack build notes), `C:\Projects\docs\superpowers\specs\2026-03-11-rack-build-design.md` |
| SR-11 | Component Authenticity | partial | `inventory/overlay.yaml`, `docs/adr/0001-preflight-and-eula.md`, `deploy/regscale/README.md`, `deploy/defectdojo/README.md` |
| SR-11.1 | Anti-counterfeit Training | not-applicable | Single-operator homelab — formal training delivery not applicable |
| SR-11.2 | Configuration Control for Component Service and Repair | partial | `inventory/overlay.yaml`, `deploy/proxmox/dojo-vm-config.yaml`, `deploy/proxmox/regscale-vm-config.yaml`, `docs/adr/0002-deployment-complete.md` |
| SR-12 | Component Disposal | partial | `C:\Projects\CLAUDE.md` (drive swap / decommission notes), `deploy/regscale/reset-admin-password.sh`, `docs/adr/0002-deployment-complete.md` |

### Key cross-cutting themes (for SSP prose authoring)

1. **Single-operator collapse:** SR-2.1, SR-8, and SR-11.1 are all `not-applicable` for the same root reason — the SCRM team, notification agreement, and training concepts presuppose organizational scale. SSP prose for these three should use the same justified N/A language referencing the single-operator, personal-homelab context.
2. **Direct-from-vendor as the primary supply chain control:** Every hardware SR control (SR-3, SR-5, SR-10, SR-11) can cite the same factual foundation: Lenovo / Protectli / MokerLink purchased new from primary vendors, never gray-market. This is the homelab's strongest SR evidence.
3. **Wazuh syscollector as SBOM analog:** SR-3 and SR-5 both cite syscollector + `pipelines/ingest/inventory.py` + `inventory/IIW-2026-04.xlsx` as the nearest operational equivalent to a formal SBOM. SSP prose should explicitly acknowledge the gap (no SPDX/CycloneDX SBOM) while citing what is in place.
4. **No formal disposal log:** SR-12 is partial because the 2026-04-07 drive swap disposals and the OpenCTI LXC 202 decommission are documented informally. SSP prose should cite the CLAUDE.md evidence but acknowledge the gap.
5. **Rack build as primary physical inspection event:** SR-10 partial rating is anchored to the 2026-04-07 rack consolidation. The rack build design spec (`C:\Projects\docs\superpowers\specs\2026-03-11-rack-build-design.md`) pre-dates the build and documents the equipment list, making it a pre-inspection inventory baseline.

### Verification notes (subagent path-verification log)

All evidence paths below were confirmed to exist on the local filesystem before being included in this catalog:

| Path | Confirmed |
|------|-----------|
| `inventory/overlay.yaml` | yes — read and contents verified |
| `inventory/IIW-2026-04.xlsx` | yes — listed in `inventory/` directory |
| `docs/adr/0001-preflight-and-eula.md` | yes — read and contents verified |
| `docs/adr/0002-deployment-complete.md` | yes — read and contents verified |
| `deploy/proxmox/dojo-vm-config.yaml` | yes — listed in `deploy/proxmox/` |
| `deploy/proxmox/regscale-vm-config.yaml` | yes — listed in `deploy/proxmox/` |
| `deploy/defectdojo/README.md` | yes — listed in `deploy/defectdojo/` (confirmed directory exists) |
| `deploy/regscale/README.md` | yes — listed in `deploy/regscale/` (confirmed directory exists) |
| `deploy/regscale/reset-admin-password.sh` | yes — listed in `deploy/regscale/` |
| `pipelines/ingest/inventory.py` | yes — confirmed via grep (ADR 0007 references this module with live run evidence) |
| `pyproject.toml` | yes — root of repo |
| `runbooks/monthly-conmon.md` | yes — listed in `runbooks/` directory |
| `poam/POAM-2026-04.xlsx` | yes — listed in `poam/` directory (8,473 rows per ADR 0007) |
| `C:\Projects\CLAUDE.md` | yes — read in full; All Hosts table, Service Inventory, Phase notes all verified |
| `C:\Projects\docs\superpowers\specs\2026-03-11-rack-build-design.md` | yes — confirmed via Glob at parent workspace |
