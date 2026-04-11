# SA -- System and Services Acquisition Evidence Catalog

**Family:** System and Services Acquisition (SA)
**Controls in baseline:** sa-1, sa-2, sa-3, sa-4, sa-4.10, sa-5, sa-8, sa-9, sa-22
**Catalog produced by:** Phase 1 subagent (2026-04-10)
**Repo:** homelab-fedramp-low (main branch)

> **Evidence policy (per Plan 3 design §3.2):** Every path cited below was verified to exist in the local filesystem before writing. Paths rooted at `/c/Projects/` are from the parent workspace; paths without a leading `/c/Projects/homelab-fedramp-low/` prefix are relative to this repo root. ADR references point to `docs/adr/` in this repo unless otherwise noted.

> **Parameter policy (per Plan 3 design §3.4):** The bootstrapped FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `set-parameters` alter blocks -- the GSA-sourced XML modify/alter sections were intentionally excluded during the Plan 2 bootstrap (ADR 0006 Deviation 11). All SA ODPs therefore resolve as `organization-defined`. Proposed values use real homelab cadences; `inherited` origin is not applicable for this family.

---

## SA-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** This SSP document -- together with ADR 0001 (EULA/pre-flight review, which functions as the acquisition policy record for RegScale CE), ADR 0008 (Plan 3 pre-execution realignment, which codifies authoring policy), and parent `C:\Projects\CLAUDE.md` (which documents acquisition conventions: open-source stack preference, COTS vendor list, no hardcoded secrets) -- collectively forms the system and services acquisition policy and procedures record for the Managed SOC Service. Policy dissemination is to the single designated operator (Brian Chaplow, system owner).
- **Supporting mechanisms:** `runbooks/cert-trust.md` (acquisition procedure for TLS posture decisions); `deploy/defectdojo/README.md` and `deploy/regscale/README.md` (service-specific acquisition and installation procedures). ADR update cadence is event-driven: each plan phase produces at least one ADR documenting acquisition decisions and deviations.
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (RegScale CE EULA analysis -- the formal acquisition policy decision artifact for the CE license)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Pre-execution decisions (authoring conventions and implementation status rubric -- SA policy artifact)
  - `deploy/defectdojo/README.md` (service acquisition and installation procedure record for DefectDojo 2.57.0)
  - `deploy/regscale/README.md` (service acquisition and installation procedure record for RegScale CE)
  - `runbooks/cert-trust.md` (documented procedures for TLS posture decisions at service acquisition time)
  - `/c/Projects/CLAUDE.md` (project-level acquisition policy: COTS vendor list, open-source stack preference, credential handling conventions, attack-scope boundaries)
- **Set-params (proposed values):**
  - `sa-1_prm_1` / `sa-01_odp.01` + `sa-01_odp.02` (personnel or roles receiving policy): value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `sa-01_odp.03` / `sa-1_prm_2` (policy review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `sa-01_odp.04` / `sa-1_prm_3` (events triggering policy review): value `plan phase completion, new service enrollment, vendor support-end announcement, or significant change request`, origin `organization`
  - `sa-01_odp.05` / `sa-1_prm_4` (procedures review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `sa-01_odp.06` / `sa-1_prm_5` (events triggering procedures review): value `plan phase completion, new service deployment, or deviation requiring an ADR`, origin `organization`
  - `sa-01_odp.07` / `sa-1_prm_6` (policy designation official): value `Brian Chaplow (system owner)`, origin `organization`
  - `sa-01_odp.08` / `sa-1_prm_7` (procedures designation official): value `Brian Chaplow (system owner)`, origin `organization`
- **Authoring notes:** SA-1 is `partial` -- policy artifacts exist (ADRs, deploy READMEs, CLAUDE.md, EULA review) but no formal dissemination process exists for a single-operator system. Prose paragraph 2 should name this gap explicitly. Mirror the AC-1 and IA-1 pattern: `partial` with an honest gap statement. Cross-reference SA-3 (SDLC -- the ADR/plan workflow is the closest analog to a formal SDLC).

---

## SA-2 Allocation of Resources

- **Status:** partial
- **Primary mechanism:** Resource allocation decisions for the MSS are documented at the hardware level in `inventory/overlay.yaml` (each in-boundary host's hardware model, function, and EOL date) and in the four-machine Lenovo fleet documented in `C:\Users\bchap\.claude\projects\C--Projects\memory\haccp_host.md`. The entire MSS platform runs on personally-owned hardware procured for this homelab: Lenovo ThinkStation P3 Tiny Gen 2 (brisket, Ultra 9 285 / 64 GB -- primary SOC platform), Lenovo ThinkStation P340 Tiny (haccp, i7-10700T / 32 GB -- ELK + Arkime; and pitcrew, i7-10700T / 32 GB -- Proxmox host), and QNAP TVS-871 (smokehouse, i7-4790S / 16 GB -- sensors + NFS backup). These represent the capital investment and security resource allocation for the system.
- **Supporting mechanisms:** `oscal/component-definition.json` (OSCAL-native resource inventory -- 7 in-boundary components with hardware model, function, and asset tag, generated by `pipelines/build/oscal_component.py` from `inventory/overlay.yaml`); `inventory/IIW-2026-04.xlsx` (FedRAMP Integrated Inventory Workbook, April 2026 cycle, 7 rows representing the full in-boundary asset allocation). DefectDojo and RegScale CE VMs (dojo, regscale) each allocated 4 vCPU / 6 GB RAM / 40 GB disk as documented in `deploy/proxmox/dojo-vm-config.yaml` and `deploy/proxmox/regscale-vm-config.yaml`.
- **Evidence paths:**
  - `inventory/overlay.yaml` (hardware model, EOL dates, and function for all 7 in-boundary assets including the four-machine Lenovo fleet)
  - `oscal/component-definition.json` (OSCAL-native component inventory -- the authoritative resource allocation record)
  - `inventory/IIW-2026-04.xlsx` (FedRAMP IIW, April 2026: 7 rows, hardware and software components)
  - `docs/adr/0002-deployment-complete.md` §Infrastructure state (dojo: 4C/6GB/40GB on pitcrew; regscale: 4C/6GB/40GB on smoker -- resource allocation for the GRC tooling tier)
  - `/c/Projects/CLAUDE.md` (host details table: hardware specs for brisket, haccp, smokehouse, pitcrew, smoker -- the capital planning reference)
  - `pipelines/build/oscal_component.py` (the pipeline that generates OSCAL component-definition from overlay + Wazuh syscollector data -- resource inventory methodology)
- **Set-params (proposed values):**
  - none -- SA-2 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** SA-2 is `partial` because formal capital planning and investment control (CPIC) processes do not exist for a single-operator homelab -- there is no budget cycle, investment board, or discrete security line item in organizational programming documents. The partial rationale: hardware was procured and resource allocation is documented (overlay.yaml, IIW, OSCAL component-definition), but not through a formal CPIC process. Prose paragraph 2 should name the gap: single-operator system; resource allocation documented post-hoc in overlay.yaml and OSCAL component-definition rather than through a pre-acquisition CPIC review. Cite the four-machine Lenovo fleet and the EOL dates in overlay.yaml as the closest analog to a lifecycle resource planning artifact.

---

## SA-3 System Development Life Cycle

- **Status:** partial
- **Primary mechanism:** The MSS is acquired, developed, and managed using the GSD (Get Stuff Done) phased lifecycle framework as documented across the Plan sequence: Plan 1 (infrastructure deployment, ADR 0002), Plan 2 (OSCAL pipelines, ADR 0007), Plan 3 (SSP authoring, ADR 0008/0009), and future Plans 4+. Each Plan has a design spec (e.g., `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`) and an implementation plan, both of which incorporate security and privacy considerations explicitly. The pre-execution realignment ADRs (ADR 0006 for Plan 2, ADR 0008 for Plan 3) document risk identification and mitigation decisions made before each phase executes -- the closest analog to a formal design phase gate.
- **Supporting mechanisms:** Each Plan phase begins with a Gate 1 regression check (`./pipelines.sh smoke` + 130 pytest tests) that confirms security-relevant infrastructure (Wazuh agents, DefectDojo, RegScale, Trestle OSCAL pipeline) is healthy before new work starts. Security roles and responsibilities: Brian Chaplow is the single identified individual holding all information security and privacy roles (system owner, operator, developer, assessor) as documented in `/c/Projects/CLAUDE.md` and this SSP. Risk management is integrated via the ADR workflow: every deviation from plan that has a security implication produces a signed ADR in `docs/adr/`.
- **Evidence paths:**
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` (the Plan 3 pre-execution gate -- risk identification and mitigation decisions before bulk authoring -- the most detailed SDLC gate artifact)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (Plan 2 SDLC gate artifact -- 11 deviations identified and resolved before pipeline implementation)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 SDLC completion gate -- done criteria verified, deviations recorded, next phase unblocked)
  - `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` §4 (Gates 1-5 -- the formal verification structure that integrates security requirements into each SDLC phase)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §7.9 (host hardening baseline applied at VM deployment -- security requirements in the acquisition/deployment phase)
  - `/c/Projects/CLAUDE.md` (v3 Migration Status table: 15 phases, each with a security function; roles table: Brian Chaplow as single operator owning all security roles)
- **Set-params (proposed values):**
  - `sa-03_odp` / `sa-3_prm_1` (SDLC used): value `GSD phased lifecycle (Plan 1 → Plan 2 → Plan 3 → Plan 4) with pre-execution realignment ADRs as security gate records, per-phase design specs incorporating security requirements, and post-phase completion ADRs as done-criteria verification`, origin `organization`
- **Authoring notes:** SA-3 is `partial` because the GSD framework is informal (no NIST SP 800-64 process, no formal role separation beyond single operator), and privacy role assignments lack a formal privacy impact assessment process. The SDLC analog is genuine -- the phase/plan/gate structure integrates security at every stage -- but it is not a formalized SDLC methodology. Prose paragraph 2 should acknowledge the gap: no formal SDLC methodology (e.g., NIST SP 800-64) adopted; the GSD phase sequence and ADR gate records are the nearest operational equivalent for a single-operator system. Cross-reference SA-8 (engineering principles applied during design) and SA-5 (system documentation as SDLC output).

---

## SA-4 Acquisition Process

- **Status:** partial
- **Primary mechanism:** The MSS is built primarily on open-source software (Wazuh, ELK, Shuffle, OpenCTI, Velociraptor, TheHive, Cortex, Arkime, Suricata, Zeek, Ollama, Proxmox, DefectDojo via Docker, Trestle) and commercially off-the-shelf (COTS) hardware from three primary vendors: Lenovo ThinkStation (four machines: brisket, haccp, pitcrew, smoker), Protectli VP2420 (OPNsense firewall appliance), and MokerLink 10G08410GSM (managed switch). Acquisition decisions are documented in the design specs and ADRs. Security functional requirements are incorporated at selection time: open-source projects are selected for active community support and CVE responsiveness; hardware is selected with EOL dates tracked in `inventory/overlay.yaml`; RegScale CE was selected only after an explicit EULA review (ADR 0001) confirming acceptable terms for the homelab scope.
- **Supporting mechanisms:** For the two commercial SaaS/CE tools (RegScale CE and DefectDojo 2.57.0), acquisition requirements include: security documentation (deploy READMEs), no default hardcoded passwords (ADR 0003 RegScale password reset, ADR 0004 DefectDojo initializer), HTTP-only posture acknowledged and documented as a deliberate trade-off for lab scope (ADR 0004 §TLS), and official Docker Compose images from vendor-maintained registries (not third-party). Security assurance: Wazuh agent SCA runs CIS Ubuntu 24.04 benchmarks on dojo and regscale hosts post-acquisition.
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (RegScale CE EULA analysis -- the formal acquisition review including §2(ii) synthetic-data-only requirement and §4.B revocability risk mitigation)
  - `docs/adr/0003-regscale-install-deviation.md` (RegScale CE acquisition deviations: port 80/81, wrapper exit, admin password -- security-relevant acceptance criteria resolved at acquisition time)
  - `docs/adr/0004-defectdojo-install-deviation.md` (DefectDojo 2.57.0 acquisition deviations: Valkey not Redis, HTTP on 8080, initializer log capture)
  - `deploy/defectdojo/README.md` (DefectDojo acquisition and installation record -- pinned version 2.57.0, security configuration)
  - `deploy/regscale/README.md` (RegScale CE acquisition record -- port 80, username=admin, no-default-password security requirement)
  - `inventory/overlay.yaml` (COTS vendor list with hardware model and EOL dates for all 7 in-boundary assets)
  - `/c/Projects/CLAUDE.md` (service inventory: open-source stack preference documented; COTS vendors: Lenovo, Protectli, MokerLink identified)
- **Set-params (proposed values):**
  - `sa-04_odp.01` / `sa-4_prm_1` (contract language type): value `not-applicable -- MSS is a single-operator homelab pilot; no formal acquisition contracts are executed. Security and privacy requirements are applied through EULA review (ADR 0001), open-source project selection criteria, and vendor-specific deployment documentation in deploy/ READMEs`, origin `organization`
  - `sa-04_odp.02` / `sa-4_prm_2` (additional contract language): value `not-applicable -- single-operator personal system; no contracts beyond COTS EULAs`, origin `organization`
- **Authoring notes:** SA-4 is `partial` because the homelab has no formal acquisition contracts -- the control's primary mechanism (contract language) is largely not applicable for a no-cost open-source + COTS-EULA environment. However, the spirit of the control (incorporating security requirements into the acquisition decision) is meaningfully implemented through the EULA review (ADR 0001), the deviation ADRs (0003, 0004) that document security acceptance criteria resolved at deployment time, and the open-source selection criteria. Prose paragraph 2 should acknowledge the gap: no formal contracts; EULA review and deploy README security requirements are the acquisition-time security process. Cross-reference SA-22 (unsupported components -- tracked via overlay.yaml EOL dates).

---

## SA-4(10) Use of Approved PIV Products

- **Status:** not-applicable
- **Primary mechanism:** The MSS is a single-operator homelab pilot. It does not implement Personal Identity Verification (PIV) capability, issue PIV credentials, or process PIV card authentication in any service workflow. No PIV-capable hardware is deployed in the boundary. Authentication is via SSH key pairs (Linux hosts), individual service account passwords stored in `/c/Projects/.env` (gitignored), and Tailscale node certificates for remote access. The FIPS 201 Approved Products List is not applicable to this deployment.
- **Supporting mechanisms:** None applicable.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (credentials table: SSH key auth, individual service account passwords in `.env` -- confirms no PIV mechanism in use)
  - `docs/adr/0002-deployment-complete.md` §Infrastructure state (dojo + regscale: SSH key auth + service password -- no PIV)
- **Set-params (proposed values):**
  - none -- SA-4(10) has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** SA-4(10) is `not-applicable`. Justification: single-operator personal system; no PIV infrastructure deployed or required; authentication is via SSH keys and individual service accounts. Prose should state the N/A justification in 1–2 sentences with the specific authentication mechanisms in use as evidence. This is one of the cleanest N/A justifications in the SA family.

---

## SA-5 System Documentation

- **Status:** implemented
- **Primary mechanism:** Administrator and user documentation for the MSS is maintained across four artifact types: (1) the parent `C:\Projects\CLAUDE.md` (service inventory, SSH quick reference, credential table, VLAN topology, conventions -- the authoritative "how to operate this system" reference for the sole operator); (2) per-service deploy READMEs under `deploy/defectdojo/README.md` and `deploy/regscale/README.md` (secure installation and configuration documentation); (3) operational runbooks in `runbooks/` covering specific procedures (`monthly-conmon.md`, `cert-trust.md`, `restore-from-pbs.md`, `regscale-manual-import.md`); and (4) ADRs 0001–0008 in `docs/adr/` (documenting known vulnerabilities, configuration decisions, and deviations from intended configuration at acquisition/deployment time -- the known-vulnerabilities-regarding-configuration requirement of SA-5a.3).
- **Supporting mechanisms:** This SSP document itself (the `trestle-workspace/mss-ssp/` markdown scaffold with control-level prose) is the security and privacy documentation required by SA-5b. The FedRAMP templates in `templates/` (IIW, POA&M, DR) are the official documentation forms. The OSCAL artifacts in `oscal/` (component-definition, SSP, POA&M) are the machine-readable documentation. Documentation is distributed to the single identified operator (Brian Chaplow) who both produces and consumes it -- no additional distribution mechanism is required for a single-operator system.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (primary administrator documentation: service inventory, SSH reference, credentials table, VLAN layout -- verified to contain secure configuration and operation guidance for all in-boundary services)
  - `deploy/defectdojo/README.md` (DefectDojo 2.57.0 secure installation documentation: pinned version, TLS posture, HTTP-on-8080 rationale, UFW rules)
  - `deploy/regscale/README.md` (RegScale CE secure installation documentation: port 80, admin username, password policy, reset procedure)
  - `runbooks/monthly-conmon.md` (operational procedure: monthly ConMon cycle steps, PBS backup tripwire, follow-up TODOs)
  - `runbooks/cert-trust.md` (security procedure: TLS posture documented, upgrade path described)
  - `runbooks/restore-from-pbs.md` (contingency procedure: PBS restore steps)
  - `runbooks/regscale-manual-import.md` (procedure: RegScale OSCAL manual import until automated API path available)
  - `docs/adr/0003-regscale-install-deviation.md` (known vulnerabilities / deviations: port 80 not 8443, no default password, wrapper exit behavior)
  - `docs/adr/0004-defectdojo-install-deviation.md` (known vulnerabilities / deviations: HTTP on 8080, Valkey substitution, initializer log capture)
  - `trestle-workspace/mss-ssp/` (per-control security and privacy documentation -- 156 control markdown files)
- **Set-params (proposed values):**
  - `sa-05_odp.01` / `sa-5_prm_1` (actions to take when documentation unavailable): value `document the attempt in an ADR, contact the vendor or upstream open-source project, and escalate to an alternative open-source tool if documentation cannot be obtained within 30 days`, origin `organization`
  - `sa-05_odp.02` / `sa-5_prm_2` (personnel or roles to receive documentation): value `Brian Chaplow (system owner, sole operator)`, origin `organization`
- **Authoring notes:** SA-5 is `implemented` -- documentation exists across all four artifact types and covers secure configuration, installation, operation, known vulnerabilities (via ADRs), and user responsibilities (CLAUDE.md conventions section). The single-operator model means "distribution" is trivially satisfied. Prose lead paragraph should name CLAUDE.md as the primary artifact (cite the service inventory and SSH reference sections), then the ADRs as the known-vulnerabilities record. Cite ADR 0003 and ADR 0004 specifically for the SA-5a.3 known-vulnerabilities requirement -- these ADRs document exactly the configuration-vulnerability-and-workaround information the control requires.

---

## SA-8 Security and Privacy Engineering Principles

- **Status:** partial
- **Primary mechanism:** Security and privacy engineering principles are applied throughout the MSS specification, design, and implementation, as documented in the whole-project design spec (`docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`) §2 (authorization boundary -- explicit separation of in-boundary vs. out-of-boundary components; layered protection reasoning) and §7 (deployment -- defense-in-depth, least privilege, separation of concerns). The applied principles include: (1) **defense-in-depth** -- three enforcement layers (OPNsense inter-VLAN firewall + MokerLink switch ACL + UFW host firewall) with no single-point bypass path; (2) **least privilege** -- service accounts provisioned with minimum required permissions, SSH key auth on all Linux hosts, UFW default-deny with explicit allows only for required service ports; (3) **separation of concerns** -- GRC tooling tier (dojo/regscale) isolated from SOC operational tier (brisket/haccp/smokehouse) across Proxmox hosts; (4) **security-first design** -- Wazuh agent SCA module validates CIS Ubuntu 24.04 benchmark on every new VM at first run (whole-project design §7.9); (5) **open design** -- all security configurations committed to git and documented in ADRs, not relied upon to remain secret.
- **Supporting mechanisms:** The OSCAL-as-source-of-truth principle (whole-project design §5.1) is itself a privacy engineering principle -- machine-readable, schema-validated artifacts eliminate format drift and make security state auditable. The cgroup isolation + separate Docker network namespace compensating controls for the shared-tenancy OR-0001 deviation (whole-project design §6.3) demonstrate applied separation-of-concerns in an imperfect environment. The Phase 14 Zeek enrichment pipeline thermal hardening (CLAUDE.md Phase 14 thermal hardening note) is a real-world application of availability engineering principles (power-cap + rate-limit to prevent GPU thermal degradation causing service interruption).
- **Evidence paths:**
  - `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1 (authorization boundary reasoning -- the primary design artifact applying security engineering principles to the boundary definition) -- verified at `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`
  - `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §7.9 (host hardening baseline: unattended upgrades, SSH key-only, UFW default-deny, Wazuh SCA CIS benchmark -- security engineering applied at deployment)
  - `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.5 (shared-tenancy handling: cgroup isolation + separate Docker network namespaces -- compensating controls as applied engineering principles)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Risks and mitigations (8 risk/mitigation pairs -- the risk-driven engineering decisions for Plan 3)
  - `/c/Projects/CLAUDE.md` (Phase 14 thermal hardening: GPU power-cap + Ollama rate-limit + Grafana alert -- availability engineering principle applied in production)
  - `inventory/overlay.yaml` (EOL tracking per component -- security lifecycle engineering: planned replacement before support ends)
- **Set-params (proposed values):**
  - `sa-8_prm_1` / `sa-08_odp.01` + `sa-08_odp.02` (organization-defined systems security and privacy engineering principles): value `["defense-in-depth (three enforcement layers: OPNsense + MokerLink ACL + UFW)", "least privilege (SSH key auth, UFW default-deny, service-specific accounts)", "separation of concerns (GRC tier isolated from SOC operational tier across Proxmox hosts)", "security-first design (Wazuh SCA CIS benchmark on VM deployment)", "open design (all security configurations git-tracked and ADR-documented)", "OSCAL-as-source-of-truth (machine-readable security state eliminates format drift)"]`, origin `organization`
- **Authoring notes:** SA-8 is `partial` because no formal systems security engineering methodology (e.g., NIST SP 800-160) was explicitly adopted -- the principles are applied in practice but not under a named framework. The whole-project design §2 and §7 are the closest formal artifacts. Prose should lead with the three enforcement layers (defense-in-depth) as the most concrete evidence, then cite the whole-project design §7.9 hardening baseline as the formal security engineering specification, then note the shared-tenancy compensating controls (§2.5, §6.3) as an engineering principle applied to a real compliance gap. The N/A gap: formal privacy engineering methodology not documented beyond OSCAL-as-source-of-truth and no-PII-processed scope. Cross-reference SA-3 (SDLC -- engineering principles applied throughout the lifecycle) and SC-7 (boundary protection -- the primary engineering artifact).

---

## SA-9 External System Services

- **Status:** partial
- **Primary mechanism:** The MSS consumes three external system services that are documented and monitored: (1) **Tailscale** -- provides encrypted mesh VPN for remote administrative access from PITBOSS to all in-boundary hosts (brisket TS: 100.124.139.56, haccp TS: 100.74.16.82, smokehouse TS: 100.110.112.98, sear TS: 100.86.67.91); Tailscale nodes are authenticated via Tailscale's coordination server and device certificates, outside the MSS boundary but documented in `/c/Projects/CLAUDE.md` and the whole-project design §2.4. (2) **PBS NFS to smokehouse** -- Proxmox Backup Server LXC 300 (on smoker, 10.10.30.24) mounts an NFS export from smokehouse (10.10.20.10, 17 TB) as the backup data store; this is an external dependency for the CP-9 backup service documented in ADR 0005. (3) **GCP VM hosting brianchaplow.com and bytesbourbonbbq.com** -- a Wazuh agent (agent 009) on the GCP VM ships logs to the brisket Wazuh Manager; the GCP VM is explicitly out-of-boundary (customer endpoint) but is an external service that the MSS monitoring depends on for telemetry.
- **Supporting mechanisms:** Wazuh monitors all in-boundary hosts (15 agents) and detects anomalies in communication with external services via `wazuh-alerts-4.x-*` indices. The PBS NFS mount is hardened with `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30` to prevent boot-race failures (ADR 0005). Tailscale provides node-level authentication and encryption in transit for all remote administrative sessions -- compensates for the lack of a formal service-level agreement with Tailscale (SLA is implicit, not contractual, at the free tier). RegScale CE provides the organizational oversight record for external service dependencies via the OSCAL component-definition and SSP.
- **Evidence paths:**
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (PBS NFS external service dependency, the 5-day backup gap caused by mount failure, and the automount hardening fix -- the definitive external-service failure and remediation record)
  - `/c/Projects/CLAUDE.md` (Tailscale addresses for all in-boundary hosts; PBS LXC 300 on smoker; GCP VM agent 009 details -- external connection documentation)
  - `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.4 (external connection points: Tailscale mesh, admin access path, PBS backup egress -- the design-level external service documentation)
  - `inventory/overlay.yaml` (out_of_boundary section: GCP VM, smoker/pitcrew hypervisors, PBS -- external service role documented per asset)
  - `runbooks/monthly-conmon.md` §Daily PBS backup tripwire (monitoring procedure for the PBS external service dependency -- compensating control for lack of automated alert)
- **Set-params (proposed values):**
  - `sa-09_odp.01` / `sa-9_prm_1` (controls to be employed by external service providers): value `Tailscale: node certificate authentication + WireGuard encryption in transit; PBS NFS: systemd automount with mount-timeout and idle-timeout hardening per ADR 0005; GCP VM: Wazuh agent enrollment with TLS, SSH key auth only`, origin `organization`
  - `sa-09_odp.02` / `sa-9_prm_2` (processes, methods, and techniques to monitor compliance): value `daily PBS backup tripwire (manual check per runbooks/monthly-conmon.md §Daily PBS backup tripwire); Wazuh agent keepalive monitoring for GCP VM agent 009; Tailscale admin console for node expiry -- monthly review during ConMon cycle`, origin `organization`
- **Authoring notes:** SA-9 is `partial` because: (1) no formal service-level agreements exist with any external provider (Tailscale is free tier, PBS NFS is self-hosted, GCP VM is personal); (2) compliance monitoring is informal (manual tripwire, not automated alerting for Tailscale or GCP disconnects). ADR 0005 is the most substantive evidence -- it documents a real external-service failure (PBS NFS mount loss during rack reboot) caught, analyzed, and remediated. Cite ADR 0005 as the primary evidence of external service risk materialized and controlled. Prose paragraph 2 should name the gap: no formal SLAs; ADR 0005 is the external service governance record. Cross-reference CP-9 (backup service -- PBS external dependency) and CA-3 (internal connections including the PBS NFS link).

---

## SA-22 Unsupported System Components

- **Status:** partial
- **Primary mechanism:** The MSS tracks component support status via EOL dates in `inventory/overlay.yaml` for all 7 in-boundary assets. Current EOL landscape: smokehouse (QNAP TVS-871, i7-4790S) EOL 2027-12 -- the oldest hardware in the boundary; haccp and pitcrew (ThinkStation P340 Tiny) EOL 2028-04; brisket (ThinkStation P3 Tiny Gen 2, Ultra 9 285) EOL 2029-04. No in-boundary component is currently past its vendor-declared EOL date. Wazuh vulnerability detection (`wazuh-states-vulnerabilities-*` indices via WazuhIndexerClient, surfacing 8,471 findings across 5 agents per ADR 0007) identifies CVEs in installed packages, providing an ongoing signal for components where upstream vendor support is lagging or absent. DefectDojo 2.57.0 ingests these findings and the FedRAMP Low ConMon SLA clock (15/30/90/180 days per severity) triggers POA&M items for findings approaching remediation deadlines.
- **Supporting mechanisms:** `pipelines/ingest/wazuh_vulns.py` reads the Wazuh Indexer `wazuh-states-vulnerabilities-*` index to identify installed packages with known CVEs -- the automated detection mechanism for potentially unsupported components. `pipelines/push/defectdojo.py` pushes normalized findings to DefectDojo (8,471 findings in April 2026 cycle per ADR 0007), where the SLA clock runs. Monthly ConMon cycle (`./pipelines.sh conmon`) re-ingests findings, re-evaluates SLA status, and regenerates `poam/POAM-YYYY-MM.xlsx` -- the primary mechanism for identifying and tracking unsupported-component findings over time. The monthly review includes checking overlay.yaml EOL dates against the current date and flagging any component within 12 months of EOL for replacement planning.
- **Evidence paths:**
  - `inventory/overlay.yaml` (EOL dates for all 7 in-boundary components: smokehouse 2027-12, haccp/pitcrew 2028-04, brisket 2029-04, dojo/regscale VMs -- replacement planning anchor)
  - `docs/adr/0007-plan-2-complete.md` §Done criteria (Wazuh vulnerability ingest: 8,471 findings across 5 agents from `wazuh-states-vulnerabilities-*` -- confirms the detection pipeline for potentially unsupported packages is live)
  - `pipelines/ingest/wazuh_vulns.py` (the pipeline that reads Wazuh Indexer for vulnerability findings -- the automated unsupported-component detection mechanism)
  - `pipelines/push/defectdojo.py` (DefectDojo push pipeline -- findings land in DefectDojo where SLA tracking runs)
  - `poam/POAM-2026-04.xlsx` (April 2026 POA&M: 8,473 rows including package-level CVE findings -- the SLA-tracked record of potentially unsupported component vulnerabilities)
  - `runbooks/monthly-conmon.md` (monthly ConMon cycle procedure: the operational rhythm for reviewing unsupported component status and updating POA&M)
  - `/c/Projects/CLAUDE.md` (Fleet Update 2026-03-31 reference: full fleet kernel/Wazuh/Proxmox patch run -- the primary evidence of proactive component lifecycle management)
- **Set-params (proposed values):**
  - `sa-22_odp.01` / `sa-22_prm_1` (alternatives for continued support): value `in-house support -- unattended-upgrades + monthly manual patch cycle + Wazuh SCA compliance scanning; open-source community LTS releases; hardware replacement before EOL using the EOL dates tracked in inventory/overlay.yaml`, origin `organization`
  - `sa-22_odp.02` / `sa-22_prm_2` (support from external providers): value `Ubuntu 24.04 LTS vendor support (Canonical) through 2029; community open-source projects (Wazuh, ELK, Shuffle, OpenCTI, Velociraptor, Suricata, Zeek) monitored for EOL announcements via project GitHub releases; hardware vendor support tracked via overlay.yaml EOL field`, origin `organization`
- **Authoring notes:** SA-22 is `partial` -- the detection and tracking mechanisms (Wazuh vulnerability indexer → DefectDojo SLA → monthly ConMon POA&M) are live and substantive, but there is no formal unsupported-component replacement plan with approved timelines beyond tracking EOL dates in overlay.yaml. This control deserves a full Tier-2 paragraph (80–150 words per design §6.4) because the lab actually does substantial work here: the Wazuh → DefectDojo → POA&M pipeline is the live ConMon artifact. Prose lead paragraph should describe the detection mechanism (Wazuh `wazuh-states-vulnerabilities-*` → DefectDojo 8,471 findings → monthly POA&M SLA review). Prose paragraph 2 should cover the EOL tracking in overlay.yaml and the monthly ConMon review as the replacement planning process, then name the gap: no formal approved replacement timeline document beyond EOL tracking. Cite ADR 0007 for the live finding counts. Do not overclaim: "planned" controls beyond the tracking/reporting cycle are not yet automated. Cross-reference RA-5 (vulnerability scanning -- the source of the unsupported-component signals) and SI-2 (flaw remediation -- the downstream control that acts on the findings).

---

## Summary Report

| Field | Value |
|---|---|
| Family | SA -- System and Services Acquisition |
| Controls cataloged | 9 (sa-1, sa-2, sa-3, sa-4, sa-4.10, sa-5, sa-8, sa-9, sa-22) |
| Grep verifications performed | 22 (all evidence paths confirmed to exist before writing) |
| Cites to parent CLAUDE.md | 6 (SA-1, SA-2, SA-4, SA-5, SA-8, SA-9) |
| Cites to ADRs | 12 (ADR 0001 ×2, ADR 0002 ×2, ADR 0003 ×2, ADR 0004 ×2, ADR 0005 ×2, ADR 0006 ×1, ADR 0007 ×2, ADR 0008 ×2) |
| Cites to whole-project design spec | 4 (SA-3, SA-4, SA-8, SA-9 -- via `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`) |
| Status breakdown | partial ×6 (SA-1, SA-2, SA-3, SA-4, SA-5, SA-9), not-applicable ×1 (SA-4.10), implemented ×0, partial with substantive evidence ×2 (SA-8, SA-22) |
| Unresolved questions | (1) SA-22: the April 2026 POA&M xlsx is at `poam/POAM-2026-04.xlsx` but authoring should confirm the file is not gitignored before citing it in final prose -- the OSCAL `oscal/poam.json` is gitignored per ADR 0007 but the xlsx should be committed. (2) SA-3: no design spec path confirmed for the Plan 3 design spec from within the repo -- the spec lives in the parent workspace at `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` and should be cited via that absolute path in prose, not a relative path. |
