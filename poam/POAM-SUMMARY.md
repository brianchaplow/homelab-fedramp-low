# POA&M Summary -- May 2026

> The full POA&M is in `POAM-2026-05.xlsx` (2.4 MB). This summary provides the key metrics. Download the xlsx for the complete item-level data.

## Totals

| Metric | Count |
|---|---:|
| Total POA&M items | 4,195 |
| Unique CVEs | 1,019 |
| Unique affected packages | ~70 |

## Diff vs April 2026 baseline

| Metric | April 2026 | May 2026 (this run) | Change |
|---|---:|---:|---:|
| Total POA&M items | 16,944 | 4,195 | -12,749 (-75.2%) |
| Critical | 72 | 60 | -12 (-16.7%) |
| High | 3,254 | 991 | -2,263 (-69.5%) |
| Medium | 7,622 | 1,974 | -5,648 (-74.1%) |
| Low | 5,996 | 1,170 | -4,826 (-80.5%) |
| Unique CVEs | 1,003 | 1,019 | +16 |

The 75.2% cumulative reduction reflects two remediation passes against the April baseline:

1. **2026-04-12 pass:** Stale 6.8.0-106 kernel removal across haccp/dojo/regscale and stale 6.8.0-107 removal from brisket. April baseline 16,944 → 4,876 (-71.2%).
2. **2026-05-04 pass:** All four Ubuntu in-boundary hosts upgraded to HWE kernel 6.17.0-23 (CVE-2026-31431 "Copy Fail" sweep on 2026-05-03), then stale predecessor kernels (6.17.0-22 on all four; 6.17.0-20 lingering on haccp; orphaned NVIDIA module packages on haccp and brisket) purged today. April POAM 4,876 → 4,195 this cycle (-14.0%).

The new unique-CVE count is **higher** than April even though item count fell, because the active 6.17.0-23 HWE kernel introduced a fresh tranche of upstream CVEs that did not exist against the prior 6.8.0-107 baseline. Those will close once Canonical ships the corresponding HWE security patches.

## Diff vs prior May submission (the 2026-04-12 generated artifact)

| Metric | May 2026 (4/12 run) | May 2026 (5/4 run) | Change |
|---|---:|---:|---:|
| Total POA&M items | 4,876 | 4,195 | -681 (-14.0%) |
| Critical | 20 | 60 | +40 |
| High | 937 | 991 | +54 |
| Medium | 2,203 | 1,974 | -229 |
| Low | 1,716 | 1,170 | -546 |
| Unique CVEs | 998 | 1,019 | +21 |

Net item count down because 6.8.0-107 (running kernel on 3 hosts) and 6.17.0-19/20 (brisket's running + pending) were all replaced with 6.17.0-23, then their predecessor packages were purged from disk. Critical/High counts edged up because the 6.17.0-23 HWE has fewer CVEs against it overall (889 per host vs 898 before) but a slightly different severity mix.

## Severity Distribution (this run)

| Severity | Total Items |
|---|---:|
| Critical | 60 |
| High | 991 |
| Medium | 1,974 |
| Low | 1,170 |

## Top 10 Affected Packages

| Items | Package |
|---:|---|
| 3,556 | linux-image-6.17.0-23-generic (running HWE kernel on brisket, haccp, dojo, regscale) |
| 24 | Qemu-Guest-Agent |
| 20 | Amd64-Microcode |
| 20 | Binutils, Binutils-Common, Binutils-X86-64-Linux-Gnu, Libbinutils, Libctf0, Libctf-Nobfd0, Libgprofng0, Libsframe1 (binutils suite, 8 packages × 20 items) |
| 16 | Busybox-Static, Busybox-Initramfs |
| 16 | Libarchive13t64 |
| 16 | Openssl-Fips-Provider-Latest |
| 16 | Openssl-Libs |
| 12 | Libc-Bin, Libc6, Locales |
| 8 | Libelf1t64, Libdw1t64, Patch, Python3, Python3-Libs, Tar, Vim, Libxslt1.1, Libde265-0 |

84.8% of remaining items (3,556 of 4,195) are CVEs against the running HWE kernel `linux-image-6.17.0-23-generic`. Closing them requires Canonical to ship a 6.17.0-24 HWE update (or later) plus a coordinated reboot of all four hosts. The non-kernel residual (binutils suite, busybox, libc, openssl, etc.) is a candidate for the next remediation pass once Ubuntu publishes the relevant security updates.

## Remediation Summary (2026-05-04 pass only)

| Action | Items Eliminated | Detail |
|---|---:|---|
| Purged linux-image-6.17.0-22-generic (modules + extras) | 3,556 | 4 hosts × 889 CVEs/kernel; predecessor of yesterday's Copy Fail upgrade |
| Purged linux-image-6.17.0-20-generic + modules + headers | 889 | Stale on haccp; older predecessor never autoremoved |
| Purged linux-modules-nvidia-535-6.17.0-20-generic + nvidia-firmware-535 + nvidia-kernel-common-535 + linux-objects-nvidia-535-6.17.0-20-generic + libpciaccess0 | 0 (orphans, not in vuln state) | Dead-weight cleanup on haccp; no driver loaded |
| Purged linux-headers-6.17.0-22-generic + linux-tools-6.17.0-22-generic + linux-hwe-6.17-tools-6.17.0-22 + nvidia-firmware-580-580.126.09 | 0 (orphans) | Dead-weight cleanup on brisket; -22 nvidia firmware superseded by 580.142 |
| apt upgrade (curl, libcurl4t64, libcurl3t64-gnutls, iproute2) | ~21 unique CVEs | Late-arriving upstream patches across regscale + dojo |
| **Net items removed** | **-681** | **14.0% reduction vs prior May POAM** |

## Smokehouse note

Smokehouse (10.10.20.10) is a QNAP NAS running kernel 5.10.60-qnap. It has no apt-based package management. Its 73 Wazuh findings are QNAP-specific and cannot be remediated via the same process as the Ubuntu hosts. QNAP firmware updates are the remediation path for those findings.

## Data Source

Generated from `oscal/mss-poam-2026-05.json` by the `pipelines.sh conmon` pipeline on 2026-05-04. Findings sourced from the Wazuh Indexer vulnerability state index. DefectDojo was cleared of all prior engagements (4 engagements, 9,071 stale findings) before this run to eliminate import-scan pile-up per ADR 0007.
