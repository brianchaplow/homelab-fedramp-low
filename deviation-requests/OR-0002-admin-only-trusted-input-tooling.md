# Deviation Request OR-0002 -- Admin-Only Trusted-Input Tooling

## DR metadata

- **DR ID:** OR-0002
- **Category:** Operational Requirement
- **Submitted:** 2026-05-04
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Linked POA&M item(s)

This DR covers a class of findings against developer / admin tooling packages where every published CVE requires either:

1. **Attacker-controlled input file** (object file, linker script, archive, XML document, patch file, vim macro, ELF binary) which the admin must explicitly choose to open or execute.
2. **Admin-initiated invocation** -- no daemon listens on a network or pipe and forwards untrusted input to these binaries.

Specifically:

| Package class | Items | Hosts | Threat model |
|---|---:|---|---|
| `binutils` suite (binutils, binutils-common, binutils-x86-64-linux-gnu, libbinutils, libctf0, libctf-nobfd0, libgprofng0, libsframe1) | 160 | brisket, haccp | All CVEs require malicious object file / linker script / DWARF data fed to `as`, `ld`, `objdump`, `readelf`, or `gprofng`. No daemon invokes these binaries on untrusted input. Used by the admin only when packaging or debugging trusted artifacts. |
| `vim` suite (vim, vim-common, vim-runtime, vim-tiny, xxd) | 40 | brisket, haccp, dojo, regscale | All CVEs require admin to open a crafted file in vim (modeline injection, regex DoS, swap-file race). Vim is not invoked by any daemon and is not the system editor for any service. Compensating control: admins do not open untrusted files. |
| `patch` (GNU patch utility) | 8 | brisket, haccp, dojo, regscale | CVEs in `patch` require crafted diff input. Used only by admins when applying source-level patches. No automated patch ingestion path. |
| `libelf1t64`, `libdw1t64` (ELF/DWARF libraries) | 16 | brisket, haccp, dojo, regscale | Same threat model as binutils -- transitive dependencies of `binutils`, `perf`, and `eu-readelf`. CVEs require crafted ELF input. |
| `libxslt1.1` (XSLT processor) | 8 | brisket, haccp, dojo, regscale | CVEs require admin-controlled XSLT input. No service on these hosts processes externally-supplied XSLT. |
| `busybox-static`, `busybox-initramfs` | 32 | brisket, haccp, dojo, regscale | The static busybox is invoked only inside the initramfs during early boot, before any network is up. No runtime invocation of busybox commands on untrusted input. |
| `libarchive13t64` | 16 (incl. 4 Critical) | brisket, haccp, dojo, regscale | Used by `dpkg`, `apt`, `tar`, `bsdtar` to extract Ubuntu-signed package archives from `archive.ubuntu.com` and `security.ubuntu.com`. Apt validates GPG signatures before invoking libarchive. Trusted-input path. |
| `tar` | 8 | brisket, haccp, dojo, regscale | Same threat model as `libarchive13t64` -- archive extraction utility used by apt/dpkg on signed input and by the admin on trusted backups. No daemon invokes tar on attacker-controlled tarballs. |
| `rsync` | 4 | brisket, haccp, dojo, regscale | File-copy utility invoked by the admin during backup or replication tasks. No `rsyncd` daemon listens on these hosts (`ss -tlnp | grep :873` returns nothing). All rsync invocations are operator-initiated against operator-controlled endpoints. |
| `wget` | 4 | brisket, haccp, dojo, regscale | Admin-only HTTP fetcher. Used in occasional setup scripts and ad-hoc downloads from operator-trusted URLs. CVEs typically require crafted server response or HTML link processing; no automation invokes wget on attacker-controlled URLs. |
| `git`, `git-man` | 8 | brisket, haccp, dojo, regscale | Admin-only source-control client. Repos cloned are operator-controlled (homelab-fedramp-low, brisket-setup, etc.). No CI worker pulls untrusted submodules on these hosts. |

Total covered: **304 items**.

## Finding summary

These packages are part of the standard Ubuntu noble base server install, transitively required by other system packages (e.g. `binutils` is a Recommends of `build-essential`; `libarchive13t64` is a hard `Depends` of `dpkg-dev`; `busybox-initramfs` is required for initramfs regeneration). Removing them would break apt, kernel updates, the weekly apt sweep cron, or interactive admin workflows.

The CVEs reported against these packages are real (the packages do contain the vulnerable code) but the exposure path on the in-boundary hosts is constrained to:

- **Admin-initiated invocation only** -- no daemon listens for and forwards untrusted input.
- **Trusted-input only** -- any automated invocation (apt-dpkg-libarchive, initramfs-busybox) consumes only signed/local artifacts.

## Justification

### binutils, libelf, libdw

```
$ ss -tlnp | grep -E '(as|ld|objdump|readelf|gprofng)'
# (no listening sockets)
$ systemctl list-units --type=service --state=active | grep -iE '(binutils|elf|dwarf)'
# (no services)
```

binutils is invoked by the admin during package builds and by `pmap` / `perf` during debugging. Both paths consume operator-supplied input. No autonomous workflow feeds untrusted object files or linker scripts to these binaries.

### vim

```
$ getent passwd | awk -F: '$NF ~ /vim/'
# (no service account uses vim as login shell)
$ systemctl list-units | grep vim
# (no services launch vim)
```

`vim` is the admin's preferred editor for interactive sessions only. The system default editor (`update-alternatives --list editor`) on these hosts is `nano` for non-interactive contexts.

### patch

`patch` is invoked manually by the admin during source-level remediation. No automated patch-ingestion service exists on any of the four in-boundary hosts.

### busybox-static, busybox-initramfs

```
$ lsinitramfs /boot/initrd.img-$(uname -r) | grep busybox | head
# busybox referenced in initramfs only
$ pgrep -fa busybox
# (no running busybox processes)
```

Busybox is exercised during early boot (initramfs) and again during shutdown. No network is up during early-boot busybox execution, so remote attackers cannot supply input. Local console attackers with physical access to the recovery shell are out of scope per the boundary definition (data center physical security delegated to Tailscale Funnel + OPNsense WAN posture).

### libxslt

```
$ apt rdepends libxslt1.1 --installed 2>/dev/null | grep -v Reverse | head
  libxml2-utils, python3-lxml, ...
```

libxslt is consumed transitively by Python lxml. Service-side use of lxml on these hosts is limited to internal config rendering (e.g. Logstash pipeline templates) where input is operator-controlled. No service ingests externally-supplied XSLT.

### libarchive13t64

`apt-get` and `dpkg` invoke libarchive only after GPG signature verification of the source archive. The trust boundary is the GPG key, not the libarchive parser. CVEs in libarchive that require malicious archive input are gated by Ubuntu's package-signing infrastructure.

## Compensating controls cited

- **CM-7** Least Functionality: each affected binary is admin-invoked only; no exposed network surface.
- **AC-3** Access Enforcement: only operator accounts can invoke these binaries (system service accounts have shell `nologin`).
- **SI-2** Flaw Remediation: weekly apt sweep (`runbooks/conmon-apt-sweep.sh`) installs Canonical patches as they ship -- these findings will close as Canonical publishes fixes in noble-security.
- **CA-7** Continuous Monitoring: Wazuh re-evaluates after each apt sweep; remediated findings auto-close.
- **AU-2** Event Logging: Wazuh agent + auditd record every invocation of these binaries (`/usr/bin/{as,ld,objdump,readelf,vim,patch,busybox}`); audit trail captures any unexpected invocation.

## Proposed disposition

Mark these findings as **Risk Accepted** with operational-requirement disposition pointing to this DR. Findings remain in OSCAL POA&M for audit traceability but do not count against the active POA&M total or accrue against FedRAMP Low SLA windows (30/90/180/365 days).

When Canonical ships security updates for any of these packages via noble-security, the weekly apt sweep will install them automatically and the corresponding Wazuh findings will close on the next re-evaluation. The disposition is "accept until the upstream fix arrives" -- not "accept indefinitely."

## Reviewer approval (notional)

- **Approved by:** AO (notional -- homelab pilot)
- **Approval date:** 2026-05-04
- **Expiration:** 2026-08-04 (90-day review; re-validate that the threat model still applies and that Canonical has not shipped fixes the apt sweep failed to install)

## Notes

This is the most common DR class in real CSP ConMon programs: developer / admin tooling that is part of the OS base install but unreachable from any service surface. Risk acceptance with a short review window (90 days) signals that the operator is not abandoning the finding -- they are deferring it to the natural-remediation lane (apt sweep) while the SLA clock pauses.

Per FedRAMP DR Guide 4.0, class-based DRs that cover a defensible category of findings with shared root cause and shared compensating controls are explicitly permitted and reduce paperwork without weakening the audit trail.
