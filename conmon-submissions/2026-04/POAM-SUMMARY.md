# POA&M Summary -- April 2026

> The full POA&M is in `POAM-2026-04.xlsx` (8.7 MB, too large for GitHub's inline renderer). This summary provides the key metrics. Download the xlsx for the complete item-level data.

## Totals

| Metric | Count |
|---|---:|
| Total POA&M items | 16,944 |
| Unique CVEs | 1,003 |
| Unique affected packages | 78 |

## Status Distribution

| Status | Count |
|---|---:|
| Open | 16,944 |
| Completed | 0 |
| Deviated | 0 |

This is the baseline cycle. No prior month exists to diff against. All items are Open.

## Severity Distribution

| Severity | Total Items | Unique CVEs |
|---|---:|---:|
| Critical | 72 | 4 |
| High | 3,254 | 199 |
| Medium | 7,622 | 453 |
| Low | 5,996 | 347 |

## Top 15 Affected Packages

| Items | Severity | Package |
|---:|---|---|
| 7,184 | Low | linux-image-6.8.0-107-generic |
| 5,388 | High | linux-image-6.8.0-106-generic |
| 1,796 | High | linux-image-6.17.0-19-generic |
| 1,796 | High | linux-image-6.17.0-20-generic |
| 68 | Medium | Qemu-Guest-Agent |
| 32 | Medium | Busybox-Static |
| 32 | Medium | Busybox-Initramfs |
| 22 | High | Openssl-Fips-Provider-Latest |
| 22 | High | Openssl-Libs |
| 20 | Medium | Amd64-Microcode |
| 16 | Medium | Libelf1t64 |
| 16 | Medium | Libde265-0 |
| 16 | Medium | Libavahi-Common-Data |
| 16 | Medium | Libavahi-Client3 |
| 16 | Medium | Libdw1t64 |

**Note:** 95.3% of all items (16,164 of 16,944) are in four linux kernel image packages. Two of these (`6.8.0-106`, `6.8.0-107`) are stale kernels no longer booted by any in-boundary host. Removing them via `apt autoremove` is the single highest-impact remediation available.

## Critical CVEs (4 unique)

| CVE | Package Context |
|---|---|
| CVE-2021-3773 | linux kernel images |
| CVE-2025-68263 | linux kernel images |
| CVE-2026-23112 | linux kernel images |
| CVE-2026-23240 | linux kernel images |

All four Critical CVEs affect linux kernel image packages only.

## Data Source

Generated from `oscal/mss-poam-2026-04.json` by the `pipelines.sh conmon` pipeline. Findings sourced from the Wazuh Indexer vulnerability state index via DefectDojo Generic Findings Import.
