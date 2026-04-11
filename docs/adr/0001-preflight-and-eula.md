# ADR 0001 -- Pre-flight Verification + RegScale CE EULA Review

**Date:** 2026-04-08
**Status:** Accepted
**Context:** Plan 1 Task 1 pre-flight checks + Plan 1 Task 1 Step 4 EULA review

## Decision

Proceed with Plan 1 execution based on the following verified pre-flight results
and accepted RegScale Community Edition license terms.

## Pre-flight results

| Check | Expected | Actual | Status |
|---|---|---|---|
| pitcrew SSH reachability | ✓ as root | ✓ root@10.10.30.20, Proxmox 9.1.6 | ✓ |
| smoker SSH reachability | ✓ as root | ✓ root@10.10.30.21, Proxmox 9.1.6 | ✓ |
| pitcrew free memory | >= 8 GB | 17 GB free of 30 GB | ✓ |
| smoker free memory | >= 8 GB | 20 GB free of 31 GB | ✓ |
| VM ID dojo (on pitcrew) | unused | **201** (VMs 100, 101 present; 201+ free) | ✓ |
| VM ID regscale (on smoker) | unused | **301** (VMs 200-203 present; 300 is PBS LXC; 301+ free) | ✓ |
| Proxmox clustering | N/A | pitcrew and smoker are independent, not clustered (no corosync.conf) | ✓ |
| 10.10.30.27 IP free | ✓ | ✓ ping 100% loss | ✓ |
| 10.10.30.28 IP free | ✓ | ✓ ping 100% loss | ✓ |
| RegScale CE EULA | accepts homelab/portfolio use | ✓ full review, see appendix | ✓ |
| FedRAMP Rev 5 template URLs | reachable | ✓ all three HTTP 200, pre-downloaded to `templates/` | ✓ |
| WSL2 Ubuntu | available | ✓ Ubuntu-22.04 present (not 24.04 -- see deviation below) | ✓ |
| Wazuh API authentication | working | ✓ JWT token received for `wazuh-wui` | ✓ |
| PBS LXC 300 | running | ✓ `pct status 300` = running on smoker | ✓ |

## Path / environment deviations from original plan

| Plan assumption | Actual | Resolution |
|---|---|---|
| Repo at `/home/brian/homelab-fedramp-low` (WSL Ubuntu 24.04) | WSL user is `chappy`, distro is 22.04, repo lives at `C:\Projects\homelab-fedramp-low` | Repo on Windows-native filesystem, accessed from WSL via `/mnt/c/Projects/homelab-fedramp-low` or from Git Bash directly. No functional difference for any Plan 1 task. |
| WSL has Python 3.12 | WSL Ubuntu 22.04 has Python 3.10.12 | Install Python 3.12 via deadsnakes PPA in Plan 2 Task 19 (or continue to use 3.10 if Compliance Trestle supports it; relax `requires-python` in pyproject.toml) |
| `gh` CLI in WSL | Missing in WSL, present in Git Bash (Windows side) | Use Windows-side `gh` for GitHub repo creation |
| `jq` in WSL | Missing | Install on first use |
| Secrets in `~/.env` on PITBOSS | Secrets in `/c/Projects/.env` (project root) | Pipelines will source from `/c/Projects/.env` (readable from both Git Bash and WSL) |

## RegScale CE EULA review

Full text of the RegScale Community Edition License Agreement at
`https://regscale.com/community-edition-license-agreement/` was reviewed in
full on 2026-04-08.

### Material clauses and their effect on this deployment

| Clause | Effect |
|---|---|
| §1.A -- License "solely for internal business purposes" | OK. Personal professional development + homelab learning fits. No paid client work on this instance. |
| §2(i) -- No commercial exploitation; no making the Software available to others | OK. Single-user lab. Public writeup will reference RegScale CE only with attribution and a link to community.regscale.com; no redistribution of binaries or installer. |
| §2(ii) -- **No real PHI, credit card, financial, HIPAA/GLBA/PCI-scope data** | **HARD REQUIREMENT.** All FedRAMP-Low scope data loaded into CE will be synthetic. Spec already calls for this. |
| §2(v) -- No modifying, copying, derivative works of the Software | OK. We are using CE as-shipped. The MIT-licensed `standalone_regscale.py` wrapper is separate and may be modified. |
| §2(vii) -- No use for competing product or copying UI | OK. Portfolio is a FedRAMP automation case study, not a GRC product. |
| §2(ix) -- No publishing circumvention info | OK. Writeup will not include circumvention techniques. |
| §4.B -- License revocable at RegScale's sole discretion | Acknowledged risk: RegScale could pull CE at any time. Mitigation: data exports stay in OSCAL JSON (vendor-neutral), so a future migration to Compliance-Trestle-only is possible. Already in spec §11 risks. |
| §6 -- Damages capped at $100 | Acknowledged. No reliance on uptime guarantees. |
| §7 -- Operator indemnifies RegScale for submitted content | Acknowledged. Synthetic data only. |
| §12 -- Arbitration, Virginia jurisdiction, class action waiver | Acknowledged. |

### EULA line items

```
RegScale CE EULA verified:         yes
Date verified:                      2026-04-08
EULA source:                        https://regscale.com/community-edition-license-agreement/
EULA version on file:               no explicit version; SHA of this ADR file acts as pin
"Internal business purposes" fit:   yes (personal professional development)
Synthetic data only:                REQUIRED (§2(ii))
Public writeup attribution:         REQUIRED (link community.regscale.com, no endorsement implied)
Revocability acknowledged:          yes (mitigation: OSCAL exports, Trestle fallback path)
Installer source:                   github.com/RegScale/community (MIT)
Docker image source:                Docker Hub regscale/regscale (public, no auth)
Signup required:                    NO -- bypassed entirely
```

## Pre-fetched templates

Pre-downloaded by operator on 2026-04-08 and copied into `templates/`:
- `FedRAMP-POAM-Template-Rev5.xlsx` (622 KB)
- `FedRAMP-IIW-Template-Rev5.xlsx` (248 KB)
- `FedRAMP-DR-Form.xlsx` (151 KB)

Source URLs in `templates/README.md`.

## Consequences

- Plan 1 execution proceeds with VMIDs 201 and 301 on pitcrew and smoker respectively
- Plan 1 Task 15 follows the deviated install path (ADR 0003)
- Plan 1 Task 8 follows the deviated install path (ADR 0004)
- Repo lives on Windows-native filesystem; no blocker for WSL interoperability
- All templates are present locally; `curl` in Task 3 becomes redundant (keeps as fallback)

## Blockers encountered

None. Plan 1 is unblocked end-to-end.
