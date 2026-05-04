# POA&M Summary -- May 2026

> The full POA&M is in `POAM-2026-05.xlsx` (2.3 MB). This summary provides the key metrics. Download the xlsx for the complete item-level data.

## Totals

| Metric | Count |
|---|---:|
| Open POA&M items (this cycle) | **3,796** |
| DR-adjudicated (Risk Accepted via OR-0002) | 304 |
| DR-adjudicated (False Positive via FP-0002) | 43 |
| **Total findings tracked** | **4,143** |
| Unique CVEs (in Open) | ~950 |
| Unique affected packages | ~65 |

## Diff vs April 2026 baseline

| Metric | April 2026 | May 2026 (Open) | Change |
|---|---:|---:|---:|
| Total POA&M items | 16,944 | 3,796 | -13,148 (-77.6%) |
| Critical | 72 | 56 | -16 (-22.2%) |
| High | 3,254 | 946 | -2,308 (-70.9%) |
| Medium | 7,622 | 1,696 | -5,926 (-77.7%) |
| Low | 5,996 | 1,098 | -4,898 (-81.7%) |
| Unique CVEs | 1,003 | ~950 | ~ -53 |

The 77.6% cumulative reduction reflects four remediation passes plus two Deviation Requests against the April baseline:

1. **2026-04-12 pass:** Stale 6.8.0-106 kernel removal across haccp/dojo/regscale and stale 6.8.0-107 removal from brisket. April baseline 16,944 → 4,876 (-71.2%).
2. **2026-05-04 kernel autoremove pass:** All four in-boundary Ubuntu hosts on HWE kernel 6.17.0-23 after the CVE-2026-31431 "Copy Fail" sweep on 2026-05-03. Stale 6.17.0-22 + 6.17.0-20 kernels and orphaned NVIDIA modules purged. 4,876 → 4,195 (-14.0%).
3. **2026-05-04 Wazuh agent pass:** Smokehouse Wazuh agent container upgraded `4.14.2 → 4.14.4` (matching the brisket manager). 4,195 → 4,151 (-1.0%, smokehouse 73 → 29).
4. **2026-05-04 dead-weight package purge:** Removed `telnet` + `inetutils-telnet` (insecure-by-design clients with zero legitimate use) from all four hosts. 4,151 → 4,143 (-8 items, all High severity).
5. **2026-05-04 DR adjudication:** FP-0002 (amd64-microcode unreachable on Intel CPUs, libde265 with no media path, libavahi-* with no avahi-daemon) flips 43 items to False Positive; OR-0002 (admin-only trusted-input tooling: binutils, vim, patch, libelf/libdw, libxslt, busybox, libarchive, tar, rsync, wget, git) flips 304 items to Risk Accepted. 4,143 → 3,796 in the Open sheet.

## Severity Distribution (Open items only)

| Severity | Total Open Items |
|---|---:|
| Critical | 56 |
| High | 946 |
| Medium | 1,696 |
| Low | 1,098 |

## DR-adjudicated breakdown

The 347 items moved out of "Open" via deviation request remain in the OSCAL POA&M JSON (`oscal/mss-poam-2026-05.json`) for audit traceability. They do not count against active SLA windows (30/90/180/365 days by severity) because their disposition is documented and approved.

| State | Count | Severity (C/H/M/L) | DR | Coverage |
|---|---:|---|---|---|
| False Positive | 43 | 0 / 2 / 33 / 8 | FP-0002 | amd64-microcode (20, hard dep of HWE meta on Intel hosts), libde265-0 (8, HEVC unused), libavahi-client3 + libavahi-common3 + libavahi-common-data (15, no avahi-daemon installed) |
| Risk Accepted | 304 | 4 / 24 / 220 / 56 | OR-0002 | binutils suite (160), vim suite (40), busybox (32), libarchive13t64 (16), libelf+libdw (16), libxslt (8), patch (8), tar (8), rsync (4), wget (4), git+git-man (8) |

## Top Affected Packages (Open items only)

| Items | Package |
|---:|---|
| 3,556 | linux-image-6.17.0-23-generic (running HWE kernel on brisket, haccp, dojo, regscale) |
| 24 | Qemu-Guest-Agent (dojo + regscale; many CVEs are QEMU host-side, future Risk-Adjustment DR candidate) |
| 36 | Libc-Bin + Libc6 + Locales |
| 12 | Openssl-Fips-Provider-Latest + Openssl-Libs (smokehouse-internal Wazuh image) |
| 16 | Python3 + Python3-Libs (smokehouse + brisket python3-pip-whl) |
| 36 | util-linux suite (mount, fdisk, libmount1, libfdisk1, libsmartcols1, libuuid1, libblkid1, uuid-runtime, eject, bsdutils, bsdextrautils) |
| 24 | python3.12 + libpython3.12-* (4 Ubuntu hosts) |
| 12 | polkitd + libpolkit-* (all High; 4 Ubuntu hosts) |
| 12 | Curl-Minimal + Libcurl-Minimal |
| ~150 | misc tail: snapd, dpkg, libicu74, libcairo2, libgcrypt20, login, passwd, libdebuginfod, libnghttp2, libtasn1, expat, gnupg2-minimal, etc. |

93.7% of remaining open items (3,556 of 3,796) are in `linux-image-6.17.0-23-generic`. Closing them requires Canonical to ship a 6.17.0-24+ HWE update plus a coordinated reboot. Tracked under "vendor-dependent" with no SLA accrual until upstream patch availability.

## Remediation summary -- 2026-05-04 cycle

| Action | Items Eliminated | Detail |
|---|---:|---|
| Purged linux-image-6.17.0-22-generic across all 4 Ubuntu hosts | 3,556 | 4 hosts × 889 CVEs/kernel; predecessor of Copy Fail upgrade |
| Purged linux-image-6.17.0-20-generic + nvidia modules on haccp | 889 | Older predecessor + dead-weight NVIDIA |
| Wazuh agent 4.14.2 → 4.14.4 on smokehouse | 44 | Image bundled-package CVEs (openssl, python, curl, libxml2, etc.) |
| Purged telnet + inetutils-telnet across all 4 hosts | 8 | Insecure-by-design CLI; zero legitimate use; all High severity |
| FP-0002 + OR-0002 deviation requests | 347 | Adjudicated out of Open via documented justification + compensating controls (43 FP + 304 RA) |
| **Net Open-sheet reduction this cycle** | **-1,080** | from 4,876 (prior May POAM) to 3,796 (this run) |

## Smokehouse note

Smokehouse (10.10.20.10) is a QNAP TVS-871 NAS running QTS 5.2.9 build 20260327 -- the latest QTS firmware available for the TVS-X71 series (verified against `update.qnap.com/QTS_FW_5.2.0.xml` on 2026-05-04). The 29 remaining Wazuh findings on smokehouse are inside the Wazuh agent Docker container (Amazon Linux 2 base image). They will close when Wazuh publishes 4.14.5+ with refreshed base packages and we coordinate a manager + agent bump.

## Data Source

Generated from `oscal/mss-poam-2026-05.json` by the `pipelines.sh conmon` pipeline on 2026-05-04. Findings sourced from the Wazuh Indexer vulnerability state index. DefectDojo was cleared of all prior engagements (4 engagements, 3,843 stale findings carrying forward from the previous mid-day May run) before this run to eliminate the import-scan pile-up documented in ADR 0007. After ingest, `runbooks/apply-deviation-requests.py` walked the OSCAL POA&M and flipped 347 items to FP/RA states per FP-0002 and OR-0002. The renderer in `pipelines/render/poam.py` then skipped DR-adjudicated items from the "Open POA&M Items" sheet.
