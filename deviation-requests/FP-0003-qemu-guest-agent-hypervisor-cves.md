# Deviation Request FP-0003 -- qemu-guest-agent: hypervisor-side CVEs against guest-only binary

## DR metadata

- **DR ID:** FP-0003
- **Category:** False Positive
- **Submitted:** 2026-05-04
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Linked POA&M item(s)

This DR covers all current Wazuh findings against the `qemu-guest-agent` package on the in-boundary VMs (dojo and regscale). 24 items total at this cycle:

| Package | Items | Hosts | CVEs |
|---|---:|---|---|
| `qemu-guest-agent` | 24 | dojo (12), regscale (12) | CVE-2019-12067, CVE-2020-13791, CVE-2020-24352, CVE-2020-25741, CVE-2020-25742, CVE-2020-25743, CVE-2020-35503, CVE-2021-20255, CVE-2021-3735, CVE-2022-3872, CVE-2023-1386, CVE-2024-8612 |

## Finding summary

The Wazuh vulnerability detector flags `qemu-guest-agent` as vulnerable because Canonical's `qemu` source package version `1:8.2.2+ds-0ubuntu1.16` is listed in NVD as containing each of the 12 CVEs above. The CPE match is correct at the source-package level: the source package `qemu` is genuinely affected.

What the CPE match cannot distinguish is **which binary inside the source package contains the vulnerable code**. A single `qemu` source package produces ~20 different binary packages including:

- `qemu-system-x86_64` -- the actual hypervisor binary, runs hardware device emulation
- `qemu-system-arm`, `qemu-system-aarch64`, etc. -- additional architectures
- `qemu-utils` -- qemu-img, qemu-nbd, qemu-storage-daemon utilities
- `qemu-block-extra` -- additional block-driver plugins
- **`qemu-guest-agent`** -- the `qemu-ga` daemon that runs *inside* a guest VM and exposes a virtio-serial channel for host-to-guest communication (clipboard sync, fsfreeze for backup, time sync, etc.)

Every CVE listed above describes a vulnerability in one of the hypervisor's *device emulation* paths:

| CVE | Vulnerable subsystem | Source file path |
|---|---|---|
| CVE-2019-12067 | AHCI/SATA controller emulation | `hw/ide/ahci.c` |
| CVE-2020-13791 | PCI configuration space | `hw/pci/pci.c` |
| CVE-2020-24352 | ATI VGA device | `hw/display/ati_2d.c` |
| CVE-2020-25741 | Floppy disk controller | `hw/block/fdc.c` |
| CVE-2020-25742 | PCI IRQ handling | `hw/pci/pci.c` |
| CVE-2020-25743 | IDE PCI controller | `hw/ide/pci.c` |
| CVE-2020-35503 | megasas SCSI HBA emulator | `hw/scsi/megasas.c` |
| CVE-2021-20255 | eepro100 NIC emulator | `hw/net/eepro100.c` |
| CVE-2021-3735 | AHCI controller (port reset) | `hw/ide/ahci.c` |
| CVE-2022-3872 | SDHCI / SD card emulator | `hw/sd/sdhci.c` |
| CVE-2023-1386 | 9pfs passthrough filesystem | `hw/9pfs/9p.c` |
| CVE-2024-8612 | virtio-scsi / virtio-blk / virtio-crypto | `hw/scsi/virtio-scsi.c`, `hw/block/virtio-blk.c`, `hw/virtio/virtio-crypto.c` |

All 12 CVEs are in `hw/` paths -- code that runs **only inside the QEMU hypervisor binary** (`qemu-system-x86_64`) when emulating virtual hardware to a guest VM. The hypervisor binary is **not installed** on dojo or regscale; only the `qemu-guest-agent` package providing `/usr/sbin/qemu-ga` is.

## Justification

`dpkg -l qemu-system\* qemu-utils qemu-block-extra` on both in-boundary VMs returns no installed binary packages other than `qemu-guest-agent`:

```
$ ssh root@10.10.30.20 "qm guest exec 201 -- bash -c 'dpkg -l \"qemu-*\" | grep ^ii'"
ii  qemu-guest-agent  1:8.2.2+ds-0ubuntu1.16  amd64  Guest-side qemu-system agent
$ ssh root@10.10.30.21 "qm guest exec 301 -- bash -c 'dpkg -l \"qemu-*\" | grep ^ii'"
ii  qemu-guest-agent  1:8.2.2+ds-0ubuntu1.16  amd64  Guest-side qemu-system agent
```

The qemu-ga binary itself implements only:

- a virtio-serial JSON protocol listener for host-issued commands like `guest-exec`, `guest-fsfreeze-freeze`, `guest-set-time`, `guest-network-get-interfaces`
- no IDE / AHCI / PCI / SCSI / virtio device emulation
- no SD / floppy / VGA / network-card emulation
- no 9pfs server

None of the 12 CVEs above touch code paths that exist in `qemu-ga`. The vulnerable functions cannot execute on these hosts because the binaries that contain them are not installed.

This is the same DR pattern as **FP-0002 libavahi-***: the package is on disk, the CPE match is correct, but the runtime code path is in a sibling binary that the host does not have.

## Compensating controls cited

- **CM-7** Least Functionality: only the guest-side qemu-ga package is installed; the hypervisor binary that contains the vulnerable hardware-emulation code is absent.
- **AU-2** Event Logging: Wazuh agent on dojo and regscale logs all binary executions; no instance of `qemu-system-x86_64`, `qemu-img`, or `qemu-storage-daemon` execution has been observed.
- **CA-7** Continuous Monitoring: if a future ConMon cycle introduces a CVE that genuinely affects the qemu-ga binary itself (e.g., a virtio-serial protocol parsing bug in `qga/`), the FP disposition for that CVE must be re-evaluated. The DR's expiration date below forces this review.
- **SC-7** Boundary Protection: the qemu-ga virtio-serial channel is reachable only from the Proxmox hypervisor (out of FedRAMP boundary). External attackers have no path to the guest agent.

## Proposed disposition

Mark all 24 findings against `qemu-guest-agent` as **False Positive**, with the binary-mismatch rationale above. Findings remain documented in the OSCAL POA&M for audit traceability but do not count against the active POA&M total or accrue against FedRAMP Low SLA windows.

**Per-cycle review:** because `qemu-guest-agent` could in principle be affected by a future CVE that genuinely lives in the qemu-ga binary (`qga/main.c`, `qga/commands*.c`, virtio-serial protocol), the apply-deviation-requests script will flip ALL qemu-guest-agent findings as long as this DR is active. The operator must scan new CVE descriptions on each cycle and remove this DR (or carve out the affected CVE) if a guest-agent-specific issue surfaces. The 90-day expiration below enforces a re-validation cadence shorter than the typical CVE publication-to-Canonical-fix window.

## Reviewer approval (notional)

- **Approved by:** AO (notional -- homelab pilot)
- **Approval date:** 2026-05-04
- **Expiration:** 2026-08-04 (90-day review; short window because future qemu-ga-specific CVEs could legitimately apply)

## Notes

This is the third pattern of false positive identified in this portfolio:

1. **FP-0001:** Vendor-vs-scanner mismatch (Canonical patched, NVD hasn't updated yet).
2. **FP-0002:** Package installed but code path unreachable (hardware/media/daemon absent).
3. **FP-0003:** Package installed but vulnerable code lives in a sibling binary from the same source package that is NOT installed.

All three patterns are common in real CSP ConMon programs. FP-0003 specifically is endemic anywhere a multi-binary source package is partially deployed -- nginx (extras vs core), apache (mod-* packages), python (3.x vs 3.x-minimal), the qemu suite, etc.
