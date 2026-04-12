# POA&M Summary -- May 2026

> The full POA&M is in `POAM-2026-05.xlsx` (3.0 MB). This summary provides the key metrics. Download the xlsx for the complete item-level data.

## Totals

| Metric | Count |
|---|---:|
| Total POA&M items | 4,876 |
| Unique CVEs | 998 |
| Unique affected packages | ~70 |

## Diff vs April 2026

| Metric | April 2026 | May 2026 | Change |
|---|---:|---:|---:|
| Total POA&M items | 16,944 | 4,876 | -12,068 (-71.2%) |
| Critical | 72 | 20 | -52 (-72.2%) |
| High | 3,254 | 937 | -2,317 (-71.2%) |
| Medium | 7,622 | 2,203 | -5,419 (-71.1%) |
| Low | 5,996 | 1,716 | -4,280 (-71.4%) |
| Unique CVEs | 1,003 | 998 | -5 |

The 71.2% reduction is from real remediation (stale kernel removal + package upgrades) across all four in-boundary Ubuntu hosts on 2026-04-12. See the [submission README](README.md) for the full remediation narrative.

## Severity Distribution

| Severity | Total Items |
|---|---:|
| Critical | 20 |
| High | 937 |
| Medium | 2,203 |
| Low | 1,716 |

## Top 10 Affected Packages

| Items | Package |
|---:|---|
| 2,694 | linux-image-6.8.0-107-generic (running kernel on haccp, dojo, regscale) |
| 898 | linux-image-6.17.0-19-generic (running kernel on brisket) |
| 898 | linux-image-6.17.0-20-generic (pending kernel on brisket) |
| 34 | Qemu-Guest-Agent |
| 16 | Busybox-Static |
| 16 | Busybox-Initramfs |
| 11 | Openssl-Fips-Provider-Latest |
| 11 | Openssl-Libs |
| 10 | Amd64-Microcode |
| 8 | Libelf1t64 |

91.7% of remaining items (4,490 of 4,876) are in linux kernel image packages that require a kernel upgrade + reboot or upstream Ubuntu security patches to close.

## Remediation Summary

| Action | Items Eliminated | Detail |
|---|---:|---|
| Removed linux-image-6.8.0-106-generic | ~8,082 | Was stale on haccp, dojo, regscale (not booted) |
| Removed linux-image-6.8.0-107-generic from brisket | ~3,592 | Was stale on brisket (HWE kernel 6.17.0 is active) |
| Package upgrades (apt upgrade) | ~394 | apparmor, Docker CE, fwupd, systemd, filebeat, etc. |
| **Total eliminated** | **~12,068** | **71.2% of April baseline** |

## Data Source

Generated from `oscal/mss-poam-2026-05.json` by the `pipelines.sh conmon` pipeline on 2026-04-12. Findings sourced from the Wazuh Indexer vulnerability state index. DefectDojo was cleared of all prior engagements before this run to eliminate import-scan pile-up.
