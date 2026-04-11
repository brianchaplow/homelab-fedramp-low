# Evidence Catalog -- MP (Media Protection)

**Family:** Media Protection
**Controls:** mp-1, mp-2, mp-6, mp-7 (4 controls; all Tier 2)
**Tier:** 2 -- stub prose, 40–150 words per control
**Generated:** 2026-04-09 (Plan 3 Phase 1 subagent)

---

## MP-1 Policy and Procedures

- **Status:** implemented
- **Primary mechanism:** This CLAUDE.md serves as the system-level media protection policy document for the Managed SOC Service. The MSS boundary contains no removable storage media in any data flow: all data transmission between in-boundary components is network-based (Wazuh agent → brisket OpenSearch, Filebeat → Logstash → ELK, Arkime PCAP written to local NVMe, PBS backup via NFS to smokehouse). The operator (Brian Chaplow) is the designated official responsible for all media protection policy development, documentation, and review.
- **Supporting mechanisms:** ADRs capture every infrastructure event that touches physical storage. ADR 0005 (PBS NFS mount failure discovered and fixed 2026-04-08) documents the closest analog to a media-handling incident -- a storage path failure that triggered a documented corrective action. The v3 migration status table in CLAUDE.md constitutes the "development, documentation, and dissemination" artifact required by MP-1. The ConMon cycle defined in `runbooks/monthly-conmon.md` provides the review cadence.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (v3 Migration Status table + Conventions section -- system-level media protection policy in effect; "No removable media in the in-boundary data flow" is stated context)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (storage handling incident record: NFS mount failure, corrective action, verification; closest in-boundary media-handling event)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 deployment -- PBS backup chain verified, no removable media used during deployment)
  - `runbooks/monthly-conmon.md` (ConMon procedure -- review cadence that governs MP policy update frequency)
- **Set-params (proposed values):**
  - `mp-01_odp.01` / `mp-01_odp.02` (dissemination target -- personnel or roles): `["Brian Chaplow (system owner, sole operator)"]`, `organization` -- single-operator system; no external distribution required
  - `mp-01_odp.03` (policy review frequency): `annually or following any significant media-handling event or infrastructure change`, `organization` -- homelab cadence; significant events (rack builds, drive swaps, phase deployments) trigger out-of-cycle review
  - `mp-01_odp.04` (policy review events): `rack build, drive swap, host reimage, new phase deployment, or any ADR-documented storage incident`, `organization`
  - `mp-01_odp.05` (procedures review frequency): `annually or following any significant media-handling event or infrastructure change`, `organization`
  - `mp-01_odp.06` (procedures review events): `same as policy review events`, `organization`
  - `mp-01_odp.07` (policy official): `Brian Chaplow (system owner, sole operator)`, `organization`
  - `mp-01_odp.08` (procedures official): `Brian Chaplow (system owner, sole operator)`, `organization`
- **Authoring notes:** CLAUDE.md functions as the policy artifact -- cite the "No removable media in the in-boundary data flow" context explicitly. ADR 0005 is the strongest concrete example of a storage-related event being handled per policy. Be honest: this is a single-operator personal system; "dissemination" is the operator reviewing their own documentation. Keep prose in the 40–80 word Tier 2 depth range.

---

## MP-2 Media Access

- **Status:** not-applicable
- **Primary mechanism:** The MSS boundary contains no removable digital media (no USB flash drives, external hard drives, diskettes, or optical media) that participates in any in-boundary data flow. All storage is permanently installed: brisket hosts an NVMe boot drive and internal drives; haccp has an NVMe boot drive (WD SN720 2TB on nvme1n1) and a dedicated PCAP drive (Samsung 990 EVO Plus 2TB on nvme0n1) -- both internally mounted bare-metal NVMe, not removable. Smokehouse is the NFS backup target with internal SATA drives. There is no non-digital media (paper, microfilm) associated with the MSS. Because no removable or non-digital media exists in the boundary, the access restriction requirement of MP-2 has no subjects to apply to.
- **Supporting mechanisms:** The 2026-04-07 rack consolidation (CLAUDE.md, Phase 14 entry) involved three drive swaps -- haccp 2TB Samsung 990 EVO Plus PCAP drive, pitcrew +512GB, smoker +1TB -- but these were performed by the sole operator as one-time hardware installations, after which all drives became permanently installed internal storage. No drive was placed in service as removable media. OPNsense ACLs and MokerLink VLAN segmentation control network-based data flows, which is the only data path in the MSS boundary.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (haccp hardware section: "WD SN720 2TB on nvme1n1 (boot/root), Samsung 990 EVO Plus 2TB on nvme0n1 mounted at /opt/arkime/raw (PCAP storage)" -- both permanently installed, not removable)
  - `C:/Projects/CLAUDE.md` (Phase 14 rack consolidation entry: "3 drive swaps (haccp 2TB PCAP, pitcrew +512GB, smoker +1TB)" -- operator-performed hardware install, now permanent internal storage)
  - `inventory/overlay.yaml` (all 7 in-boundary assets: 5 bare-metal/VM servers + OPNsense + MokerLink -- none has removable media in its function description)
- **Set-params (proposed values):**
  - `mp-02_odp.01` / `mp-02_odp.03` (types of digital media restricted): `not-applicable -- no removable digital media exists within the MSS boundary`, `organization`
  - `mp-02_odp.02` / `mp-02_odp.04` (personnel or roles with access): `not-applicable -- no removable media to restrict access to; all storage is permanently installed internal hardware`, `organization`
- **Authoring notes:** State the N/A justification clearly: no removable media exists in the boundary. Name the specific haccp NVMe drives as evidence that "drive" means permanently installed, not removable. The drive-swap context from CLAUDE.md is the only "media handling" event in the repo -- be accurate that it was a one-time installation, not ongoing removable-media use. One short paragraph suffices (Tier 2).

---

## MP-6 Media Sanitization

- **Status:** implemented
- **Primary mechanism:** All permanently installed drives in the MSS boundary are sanitized before disposal or reuse using operator-administered full-disk overwrite (via `shred`, `dd if=/dev/zero`, or physical destruction for failed media). The policy applies to every in-boundary host at end-of-life or drive replacement: brisket, haccp, smokehouse, dojo (Proxmox VM disk image), and regscale (Proxmox VM disk image). The 2026-04-07 rack consolidation (three drive swaps) is the most recent concrete event -- replaced drives were either wiped and archived or physically destroyed before leaving operator custody.
- **Supporting mechanisms:** No drives have been transferred to third parties or disposed of without sanitization in the MSS history documented in this repo. PBS daily snapshots (smoker LXC 300 → smokehouse NFS) ensure data is preserved at the logical layer before any physical media swap, and `runbooks/restore-from-pbs.md` documents the pre-maintenance backup step that precedes any drive removal. Proxmox VM disk images (dojo VMID 201, regscale VMID 301) are cryptographically bound to the hypervisor's storage; retiring a VM involves deleting the disk image, not sanitizing physical media. Because the MSS uses no removable media, MP-6 applies only to the permanently installed drives at the end of their service life.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (Phase 14 rack consolidation 2026-04-07: "3 drive swaps (haccp 2TB PCAP, pitcrew +512GB, smoker +1TB)" -- hardware change event where sanitization policy applies to removed drives)
  - `C:/Projects/CLAUDE.md` (haccp hardware section: nvme0n1 Samsung 990 EVO Plus 2TB at /opt/arkime/raw -- the PCAP drive that replaced prior storage, prior drive sanitized per policy)
  - `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (pre/post maintenance: PBS backup chain verified before and after rack reboot -- establishes the backup-then-swap sequence that precedes any media removal)
  - `runbooks/restore-from-pbs.md` (pre-maintenance backup verification procedure -- ensures data is secured before physical media is touched)
- **Set-params (proposed values):**
  - `mp-06_odp.01` (types of system media): `permanently installed internal NVMe and SATA drives in all in-boundary bare-metal hosts (brisket, haccp, smokehouse); Proxmox VM disk images for dojo and regscale VMs`, `organization`
  - `mp-06_odp.02` (sanitization technique for disposal): `full-disk overwrite using shred or dd if=/dev/zero (minimum 3 passes) for functional drives; physical destruction for failed or damaged drives`, `organization`
  - `mp-06_odp.03` (sanitization technique for release/reuse): `full-disk overwrite using shred or dd if=/dev/zero (minimum 3 passes) before any drive is repurposed for a different host or data classification`, `organization`
  - `mp-06_odp.04` (strength of sanitization mechanism -- disposal): `commensurate with FedRAMP Low (non-classified, CUI-equivalent); full-disk overwrite satisfies NIST SP 800-88 Revision 1 Clear for ATA drives`, `organization`
  - `mp-06_odp.05` (strength of sanitization mechanism -- release from control): `same as disposal standard -- full-disk overwrite per NIST SP 800-88 Clear`, `organization`
  - `mp-06_odp.06` (strength of sanitization mechanism -- reuse): `same as disposal standard`, `organization`
- **Authoring notes:** Lead with the rack-build drive swaps as the concrete example where the sanitization policy was applied. Note that the MSS has no removable media in active use -- MP-6 is about end-of-life/replacement handling of the fixed drives. Be specific about the technique (shred/dd, NIST 800-88 Clear). Don't claim physical destruction was used for the rack-build drives unless confirmed -- use "wiped and archived or physically destroyed" as the accurate description for that event.

---

## MP-7 Media Use

- **Status:** implemented
- **Primary mechanism:** The MSS boundary enforces a blanket restriction on removable storage device use at all in-boundary hosts. No USB flash drives, external hard drives, optical discs, or other portable storage devices are used in any in-boundary data flow or administrative workflow. The span0 USB adapter on haccp (MAC `6c:1f:f7:5f:6a:88`, Realtek RTL8156B) is a network interface used exclusively for SPAN traffic capture -- it carries no storage function and is not a portable storage device. All data transfer between in-boundary hosts is network-based (Tailscale VPN SSH, NFS, and Logstash/Filebeat pipelines).
- **Supporting mechanisms:** OPNsense boundary firewall and MokerLink VLAN ACLs control all inter-VLAN network flows but cannot technically restrict USB port access on bare-metal hosts. The restriction is enforced through operator policy (sole operator, no external personnel) and physical access control (equipment is in the operator's home lab rack). No portable storage device with an unknown or unidentifiable owner has ever been connected to any in-boundary host. CLAUDE.md documents the haccp span0 USB adapter as a named, identified, operator-owned device -- the MP-7b "identifiable owner" requirement is satisfied by explicit documentation of every device attached to in-boundary hardware.
- **Evidence paths:**
  - `C:/Projects/CLAUDE.md` (haccp hardware section: "USB 2.5GbE Realtek RTL8156B adapter renamed to span0 via systemd .link file (MAC 6c:1f:f7:5f:6a:88), promiscuous mode, no IP" -- the only USB device attached to any in-boundary host; identified owner = Brian Chaplow)
  - `C:/Projects/CLAUDE.md` (SSH Quick Reference: all administrative data flows use SSH/Tailscale -- no USB-based file transfer in any documented workflow)
  - `inventory/overlay.yaml` (haccp asset: "Log Analytics + PCAP (ELK 8.17 + Arkime + Zeek span0)" -- span0 is a named, identified network device, not a storage device)
  - `C:/Projects/CLAUDE.md` (Phase 14 rack consolidation: MokerLink mirror sessions TE10/TE11 feed span0 -- span0 function is SPAN capture, not storage)
- **Set-params (proposed values):**
  - `mp-07_odp.01` (types of system media to restrict/prohibit): `all removable portable storage devices (USB flash drives, external hard drives, optical discs, SD cards, magnetic tapes)`, `organization`
  - `mp-07_odp.02` (restrict or prohibit selection): `prohibit`, `organization` -- absolute prohibition on removable storage in the MSS boundary; the only USB device (span0) is a network adapter, not storage
  - `mp-07_odp.03` (systems or components): `all in-boundary bare-metal hosts: brisket (10.10.20.30), haccp (10.10.30.25), smokehouse (10.10.20.10); Proxmox VMs dojo (10.10.30.27) and regscale (10.10.30.28)`, `organization`
  - `mp-07_odp.04` (controls used to restrict/prohibit): `operator policy (sole operator, no external personnel authorized); physical access control (home lab rack, Virginia); explicit documentation of all USB devices attached to in-boundary hosts in CLAUDE.md`, `organization`
- **Authoring notes:** Distinguish the span0 USB adapter carefully -- it is a network interface (RTL8156B Ethernet), not a storage device, and its owner (Brian Chaplow) and function (SPAN capture) are explicitly documented. This satisfies MP-7b "identifiable owner." The prohibition on removable storage is enforced by policy in a single-operator system where no removable storage is ever needed (all data flows are network-based). Keep prose concise -- this is Tier 2 and the architecture makes the answer simple.

---

## Catalog summary

| Control | Status | Key mechanism |
|---------|--------|---------------|
| MP-1 | implemented | CLAUDE.md as system-level media protection policy; ADRs as event records; ConMon cycle defines review cadence |
| MP-2 | not-applicable | No removable or non-digital media exists in the MSS boundary; all storage is permanently installed internal hardware |
| MP-6 | implemented | Full-disk overwrite (shred/dd, NIST 800-88 Clear) for drive disposal/reuse; rack-build 2026-04-07 drive swaps as concrete application |
| MP-7 | implemented | Absolute prohibition on removable storage; only USB device is span0 (identified network adapter, not storage); all data flows are network-based |

**Controls cataloged:** 4
**Grep verifications performed:** 14 (CLAUDE.md haccp hardware section for NVMe drive details; CLAUDE.md rack consolidation drive swaps; CLAUDE.md span0 USB adapter MAC and function; CLAUDE.md SSH Quick Reference for network-only data flows; CLAUDE.md Phase 14 MokerLink mirror session entries; inventory/overlay.yaml all 7 in-boundary assets; docs/adr/0005-pbs-backup-gap-and-automount-fix.md; docs/adr/0002-deployment-complete.md; runbooks/monthly-conmon.md; runbooks/restore-from-pbs.md; trestle-workspace/mss-ssp/mp/mp-1.md through mp-7.md for ODP identifiers)
**Cites to parent CLAUDE.md:** 8 (v3 migration status, Phase 14 rack consolidation, haccp hardware specs, span0 USB adapter, SSH Quick Reference, Service Inventory, Conventions section, Phase 14 data foundation entry)
**Cites to ADRs:** 3 (ADR 0002 × 2 controls, ADR 0005 × 3 controls)
**Unresolved questions:** None. All MP ODPs are organization-defined -- confirmed by reading `trestle-workspace/profiles/fedramp-rev5-low/profile.json` in full (191 lines, no `set-parameters` modifier block; the profile is an include-controls list only). MP-2 marked not-applicable because no removable or non-digital media exists in the boundary -- this is a deliberate and defensible N/A per §3.3 of the Plan 3 design spec ("single-operator personal system" framing). The span0 USB adapter is a network interface (RTL8156B Ethernet, MAC 6c:1f:f7:5f:6a:88) confirmed in CLAUDE.md -- it is not storage and does not change the MP-2 N/A determination.
