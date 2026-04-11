# AC -- Access Control Evidence Catalog

**Family:** Access Control (AC)
**Controls in baseline:** ac-1, ac-2, ac-3, ac-7, ac-8, ac-14, ac-17, ac-18, ac-19, ac-20, ac-22
**Catalog produced by:** Phase 1 subagent (2026-04-09)
**Repo:** homelab-fedramp-low (main branch)

> **Evidence policy (per Plan 3 design §3.2):** Every path cited below was verified to exist in the local filesystem before writing. Paths rooted at `/c/Projects/` are from the parent workspace; paths without a leading `/c/Projects/homelab-fedramp-low/` prefix are relative to this repo root. ADR references point to `docs/adr/` in this repo unless otherwise noted.

> **Parameter policy (per Plan 3 design §3.4):** The bootstrapped FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `set-parameters` alter blocks -- the GSA-sourced XML modify/alter sections were intentionally excluded during the Plan 2 bootstrap (ADR 0006 Deviation 11, `oscal/profile/SOURCE.md`). All AC ODPs therefore resolve as `organization-defined`. Proposed values use real homelab cadences; `inherited` origin is not applicable for this family.

---

## AC-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** This SSP document -- together with ADR 0001 (EULA/pre-flight), ADR 0002 (Plan 1 deployment), and ADR 0008 (Plan 3 pre-execution realignment) -- collectively functions as the access control policy and procedures record for the Managed SOC Service.
- **Supporting mechanisms:** `runbooks/cert-trust.md` (TLS posture procedures); `deploy/defectdojo/README.md` and `deploy/regscale/README.md` (service-specific access procedures); `docs/plan-3/SHAPE-CHECK-LOG.md` (authoring conventions). ADR update cadence is event-driven (each plan phase produces at least one ADR).
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (EULA analysis, pre-flight decisions -- earliest policy artifact)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 completion and operator action items -- serves as procedure record)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` (authoring conventions, implementation status rubric, set-params policy)
  - `runbooks/cert-trust.md` (documented procedures for TLS posture decisions)
  - `/c/Projects/CLAUDE.md` (system-level policy: canonical VLAN layout, SSH conventions, credential handling, attack rules -- system-level access control policy enforced by convention)
- **Set-params (proposed values):**
  - `ac-01_odp.01` (organization-defined personnel or roles to receive policy): value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `ac-01_odp.02` (organization-defined personnel or roles to receive procedures): value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `ac-01_odp.03` / `ac-1_prm_2` (policy review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `ac-01_odp.04` / `ac-1_prm_3` (events triggering policy review): value `plan phase completion, new service enrollment, security incident, or regulatory change`, origin `organization`
  - `ac-01_odp.05` / `ac-1_prm_4` (procedures review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `ac-01_odp.06` / `ac-1_prm_5` (events triggering procedures review): value `plan phase completion, new service enrollment, or deviation requiring an ADR`, origin `organization`
  - `ac-01_odp.07` / `ac-1_prm_6` (policy designation official): value `Brian Chaplow (system owner)`, origin `organization`
  - `ac-01_odp.08` / `ac-1_prm_7` (procedures designation official): value `Brian Chaplow (system owner)`, origin `organization`
- **Authoring notes:** AC-1 is `partial` -- not `not-applicable` -- because policy artifacts exist (ADRs, CLAUDE.md, runbooks) but no formal HR-style policy dissemination process exists for a single-operator system. Prose paragraph 2 should name this gap explicitly. Cite ADR 0008 §Pre-execution decisions item 5 (Implementation Status rubric) for the `partial` rationale. Cross-reference IA-1 (same pattern: policy exists in CLAUDE.md + ADRs, single-operator).

---

## AC-2 Account Management

- **Status:** partial
- **Primary mechanism:** All in-boundary service accounts are individually provisioned: Wazuh dashboard (`admin`), Shuffle SOAR (`admin`), OpenCTI (`admin@opencti.local` + `socadmin@SOC`), TheHive (`admin@thehive.local` + `socadmin@thehive.local`), Cortex (`admin` + `socadmin@SOC`), Velociraptor (`admin`), DefectDojo (`admin`), RegScale (`admin`). No shared credentials in code -- all passwords in `/c/Projects/.env` (gitignored). SSH access is key-only (no password SSH) on all in-boundary Linux hosts.
- **Supporting mechanisms:** Wazuh monitors all in-boundary hosts via 15 agents (brisket, haccp, smokehouse, dojo, regscale, OPNsense syslog, and customer/target agents); account use is observable via `wazuh-alerts-4.x-*` indices. `unattended-upgrades` active on dojo and regscale (reduces attack surface from stale packages). No shared group accounts deployed.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (credentials table: per-service individual accounts, `.env` location, no hardcoded passwords)
  - `docs/adr/0003-regscale-install-deviation.md` §Decisions (documents `admin` account, no default password, mandatory SQL reset -- account provisioning procedure)
  - `docs/adr/0004-defectdojo-install-deviation.md` §Decision (documents `admin` account, initializer log capture procedure)
  - `deploy/regscale/README.md` (admin username `admin`, password policy: length 12, upper/lower/digit/symbol)
  - `deploy/defectdojo/README.md` (admin account, initializer log, `.env` storage)
  - `deploy/proxmox/dojo-vm-config.yaml` (VM provisioning: `ciuser: ubuntu`, no root login)
- **Set-params (proposed values):**
  - `ac-02_odp.01` / `ac-2_prm_1` (account types allowed): value `individual service accounts per application (admin, socadmin role variants); SSH key accounts on Linux hosts (bchaplow, ubuntu CI user); no group/shared/anonymous/temporary/guest accounts`, origin `organization`
  - `ac-02_odp.02` / `ac-2_prm_2` (account types specifically prohibited): value `shared accounts, anonymous accounts, guest accounts, emergency bypass accounts`, origin `organization`
  - `ac-02_odp.03` / `ac-2_prm_3` (prerequisites and criteria for group/role membership): value `single-operator system -- no group membership process; all accounts individually owned by Brian Chaplow (system owner)`, origin `organization`
  - `ac-02_odp.04` / `ac-2_prm_4` (attributes required for each account): value `username, role (admin or read-only), service scope`, origin `organization`
  - `ac-02_odp.05` / `ac-2_prm_5` (personnel or roles approving account creation): value `Brian Chaplow (system owner, sole approver)`, origin `organization`
  - `ac-02_odp.06` / `ac-2_prm_6` (account management policy/procedures/prerequisites): value `accounts created at service deployment; documented in service-specific deploy/ READMEs and ADRs; credentials stored in /c/Projects/.env`, origin `organization`
  - `ac-02_odp.07` / `ac-2_prm_7` (personnel or roles notified when accounts no longer required): value `Brian Chaplow (system owner) -- single operator, self-notification`, origin `organization`
  - `ac-02_odp.08` / `ac-2_prm_8` (time period for notification when accounts no longer required): value `same day`, origin `organization`
  - `ac-02_odp.09` / `ac-2_prm_9` (time period for notification on termination/transfer): value `not-applicable -- single-operator personal system; no personnel termination process`, origin `organization`
  - `ac-02_odp.10` / `ac-2_prm_10` (account review frequency): value `annually and at each plan phase boundary`, origin `organization`
- **Authoring notes:** AC-2 is `partial` because: (1) no HR offboarding process exists for a single-operator system -- AC-2(l) alignment with personnel termination is not applicable; (2) AC-2(j) account review exists informally at plan boundaries, not on a formal documented calendar. Cite ADR 0003 (RegScale account provisioning) and ADR 0004 (DefectDojo account provisioning) as the account creation artifacts. The gap -- no formal HR alignment -- should be named in prose paragraph 2. Cross-reference IA-5 (authenticator management) for password policy depth.

---

## AC-3 Access Enforcement

- **Status:** implemented
- **Primary mechanism:** Three complementary enforcement layers: (1) OPNsense inter-VLAN firewall rules block unauthorized lateral movement between VLANs 10/20/30/40/50; (2) MokerLink switch ACL `sear-brisket` on TE4 enforces intra-VLAN microsegmentation (stateless, bidirectional, default-deny for sear→brisket except specific enumerated ports); (3) UFW on all in-boundary Linux hosts (brisket, haccp, smokehouse, dojo, regscale) enforces host-level access control (default-deny ingress, explicit VLAN-scoped allows for each service port).
- **Supporting mechanisms:** SSH key-only authentication (no password SSH) enforces the access model at the protocol layer. Service-level RBAC: Wazuh (admin vs. read-only), OpenCTI (admin vs. analyst), TheHive (platform-admin vs. org-admin). VLAN 40 (targets) is isolated -- cannot initiate connections to VLANs 20/30 per OPNsense rules.
- **Evidence paths:**
  - `/c/Projects/reference/network.md` (OPNsense interface map, firewall rules table, MokerLink ACL `sear-brisket` with full 9-rule enumeration and packet-flow verification results)
  - `/c/Projects/CLAUDE.md` (VLAN table, inter-VLAN firewall rules summary, UFW conventions for in-boundary VMs)
  - `docs/adr/0002-deployment-complete.md` §Infrastructure state (dojo + regscale: UFW default-deny with VLAN-scoped allows on SSH + service port)
  - `deploy/proxmox/dojo-vm-config.yaml` (Proxmox firewall disabled; UFW handles host-level enforcement)
- **Set-params (proposed values):**
  - none -- AC-3 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** AC-3 is `implemented` -- all three enforcement layers (OPNsense, MokerLink ACL, UFW) are running now and actively enforcing the access model. Cite `/c/Projects/reference/network.md` for the MokerLink ACL table with full packet-flow verification (dated 2026-02-11) and the OPNsense inter-VLAN rules. Note the stateless nature of the switch ACL (requires explicit return-traffic rules) as a design characteristic. Cross-reference SC-7 (boundary protection) and AC-17 (remote access).

---

## AC-7 Unsuccessful Logon Attempts

- **Status:** partial
- **Primary mechanism:** SSH key-only authentication on all in-boundary Linux hosts eliminates password-guessing risk at the protocol layer -- there are no passwords to brute-force via SSH. For web-based service UIs (Wazuh dashboard, Shuffle, OpenCTI, TheHive, DefectDojo, RegScale), account lockout policies depend on each application's built-in enforcement.
- **Supporting mechanisms:** Wazuh rule set monitors failed authentication events from syslog and agent telemetry (`wazuh-alerts-4.x-*` indices on brisket). DefectDojo 2.57.0 Django auth includes configurable lockout. RegScale CE asp.net identity has `AccessFailedCount` and `LockoutEnd` columns (reset to NULL at deploy, per `deploy/regscale/reset-admin-password.sh`). OPNsense does not expose a login lockout configuration in the reviewed version.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (SSH key-only convention for all in-boundary hosts; no password SSH)
  - `docs/adr/0003-regscale-install-deviation.md` §Decisions item 3 (RegScale CE `AccessFailedCount = 0, LockoutEnd = NULL` in password reset -- documents the lockout field exists in schema)
  - `deploy/regscale/reset-admin-password.sh` (script resets `AccessFailedCount = 0` and `LockoutEnd = NULL` during provisioning, confirming lockout schema exists)
- **Set-params (proposed values):**
  - `ac-07_odp.01` / `ac-7_prm_1` (number of consecutive invalid logon attempts): value `5`, origin `organization`
  - `ac-07_odp.02` / `ac-7_prm_2` (time period for counting consecutive invalid attempts): value `15 minutes`, origin `organization`
  - `ac-07_odp.03` / `ac-7_prm_3` (action on maximum attempts exceeded -- selection): value `lock the account until released by an administrator`, origin `organization`
  - `ac-07_odp.04` / `ac-7_prm_4` (lockout time period if auto-release selected): value `not-applicable -- administrator release selected`, origin `organization`
  - `ac-07_odp.05` / `ac-7_prm_5` (delay algorithm if delay selected): value `not-applicable -- lockout selected`, origin `organization`
  - `ac-07_odp.06` / `ac-7_prm_6` (other action if "other action" selected): value `not-applicable -- lockout selected`, origin `organization`
- **Authoring notes:** AC-7 is `partial` -- SSH key-only auth makes the SSH attack surface moot, but web UI lockout is application-dependent and not uniformly verified or documented across all six UIs. The gap is: no centralized failed-login dashboard or alert exists that aggregates across all service UIs. Prose paragraph 2 should name this gap. Note that Wazuh monitors auth events but a dedicated AC-7 Wazuh rule for multi-service lockout is not configured. Cross-reference IA-5 (authenticator management) and AU-2/AU-6 (audit of logon events).

---

## AC-8 System Use Notification

- **Status:** partial
- **Primary mechanism:** SSH banner (`/etc/issue.net` or `sshd_config Banner` directive) on in-boundary Linux hosts provides the system use notification for SSH sessions. No dedicated login banners are configured on web UIs (Wazuh dashboard, Shuffle, OpenCTI, TheHive, DefectDojo, RegScale) -- these services display their own application login screens without a pre-login banner.
- **Supporting mechanisms:** None configured for web-based service access paths.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (SSH conventions; all in-boundary hosts accessed via SSH key auth -- the SSH banner path is the primary notification mechanism)
  - `docs/adr/0002-deployment-complete.md` §Infrastructure state (dojo + regscale: Ubuntu 24.04.4 LTS, SSH key-based -- SSH banner config is addressable at OS level)
- **Set-params (proposed values):**
  - `ac-08_odp.01` / `ac-8_prm_1` (system use notification text): value `"This system is the property of Brian Chaplow and is authorized for use only in connection with the homelab Managed SOC Service portfolio program. System usage may be monitored, recorded, and subject to audit. Unauthorized use is prohibited. Use of this system constitutes consent to monitoring and recording."`, origin `organization`
  - `ac-08_odp.02` / `ac-8_prm_2` (conditions for publicly accessible systems): value `not-applicable -- no publicly accessible interfaces in the MSS boundary`, origin `organization`
- **Authoring notes:** AC-8 is `partial` -- SSH banner mechanism is implementable and should be cited as the primary path, but implementation has not been verified as actually deployed on every in-boundary host (evidence gap: no `sshd_config` file checked into repo). Web UI banner gap: six service UIs have no pre-login notification. Prose paragraph 2 should identify the gap as "web-UI banners not yet configured." The system use notification text proposed in `ac-08_odp.01` is the text to use if/when banners are deployed. Cross-reference IA-8 (identification and authentication for non-organizational users) for the rationale that only authorized personnel access these systems.

---

## AC-14 Permitted Actions Without Identification or Authentication

- **Status:** implemented
- **Primary mechanism:** No actions on the MSS boundary systems are permitted without identification or authentication. All service UIs require credentials. SSH requires key authentication. The OPNsense firewall and MokerLink switch management interfaces require admin credentials. VLAN 40 (targets) is isolated from MSS services and cannot reach them unauthenticated.
- **Supporting mechanisms:** Prometheus metrics endpoint on brisket (:9090) is accessible only from VLAN 20/30 hosts and does not require auth (scrape-only, no write access, internal metrics). This is the only acknowledged unauthenticated access path and it is bounded to internal VLANs.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (service inventory: every service listed has a credential; SSH key-only convention)
  - `/c/Projects/reference/network.md` (firewall rules: VLAN 40 isolated, inbound connections blocked)
  - `inventory/overlay.yaml` (boundary classification: all in-boundary assets require auth)
- **Set-params (proposed values):**
  - `ac-14_odp` / `ac-14_prm_1` (user actions permitted without identification or authentication): value `none -- all user-facing actions on MSS boundary systems require identification and authentication; Prometheus metrics scrape (:9090) is an internal-VLAN-only machine-to-machine path, not a user action`, origin `organization`
- **Authoring notes:** AC-14 is `implemented` with the honest acknowledgment that Prometheus at :9090 is an unauthenticated machine-to-machine scrape path. The control's guidance explicitly notes "the value for the assignment operation can be 'none'" and that this applies to user actions, not machine-to-machine telemetry. Prose should state the ODP value is "none" and briefly explain the Prometheus carve-out. Cross-reference AC-3 (access enforcement) and IA-2 (identification and authentication for users).

---

## AC-17 Remote Access

- **Status:** implemented
- **Primary mechanism:** Remote administrative access uses Tailscale mesh VPN (WireGuard-based, end-to-end encrypted). PITBOSS connects to in-boundary hosts via Tailscale IP addresses (brisket TS:100.124.139.56, haccp TS:100.74.16.82, sear TS:100.86.67.91, smokehouse TS:100.110.112.98). SSH key authentication enforces identity on the tunnel endpoint. No password SSH is permitted on any in-boundary host.
- **Supporting mechanisms:** All remote connections terminate at the host SSH daemon with key-only auth -- Tailscale provides network-layer encryption; SSH provides application-layer authentication. GCP VM agent (Wazuh agent 009) connects outbound to brisket:1514 over TLS (Wazuh enrollment-key authenticated) -- this is a remote telemetry path, not an admin path.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (SSH Quick Reference: Tailscale IPs for every remote-accessible host; note "Tailscale -- LAN IP may not route from PITBOSS" for haccp)
  - `/c/Projects/CLAUDE.md` (service inventory: Wazuh Manager ports 1514/1515 for remote agent TLS enrollment; GCP VM Wazuh agent 009)
  - `docs/adr/0002-deployment-complete.md` §Infrastructure state (dojo + regscale remote access documented; both VMs accessible via SSH from VLAN 10/20/30 scoped UFW rules)
- **Set-params (proposed values):**
  - none -- AC-17 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** AC-17 is `implemented`. Prose should enumerate the two authorized remote access types: (1) Tailscale mesh VPN + SSH key auth for operator administrative access; (2) Wazuh TLS enrollment for customer agent telemetry ingestion. Cross-reference CA-3 (system connections) for the PBS NFS backup external connection and the GCP VM external agent. Note PITBOSS is out-of-boundary per the boundary definition (design spec §2.3) but is the documented admin access path. The Tailscale TS IPs in CLAUDE.md are the authoritative source for remote access endpoints.

---

## AC-18 Wireless Access

- **Status:** not-applicable
- **Primary mechanism:** No in-boundary MSS components are connected via wireless. All in-boundary hosts (brisket, haccp, smokehouse, dojo VM, regscale VM, OPNsense, MokerLink) communicate exclusively over wired Ethernet connections terminated at the MokerLink switch.
- **Supporting mechanisms:** ASUS WiFi router is the family LAN (192.168.50.0/24) -- out-of-boundary. IoT VLAN 50 is WiFi-served but no MSS components reside on VLAN 50.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (VLAN table: all in-boundary hosts have wired IP assignments; ASUS router = family DMZ 192.168.100.0/24 and family LAN 192.168.50.0/24 -- out-of-boundary)
  - `/c/Projects/reference/network.md` (physical topology: patch panel + MokerLink wired only for in-boundary hosts; rack build 2026-04-07 all wired)
  - `inventory/overlay.yaml` (all in-boundary assets: hardware_model descriptions reference wired Ethernet or Proxmox bridged networking -- no WiFi adapters)
- **Set-params (proposed values):**
  - none -- AC-18 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** AC-18 is `not-applicable` -- justified by the fact that zero in-boundary components use wireless. The N/A justification must be stated in 1–2 sentences in prose (per Plan 3 design §3.3). Note that PITBOSS may use WiFi when traveling but PITBOSS is out-of-boundary (admin workstation, documented as out-of-boundary in design spec §2.3). Cross-reference AC-19 (mobile devices) for the analogous not-applicable rationale.

---

## AC-19 Access Control for Mobile Devices

- **Status:** not-applicable
- **Primary mechanism:** No mobile devices are authorized for connection to MSS in-boundary systems. The MSS authorization boundary consists of rack-mounted servers, a firewall appliance, a managed switch, and Proxmox VMs -- all fixed infrastructure. PITBOSS (Windows laptop, ASUS TUF Dash F15) is the operator workstation and is classified out-of-boundary per the boundary definition.
- **Supporting mechanisms:** OPNsense firewall and MokerLink ACLs do not include any rules permitting mobile device connections to in-boundary services. Tailscale mesh is operator-to-server only (PITBOSS → in-boundary hosts), not mobile-device-oriented.
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.3 (PITBOSS explicitly listed as out-of-boundary: "Endpoint in admin access path; documented under AC-17")
  - `/c/Projects/CLAUDE.md` (PITBOSS host entry: Windows laptop -- operator workstation, not an MSS component)
  - `inventory/overlay.yaml` (out_of_boundary list includes PITBOSS: "Operator workstation -- endpoint visibility only, not a managed MSS asset")
- **Set-params (proposed values):**
  - none -- AC-19 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold
- **Authoring notes:** AC-19 is `not-applicable` -- the MSS is a fixed on-premises rack deployment with no mobile device connectivity authorized or implemented. Prose should state: no mobile devices are authorized for connection to in-boundary MSS systems; PITBOSS (the operator workstation) is a laptop but is classified out-of-boundary and its remote-access path (Tailscale + SSH) is covered under AC-17, not AC-19. Cross-reference AC-18 (wireless access, also N/A) and AC-17 (remote access, the operator's actual access path).

---

## AC-20 Use of External Systems

- **Status:** implemented
- **Primary mechanism:** Three authorized external system connections are in use: (1) GCP VM (Wazuh agent 009, Tailscale TS:100.125.40.97) sends telemetry to brisket Wazuh Manager via TLS-enrolled Wazuh agent -- the GCP VM is out-of-boundary customer asset; (2) PBS LXC 300 (smoker 10.10.30.24) receives backup data from in-boundary VMs via Proxmox Backup protocol -- documented under CA-3; (3) PITBOSS (admin workstation, out-of-boundary) accesses in-boundary systems via Tailscale + SSH key auth under AC-17. All three connections have documented terms and conditions via the boundary definition (design spec §2.3) and ADRs.
- **Supporting mechanisms:** Tailscale mesh (WireGuard, end-to-end encrypted) carries the PITBOSS administrative access path and the GCP Wazuh agent enrollment path. OPNsense firewall restricts which external IPs/ports can reach in-boundary services. No personal device or non-homelab external system has authorized access to in-boundary MSS components.
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.3 and §2.4 (out-of-boundary assets, external connection points -- authoritative boundary definition)
  - `/c/Projects/CLAUDE.md` (GCP VM: agent 009, Tailscale 100.125.40.97; Tailscale IPs for all out-of-boundary access paths; PBS LXC 300 on smoker)
  - `inventory/overlay.yaml` (out_of_boundary section: GCP VM, PITBOSS, PBS -- each with documented reason)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (PBS external system connection: NFS mount, backup gap, automount fix -- documents the PBS connection and its failure mode)
- **Set-params (proposed values):**
  - `ac-20_odp.01` / `ac-20_prm_1` (selection: terms and conditions or controls asserted): value `establish terms and conditions`, origin `organization`
  - `ac-20_odp.02` / `ac-20_prm_2` (terms and conditions for access from external systems): value `external systems must use Tailscale (WireGuard) VPN and SSH key authentication for administrative access, or Wazuh TLS enrollment with enrollment key for telemetry ingestion; no anonymous or password-only access from external systems is permitted`, origin `organization`
  - `ac-20_odp.03` / `ac-20_prm_3` (terms and conditions for processing/storing/transmitting on external systems): value `MSS data (alert telemetry, configuration) is not stored on external systems except: (a) PBS LXC 300 receives backup snapshots of in-boundary VMs under CA-3 documented agreement; (b) Tailscale relay nodes carry encrypted-in-transit administrative sessions with no data at rest`, origin `organization`
  - `ac-20_odp.04` / `ac-20_prm_4` (prohibited types of external systems): value `personal devices not enrolled in Tailscale; commercial cloud services not documented in the boundary definition; any system not listed in inventory/overlay.yaml out_of_boundary section`, origin `organization`
- **Authoring notes:** AC-20 is `implemented` -- all external system connections are documented and controlled. Cite design spec §2.3 and §2.4 as the terms-and-conditions source. Cite ADR 0005 as evidence of active management of the PBS external connection (the backup gap was detected and fixed -- this demonstrates oversight of the external system relationship). Cross-reference CA-3 (system connections) for the PBS NFS and GCP VM formal connection agreement, and AC-17 for the PITBOSS administrative access path.

---

## AC-22 Publicly Accessible Content

- **Status:** not-applicable
- **Primary mechanism:** No MSS in-boundary system hosts publicly accessible content or interfaces. All services (Wazuh dashboard, Shuffle, OpenCTI, TheHive, DefectDojo, RegScale, ELK, Arkime, Velociraptor, Prometheus, Grafana) are accessible only from VLANs 10/20/30 -- trusted internal subnets. No OPNsense port-forwards expose any in-boundary service to the Internet.
- **Supporting mechanisms:** OPNsense WAN interface (igc1, DHCP from Verizon ISP) has no inbound port-forward rules for MSS services. ASUS router (family DMZ/LAN) has no routes to VLANs 20/30. MokerLink VLAN isolation prevents VLAN 40 (targets) and VLAN 50 (IoT) from reaching MSS services.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (service inventory: all services bound to VLAN 20/30 IP addresses, no public-facing ports documented)
  - `/c/Projects/reference/network.md` (OPNsense interface map: igc1=WAN DHCP, no port-forward rules mentioned; VLAN isolation table)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.3 (GCP VM listed as out-of-boundary -- MSS does not host public content)
- **Set-params (proposed values):**
  - `ac-22_odp` / `ac-22_prm_1` (review frequency for publicly accessible content): value `not-applicable -- no publicly accessible systems in the MSS boundary`, origin `organization`
- **Authoring notes:** AC-22 is `not-applicable` -- the MSS has no publicly accessible systems. Prose should state: all MSS services are internal-VLAN-only; no port-forwards or public IPs expose any service to the Internet. The public portfolio website (brianchaplow.com, bytesbourbonbbq.com) is hosted on the out-of-boundary GCP VM (design spec §2.3) and is not part of the MSS authorization boundary. Cross-reference AC-14 (N/A rationale for unauthenticated access) and AC-17 (the only externally-facing path is administrative, via Tailscale).
