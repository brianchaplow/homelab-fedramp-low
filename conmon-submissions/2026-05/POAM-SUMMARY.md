# POA&M Summary -- May 2026

> The full POA&M is in `POAM-2026-05.xlsx` (13 MB, too large for GitHub's inline renderer). This summary provides the key metrics. Download the xlsx for the complete item-level data.

## Totals

| Metric | Count |
|---|---:|
| Total POA&M items | 25,416 |
| Unique CVEs | 1,004 |
| Unique affected packages | 79 |

## Status Distribution

| Status | Count | Change vs April |
|---|---:|---:|
| Open | 25,414 | +8,470 |
| Completed | 1 | +1 |
| Deviated | 1 | +1 |

## State Transitions (April to May)

| Transition | Finding | Detail |
|---|---|---|
| Open to Completed | CVE-2026-32249 in Vim | Patched via `apt upgrade` across all in-boundary Ubuntu 24.04 hosts, verified by re-scan |
| Open to Deviated | Openssl Heap Overflow | Risk-accepted via DefectDojo risk_acceptance endpoint, linked to Deviation Request RA-0001 |
| New (May only) | CVE-2026-99999 in Libfoo | Synthetic finding created for May cycle demo (see README for staging disclosure) |

All three transitions were staged intentionally before running the May cycle, per ADR 0010. See the [May submission README](README.md) for the full staging disclosure.

## Severity Distribution

| Severity | Total Items | Unique CVEs | Change vs April |
|---|---:|---:|---:|
| Critical | 108 | 4 | +36 items, +0 CVEs |
| High | 4,880 | 199 | +1,626 items, +0 CVEs |
| Medium | 11,434 | 454 | +3,812 items, +1 CVE |
| Low | 8,994 | 347 | +2,998 items, +0 CVEs |

The +8,472 total-item growth is the documented import-scan pile-up (ADR 0007 Risk #2): each monthly run re-imports the full Wazuh indexer hit set into a new engagement. The unique CVE count grew by only 1 (the synthetic finding).

## Top 20 Affected Packages

| Items | Severity | Package |
|---:|---|---|
| 10,776 | Low | linux-image-6.8.0-107-generic |
| 8,082 | High | linux-image-6.8.0-106-generic |
| 2,694 | High | linux-image-6.17.0-19-generic |
| 2,694 | High | linux-image-6.17.0-20-generic |
| 102 | Medium | Qemu-Guest-Agent |
| 48 | Medium | Busybox-Static |
| 48 | Medium | Busybox-Initramfs |
| 33 | High | Openssl-Fips-Provider-Latest |
| 33 | High | Openssl-Libs |
| 30 | Medium | Amd64-Microcode |
| 24 | Medium | Libelf1t64 |
| 24 | Medium | Libde265-0 |
| 24 | Medium | Libavahi-Common-Data |
| 24 | Medium | Libavahi-Client3 |
| 24 | Medium | Libdw1t64 |
| 24 | High | Patch |
| 24 | Medium | libxslt1.1 |
| 24 | Medium | Libavahi-Common3 |
| 24 | High | Libarchive13t64 |
| 18 | Medium | Libctf-Nobfd0 |

**Note:** 95.4% of all items (24,246 of 25,416) are in four linux kernel image packages. Two of these (`6.8.0-106`, `6.8.0-107`) are stale kernels no longer booted by any in-boundary host. Removing them via `apt autoremove` would eliminate approximately 18,858 items (74.3%) as legitimate remediations.

## Critical CVEs (4 unique)

| CVE | Package Context |
|---|---|
| CVE-2021-3773 | linux kernel images |
| CVE-2025-68263 | linux kernel images |
| CVE-2026-23112 | linux kernel images |
| CVE-2026-23240 | linux kernel images |

All four Critical CVEs affect linux kernel image packages only.

## Remediation Priorities

1. **Remove stale kernel packages** (`6.8.0-106`, `6.8.0-107`) via `apt autoremove` on all in-boundary hosts. Estimated impact: ~18,858 items closed (74.3%).
2. **Patch non-kernel packages** (Qemu-Guest-Agent, Busybox, OpenSSL, Patch, libde265, libxslt, libarchive) via `apt upgrade`. Estimated impact: ~500+ items.
3. **Evaluate current-kernel CVEs** (`6.17.0-19`, `6.17.0-20`) for available Ubuntu security patches. If patched upstream, a kernel upgrade + reboot closes ~5,388 items.
4. **File additional DRs** for kernel CVEs with no upstream patch available (OR or FP category depending on root cause).

## Data Source

Generated from `oscal/mss-poam-2026-05.json` by the `pipelines.sh conmon` pipeline. Findings sourced from the Wazuh Indexer vulnerability state index via DefectDojo Generic Findings Import.
