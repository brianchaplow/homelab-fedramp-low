# SC — System and Communications Protection: Evidence Catalog

**Family:** SC (14 controls)
**Cataloged:** 2026-04-09
**Subagent obligations:** all evidence paths grep/Read-verified before inclusion; baseline-mandated params flagged; no network access used.

---

## SC-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** System and communications protection policy is documented in-line across CLAUDE.md (network segmentation conventions, VLAN isolation rules, attack-only-on-VLAN-40 mandate) and enforced via OPNsense firewall rules and MokerLink ACLs. Brian Chaplow (sole operator) serves as the designated official for SC policy management.
- **Supporting mechanisms:** ADR series (0001–0008) provides an auditable policy-evolution trail; `runbooks/cert-trust.md` documents the TLS posture trade-off and upgrade path; `reference/network.md` documents firewall rules and switch ACL rationale.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Network Quick Reference (VLAN table, firewall rule conventions)
  - `C:/Projects/reference/network.md` §Firewall Rules (inter-VLAN policy)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (TLS posture trade-off + upgrade path)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` (pre-flight security posture)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0008-plan-3-pre-execution-realignment.md` (policy evolution record)
- **Set-params (proposed values):**
  - `sc-01_odp.01` / `sc-01_odp.02` (personnel/roles to disseminate policy to): `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `sc-01_odp.03` (designated official): `Brian Chaplow (system owner, sole operator)`, `organization`
  - `sc-01_odp.04` (policy review frequency): `annually`, `organization` — homelab cadence; no baseline-mandated value
  - `sc-01_odp.05` (policy review events): `when a new phase adds infrastructure components or when a security incident reveals a gap`, `organization`
  - `sc-01_odp.06` (procedures review frequency): `annually`, `organization`
  - `sc-01_odp.07` (procedures review events): `when a new phase adds infrastructure components or when a security incident reveals a gap`, `organization`
  - `sc-01_odp.08` (selection — level): `system-level`, `organization`
- **Authoring notes:** Gap: no formal standalone SC policy document — policy lives in CLAUDE.md conventions and ADR artifacts. Cite as partial. Second paragraph should name the gap explicitly and note CLAUDE.md as the de facto policy anchor. Review cadence is organization-defined (no FedRAMP-mandated frequency for this ODP).

---

## SC-5 Denial-of-Service Protection

- **Status:** partial
- **Primary mechanism:** OPNsense firewall on the Protectli VP2420 (10.10.10.1) provides the primary DoS mitigation layer: stateful packet inspection limits connection flooding from external sources, inter-VLAN rules deny inbound traffic from VLAN 40 (targets), and VLAN 50 (IoT) is restricted to internet-only egress with no lateral movement.
- **Supporting mechanisms:** MokerLink port-bound ACLs (TE4 sear-brisket) prevent intra-VLAN flooding between SOC components. Suricata IDS on smokehouse eth4 (SPAN of TE1-TE9) detects volumetric signatures. Wazuh ships Suricata alerts to `wazuh-alerts-*` for correlation. There is no cloud-based DoS scrubbing service; high-volume external floods would rely on Verizon upstream throttling.
- **Evidence paths:**
  - `C:/Projects/reference/network.md` §Firewall Rules (VLAN 40 deny rule, IoT restriction)
  - `C:/Projects/reference/network.md` §MokerLink Switch ACL (TE4 stateless ACL entries)
  - `C:/Projects/CLAUDE.md` §Service Inventory (Suricata on smokehouse, OPNsense on VP2420)
- **Set-params (proposed values):**
  - `sc-05_odp.01` (types of DoS events): `["volumetric network floods", "connection exhaustion", "intra-VLAN lateral flooding from compromised VMs"]`, `organization`
  - `sc-05_odp.02` (selection — protect against or limit): `limit`, `organization` — no full scrubbing; stateful firewall limits impact
  - `sc-05_odp.03` (controls by type): `["OPNsense stateful packet filtering for external volumetric events", "MokerLink port ACL for intra-VLAN flooding", "Suricata IDS for signature detection"]`, `organization`
- **Authoring notes:** Gap: no dedicated anti-DDoS appliance or cloud scrubbing. Partial is accurate — OPNsense limits effects but does not fully protect against sustained external floods. State the gap explicitly.

---

## SC-7 Boundary Protection

- **Status:** implemented
- **Primary mechanism:** OPNsense firewall (Protectli VP2420, 10.10.10.1) is the boundary enforcement point for all five VLANs (10 mgmt, 20 SOC, 30 lab, 40 targets, 50 IoT) via 802.1Q trunk on igc0 to the MokerLink switch. Inter-VLAN rules: VLAN 40 (targets) has an explicit DENY outbound with only established-session return allowed, enforcing isolation of customer test workloads. VLAN 50 (IoT) is restricted to internet-only with no lateral movement permitted.
- **Supporting mechanisms:** MokerLink 10G L3 managed switch (10.10.10.2) extends boundary enforcement intra-VLAN via port-bound stateless ACLs. The `sear-brisket` ACL on TE4 limits sear (10.10.20.20) to Wazuh-agent ports (1514, 1515) and OpenSearch (9200) inbound to brisket, blocking all other same-subnet access without routing through OPNsense. Tailscale encrypted mesh overlay provides the only authorized remote management path (PITBOSS → brisket/sear/smokehouse/haccp). External connection points documented in the whole-project design §2.4: customer Wazuh agent telemetry (brisket:1514 TLS), admin access via SSH key auth, PBS backup egress to smokehouse NFS.
- **Evidence paths:**
  - `C:/Projects/reference/network.md` §Firewall Rules (inter-VLAN deny table)
  - `C:/Projects/reference/network.md` §MokerLink Switch ACL (TE4 sear-brisket ACL entries, verification results 2026-02-11)
  - `C:/Projects/reference/network.md` §OPNsense Interface Map (igc0 trunk, VLAN assignments)
  - `C:/Projects/CLAUDE.md` §Network Quick Reference (VLAN table with ISOLATED notation for VLAN 40)
  - `C:/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.4 (external connection points: Wazuh agent telemetry, Tailscale, admin SSH)
- **Set-params (proposed values):**
  - `sc-07_odp` (managed interfaces / external systems): `["OPNsense inter-VLAN firewall on VP2420 (10.10.10.1)", "MokerLink L3 port ACLs on TE4 for intra-VLAN microsegmentation", "Tailscale mesh for authorized remote administrative access"]`, `organization`
- **Authoring notes:** Lead with OPNsense + 5-VLAN architecture. Second paragraph covers MokerLink same-subnet enforcement and Tailscale as the sole authorized remote boundary crossing. Cite VLAN 40 isolation explicitly. Reference §2.4 of the whole-project design for the three documented external connection types.

---

## SC-8 Transmission Confidentiality and Integrity

- **Status:** partial
- **Primary mechanism:** Transmission confidentiality and integrity is enforced for all in-boundary service-to-service paths using TLS: Wazuh Manager API (brisket:55000, HTTPS with self-signed cert), Wazuh Indexer/OpenSearch (brisket:9200, HTTPS), ELK Elasticsearch on haccp (10.10.30.25:9200, HTTPS). Tailscale encrypted mesh (WireGuard-based) protects all administrative remote access paths (PITBOSS to brisket/sear/smokehouse/haccp).
- **Supporting mechanisms:** Wazuh agent-to-manager telemetry (brisket:1514) uses TLS with enrollment-key authentication. Fluent Bit shipping Zeek logs from smokehouse to brisket:9200 transits over HTTPS. PCAP archival from haccp to smokehouse uses SSH/rsync (encrypted channel). Customer Wazuh agent enrollment uses TLS on port 1515.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Service Inventory brisket (Wazuh API :55000, Wazuh Indexer :9200 — HTTPS noted)
  - `C:/Projects/CLAUDE.md` §haccp service entry (ES HTTPS at :9200, Kibana HTTP at :5601)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (TLS gap for DefectDojo/RegScale HTTP-only + upgrade path)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0003-regscale-install-deviation.md` §Consequences (plain HTTP on port 80 — SC-8 POA&M callout)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0004-defectdojo-install-deviation.md` (HTTP-only on 8080, port 8443 unused)
- **Set-params (proposed values):**
  - `sc-08_odp` (selection — confidentiality and/or integrity): `["confidentiality", "integrity"]`, `organization` — both properties protected where TLS is implemented
- **Authoring notes:** Gap: DefectDojo (10.10.30.27:8080) and RegScale CE (10.10.30.28:80) are HTTP-only per ADRs 0003/0004; this is a documented trade-off (lab-only, VLAN-scoped, no external exposure, synthetic data). `runbooks/cert-trust.md` describes the upgrade path. Kibana on haccp is also HTTP (:5601). Status is partial — Wazuh/ELK core paths use TLS; two GRC tools do not. Name the gap explicitly in paragraph 2.

---

## SC-8(1) Cryptographic Protection (Transmission)

- **Status:** partial
- **Primary mechanism:** Cryptographic mechanisms protect transmitted information for Wazuh core paths and remote administration. Wazuh Manager API (brisket:55000) and Wazuh Indexer (brisket:9200) use HTTPS with TLS (self-signed certs per `runbooks/cert-trust.md`). ELK Elasticsearch (haccp:9200) uses HTTPS. Tailscale remote access uses WireGuard (ChaCha20-Poly1305 authenticated encryption). PCAP sync from haccp to smokehouse uses SSH (AES-based session encryption).
- **Supporting mechanisms:** Wazuh agent-to-manager channel (1514/TLS) is cryptographically protected via the Wazuh enrollment key exchange on port 1515. Fleet agent communications to haccp:8220 use HTTPS.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Service Inventory brisket (Wazuh API/Indexer HTTPS, Wazuh Dashboard :5601 HTTPS)
  - `C:/Projects/CLAUDE.md` §haccp host entry (ES HTTPS :9200, Fleet HTTPS :8220)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (self-signed cert context, TLS for Wazuh/ELK)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0003-regscale-install-deviation.md` §Consequences (HTTP-only gap called out as SC-8 POA&M item)
- **Set-params (proposed values):**
  - `sc-08.01_odp` (selection — prevent disclosure and/or detect changes): `["prevent unauthorized disclosure of information", "detect changes to information"]`, `organization`
- **Authoring notes:** Same partial justification as SC-8 — two GRC tools lack TLS. Distinguish this enhancement by naming the specific cryptographic mechanisms (TLS, WireGuard) rather than just the policy. FedRAMP-mandated: the selection ODP is organization-defined (no baseline mandate on the specific choices). Status matches SC-8 at partial.

---

## SC-12 Cryptographic Key Establishment and Management

- **Status:** partial
- **Primary mechanism:** Cryptographic key management for in-boundary services relies on: (1) Wazuh self-signed CA and agent enrollment keys managed via the Wazuh manager CLI (key generation at enrollment, stored in `/var/ossec/etc/sslmanager.*` on brisket); (2) Tailscale public-key infrastructure managed by Tailscale's coordination server (keys rotated automatically per Tailscale's key expiry policy); (3) SSH host keys on all in-boundary Linux hosts (generated at provision time, rotated on reimage).
- **Supporting mechanisms:** There is no formal key management system (KMS) or hardware security module (HSM). Self-signed cert renewal for Wazuh/ELK is a manual runbook operation (not yet written; tracked as a gap). PBS backup data is not separately encrypted at rest with managed keys (see SC-28).
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Service Inventory brisket (Wazuh Manager 1515 enrollment, HTTPS services)
  - `C:/Projects/CLAUDE.md` §SSH Quick Reference (SSH key authentication for all in-boundary hosts)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (self-signed cert lifecycle + upgrade path to step-ca)
- **Set-params (proposed values):**
  - `sc-12_odp` (key management requirements): `["keys generated at service provisioning using openssl or native tooling", "self-signed CA for Wazuh/ELK managed by sole operator Brian Chaplow", "Tailscale keys managed via Tailscale coordination server with automatic rotation", "SSH host keys generated at host provision, rotated on reimage", "no HSM or external KMS in scope for this homelab deployment"]`, `organization`
- **Authoring notes:** Gap: no formal KMS, no documented cert-renewal runbook. Partial is correct. Paragraph 2 should name the gap and reference `runbooks/cert-trust.md` upgrade path (step-ca as a future option).

---

## SC-13 Cryptographic Protection

- **Status:** partial
- **Primary mechanism:** Cryptographic uses in the MSS boundary are: (1) TLS 1.2/1.3 for HTTPS services (Wazuh API, OpenSearch, ELK Elasticsearch, Wazuh Dashboard); (2) WireGuard via Tailscale for remote administrative access; (3) SSH for host management and PCAP sync; (4) Wazuh enrollment key exchange on agent registration. All cryptographic implementations use standard open-source primitives (OpenSSL for TLS, WireGuard kernel module for Tailscale, OpenSSH for SSH).
- **Supporting mechanisms:** No FIPS-validated cryptographic modules are in use — this is a homelab environment running standard Linux kernel cryptography. The standard is NIST-approved algorithm coverage (AES, SHA-2, ECDHE) via OpenSSL and kernel crypto subsystem, not FIPS 140-2/3 validation.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Service Inventory brisket (HTTPS services enumerated)
  - `C:/Projects/CLAUDE.md` §SSH Quick Reference (SSH key auth for all in-boundary hosts)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (TLS implementation details)
- **Set-params (proposed values):**
  - `sc-13_odp.01` (cryptographic uses): `["HTTPS/TLS for Wazuh API, Wazuh Indexer, ELK Elasticsearch, Wazuh Dashboard", "WireGuard (via Tailscale) for remote administrative access", "SSH for host management and PCAP archival", "Wazuh enrollment key exchange"]`, `organization`
  - `sc-13_odp.02` (types of cryptography for each use): `["TLS 1.2/1.3 via OpenSSL for HTTPS services", "WireGuard ChaCha20-Poly1305 for Tailscale mesh", "AES-256-GCM / ECDHE via OpenSSH for host management", "Wazuh-native symmetric key for agent enrollment"]`, `organization`
- **Authoring notes:** Gap: no FIPS 140-2/3 validated modules. For a real FedRAMP-Low production deployment this would be a finding. For this homelab ConMon portfolio, document it as a known gap (partial) with the upgrade path being a FIPS-enabled OpenSSL build. FedRAMP Low does not mandate FIPS validation in the baseline profile itself, but the FedRAMP PMO expects FIPS-approved algorithms — all algorithms in use (AES, SHA-256, ECDHE) are NIST-approved even without module validation.

---

## SC-15 Collaborative Computing Devices and Applications

- **Status:** not-applicable
- **Primary mechanism:** The MSS boundary contains no collaborative computing devices or applications. There are no video conferencing endpoints, network-connected cameras, microphones, or interactive whiteboards within the authorization boundary. The in-boundary hosts are bare-metal servers (brisket, haccp, smokehouse), a Proxmox hypervisor (pitcrew), and network appliances (OPNsense, MokerLink). None have collaborative computing hardware.
- **Supporting mechanisms:** PITBOSS (admin workstation) is out-of-boundary. Any video or audio devices on PITBOSS are not in scope.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Network Quick Reference Host table (all in-boundary hosts — server/appliance role only)
  - `C:/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1 (in-boundary asset table — no collaborative devices listed)
- **Set-params (proposed values):**
  - `sc-15_odp` (exceptions where remote activation is allowed): `["not-applicable — no collaborative computing devices or applications within the MSS authorization boundary"]`, `organization`
- **Authoring notes:** Straightforward N/A. One or two sentences. Cite the in-boundary asset table as evidence no such devices are in scope. FedRAMP Low does not mandate a particular value for the exceptions ODP — organization-defined.

---

## SC-20 Secure Name/Address Resolution Service (Authoritative Source)

- **Status:** not-applicable
- **Primary mechanism:** The MSS does not operate an authoritative DNS server. Internal name resolution is handled by OPNsense Unbound (a caching/recursive resolver, not an authoritative source). The system does not serve authoritative DNS responses to external clients or operate as part of a distributed hierarchical namespace.
- **Supporting mechanisms:** External DNS for public-facing services (brianchaplow.com, bytesbourbonbbq.com) is delegated to Cloudflare — those are out-of-boundary assets. No DNSSEC signing is performed by any in-boundary component.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Network Quick Reference (OPNsense at 10.10.10.1 — firewall/gateway role, no authoritative DNS noted)
  - `C:/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.3 (GCP VM + public DNS out of boundary)
- **Set-params (proposed values):** (SC-20 has no ODPs in the FedRAMP Rev 5 Low profile)
- **Authoring notes:** N/A — no authoritative DNS in boundary. One sentence is sufficient: the MSS relies on OPNsense Unbound as a caching resolver and does not serve authoritative DNS responses. Distinguish from SC-21 (recursive/caching resolver, which is slightly more relevant).

---

## SC-21 Secure Name/Address Resolution Service (Recursive or Caching Resolver)

- **Status:** partial
- **Primary mechanism:** OPNsense Unbound (running on the Protectli VP2420 at 10.10.10.1) provides recursive DNS resolution for all in-boundary hosts across VLANs 10, 20, 30, and 40. Unbound forwards queries to upstream resolvers and caches responses for in-boundary clients.
- **Supporting mechanisms:** DNSSEC validation is not confirmed as enabled in the Unbound configuration — this is a gap. Without DNSSEC validation, data origin authentication and integrity verification for DNS responses are not performed. Linux hosts use OPNsense as their primary DNS resolver (DHCP-assigned). No independent DNSSEC-validating stub resolver is deployed on individual hosts.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Network Quick Reference (OPNsense at 10.10.10.1, DHCP/DNS for all VLANs implied by GW .1 architecture)
  - `C:/Projects/reference/network.md` §OPNsense Interface Map (OPNsense handles all VLAN routing and DNS)
- **Set-params (proposed values):** (SC-21 has no ODPs in the FedRAMP Rev 5 Low profile)
- **Authoring notes:** Partial — Unbound is deployed but DNSSEC validation status is unconfirmed/likely disabled (common default for homelab Unbound). Paragraph 2 should name the DNSSEC gap explicitly. This is an honest partial: recursive resolution exists, cryptographic validation does not. A planned fix would be enabling `harden-dnssec-stripped: yes` and `val-permissive-mode: no` in Unbound.

---

## SC-22 Architecture and Provisioning for Name/Address Resolution Service

- **Status:** partial
- **Primary mechanism:** OPNsense Unbound on the Protectli VP2420 (10.10.10.1) is the sole in-boundary DNS resolver. It serves all VLANs (10/20/30/40/50) as both the internal caching resolver and the forwarder to upstream resolvers. Internal hosts use OPNsense as primary DNS via DHCP assignment.
- **Supporting mechanisms:** There is no secondary DNS resolver providing fault-tolerance or role separation — single point of failure. If OPNsense is unavailable, in-boundary hosts lose DNS resolution. External authoritative DNS (Cloudflare for public zones) is out-of-boundary and unaffected. The MSS is a single-operator homelab, so the FedRAMP intent of geographic and role separation is not achievable at this scale.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Network Quick Reference (OPNsense at 10.10.10.1, single gateway per VLAN)
  - `C:/Projects/reference/network.md` §OPNsense Interface Map (single appliance handling all VLAN DNS/routing)
- **Set-params (proposed values):** (SC-22 has no ODPs in the FedRAMP Rev 5 Low profile)
- **Authoring notes:** Partial — single DNS resolver, no fault tolerance, no role separation. Honest gap. Paragraph 2: state that the MSS is a single-operator personal lab and a fully redundant DNS architecture is not implemented; OPNsense failure would require SSH-direct-IP to continue operations.

---

## SC-28 Protection of Information at Rest

- **Status:** partial
- **Primary mechanism:** Information at rest protection relies on OS-level access controls and filesystem permissions across all in-boundary hosts. Wazuh configuration and indexer data on brisket are protected by Linux DAC (root-owned `/var/ossec/`). ELK indices on haccp are protected by filesystem permissions on `/opt/elk/` Docker volumes. PBS backup snapshots on smoker LXC 300 are stored on the smokehouse NFS share at `10.10.20.10:/mnt/pbs-store/` with NFS-level access controls.
- **Supporting mechanisms:** There is no full-disk encryption (FDE) on any in-boundary host — all boot drives are unencrypted. This is a deliberate homelab trade-off (physical security of a home rack is the compensating factor). PBS backup data is not encrypted at rest (Proxmox Backup Server CE does not enforce encryption by default for the homelab configuration). Sensitive credentials are stored in `.env` files with filesystem permissions (not a secrets manager).
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §Service Inventory (brisket data locations, haccp /opt/elk/ Docker volumes)
  - `C:/Projects/CLAUDE.md` §haccp host entry (WD SN720 boot drive, Samsung 990 EVO PCAP — no FDE noted)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (PBS NFS path `/mnt/pbs-store/data/vm/`, backup storage state)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0002-deployment-complete.md` (PBS verification: `ls /mnt/pbs-store/data/vm/`)
- **Set-params (proposed values):**
  - `sc-28_odp.01` (selection — confidentiality and/or integrity): `["confidentiality", "integrity"]`, `organization`
  - `sc-28_odp.02` (information at rest): `["Wazuh SIEM configuration and alert indices on brisket", "ELK log indices and Arkime PCAP on haccp", "PBS backup snapshots on smokehouse NFS", "OpenCTI threat intelligence database on brisket Docker volumes", "DefectDojo and RegScale application data on dojo and regscale VMs"]`, `organization`
- **Authoring notes:** Partial — no FDE, no encrypted backups. Be explicit about the gap. The compensating rationale (physical home rack, no untrusted colocated users) should be stated clearly in paragraph 2. Reference ADR 0005 as evidence that backup data integrity is monitored (the gap was caught and fixed).

---

## SC-28(1) Cryptographic Protection (At Rest)

- **Status:** planned
- **Primary mechanism:** Cryptographic protection of information at rest is not currently implemented for the MSS boundary. No full-disk encryption (FDE) is applied to any in-boundary host's boot or data drives. PBS backup snapshots on smokehouse NFS are stored without encryption. Docker volumes holding Wazuh, ELK, and OpenCTI data are filesystem-protected but not cryptographically encrypted.
- **Supporting mechanisms:** The upgrade path for this control would be: (1) enable PBS datastore encryption for backup jobs (Proxmox Backup Server supports encryption at the datastore level); (2) deploy LUKS full-disk encryption on haccp's PCAP drive (`/dev/nvme0n1` Samsung 990 EVO Plus) given its 2TB of sensitive PCAP data; (3) evaluate Wazuh indexer index-level encryption. These are deferred to a future hardening phase. `runbooks/cert-trust.md` notes the TLS upgrade path but does not cover at-rest encryption.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §haccp host entry (nvme0n1 PCAP drive at /opt/arkime/raw — no encryption noted)
  - `C:/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (PBS NFS mount state — no mention of datastore encryption)
  - `C:/Projects/homelab-fedramp-low/runbooks/cert-trust.md` (TLS scope only — at-rest encryption not covered)
- **Set-params (proposed values):**
  - `sc-28.01_odp.01` (system components or media): `["haccp nvme0n1 PCAP storage drive", "brisket Docker volumes (Wazuh indexer, OpenCTI)", "smokehouse PBS datastore"]`, `organization`
  - `sc-28.01_odp.02` (information): `["full-PCAP archives at /opt/arkime/raw", "Wazuh alert indices", "OpenCTI threat intelligence data", "PBS backup snapshots"]`, `organization`
- **Authoring notes:** Planned — honest status. No cryptographic at-rest protection exists today. Paragraph 1 states the gap. Paragraph 2 describes the specific upgrade path (PBS datastore encryption, LUKS on nvme0n1, future hardening phase). Do not claim the physical rack as a compensating control here — that may satisfy SC-28 partially but does not satisfy SC-28(1)'s specific cryptographic mechanism requirement.

---

## SC-39 Process Isolation

- **Status:** implemented
- **Primary mechanism:** All in-boundary Linux hosts (brisket, haccp, smokehouse, sear, dojo, regscale) run Ubuntu 22.04/24.04 LTS kernels with standard Linux process isolation: each process operates in a separate address space via virtual memory management, enforced by the kernel's MMU. Docker containers on brisket (Wazuh, Shuffle, OpenCTI, Prometheus/Grafana) and haccp (ELK stack) run in separate Linux namespaces (PID, network, mount, UTS, IPC) providing process and filesystem isolation between service stacks.
- **Supporting mechanisms:** Proxmox LXC containers on pitcrew (TheHive LXC 200) and smoker (PBS LXC 300) use kernel namespaces and cgroups for process isolation between containers and the hypervisor. The tenant workloads on brisket (AlgoTrader, Capitol Signals — out-of-boundary) are in separate Docker network namespaces from the MSS services. Velociraptor DFIR server on brisket and the ML scorer (port 5002) each run in isolated Docker containers.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` §brisket Service Inventory (Docker-containerized services: Wazuh, Shuffle, OpenCTI, Prometheus, Grafana, Velociraptor, ML Scorer, Capitol Signals — all separate containers)
  - `C:/Projects/CLAUDE.md` §haccp host entry (ELK stack in Docker at /opt/elk/docker-compose.yml)
  - `C:/Projects/CLAUDE.md` v3 Migration Status §Phase 14 (Logstash zeek-enrichment pipeline — separate Docker stack)
  - `C:/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.5 (shared-tenancy handling: separate Docker network namespaces noted as compensating control)
- **Set-params (proposed values):** (SC-39 has no ODPs in the FedRAMP Rev 5 Low profile)
- **Authoring notes:** Implemented. Lead with kernel-level virtual memory for all Linux processes. Second paragraph on Docker namespaces as the primary container isolation mechanism, with the shared-brisket-tenancy situation (OR-0001 from §2.5 of the whole-project design) cited as evidence that namespace isolation is the documented compensating mechanism. SC-39 is a clean story for this homelab.

---

*Report: family=SC, controls_cataloged=14, grep_verifications_performed=14, cites_to_parent_claude_md=14, cites_to_adrs=7 (0001, 0002, 0003, 0004, 0005, 0007, 0008), unresolved_questions=["SC-21: DNSSEC validation status in OPNsense Unbound requires SSH verification to confirm — cited as gap rather than confirmed state", "SC-22: No secondary DNS confirmed — consistent with single-appliance architecture but operator should verify OPNsense Unbound config", "SC-28(1): PBS datastore encryption status should be verified via `pct exec 300 -- proxmox-backup-client` before authoring the planned paragraph"]*
