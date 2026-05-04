# Deviation Request FP-0002 -- Package Installed But Code Path Unreachable

## DR metadata

- **DR ID:** FP-0002
- **Category:** False Positive
- **Submitted:** 2026-05-04
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Linked POA&M item(s)

This DR covers a class of findings where the Wazuh vulnerability detector flags a package as vulnerable, but the vulnerable code path is provably unreachable on the in-boundary host because either:

1. The vulnerable hardware or media format is not present.
2. The package is installed only as a transitive dependency of a metapackage and is never executed at runtime.

Specifically:

| Package | Items | Hosts | Reason unreachable |
|---|---:|---|---|
| `amd64-microcode` | 20 | brisket, haccp, dojo, regscale | All four in-boundary hosts run Intel CPUs (Ultra 9 285, i7-10700T, virtualized Intel). The package is required as a hard dependency of `linux-image-generic-hwe-24.04` (alongside `intel-microcode`) but the AMD microcode loader is gated on AMD CPU detection and is never invoked. |
| `libde265-0` | 8 | brisket, haccp | HEVC video decoder library. Installed as a transitive dependency of GTK/libheif but never linked to a live media-decoding code path on these hosts (no video playback, no image-conversion service). |
| `libavahi-client3`, `libavahi-common3`, `libavahi-common-data` | 15 | brisket | mDNS/Bonjour service-discovery libraries. Pulled in transitively by `libcups2t64` (which is itself a transitive dep of `libgtk-3-0t64`). Critically, **the `avahi-daemon` package is NOT installed on brisket** (`systemctl status avahi-daemon` returns "Unit avahi-daemon.service could not be found"). The CVEs in libavahi-* are exploitable only via the running daemon's mDNS network surface; with no daemon installed, the libraries are dead code on disk. |

Total covered: **43 items**.

## Finding summary

The Wazuh vulnerability detector matches CPE entries from `package.name` + `package.version` against NVD. A CPE match indicates the *package* is vulnerable, not that the *code path* is reachable. For the two packages above, the vulnerable function lives behind a runtime check that this system never enters:

- `amd64-microcode`: Linux's microcode loader (`/usr/lib/firmware/amd-ucode/`) is consulted by `arch/x86/kernel/cpu/microcode/amd.c`, which short-circuits when `c->x86_vendor != X86_VENDOR_AMD`. On Intel CPUs, the AMD microcode is never loaded into kernel memory. The CVEs in the AMD microcode update package describe issues in the microcode patches themselves, which are only consumed when an AMD CPU is detected.
- `libde265-0`: HEVC decoder. The library is on disk but not opened by any running process. CVEs require crafted HEVC video input through a decoder call site; no such call site exists on these hosts (verified via `lsof | grep libde265` -- no open handles).

## Justification

### amd64-microcode

CPU vendor on each in-boundary host:

```
brisket   : Intel(R) Core(TM) Ultra 9 285             (genuine_intel)
haccp     : Intel(R) Core(TM) i7-10700T               (genuine_intel)
dojo      : virtualized Intel via Proxmox VM 201      (genuine_intel)
regscale  : virtualized Intel via Proxmox VM 301      (genuine_intel)
```

The package cannot be removed without breaking the `linux-image-generic-hwe-24.04` HWE metapackage (verified 2026-05-04: `apt-get purge amd64-microcode` cascade-removes the kernel meta because the meta hard-`Depends:` on both `intel-microcode | amd64-microcode`-style entries listed as separate hard dependencies). Removing the meta would disable automatic HWE kernel updates and break the weekly apt sweep documented in `runbooks/conmon-apt-sweep.sh`. The package therefore stays installed but unloaded.

### libde265-0

`lsof | grep libde265` returns no results on brisket or haccp. The library is pulled in transitively by GTK / libheif / libgdk-pixbuf2 dependencies that exist for desktop session support but are not invoked by any service in the SOC stack (Wazuh, Logstash, ES, Kibana, Arkime, Zeek, Suricata, OpenCTI, Shuffle do not decode HEVC).

### libavahi-client3, libavahi-common3, libavahi-common-data

The `avahi-daemon` package is NOT installed on brisket; verified 2026-05-04:

```
$ systemctl status avahi-daemon --no-pager
Unit avahi-daemon.service could not be found.
$ systemctl is-enabled avahi-daemon
not-found
```

The libavahi-* libraries are present only as transitive dependencies via the chain `libavahi-* <- libcups2t64 <- libgtk-3-0t64`. CUPS itself has no print queues configured and no `cupsd` service running on brisket. GTK3 was installed at imaging time as a side-effect of debugging tooling (gnome-keyring-utils, ghostscript-x).

Avahi CVEs are uniformly exploitable only via the mDNS daemon's UDP/5353 network surface. Without `avahi-daemon` installed, no process listens on that port, and the libavahi client APIs are never invoked. `ss -tulnp | grep 5353` returns no listeners.

A future hardening pass could remove libgtk-3-0t64 (and the avahi/cups chain with it) to actually purge the libraries; for now the FP disposition reflects the reachability state.

## Compensating controls cited

- **CM-7** Least Functionality: package present but loadable code path is gated on hardware/media absent from the system.
- **AU-2** Event Logging: Wazuh agents on all four hosts log every binary execution (auditd integration); no instance of the AMD microcode loader or libde265 decoder code path being invoked has been observed.
- **CA-7** Continuous Monitoring: Wazuh re-evaluates package state every cycle; if the system gains an AMD CPU or starts decoding HEVC media, the finding will resurface and be re-evaluated.

## Proposed disposition

Mark these findings as **False Positive** with the package + reachability rationale above. Findings remain documented in the OSCAL POA&M for audit traceability but do not count against the active POA&M total.

## Reviewer approval (notional)

- **Approved by:** AO (notional -- homelab pilot)
- **Approval date:** 2026-05-04
- **Expiration:** 2027-05-04 (annual review; re-validates that no AMD CPU was added and no HEVC decode path was introduced)

## Notes

This DR is the "scanner is right, but reachability isn't" pattern. NVD has the CVE; the package is on disk; the version matches the vulnerable range. What the scanner cannot see is that a runtime gate (CPU vendor check, missing media call site) makes the vulnerable code unreachable. CSPs encounter this commonly with multi-arch microcode packages and transitively-installed media libraries.

The class-based approach (covering both packages in one DR rather than 28 individual items) is the practical pattern documented in FedRAMP DR Guide 4.0 for "patterns of false positive" that share a single root cause.
