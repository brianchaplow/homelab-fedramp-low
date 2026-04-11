# CM -- Configuration Management Evidence Catalog

**Family:** CM -- Configuration Management
**FedRAMP Rev 5 Low controls in scope (from `trestle-workspace/profiles/fedramp-rev5-low/profile.json`):**
cm-1, cm-2, cm-4, cm-5, cm-6, cm-7, cm-8, cm-10, cm-11 (9 controls; cm-3 and cm-9 are not in the Low baseline)

**Verified:** 2026-04-09 -- all evidence paths below were grepped or `ls`-verified before citation.
**References:** CLAUDE.md §v3 Migration Status, ADR 0002, ADR 0005, ADR 0007, ADR 0008.

---

## CM-1 Policy and Procedures

### Status

partial

### Primary mechanism

No standalone CM policy document exists yet. The homelab SOC uses its git repository and ADR discipline as the procedural backbone for configuration management: every configuration-significant change produces a commit (traceable, datable, attributed) and every architecturally significant change produces an ADR. CLAUDE.md serves as the living system reference that describes scope, roles (owner: Brian Chaplow), and update cadence. The Plan 3 SSP authoring phase (ADR 0008 §Pre-execution decisions) constitutes the first attempt to formalize CM procedures into OSCAL-anchored prose.

### Supporting mechanisms

- ADR series (0001 through 0008) provides a running policy-equivalent record of CM decisions, deviations, and approvals.
- `runbooks/monthly-conmon.md` describes the monthly review cadence (CM-1c trigger: "following significant events or at least annually" -- operationalized as the monthly ConMon cycle).
- `pipelines.sh conmon` orchestrates the monthly cycle in a repeatable, documented form (ADR 0007 §done criteria).

### Evidence paths

- `/c/Projects/CLAUDE.md` -- system reference, owner, update cadence (verified present)
- `/c/Projects/homelab-fedramp-low/docs/adr/` -- ADRs 0001–0008 (verified: `ls` returns 8 files)
- `/c/Projects/homelab-fedramp-low/runbooks/monthly-conmon.md` -- monthly ConMon procedure stub (verified present)
- `/c/Projects/homelab-fedramp-low/pipelines.sh` -- `conmon` subcommand (verified: file present in repo root)
- `/c/Projects/homelab-fedramp-low/docs/plan-3/SHAPE-CHECK-LOG.md` -- Gate 2 shape-check log establishing Plan 3 authoring as the policy documentation activity (verified present)

### Set-params

- **cm-01_odp.01 / cm-01_odp.02** (personnel or roles): `organization` origin -- value: `system owner (Brian Chaplow)`
- **cm-01_odp.03** (review frequency of policy): `organization` origin -- value: `annually or following a significant change event`
- **cm-01_odp.04** (events triggering policy review): `organization` origin -- value: `a new ConMon phase, a security incident, a significant infrastructure change, or an ADR that invalidates existing policy`
- **cm-01_odp.05** (review frequency of procedures): `organization` origin -- value: `annually or following a significant change event`
- **cm-01_odp.06** (events triggering procedures review): `organization` origin -- same as cm-01_odp.04
- **cm-01_odp.07** (official designated to manage policy): `organization` origin -- value: `system owner (Brian Chaplow)`
- **cm-01_odp.08** (designation official for procedures): same as cm-01_odp.07

### Authoring notes

The primary gap driving `partial` status is the absence of a dedicated CM policy document (distinct from the CLAUDE.md system reference and ADR practice). Plan 3 SSP prose for CM-1 should document: (1) git-commit-as-change-record as the operational CM procedure; (2) ADR-as-significant-change-record as the formal approval mechanism; (3) the CLAUDE.md as the dissemination artifact; and (4) the monthly ConMon cycle as the review frequency. A future enhancement would extract a standalone CM-policy.md and reference it in the SSP. Set-param `<REPLACE_ME>` values above are all organization-defined; no FedRAMP-mandated values exist for CM-1.

---

## CM-2 Baseline Configuration

### Status

implemented

### Primary mechanism

The system baseline is maintained as git-tracked configuration across four repositories that together capture every deployed component: `homelab-soc-portfolio/` (every SOC config checked in, including Wazuh `ossec.conf` and Prometheus targets), `HomeLab-SOC-v2/` (legacy configs retained for delta analysis), `brisket-setup/monitoring/` (v3 platform install and monitoring configs including `prometheus.yml`, Grafana dashboard builders, and `docker-compose.yml`), and `reference/phase14/zeek/` (Phase 14 Zeek baseline including `local.zeek`, `networks.cfg`, `node.cfg`, `zeek.service`, and `community-id-propagate.zeek`). Every configuration change is a git commit; architecturally significant changes also produce ADRs. The baseline is reviewed on the monthly ConMon cycle and whenever a new phase adds infrastructure, a host is reimaged, or an ADR records a configuration-drift incident. Set-params cm-02_odp.01 and cm-02_odp.02 are already filled in the scaffold (see `trestle-workspace/mss-ssp/cm/cm-2.md`) and represent the live, signed-off values.

### Supporting mechanisms

- PBS (Proxmox Backup Server on smoker LXC 300): daily snapshots to smokehouse 17 TB NFS provide a VM-image-level configuration recovery backstop.
- Wazuh syscollector: captures the installed package set and hardware inventory for each enrolled agent at enrollment and on a polling cadence, providing a secondary baseline audit trail queryable from the Wazuh Dashboard (brisket:5601).
- `inventory/overlay.yaml` + `pipelines/ingest/inventory.py`: converts Wazuh syscollector output + static overlay into `InventoryComponent` records used by the OSCAL component-definition builder -- making the baseline machine-readable.
- ADR 0005 (PBS backup gap and automount fix): canonical evidence of drift detection → root-cause analysis → remediation → baseline update (fstab hardened with `x-systemd.automount`). This is the complete CM-2 lifecycle in a single documented incident.

### Evidence paths

- `/c/Projects/homelab-soc-portfolio/wazuh/configs/ossec.conf` -- Wazuh manager baseline config (verified: `ls` path confirmed)
- `/c/Projects/homelab-soc-portfolio/infrastructure/configs/` -- infrastructure baseline configs (verified: directory present)
- `/c/Projects/brisket-setup/monitoring/prometheus.yml` -- Prometheus scrape targets (verified: file present)
- `/c/Projects/brisket-setup/monitoring/docker-compose.yml` -- brisket Docker stack definition (verified: file present)
- `/c/Projects/reference/phase14/zeek/local.zeek` -- Zeek local policy baseline (verified: file present via glob)
- `/c/Projects/reference/phase14/zeek/networks.cfg` -- Zeek network ranges (verified: present in same directory)
- `/c/Projects/reference/phase14/zeek/node.cfg` -- Zeek node configuration (verified: present)
- `/c/Projects/reference/phase14/zeek/zeek.service` -- Zeek systemd service unit (verified: present)
- `/c/Projects/reference/phase14/zeek/community-id-propagate.zeek` -- Community-ID propagation script (verified: glob confirmed)
- `/c/Projects/HomeLab-SOC-v2/configs/` -- legacy SOC configuration delta baseline (verified: directory present with docker-compose, fluent-bit, opensearch, suricata subdirs)
- `/c/Projects/homelab-fedramp-low/inventory/overlay.yaml` -- static overlay for IIW + OSCAL component-definition (verified: file read)
- `/c/Projects/homelab-fedramp-low/pipelines/ingest/inventory.py` -- inventory ingestion from Wazuh syscollector (verified: file read)
- `/c/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` -- drift detection lifecycle evidence (verified: file read)
- `/c/Projects/homelab-fedramp-low/docs/adr/0002-deployment-complete.md` -- baseline establishment evidence for Plan 1 deployment (verified: file read)
- `/c/Projects/homelab-fedramp-low/trestle-workspace/mss-ssp/cm/cm-2.md` -- already-authored control prose with set-params filled (verified: file read, Implementation Status: implemented)

### Set-params

- **cm-02_odp.01** (review frequency): `organization` origin -- value: `monthly` (already filled in scaffold)
- **cm-02_odp.02** (circumstances triggering review): `organization` origin -- value: `when a new phase adds infrastructure, after a rack or cable change, after a host reimage, or when an ADR records a configuration-drift incident` (already filled in scaffold)

### Authoring notes

CM-2 is the shape-check target for Gate 2 (ADR 0008 §Gate 2) and its prose was authored in Task 2 (`trestle-workspace/mss-ssp/cm/cm-2.md`, Implementation Status: implemented, `ssp-assemble` PASS verified in `docs/plan-3/SHAPE-CHECK-LOG.md`). The catalog entry here is the reference for any future re-authoring. The set-param values in the scaffold are live, signed-off values -- not `<REPLACE_ME>`. No FedRAMP-mandated parameter values constrain CM-2; both ODPs are organization-defined. The PBS automount incident (ADR 0005) is the strongest CM-2 evidence artifact because it demonstrates the full drift-detect-remediate-update-baseline cycle with timestamps and commands.

---

## CM-4 Impact Analyses

### Status

partial

### Primary mechanism

Security and privacy impact analysis for system changes is performed ad hoc by the system owner through the ADR process. Every architecturally significant change that affects the security posture -- VLAN topology, service port configuration, agent enrollment, backup topology, Phase 14 data pipeline additions -- produces an ADR that explicitly states the security consequences (Consequences section). The ADR is written before the change is committed to the baseline, providing the pre-implementation record that CM-4 requires. Examples: ADR 0003 (RegScale HTTP-on-80 deviation), ADR 0004 (DefectDojo HTTP-on-8080 deviation), ADR 0005 (PBS backup gap -- discovered the security risk of silent backup failure and remediated it).

### Supporting mechanisms

- Wazuh SCA (Security Configuration Assessment): automated scan on enrolled agents checking OS-level hardening configuration. Provides a security-impact data point for any package or config change on in-boundary hosts.
- `brisket-setup/monitoring/build-infrastructure-fleet.py` and related Grafana dashboard builders: surface configuration drift signals (disk, memory, service health) that can trigger manual impact review.
- The `pipelines.sh conmon` cycle generates a monthly POA&M from Wazuh vulnerability data (Plan 2, ADR 0007), which surfaces vulnerability-level risk that feeds impact analysis decisions.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/docs/adr/0003-regscale-install-deviation.md` -- impact analysis for RegScale HTTP vs HTTPS deviation (verified: file listed in `ls /docs/adr/`)
- `/c/Projects/homelab-fedramp-low/docs/adr/0004-defectdojo-install-deviation.md` -- impact analysis for DefectDojo HTTP deviation (verified: file listed)
- `/c/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` -- impact analysis and consequences for backup gap (verified: file read)
- `/c/Projects/homelab-fedramp-low/docs/adr/0008-plan-3-pre-execution-realignment.md` -- pre-execution risk table for Plan 3 changes (verified: file read, §Risks section)
- `/c/Projects/brisket-setup/monitoring/build-infrastructure-fleet.py` -- Grafana fleet dashboard (verified: file present in brisket-setup/monitoring/)
- `/c/Projects/homelab-fedramp-low/poam/POAM-2026-04.xlsx` -- April 2026 POA&M with 8,473 vulnerability findings providing risk context for impact decisions (verified: directory present in project root)

### Set-params

None -- CM-4 has no ODPs in the FedRAMP Rev 5 Low scaffold (no `x-trestle-set-params` block in `trestle-workspace/mss-ssp/cm/cm-4.md`).

### Authoring notes

The primary gap is formalization: impact analysis happens through the ADR process but is not codified as a formal procedure with defined criteria. The SSP prose for CM-4 should describe the ADR-as-impact-analysis mechanism and reference the Consequences/Negative sections of ADRs as the documented impact record. `partial` status reflects that the mechanism exists but is not formally defined as a security-impact-analysis procedure. A future control enhancement would add a pre-change checklist to the ADR template.

---

## CM-5 Access Restrictions for Change

### Status

partial

### Primary mechanism

Logical access restrictions for system changes are enforced by SSH key-only authentication to all in-boundary hosts: brisket (primary SOC platform), haccp (ELK + Arkime), and the Proxmox hypervisors (pitcrew, smoker). No password-based SSH is permitted on production hosts (enforced via `/etc/ssh/sshd_config` with `PasswordAuthentication no`). All configuration changes flow through git commits on PITBOSS (operator workstation, 10.10.10.100), and the git repository on GitHub acts as the access-controlled change approval record -- only the repository owner (Brian Chaplow, GitHub: brianchaplow) can push to `main`. Physical access restrictions are enforced by the 12U rack with lock and the VLAN microsegmentation on MokerLink that prevents lateral movement from VLAN 40 (targets) to VLAN 20/30 (SOC infrastructure).

### Supporting mechanisms

- MokerLink L3 ACL enforces VLAN-level access restrictions: VLAN 40 (targets) is isolated and cannot initiate connections to VLAN 20 (SOC) or VLAN 30 (lab). Only the change-authorized operator (PITBOSS on VLAN 10) can reach all segments.
- OPNsense firewall (10.10.10.1): enforces perimeter access control preventing external entities from making configuration changes to in-boundary services.
- UFW `default-deny` on dojo (10.10.30.27) and regscale (10.10.30.28): only VLAN-scoped SSH and service ports are permitted; all other change paths are blocked at the host firewall (ADR 0002 §Infrastructure state).
- Wazuh RBAC: The Wazuh Dashboard (brisket:5601) uses role-based access -- unauthorized users cannot push SIEM rules, SCA checks, or agent configuration.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/deploy/proxmox/dojo-vm-config.yaml` -- VM configuration with firewall: false (UFW-controlled, not Proxmox firewall) and explicit VLAN placement (verified: file read)
- `/c/Projects/homelab-fedramp-low/deploy/proxmox/regscale-vm-config.yaml` -- same pattern for regscale (verified: file present)
- `/c/Projects/homelab-fedramp-low/docs/adr/0002-deployment-complete.md` -- §Infrastructure state documenting UFW default-deny on dojo and regscale (verified: file read)
- `/c/Projects/CLAUDE.md` -- §SSH Quick Reference showing key-based SSH as the only authenticated access path (verified: content read from system-reminder)
- `/c/Projects/CLAUDE.md` -- §VLANs documenting VLAN 40 isolation and MokerLink ACL enforcement (verified: content read)

### Set-params

None -- CM-5 has no ODPs in the FedRAMP Rev 5 Low scaffold (no `x-trestle-set-params` block in `trestle-workspace/mss-ssp/cm/cm-5.md`).

### Authoring notes

`partial` status because physical access restrictions are informal (home lab rack; no documented key-custody or visitor log) and logical access restrictions, while real, are not documented in a formal access-restriction procedure. The SSP prose for CM-5 should describe: (1) SSH key-only authentication as the primary logical access control; (2) GitHub-as-change-approval-record as the logical change authorization mechanism; (3) VLAN microsegmentation and OPNsense as the boundary access controls; (4) UFW default-deny as the host-level enforcement. The home lab's single-operator model simplifies the physical control gap but must be acknowledged.

---

## CM-6 Configuration Settings

### Status

partial

### Primary mechanism

Configuration settings for in-boundary components reflect the most restrictive mode consistent with SOC operational requirements through a combination of: (1) UFW default-deny with explicit service allows on dojo and regscale (ADR 0002); (2) OS-level hardening via Ubuntu 24.04 defaults and `unattended-upgrades` active on all VMs (ADR 0002 §Infrastructure state); (3) Docker `default-deny` network model with explicit port publications only (brisket-setup/monitoring/docker-compose.yml); (4) Wazuh SCA checks running on all enrolled agents validating OS hardening settings against the CIS benchmark subset. Deviations from secure-by-default settings are documented in ADRs with explicit operational justification -- for example, DefectDojo HTTP-on-8080 instead of HTTPS (ADR 0004) and RegScale HTTP-on-80 (ADR 0003) are documented deviations with rationale.

### Supporting mechanisms

- `brisket-setup/monitoring/prometheus.yml`: explicit scrape targets only -- no wildcard discovery (verified: file present, pattern confirmed).
- `reference/phase14/zeek/local.zeek`: Zeek loaded-scripts baseline pinned and git-tracked -- only explicitly loaded packages active.
- Wazuh SCA policies: generate findings for any enrolled agent that deviates from baseline OS hardening settings; these surface in the Wazuh Dashboard and feed the POA&M.
- `pipelines/ingest/wazuh_vulns.py` + `pipelines/build/oscal_poam.py`: translates SCA and vulnerability findings into OSCAL POA&M items for formal tracking of configuration deviations.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/deploy/defectdojo/README.md` -- documents HTTP-on-8080 deviation with operational justification (verified: file present)
- `/c/Projects/homelab-fedramp-low/docs/adr/0004-defectdojo-install-deviation.md` -- approved deviation from secure-default for DefectDojo (verified: file listed)
- `/c/Projects/homelab-fedramp-low/docs/adr/0003-regscale-install-deviation.md` -- approved deviation from secure-default for RegScale (verified: file listed)
- `/c/Projects/brisket-setup/monitoring/docker-compose.yml` -- Docker configuration with explicit port publications (verified: file present)
- `/c/Projects/reference/phase14/zeek/local.zeek` -- Zeek configuration settings baseline (verified: present)
- `/c/Projects/homelab-fedramp-low/deploy/proxmox/dojo-vm-config.yaml` -- VM configuration settings (verified: file read)
- `/c/Projects/homelab-fedramp-low/poam/POAM-2026-04.xlsx` -- April 2026 POA&M representing open configuration findings (verified: poam/ directory confirmed)
- `/c/Projects/homelab-fedramp-low/pipelines/ingest/wazuh_vulns.py` -- vulnerability/SCA data ingestion pipeline (verified: file present)

### Set-params

- **cm-06_odp.01** (common secure configurations): `organization` origin -- value: `Ubuntu 24.04 LTS vendor defaults with unattended-upgrades, UFW default-deny, SSH PasswordAuthentication disabled, Docker least-privilege port publication`
- **cm-06_odp.02** (system components with approved deviations): `organization` origin -- value: `DefectDojo 2.57.0 on dojo (HTTP-on-8080 per ADR 0004); RegScale CE on regscale (HTTP-on-80 per ADR 0003)`
- **cm-06_odp.03** (operational requirements justifying deviations): `organization` origin -- value: `no publicly trusted TLS certificate available for LAN-only services; reverse-proxy upgrade path documented in runbooks/cert-trust.md for future Plan 4`

### Authoring notes

`partial` status because: (1) no formal CIS Benchmark profile or STIG has been explicitly adopted and mapped to the system -- the configuration settings reflect reasonable operational hardening but not a named standard; (2) the monitoring of configuration settings is informal (Wazuh SCA + manual ADR review) rather than automated continuous enforcement. The SC-8 (transmission confidentiality) gap from HTTP-only services is acknowledged in the ADRs and deferred to Plan 4. The SSP prose for CM-6 should explicitly name the "common secure configurations" used and reference the deviation ADRs as the documented-and-approved deviation record.

---

## CM-7 Least Functionality

### Status

partial

### Primary mechanism

The system is configured to provide only mission-essential capabilities. Each in-boundary host runs only the services required for its SOC role: brisket runs Wazuh Manager, Wazuh Indexer, Wazuh Dashboard, Prometheus, Grafana, Shuffle SOAR, Velociraptor, ML Scorer, Ollama, and OpenCTI -- no unrelated services. haccp runs ELK, Arkime, and Logstash -- no unrelated services. dojo runs DefectDojo on Docker with Valkey -- no unrelated services. regscale runs RegScale CE on Docker with MSSQL -- no unrelated services. OPNsense firewall enforces perimeter restrictions. MokerLink ACL enforces VLAN-level restrictions prohibiting traffic flows not required by SOC operations (VLAN 40 targets isolated). UFW default-deny on GRC VMs ensures only explicitly opened ports are reachable.

### Supporting mechanisms

- Docker-based service isolation: each service runs in its own container namespace with no host network exposure beyond explicitly published ports.
- `brisket-setup/monitoring/prometheus.yml` + `brisket-setup/monitoring/blackbox.yml`: monitoring targets define the explicit service inventory -- any service not in these files is not in the SOC operational baseline.
- CLAUDE.md §Service Inventory: canonical list of all services and ports per host (SOC operational baseline definition).
- Wazuh SCA: checks for unnecessary running services and open ports on enrolled agents.
- Phase 14 Zeek baseline (`reference/phase14/zeek/local.zeek`): only explicitly loaded Zeek packages active -- no default Zeek plugins beyond what is pinned in the baseline.

### Evidence paths

- `/c/Projects/CLAUDE.md` -- §Service Inventory (brisket, haccp, smoker tables) defining the mission-essential service list per host (verified: present in system-reminder)
- `/c/Projects/brisket-setup/monitoring/prometheus.yml` -- scrape targets = explicit service inventory (verified: file present)
- `/c/Projects/brisket-setup/monitoring/blackbox.yml` -- blackbox probe targets for service availability (verified: file present)
- `/c/Projects/brisket-setup/monitoring/docker-compose.yml` -- container service definitions with explicit port bindings (verified: file present)
- `/c/Projects/homelab-fedramp-low/deploy/defectdojo/README.md` -- documents which DefectDojo containers are running (verified: file present)
- `/c/Projects/homelab-fedramp-low/deploy/regscale/README.md` -- documents which RegScale CE containers are running (verified: `ls` confirmed)
- `/c/Projects/reference/phase14/zeek/local.zeek` -- Zeek loaded-scripts baseline (verified: present)

### Set-params

- **cm-07_odp.01** (mission-essential capabilities): `organization` origin -- value: `SOC monitoring (Wazuh SIEM, Zeek, Suricata, Arkime PCAP, ELK analytics), SOAR automation (Shuffle), DFIR (Velociraptor), threat intelligence (OpenCTI), GRC/ConMon (DefectDojo, RegScale), ML-based scoring (ml-scorer), LLM enrichment (Ollama)`
- **cm-07_odp.02 through cm-07_odp.06** (prohibited functions, ports, protocols, software, services): `organization` origin -- value: `all functions/ports/protocols not listed in CLAUDE.md §Service Inventory; VLAN 40 target traffic to VLAN 20/30 (MokerLink ACL); peer-to-peer file sharing protocols; remote desktop protocols on SOC infrastructure hosts; Telnet and unencrypted FTP to/from SOC hosts`

### Authoring notes

`partial` status because: (1) no formal prohibited-ports/protocols list has been drafted and committed as a configuration document; (2) Wazuh SCA checks for unnecessary services exist but have not been reviewed to produce a clean bill of health against a formal least-functionality checklist. The SSP prose for CM-7 should reference CLAUDE.md §Service Inventory as the mission-essential capabilities definition and the MokerLink ACL + OPNsense firewall rules as the prohibition enforcement mechanism. The GCP VM (external Wazuh agent 009) hosts brianchaplow.com and bytesbourbonbbq.com -- these are out-of-boundary and do not affect the MSS CM-7 scope.

---

## CM-8 System Component Inventory

### Status

implemented

### Primary mechanism

The system component inventory is maintained through three complementary mechanisms: (1) `inventory/overlay.yaml` -- the authoritative static inventory overlay keyed by Wazuh agent name, documenting asset tag, function, diagram label, boundary classification, hardware model, and EOL date for all 7 in-boundary Wazuh-managed hosts plus 2 non-agent assets (OPNsense, MokerLink); (2) `inventory/IIW-2026-04.xlsx` -- the April 2026 Integrated Inventory Workbook generated by `pipelines/ingest/inventory.py` + `pipelines/render/iiw.py` from live Wazuh syscollector data merged with the overlay, producing 7 IIW rows with OS, CPU, RAM, IP, and MAC fields (ADR 0007 §done criteria Task 9); (3) Wazuh syscollector -- continuously captures hardware, OS, and network interface data for all 15 enrolled agents (13 SOC-boundary + OPNsense syslog + brisket host) and indexes them in `wazuh-*` indices on brisket:9200. The IIW is regenerated monthly via `./pipelines.sh conmon`.

### Supporting mechanisms

- `pipelines/build/oscal_component.py`: emits every `InventoryComponent` as an OSCAL component with UUID, name, type, and all overlay props -- machine-readable inventory in `oscal/component-definition.json` (16 KB, 7 components, ADR 0007 §artifact inventory).
- `oscal/component-definition.json`: OSCAL-formatted component inventory validated via `trestle.oscal.component.oscal_read` (ADR 0007).
- `deploy/proxmox/dojo-vm-config.yaml` and `deploy/proxmox/regscale-vm-config.yaml`: VM-level inventory records including VMID, memory, cores, disk size, MAC, VLAN, IP.
- CLAUDE.md §All Hosts: the human-readable inventory that is the source of truth for the overlay.yaml.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/inventory/overlay.yaml` -- authoritative inventory overlay (verified: file read, 7 in-boundary agents + 2 non-agent assets)
- `/c/Projects/homelab-fedramp-low/inventory/IIW-2026-04.xlsx` -- April 2026 IIW (verified: file present, 178 KB, 7 rows per ADR 0007)
- `/c/Projects/homelab-fedramp-low/pipelines/ingest/inventory.py` -- live inventory ingestion from Wazuh (verified: file read)
- `/c/Projects/homelab-fedramp-low/pipelines/build/oscal_component.py` -- OSCAL component-definition builder (verified: file present)
- `/c/Projects/homelab-fedramp-low/oscal/component-definition.json` -- OSCAL component-definition (verified: file present in oscal/)
- `/c/Projects/homelab-fedramp-low/deploy/proxmox/dojo-vm-config.yaml` -- VM inventory record: dojo (verified: file read)
- `/c/Projects/homelab-fedramp-low/deploy/proxmox/regscale-vm-config.yaml` -- VM inventory record: regscale (verified: file present)
- `/c/Projects/CLAUDE.md` -- §All Hosts table: human-readable inventory source (verified: content read)
- `/c/Projects/homelab-fedramp-low/docs/adr/0007-plan-2-complete.md` -- §artifact inventory and §done criteria verifying the IIW pipeline output (verified: file read)

### Set-params

- **cm-08_odp.01** (information required in component inventory): `organization` origin -- value: `asset tag, hostname, IP address, MAC address, OS name and version, kernel version, CPU model, RAM (MB), hardware model, boundary classification, function/role, diagram label, virtualization flag, end-of-life date, Wazuh agent ID`
- **cm-08_odp.02** (inventory review frequency): `organization` origin -- value: `monthly (generated automatically by ./pipelines.sh conmon)`

### Authoring notes

CM-8 is well-supported by the pipeline infrastructure. The `implemented` status reflects that the inventory is generated from live Wazuh data, maintained in an OSCAL-validated component-definition, and the IIW is regenerated monthly by the ConMon pipeline. The main gap is that the 15 enrolled Wazuh agents include out-of-boundary assets (DC01, WS01, GCP VM, sear) -- the IIW correctly excludes these via the `boundary: in` filter in the overlay. The SSP prose should be explicit that the IIW and OSCAL component-definition cover only the 7 in-boundary MSS components; the 8 out-of-boundary assets are listed in `overlay.yaml` under `out_of_boundary` for auditor transparency. No FedRAMP-mandated values constrain CM-8 ODPs.

---

## CM-10 Software Usage Restrictions

### Status

partial

### Primary mechanism

The homelab SOC uses only open-source software under documented licenses: Wazuh (GPL v2), OpenSearch (Apache 2.0), ELK (Elastic License 2.0 with SSPL restrictions on server software acknowledged), Shuffle (GPL), Velociraptor (AGPL), Arkime (Apache 2.0), Zeek (BSD), Suricata (GPL), OpenCTI (Apache 2.0 / EE tier not used), TheHive (AGPL), Cortex (AGPL), DefectDojo (BSD 3-Clause), RegScale CE (proprietary, CE license accepted during deployment per ADR 0001 EULA analysis). The Elastic ML trial license (activated 2026-03-17, 30-day) was a time-limited evaluation feature -- its expiration does not break core ELK functionality. No quantity-licensed commercial software requiring seat tracking is deployed. No peer-to-peer file sharing technology is present on in-boundary hosts.

### Supporting mechanisms

- ADR 0001 (preflight and EULA): documents the RegScale CE EULA analysis -- the only proprietary software in the deployment that required explicit license acceptance before deployment.
- CLAUDE.md §Service Inventory: canonical list of all deployed software by host. The Elastic ML trial license status is recorded in the CLAUDE.md version history.
- `deploy/defectdojo/README.md` and `deploy/regscale/README.md`: document the software versions and licensing context.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` -- EULA analysis for RegScale CE (verified: file listed in `ls /docs/adr/`)
- `/c/Projects/homelab-fedramp-low/deploy/defectdojo/README.md` -- DefectDojo 2.57.0 BSD 3-Clause context (verified: file present)
- `/c/Projects/homelab-fedramp-low/deploy/regscale/README.md` -- RegScale CE licensing context (verified: file present in deploy/regscale/)
- `/c/Projects/CLAUDE.md` -- §Service Inventory: full software list per host (verified: present in system-reminder)

### Set-params

None -- CM-10 has no ODPs in the FedRAMP Rev 5 Low scaffold (no `x-trestle-set-params` block in `trestle-workspace/mss-ssp/cm/cm-10.md`).

### Authoring notes

`partial` status because: (1) no formal software usage policy document has been drafted; (2) the Elastic License 2.0 (EL2) covers the server-side ELK components and has SSPL-adjacent restrictions on offering ELK as a managed service to others -- this is a potential legal nuance in the MSS analogy that the SSP prose should acknowledge or explicitly bound (homelab is not a commercial managed service offering); (3) the Elastic ML trial license expiration is not formally tracked. The SSP prose for CM-10 should list all software licenses, confirm no quantity-licensed software is deployed, and explicitly state that no P2P file sharing is present. The EULA analysis in ADR 0001 is the strongest CM-10 evidence artifact.

---

## CM-11 User-Installed Software

### Status

partial

### Primary mechanism

The system is a single-operator homelab SOC with no general-purpose user accounts on in-boundary hosts beyond the operator (Brian Chaplow). Software installation is restricted to the operator via SSH key-only authentication (no shared accounts, no guest access). The Ubuntu 24.04 VMs (dojo, regscale) use `unattended-upgrades` for security patches only -- no user-initiated package installation outside operator SSH sessions. Docker is the primary software deployment mechanism; no containers are deployed outside the documented `docker-compose.yml` baselines. The git repository and ADR process function as the informal policy governing software installation -- any new service must be documented in CLAUDE.md §Service Inventory and committed to a configuration file before it is considered part of the approved baseline.

### Supporting mechanisms

- UFW default-deny: prevents inbound lateral software installation attempts on dojo and regscale.
- Wazuh syscollector: captures the installed package set on all enrolled agents, providing change detection if unauthorized packages appear.
- `pipelines/ingest/inventory.py`: monthly inventory ingestion from Wazuh syscollector creates an audit trail of package state changes across ConMon cycles.
- Wazuh SCA: checks for unauthorized software installations against OS-level hardening policies.

### Evidence paths

- `/c/Projects/homelab-fedramp-low/docs/adr/0002-deployment-complete.md` -- §Infrastructure state documenting unattended-upgrades active on all VMs (verified: file read)
- `/c/Projects/homelab-fedramp-low/pipelines/ingest/inventory.py` -- monthly package/syscollector snapshot (verified: file read)
- `/c/Projects/homelab-fedramp-low/inventory/overlay.yaml` -- overlay documents approved software function per host (verified: file read)
- `/c/Projects/CLAUDE.md` -- §SSH Quick Reference: operator-only SSH key access to all hosts (verified: present in system-reminder)

### Set-params

- **cm-11_odp.01** (policies governing user-installed software): `organization` origin -- value: `operator-authored policy: all software installations must be documented in CLAUDE.md §Service Inventory and committed to the homelab-fedramp-low or homelab-soc-portfolio git repository before the service is considered part of the approved baseline; Docker is the required deployment mechanism for new services on brisket and GRC VMs`
- **cm-11_odp.02** (methods for enforcing software installation policies): `organization` origin -- value: `SSH key-only authentication to all in-boundary hosts; UFW default-deny on GRC VMs; Docker namespace isolation; Wazuh syscollector package-change detection`
- **cm-11_odp.03** (monitoring frequency for policy compliance): `organization` origin -- value: `monthly (via Wazuh syscollector → inventory ingestion pipeline in ./pipelines.sh conmon)`

### Authoring notes

`partial` status because: (1) the software installation policy is informal (CLAUDE.md convention, not a standalone policy document); (2) no automated enforcement mechanism blocks an operator from installing packages via SSH -- it relies on operator discipline; (3) the Wazuh syscollector-based monitoring detects changes but does not block them. The single-operator model significantly reduces the risk (there is no "user" population to govern beyond the operator themselves), which the SSP prose should acknowledge. The SSP prose for CM-11 should describe the ADR + git-commit convention as the operative policy, Docker as the enforcement mechanism for new service deployments, and Wazuh syscollector as the compliance monitoring tool.

---

## Cross-cutting notes

1. **No cm-3 (Configuration Change Control) or cm-9 (Configuration Management Plan)** in the FedRAMP Rev 5 Low baseline (confirmed: profile.json `with-ids` list contains only cm-1, cm-2, cm-4, cm-5, cm-6, cm-7, cm-8, cm-10, cm-11).

2. **ADR-as-change-control**: The absence of cm-3 in the Low baseline is fortunate for the homelab because the ADR process effectively implements the substance of cm-3 (change request, review, approval, documentation, post-implementation review). When authoring other families, reference the ADR process as the change control mechanism for controls that implicitly assume it.

3. **Git commit attribution**: Every change to in-boundary configuration files carries a git commit hash, author (Brian Chaplow / tubachap), and timestamp. This provides the attribution trail that cm-4 (impact analysis pre-authorization) and cm-5 (access restrictions) require as evidence.

4. **ConMon pipeline as CM machinery**: The `./pipelines.sh conmon` command (ADR 0007) generates IIW, POA&M, and OSCAL artifacts from live Wazuh state monthly. This is the operational heartbeat that makes CM-2 (baseline review), CM-8 (inventory update), and CM-11 (software monitoring) implementable as `implemented` or `partial` rather than `planned`.

5. **Elastic ML trial license expiration**: The 30-day ML trial activated 2026-03-17 expired approximately 2026-04-16. After expiration, Elastic ML features become read-only. This is a CM-10 relevant software licensing event that the monthly ConMon should track -- if the operator decides to pay for a license, that is a baseline change requiring an ADR.
