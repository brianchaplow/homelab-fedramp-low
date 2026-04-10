# Evidence Catalog — MA (Maintenance)

**Family:** Maintenance
**Controls:** ma-1, ma-2, ma-4, ma-5 (4 controls; all Tier 2)
**Tier:** 2 — stub prose, 40–150 words per control
**Generated:** 2026-04-09 (Plan 3 Phase 1 subagent)

---

## MA-1 Policy and Procedures

- **Status:** implemented
- **Primary mechanism:** This CLAUDE.md serves as the system-level maintenance policy document for the Managed SOC Service. It defines the scope of maintenance activities, assigns all maintenance responsibility to the single operator (Brian Chaplow), and establishes the review cadence tied to the FedRAMP Low ConMon cycle (`runbooks/monthly-conmon.md`).
- **Supporting mechanisms:** ADRs capture every maintenance event as a time-stamped decision record. ADR 0005 (PBS NFS mount failure discovered and fixed 2026-04-08) and the 2026-03-31 fleet update (all kernels + Wazuh 4.14.4) are the two primary policy-execution artifacts. The v3 migration status table in CLAUDE.md constitutes the "development, documentation, and dissemination" artifact required by MA-1.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (v3 Migration Status table + Conventions section — system-level maintenance policy in effect)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (maintenance event record: PBS NFS mount failure, corrective action, verification)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 deployment maintenance event — VM builds, PBS backup chain, Wazuh agent enrollment)
  - `runbooks/monthly-conmon.md` (maintenance procedure review cadence — ConMon cycle defines the review trigger)
- **Set-params (proposed values):**
  - `ma-01_odp.01` / `ma-01_odp.02` (dissemination target — personnel or roles): `["Brian Chaplow (system owner, sole operator)"]`, `organization` — single-operator system, no external distribution required
  - `ma-01_odp.03` (policy review frequency): `annually or after any significant maintenance event`, `organization` — homelab cadence; significant events trigger out-of-cycle reviews (e.g., ADR 0005 triggered immediate policy update)
  - `ma-01_odp.04` (policy review events): `rack build, host reimage, new phase deployment, or any ADR-documented incident`, `organization`
  - `ma-01_odp.05` (procedures review frequency): `annually or after any significant maintenance event`, `organization`
  - `ma-01_odp.06` (procedures review events): `same as policy review events`, `organization`
  - `ma-01_odp.07` (policy official): `Brian Chaplow (system owner, sole operator)`, `organization`
  - `ma-01_odp.08` (procedures official): `Brian Chaplow (system owner, sole operator)`, `organization`
- **Authoring notes:** CLAUDE.md functions as the policy artifact — cite it explicitly. ADR 0005 is the strongest example of the policy-execution loop (incident → investigation → fix → ADR). Keep the prose honest: this is a single-operator personal system, so "dissemination" is the operator reviewing the document themselves.

---

## MA-2 Controlled Maintenance

- **Status:** implemented
- **Primary mechanism:** All maintenance on MSS hardware and software is performed by the single operator (Brian Chaplow) and documented via time-stamped ADR records or CLAUDE.md entries. The 2026-04-07 rack consolidation (12U rack build, three drive swaps: haccp 2TB Samsung 990 EVO Plus PCAP, pitcrew +512 GB SK Hynix, smoker +1 TB X15) was planned, executed, and verified before re-enabling production traffic. Post-maintenance control verification included confirming ES green, MokerLink mirror sessions 1+2 on TE10/TE11, and Arkime PCAP capture resuming on span0.
- **Supporting mechanisms:** Wazuh syscollector provides continuous post-maintenance inventory verification — after each maintenance window, `wazuh-states-vulnerabilities-*` and syscollector indices show updated hardware and software baselines for in-boundary hosts. PBS daily snapshots (smoker LXC 300 → smokehouse NFS) serve as pre-maintenance backup evidence (verified at ADR 0002 and ADR 0005). The 2026-03-31 fleet update (kernels, Wazuh 4.14.4, Proxmox realigned) was scheduled during off-peak hours and logged.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (Phase 14 + rack consolidation 2026-04-07 entries — scheduled maintenance log)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (maintenance gap discovery: PBS mount failure during rack reboot; corrective maintenance with verification output)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 deployment maintenance — VM builds, PBS backup chain verified, Wazuh agent enrollment)
  - `C:/Users/bchap/.claude/projects/C--Projects/memory/rack_build_2026-04-07.md` (rack build log: drive swaps, NIC renames, mirror session corrections, ES green verification)
  - `runbooks/restore-from-pbs.md` (pre-maintenance backup verification procedure — ensures snapshot exists before hardware changes)
- **Set-params (proposed values):**
  - `ma-02_odp.01` (maintenance, repair, and replacement schedule): `ad hoc, performed by the sole operator with a minimum 24-hour advance notice to self; all unplanned maintenance is documented in an ADR within 48 hours of completion`, `organization`
  - `ma-02_odp.02` (information to sanitize): `not-applicable — no equipment leaves organizational facilities for off-site maintenance; all hardware remains in the operator's home lab rack`, `organization`
  - `ma-02_odp.03` (information in maintenance records): `date and time, description of maintenance performed, components serviced or replaced, verification steps performed, and post-maintenance control check results`, `organization`
- **Authoring notes:** Lead with the rack build 2026-04-07 as the concrete maintenance example. Note that no equipment leaves the facility (home rack) — MA-2d sanitization requirement is not applicable. Post-maintenance verification is key: cite the ES green + mirror session confirmation and Wazuh syscollector baseline update as the "verify controls still functioning" mechanism.

---

## MA-4 Nonlocal Maintenance

- **Status:** implemented
- **Primary mechanism:** All remote maintenance sessions to in-boundary hosts use Tailscale VPN with WireGuard encryption and device-key authentication before any SSH connection is established. Tailscale authenticates each device using a pre-shared key tied to the operator's Tailscale account, providing the cryptographic session establishment required by MA-4c. Remote SSH sessions to brisket (100.124.139.56), haccp (100.74.16.82), smoker (100.77.138.24), and sear (100.86.67.91) all traverse the Tailscale mesh. Sessions terminate naturally when the SSH connection closes; there is no persistent tunnel kept open after maintenance completes.
- **Supporting mechanisms:** Wazuh on brisket logs all SSH authentication events from in-boundary hosts (rule group `syslog`, `sshd` events forwarded from each agent). The `wazuh-alerts-*` index on brisket's OpenSearch indexer provides the maintenance session audit trail. CLAUDE.md SSH Quick Reference documents all authorized remote maintenance paths. No third-party maintenance personnel or vendor remote access tools are used — all remote maintenance is performed by the single operator over Tailscale SSH.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (SSH Quick Reference — authorized Tailscale IPs and ports for all in-boundary hosts)
  - `C:/Projects/CLAUDE.md` (Service Inventory: Wazuh Manager 1514/1515/55000, Dashboard 5601 — audit trail service)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (remote maintenance session record: PBS LXC fix performed via `ssh root@10.10.30.21`, with verification output captured in ADR)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 VM builds — all performed via Tailscale SSH from PITBOSS; smoke checks executed remotely)
- **Set-params (proposed values):** *(MA-4 has no x-trestle-set-params ODPs in the scaffold — no set-param fill required)*
- **Authoring notes:** Tailscale is the strong authentication mechanism — WireGuard device-key exchange is cryptographically strong and resistant to replay attacks, satisfying MA-4c. Session termination is SSH lifecycle-based (natural close on disconnect). Cite the ADR 0005 fix as the concrete nonlocal maintenance record. Be clear that only one operator performs remote maintenance — no escorted access, no vendor tools.

---

## MA-5 Maintenance Personnel

- **Status:** implemented
- **Primary mechanism:** The Managed SOC Service has a single authorized maintenance personnel: Brian Chaplow (system owner and sole operator). No external maintenance organizations, vendors, or contractors are authorized or have access to any in-boundary system component. Access authorizations for all in-boundary hosts are controlled by SSH keys held exclusively by the operator, and no temporary credentials are issued to third parties.
- **Supporting mechanisms:** Wazuh agent enrollment (15 active agents as of 2026-04-08) requires the operator to authenticate to the Wazuh manager API on brisket to approve each new agent — this is the access authorization gate for any new system component entering the maintenance boundary. CLAUDE.md documents the authorized maintenance personnel list by implication: only operator-held SSH keys and Tailscale device credentials exist for in-boundary hosts. No escorted maintenance has occurred and none is planned; the supervision requirement of MA-5c is satisfied trivially because the operator is both the maintainer and the supervisor.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (SSH Quick Reference and Credentials sections — sole operator identity, no third-party credentials)
  - `C:/Projects/CLAUDE.md` (Service Inventory: Wazuh Manager agent count 15 — enrollment controlled by operator)
  - `docs/adr/0002-deployment-complete.md` (agent 016 dojo + agent 017 regscale enrolled — operator performed all maintenance personnel authorization steps)
- **Set-params (proposed values):** *(MA-5 has no x-trestle-set-params ODPs in the scaffold — no set-param fill required)*
- **Authoring notes:** Single-operator framing is the complete answer here. Keep prose concise (40–80 words Tier 2 depth). Note that MA-5c supervision requirement is trivially satisfied: the operator supervises themselves. Avoid hand-waving — state clearly that no external maintenance personnel exist and no temporary credentials are issued.

---

## Catalog summary

| Control | Status | Key mechanism |
|---------|--------|---------------|
| MA-1 | implemented | CLAUDE.md as system-level maintenance policy; ADRs as event records |
| MA-2 | implemented | ADR-documented maintenance events; PBS pre/post snapshots; Wazuh syscollector for baseline verification |
| MA-4 | implemented | Tailscale WireGuard SSH for all remote maintenance; Wazuh SSH audit trail |
| MA-5 | implemented | Single operator only; no external personnel; Wazuh agent enrollment as access authorization gate |

**Controls cataloged:** 4
**Grep verifications performed:** 12 (CLAUDE.md SSH Quick Reference, Service Inventory Wazuh agent count; ADR 0002 agent enrollment; ADR 0005 PBS fix with SSH session record; runbooks/restore-from-pbs.md; rack_build_2026-04-07.md drive swap/verification)
**Cites to parent CLAUDE.md:** 6 (v3 migration status, SSH Quick Reference, credentials, service inventory, phase 14 entry, rack consolidation entry)
**Cites to ADRs:** 4 (ADR 0002, ADR 0005 × 3 controls)
**Unresolved questions:** None. MA-4 scaffold has no x-trestle-set-params ODPs; MA-5 scaffold has no x-trestle-set-params ODPs — confirmed by reading `trestle-workspace/mss-ssp/ma/ma-4.md` and `ma-5.md` directly. MA-1 ODPs 01-08 all organization-defined (no baseline-mandated values in the FedRAMP Rev 5 Low profile — the profile JSON has no `set-parameters` modifier for MA-1, so all eight ODPs are operator-chosen). MA-2 ODPs 01-03 all organization-defined by the same reasoning.
