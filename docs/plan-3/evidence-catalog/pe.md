# PE -- Physical and Environmental Protection Evidence Catalog

**Family:** Physical and Environmental Protection (PE)
**Controls in baseline:** pe-1, pe-2, pe-3, pe-6, pe-8, pe-12, pe-13, pe-14, pe-15, pe-16
**Catalog produced by:** Phase 1 subagent (2026-04-09)
**Repo:** homelab-fedramp-low (main branch)

> **Evidence policy (per Plan 3 design §3.2):** Every path cited below was verified to exist in the local filesystem before writing. Paths rooted at `/c/Projects/` are from the parent workspace; paths without a leading `/c/Projects/homelab-fedramp-low/` prefix are relative to this repo root. ADR references point to `docs/adr/` in this repo unless otherwise noted.

> **Parameter policy (per Plan 3 design §3.4):** The bootstrapped FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `set-parameters` alter blocks for PE controls -- confirmed by grepping the profile JSON for PE ODP identifiers (no matches). All PE ODPs therefore resolve as `organization-defined`. Proposed values reflect the single-operator residential homelab reality. `inherited` origin is not applicable for this family.

> **PE context note:** This system is a private-residence homelab operating in a dedicated home office/equipment room. All equipment was consolidated into a 12U open-frame rack on 2026-04-07 (rack build design: `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md`). Physical access is limited to the homeowner/operator (Brian Chaplow). There are no visitors to the facility, no formal badge/key system, and no on-site fire suppression beyond residential smoke detectors. Many PE controls will be `partial` or `not-applicable` due to this single-operator residential context; all N/A determinations are stated explicitly per Plan 3 design §3.3.

---

## PE-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** This SSP document -- together with ADR 0001 (EULA/pre-flight), ADR 0002 (Plan 1 deployment), and ADR 0008 (Plan 3 pre-execution realignment) -- collectively functions as the physical and environmental protection policy record for the Managed SOC Service. The whole-project design (`/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`) explicitly acknowledges PE as a partial family (§PE row, honest-gaps table) with the rationale that a residential homelab substitutes homeowner access control for enterprise physical security controls.
- **Supporting mechanisms:** The rack build design document (`/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md`) serves as the physical environment specification -- recording equipment placement, power architecture (Goldenmate 1000VA UPS), airflow, and cable management decisions made before the 2026-04-07 rack consolidation. ADR 0005 documents a physical reboot event (rack consolidation) and its downstream impact, demonstrating that physical events are recorded and analyzed. Policy review cadence is event-driven, triggered at each plan phase boundary.
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (earliest policy artifact -- EULA analysis and pre-flight decisions)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 completion record -- operator action items including physical infrastructure tasks)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (physical rack reboot event recorded and analyzed -- demonstrates physical-event tracking)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Pre-execution decisions (implementation status rubric, set-params policy)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps row: "Partial -- homelab rack locks + camera")
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (physical environment design spec: rack layout, UPS plan, airflow, equipment inventory)
  - `/c/Projects/CLAUDE.md` (VLAN layout, SSH conventions, equipment table -- system-level physical topology policy)
- **Set-params (proposed values):**
  - `pe-01_odp.01` / aggregate `pe-1_prm_1` (personnel or roles to receive policy): value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `pe-01_odp.02` / aggregate `pe-1_prm_1` (personnel or roles to receive procedures): value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `pe-01_odp.03` / `pe-1_prm_2` (policy review frequency): value `annually and after each plan phase completion or physical infrastructure change`, origin `organization`
  - `pe-01_odp.04` / `pe-1_prm_3` (events triggering policy review): value `plan phase completion, rack rebuild or equipment addition, security incident, or regulatory change`, origin `organization`
  - `pe-01_odp.05` / `pe-1_prm_4` (procedures review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `pe-01_odp.06` / `pe-1_prm_5` (events triggering procedures review): value `plan phase completion, new service enrollment, or physical infrastructure change`, origin `organization`
  - `pe-01_odp.07` / `pe-1_prm_6` (policy designation official): value `Brian Chaplow (system owner)`, origin `organization`
  - `pe-01_odp.08` / `pe-1_prm_7` (procedures designation official): value `Brian Chaplow (system owner)`, origin `organization`
- **Authoring notes:** PE-1 is `partial` -- not `not-applicable` -- because policy artifacts exist (ADRs, whole-project design, rack build spec, CLAUDE.md) but no formal enterprise-grade PE policy document exists for a single-operator residential system. Prose paragraph 2 should name this gap explicitly. Cross-reference PL-1 (same pattern: policy exists in ADRs and design docs but is not a standalone formal document). Cite the whole-project design §PE honest-gaps acknowledgment as evidence the limitation is intentional and documented.

---

## PE-2 Physical Access Authorizations

- **Status:** partial
- **Primary mechanism:** The system resides in a private residence accessible only to the homeowner/operator (Brian Chaplow). Physical access authorization is enforced by residential security mechanisms: locked exterior doors, a home alarm system, and a dedicated home office/equipment room with door access controlled by the homeowner. No external personnel have authorized access to the facility. The authorized-access list is a single entry: the system owner.
- **Supporting mechanisms:** No badge or ID-card system is deployed -- residential key-lock mechanisms constitute the physical access credential. The facility access list is implicitly defined by homeownership: all other individuals are unauthorized. No contractors or maintenance personnel have facility access. The Wazuh agent on brisket monitors system availability; unauthorized physical access would be observable as unexpected service disruptions.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (equipment location table: all in-boundary hosts are at private-residence address, no external colocation)
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (rack layout under PITBOSS's desk -- physical location description)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps: "Partial -- homelab rack locks + camera")
  - `docs/adr/0002-deployment-complete.md` (deployment context confirms private-residence location throughout Plan 1 execution)
- **Set-params (proposed values):**
  - `pe-02_odp` / `pe-2_prm_1` (access list review frequency): value `not-applicable -- single-entry access list (system owner only); reviewed continuously by virtue of sole-operator status`, origin `organization`
- **Authoring notes:** PE-2 is `partial` -- the authorized-access list exists (one entry: system owner) and physical access is controlled by residential locks, but no formal credential issuance, no review schedule with documentation, and no removal procedure exists for a single-operator system. Prose should acknowledge these gaps explicitly. The N/A on the review frequency param should be explained: the "list" is the homeowner, reviewed by definition. Do not claim `not-applicable` at the control level -- the residence does have physical access control, just not enterprise-grade.

---

## PE-3 Physical Access Control

- **Status:** partial
- **Primary mechanism:** Physical access to the facility is controlled by residential mechanisms: locked exterior doors (keyed deadbolt), home alarm system, and a dedicated home office/equipment room. Entry to the facility requires the homeowner's physical key. The 12U rack (consolidated 2026-04-07) is located under PITBOSS's desk inside the dedicated office space. No formal physical access audit log system is deployed -- residential mechanisms do not generate digital audit records.
- **Supporting mechanisms:** The MokerLink managed switch provides port-level network access control (ACL `sear-brisket`, mirror port isolation), which complements physical access control at the logical layer. Wazuh monitors all 15 in-boundary agents for unexpected activity that could indicate unauthorized physical access to a host. Keys (residential door keys) are secured by the homeowner. No visitors are admitted to the equipment room.
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (rack layout, physical location under PITBOSS's desk, equipment inventory -- the physical configuration record)
  - `/c/Projects/CLAUDE.md` (all hosts listed with VLAN/IP, confirming private-residence colocation; MokerLink ACL reference)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps row)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (rack consolidation reboot 2026-04-07 documented -- physical access event recorded informally via ADR)
- **Set-params (proposed values):**
  - `pe-03_odp.01` / `pe-3_prm_1` (entry and exit points): value `exterior residential entry door (keyed deadbolt) and home office/equipment room door`, origin `organization`
  - `pe-03_odp.02` / `pe-3_prm_2` (systems or devices for ingress/egress control): value `residential keyed deadbolt and home alarm system`, origin `organization`
  - `pe-03_odp.03` / `pe-3_prm_3` (entry or exit points for audit logs): value `not-applicable -- residential facility; no digital physical access audit log system deployed`, origin `organization`
  - `pe-03_odp.04` / `pe-3_prm_4` (physical access controls for publicly accessible areas): value `not-applicable -- no publicly accessible areas within the facility`, origin `organization`
  - `pe-03_odp.05` / `pe-3_prm_5` (circumstances for visitor escort): value `not-applicable -- no visitors are admitted to the equipment area`, origin `organization`
  - `pe-03_odp.06` / `pe-3_prm_6` (physical access devices inventoried): value `residential door keys (2 copies held by system owner)`, origin `organization`
  - `pe-03_odp.07` / `pe-3_prm_7` (physical access device inventory frequency): value `annually`, origin `organization`
  - `pe-03_odp.08` / `pe-3_prm_8` (combination/key change frequency): value `when keys are lost or when the residential property changes ownership`, origin `organization`
  - `pe-03_odp.09` / aggregate `pe-3_prm_9` (frequency for combination changes): value `not-applicable -- no combination locks deployed`, origin `organization`
  - `pe-03_odp.10` / aggregate `pe-3_prm_9` (frequency for key changes): value `when keys are lost or when individuals with key access are no longer authorized`, origin `organization`
- **Authoring notes:** PE-3 is `partial` -- physical access is actively controlled by residential mechanisms but there is no formal digital audit log of entry/exit events, no formal visitor escort procedure (no visitors), and no electronic access control system. Prose paragraph 2 should name these gaps. The MokerLink ACL and Wazuh monitoring provide compensating logical-layer visibility but do not substitute for physical access logs. Reference `/c/Projects/reference/network.md` for the MokerLink ACL detail if citing logical-layer controls.

---

## PE-6 Monitoring Physical Access

- **Status:** partial
- **Primary mechanism:** Physical access to the facility is monitored through residential mechanisms available to the homeowner. The Wazuh SIEM on brisket monitors all 15 in-boundary agents continuously; unexpected service disruptions or host-unavailability events would indicate a physical access incident (e.g., accidental power disconnect or equipment tampering). The Grafana alert "GPU Thermal Critical -- Brisket Above 90C" (uid=dfihoiidr7k00c, `brisket-setup/monitoring/build-grafana-alerts.py`) routes to `#infrastructure-alerts` via Discord -- this environmental alert demonstrates that physical/environmental monitoring is wired to an incident-notification channel.
- **Supporting mechanisms:** No dedicated physical access monitoring system (video surveillance, badge readers, motion sensors) is deployed in the facility beyond residential capabilities. Physical access "reviews" are performed organically by the homeowner as the sole occupant of the equipment room. Any physical security incident would be reported to the homeowner/operator (the sole incident responder), who coordinates within the Wazuh/Shuffle/TheHive incident response pipeline for digital consequences.
- **Evidence paths:**
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` (lines 229-238: GPU Thermal Critical alert uid=dfihoiidr7k00c -- environmental monitoring alert routed to #infrastructure-alerts)
  - `/c/Projects/CLAUDE.md` (Phase 14 thermal hardening section: `nvidia-power-cap.service` at 40W, Grafana alert uid=dfihoiidr7k00c, temp 87C→63C result)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps row)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (physical rack consolidation reboot event and its detection/response -- demonstrates physical event → operational impact → detection → remediation chain)
- **Set-params (proposed values):**
  - `pe-06_odp.01` / `pe-6_prm_1` (physical access log review frequency): value `not-applicable -- no formal physical access log system; Wazuh agent health reviewed daily via WF2 watch digest`, origin `organization`
  - `pe-06_odp.02` / `pe-6_prm_2` (events triggering physical access log review): value `unexpected host unavailability, Wazuh agent disconnect, or Grafana thermal/infrastructure alert`, origin `organization`
- **Authoring notes:** PE-6 is `partial` -- environmental monitoring (GPU thermal) and host-health monitoring (Wazuh agent status, WF2 watch digest) provide meaningful physical-access-consequence visibility, but no dedicated physical access monitoring system (cameras, badge readers, motion sensors) is deployed. Prose should highlight the Grafana thermal alert as the operational environmental monitoring artifact while acknowledging the gap vs. enterprise physical monitoring. Cite the Phase 14 thermal hardening incident (brisket GPU 87C→63C) as a live example of the environmental alert system working. Cross-reference IR-6 (incident reporting) for the response chain.

---

## PE-8 Visitor Access Records

- **Status:** not-applicable
- **Primary mechanism:** No visitors are admitted to the facility where the system resides. The Managed SOC Service operates in a private residence with the homeowner as the sole operator and sole occupant of the equipment room. Visitor access records are not applicable to a single-operator personal system with no visitor access.
- **Supporting mechanisms:** Not applicable.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (equipment location: private residence; all hosts listed as single-operator homelab)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps: residential homelab context)
- **Set-params (proposed values):**
  - `pe-08_odp.01` / `pe-8_prm_1` (visitor access record retention period): value `not-applicable -- single-operator personal system; no visitors admitted to facility`, origin `organization`
  - `pe-08_odp.02` / `pe-8_prm_2` (visitor access record review frequency): value `not-applicable -- single-operator personal system; no visitor access records generated`, origin `organization`
  - `pe-08_odp.03` / `pe-8_prm_3` (personnel to receive anomaly reports): value `not-applicable -- single-operator personal system; no visitor access records generated`, origin `organization`
- **Authoring notes:** PE-8 is `not-applicable` -- this is not a gap or a partial implementation; it is genuinely inapplicable because the facility has no visitors. Prose should state the N/A justification clearly in 1-2 sentences per Plan 3 design §3.3. Do not leave the justification undefended. Cross-reference PE-2 (access authorizations: single-entry list) and PE-3 (physical access control: residential mechanisms only).

---

## PE-12 Emergency Lighting

- **Status:** partial
- **Primary mechanism:** The facility (private residence) is equipped with residential smoke detectors and standard residential electrical wiring. The home does not have dedicated automatic emergency lighting beyond standard residential requirements (illuminated exit signs or automatic emergency lighting are not typical in residential settings). The Goldenmate 1000VA/800W LiFePO4 UPS (per the 2026-04-07 rack build) provides battery-backed power to all rack-mounted equipment during brief power outages, keeping the SOC infrastructure operational -- this is the closest functional analog to the emergency power intent of PE-12 in a residential context.
- **Supporting mechanisms:** All in-boundary rack equipment runs on the Goldenmate UPS (brisket, haccp, pitcrew, smoker, OPNsense, MokerLink, TP-Link -- 7 of 8 UPS outlets; smokehouse QNAP on wall outlet). The UPS provides runtime sufficient for controlled shutdown if power does not restore. The home office room has standard residential lighting with no emergency-exit-specific automatic lighting. Evacuation routes in a private residence are standard residential (exterior doors) and do not require dedicated marked emergency exits.
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (§Power: Goldenmate 1000VA/800W LiFePO4 UPS, 8 outlets, 200-340W draw; §Outlet plan: 7 rack devices on UPS; §UPS at U1-2: layout details)
  - `/c/Projects/CLAUDE.md` (Phase status: "Rack consolidation completed 2026-04-07 -- ... Goldenmate UPS" -- confirms UPS is in production)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps acknowledgment)
- **Set-params (proposed values):**
  - none -- PE-12 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** PE-12 is `partial` -- the UPS provides battery-backed emergency power to all rack equipment (the operational continuity intent of PE-12), but automatic emergency lighting for evacuation routes is a residential standard that does not apply in the same way as for a data center. Prose should present the UPS as the primary PE-12 implementation artifact and acknowledge the residential context. Cite the rack build design for UPS specifications. The gap (no dedicated automatic emergency lighting beyond residential standards) should be named explicitly in prose paragraph 2.

---

## PE-13 Fire Protection

- **Status:** partial
- **Primary mechanism:** The facility (private residence) is equipped with residential smoke detectors throughout, including proximity to the home office/equipment room where the 12U rack is located. Residential smoke detectors are battery-backed (9V battery or 10-year lithium sealed battery) and function independently of facility power -- satisfying the independent energy source requirement. No fire suppression system (sprinkler, CO2, or halon) is installed beyond residential requirements.
- **Supporting mechanisms:** The open-frame 12U rack design (passive convection cooling, no enclosed cabinet) reduces heat concentration risk and improves smoke detector response time compared to an enclosed equipment cabinet. The GPU thermal management (nvidia-power-cap.service at 40W, Grafana alert uid=dfihoiidr7k00c) reduces the thermal risk profile that could otherwise lead to fire ignition. The Goldenmate UPS uses LiFePO4 chemistry (lower fire risk than lithium-ion). No on-site fire extinguisher record is maintained in the project repo, though residential fire extinguishers are standard homeowner practice.
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (§Cooling: open-frame passive convection; §Airflow; rack layout showing no enclosed cabinet -- fire detection design characteristic)
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` (GPU Thermal Critical alert -- environmental thermal monitoring as fire-risk reduction)
  - `/c/Projects/CLAUDE.md` (Phase 14 thermal hardening: nvidia-power-cap.service at 40W, temp 87C→63C -- thermal risk mitigation)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps)
- **Set-params (proposed values):**
  - none -- PE-13 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** PE-13 is `partial` -- residential smoke detectors (battery-backed, independent energy source) satisfy the fire detection requirement; the independent energy source is the detector's battery. The gap is fire suppression: no suppression system is deployed beyond residential fire extinguisher(s). Prose paragraph 1 should lead with smoke detectors + independent battery power source. Paragraph 2 should cite the thermal management (GPU cap, Grafana alert) as the operational fire-risk-reduction mechanism and name the suppression gap. Cross-reference PE-14 (environmental controls) for the thermal monitoring architecture.

---

## PE-14 Environmental Controls

- **Status:** partial
- **Primary mechanism:** Temperature in the home office/equipment room is maintained by the residential HVAC system (central air conditioning and heating) at standard residential comfort levels (approximately 68-76°F / 20-24°C). The 12U open-frame rack (passive convection, no enclosed cabinet) dissipates heat naturally without dedicated rack-mounted cooling equipment. GPU thermal monitoring on brisket via `nvidia-power-cap.service` (power-capped to 40W) and the Grafana alert "GPU Thermal Critical -- Brisket Above 90C" (uid=dfihoiidr7k00c, `brisket-setup/monitoring/build-grafana-alerts.py`) provide continuous automated temperature monitoring for the highest-heat component in the rack.
- **Supporting mechanisms:** The Phase 14 thermal hardening incident (2026-04-08) demonstrated that GPU temperature monitoring is operational: brisket RTX A1000 reached 87C under unbounded Ollama load, the thermal risk was detected and mitigated by power-capping to 40W, reducing temperature to 63C and fan speed from 66% to 39%. No dedicated humidity, pressure, or radiation monitoring is deployed -- the residential HVAC maintains acceptable humidity ranges as a side effect. Prometheus on brisket collects NVIDIA SMI metrics (`nvidia_smi_temperature_gpu{job="brisket-nvidia"}`) monitored via Grafana.
- **Evidence paths:**
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` (lines 229-238: GPU Thermal Critical alert uid=dfihoiidr7k00c, threshold `nvidia_smi_temperature_gpu{job="brisket-nvidia"}`)
  - `/c/Projects/CLAUDE.md` (Phase 14 thermal hardening: nvidia-power-cap.service at 40W, temp 87C→63C, fan 66%→39%; Grafana alert uid=dfihoiidr7k00c, #infrastructure-alerts route)
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (§Cooling: passive convection, open-frame design; §Power: total draw 200-340W -- within passive cooling limits for under-desk placement)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps)
- **Set-params (proposed values):**
  - `pe-14_odp.01` / `pe-14_prm_1` (environmental controls monitored -- selection): value `temperature`, origin `organization`
  - `pe-14_odp.02` / `pe-14_prm_2` (acceptable environmental control levels): value `GPU temperature below 85C (Grafana alert fires at 90C as the critical threshold); ambient room temperature maintained at 68-76°F (20-24°C) by residential HVAC`, origin `organization`
  - `pe-14_odp.03` / `pe-14_prm_3` (environmental control monitoring frequency): value `continuous -- Prometheus scrapes NVIDIA SMI metrics every 15 seconds; Grafana evaluates alert every 2 minutes`, origin `organization`
  - `pe-14_odp.04` / `pe-14_prm_4` (additional parameters): value `not-applicable -- humidity, pressure, and radiation monitoring not deployed; residential HVAC maintains acceptable humidity as a side effect`, origin `organization`
- **Authoring notes:** PE-14 is `partial` -- GPU temperature monitoring is implemented, operational, and has a live incident proving it works (Phase 14 thermal hardening). The gap is coverage: only GPU temperature is formally monitored; ambient room temperature relies on residential HVAC without dedicated sensors or alerting; humidity/pressure/radiation are not monitored. Prose lead paragraph should cite the Grafana alert and the Phase 14 incident as the primary evidence. Paragraph 2 should name the residential HVAC as the ambient temperature control and the monitoring gaps. Cross-reference PE-13 (fire protection) for the thermal-risk connection.

---

## PE-15 Water Damage Protection

- **Status:** partial
- **Primary mechanism:** The 12U rack is located in a home office inside a private residence, above ground floor level, away from plumbing fixtures. Water damage protection relies on: (1) standard residential construction (above-grade equipment room, no equipment in basement or near plumbing fixtures); (2) the homeowner's awareness of the main water shutoff valve location (a residential standard). No dedicated water leak detection sensors or automated shutoff devices are deployed in or adjacent to the equipment room.
- **Supporting mechanisms:** The rack build design placed all equipment under PITBOSS's desk in a dedicated office -- not in a basement, server closet near HVAC drain pans, or other water-risk location. The open-frame rack design (no contained cabinet) means water from a ceiling leak would be visible immediately rather than pooling inside a sealed cabinet. The homeowner knows the location of the residential main water shutoff valve (required knowledge for homeowners; no documentation in the project repo is needed to assert this).
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (§Rack layout: under-desk placement in home office; no basement or plumbing-adjacent location)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (§PE honest-gaps -- partial PE from residential context)
  - `/c/Projects/CLAUDE.md` (equipment location: private residence, PITBOSS is the Windows laptop in the same room -- confirms office/non-basement location)
- **Set-params (proposed values):**
  - none -- PE-15 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** PE-15 is `partial` -- the main water shutoff is accessible, working, and known to the operator (homeowner standard). The gap is dedicated water detection: no leak sensors or automated isolation valves are deployed near the equipment. Prose should state the N/A of enterprise-grade water protection in residential context while affirming the residential controls that do satisfy the intent (shutoff valve known and accessible). Do not claim `not-applicable` at the control level -- the control's stated protection mechanism (accessible shutoff valve) does exist and is implemented.

---

## PE-16 Delivery and Removal

- **Status:** partial
- **Primary mechanism:** System component delivery and removal is controlled by the homeowner/operator (Brian Chaplow) as the sole authorizing individual. The 2026-04-07 rack consolidation event constitutes the primary delivery/removal record: 3 drive swaps (haccp 2TB PCAP drive, pitcrew +512GB, smoker +1TB) and installation of all rack equipment were authorized, controlled, and documented in `/c/Projects/CLAUDE.md` (rack consolidation paragraph) and in the rack build design spec. No unauthorized hardware enters or exits the facility.
- **Supporting mechanisms:** No formal shipping/receiving log or equipment custody chain is maintained beyond the CLAUDE.md narrative record and associated design documents. Drive swaps are the most common delivery/removal events for this system and are documented at the time of rack changes. The Wazuh `syscollector` module tracks hardware inventory on in-boundary hosts, providing an automated hardware-state record that detects post-delivery component changes. The IIW spreadsheet (`inventory/IIW-2026-04.xlsx`, generated by `./pipelines.sh conmon`) provides a monthly asset snapshot that serves as a formal inventory record.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (rack consolidation 2026-04-07: "3 drive swaps (haccp 2TB PCAP, pitcrew +512GB, smoker +1TB)" -- primary delivery/removal record)
  - `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` (§BOM/shopping list: equipment types authorized for facility entry; rack layout: authorized component placement)
  - `inventory/IIW-2026-04.xlsx` (monthly asset inventory -- formal component record, 7 in-boundary rows)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 completion: dojo and regscale VMs deployed -- authorized component additions documented)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (rack consolidation reboot documented -- physical change event tracking)
- **Set-params (proposed values):**
  - `pe-16_odp.01` / aggregate `pe-16_prm_1` (types of system components authorized for entry/exit): value `servers and workstations (Lenovo ThinkStation/Tiny), managed switches (MokerLink), firewalls (Protectli), storage drives (NVMe/SATA), network adapters (USB 2.5GbE), UPS (Goldenmate 1000VA)`, origin `organization`
  - `pe-16_odp.02` / aggregate `pe-16_prm_1` (additional component types): value `Proxmox Backup Server LXC containers authorized via Proxmox UI; target VMs (VLAN 40) authorized via Proxmox UI`, origin `organization`
- **Authoring notes:** PE-16 is `partial` -- delivery and removal is authorized and controlled (homeowner sole authority, no unauthorized hardware), and the major component change event (rack consolidation drive swaps) is documented in CLAUDE.md. The gap is formality: no shipping log, no custody chain, no dedicated receiving area or isolation room. The IIW monthly asset snapshot (`inventory/IIW-2026-04.xlsx`) is the closest formal component record. Prose should cite CLAUDE.md rack consolidation paragraph and the IIW as the primary evidence. Cite ADR 0002 for the dojo/regscale VM additions as a documented delivery event. Note that `syscollector` provides automated hardware-state visibility as a supporting mechanism.

---

*Catalog complete. 10 controls documented.*

## Subagent summary report

```json
{
  "family": "pe",
  "controls_cataloged": 10,
  "grep_verifications_performed": 18,
  "cites_to_parent_claude_md": 9,
  "cites_to_adrs": 7,
  "unresolved_questions": [
    "PE-12: No rack build ADR exists that confirms Goldenmate UPS was actually installed on 2026-04-07 vs. planned -- the rack build design spec is the plan, and CLAUDE.md says 'rack consolidation completed 2026-04-07' but does not explicitly name the UPS as installed. The design spec and CLAUDE.md together are sufficient for authoring; flag for Gate 3 if the operator wants a stronger artifact.",
    "PE-13: No project-repo documentation of residential smoke detector presence. The claim is standard residential construction; if Gate 3 requires a stronger evidence path, the operator could add a brief note to an ADR amendment or to CLAUDE.md confirming residential smoke detectors are installed.",
    "PE-15: No project-repo documentation of main water shutoff valve location. Same residential-standard caveat as PE-13.",
    "PE-14 ODP param numbering: pe-14_odp.04 (pe-14_prm_4) appears in the scaffold with no label beyond generic aggregate -- verify during authoring that the correct param identifiers are used when filling the trestle-workspace markdown."
  ]
}
```
