# homelab-fedramp-low -- Claude session reference

This is a public portfolio project demonstrating FedRAMP Low Continuous Monitoring (ConMon) on a homelab. Real artifacts (POA&Ms, OSCAL JSON, deviation requests, SSP, IIW), real Wazuh-sourced findings, real remediation passes. Designed to look familiar to a 3PAO or FedRAMP TRC.

**Public repo:** github.com/brianchaplow/homelab-fedramp-low
**Status:** Plans 1-4 complete (`plan-4-complete` tag, ADR 0011). Active monthly ConMon cycles run in-place on this tree.

## Most-used commands

```bash
# from repo root
./pipelines.sh smoke          # DefectDojo + RegScale reachability check
./pipelines.sh conmon         # full monthly cycle (ingest -> oscal -> render)
./pipelines.sh test           # 136-test pytest suite (must stay green)
./pipelines.sh ssp-assemble   # rebuild OSCAL SSP from trestle-workspace markdown
.venv/Scripts/python.exe runbooks/apply-deviation-requests.py --poam-json oscal/poam.json
.venv/Scripts/python.exe -m pytest tests/        # tests directly
```

`CONMON_MONTH=YYYY-MM` env var pins a cycle to a specific month (used to stage future cycles or re-run a closed month).

## Repo layout

| Path | What lives there |
|---|---|
| `pipelines/` | Click CLI + ingest/build/render Python modules. `pipelines/cli.py` wires the public `inventory`, `ingest-findings`, `build-poam`, `render-iiw`, `render-poam`, `oscal`, `conmon`, `regscale-push`, `ssp-assemble` commands. |
| `pipelines.sh` | Cross-platform shell wrapper (Git Bash on Windows, POSIX on Linux/WSL). Sources env, selects venv, dispatches to `pipelines.cli`. |
| `oscal/` | Build artifacts (gitignored): `poam.json`, `component-definition.json`, `ssp.json`. Authoritative copies are inside `conmon-submissions/YYYY-MM/oscal/` once a cycle is committed. |
| `poam/` | Latest rendered POA&M xlsx + `POAM-SUMMARY.md`. Mirror of the most recent submission. |
| `inventory/` | Latest IIW xlsx + `overlay.yaml` (manual operator additions to the Wazuh-derived inventory). |
| `conmon-submissions/YYYY-MM/` | Per-cycle submission package: POAM xlsx, IIW xlsx, OSCAL JSON, scan-evidence/, README, POAM-SUMMARY. April + May 2026 are the live cycles as of 2026-05. |
| `deviation-requests/` | DR markdowns (FedRAMP Low DR Guide format). Three categories: RA (Risk Adjustment), FP (False Positive), OR (Operational Requirement). Apply via `runbooks/apply-deviation-requests.py`. |
| `significant-changes/` | SCR documents (boundary expansion, etc.). |
| `runbooks/` | Operational scripts + procedure docs. Includes `conmon-apt-sweep.sh` (weekly cron deployed to in-boundary hosts), `apply-deviation-requests.py` (idempotent OSCAL state-flipper), `monthly-conmon.md` (procedure), `cert-trust.md`, `regscale-manual-import.md`, `restore-from-pbs.md`. |
| `ssp/` + `trestle-workspace/` | OSCAL SSP source: control markdown files (156 controls × 18 families) + Trestle workspace metadata. `pipelines.sh ssp-assemble` regenerates the SSP JSON. |
| `templates/` | FedRAMP Rev 5 POA&M + IIW xlsx templates. Renderer populates these at the per-template-defined header rows. |
| `evidence/` | Operator screenshots, config exports, attestations referenced by DRs and SSP. |
| `writeups/` | Public-facing portfolio narratives. Writeup #1 is the main build narrative (3229 words); Writeup #2 is the Paramify comparison (1805 words). |
| `docs/` | ADRs (`docs/adr/0001` through `0011`), Plan-3 evidence catalog, Plan-2/3/4 design specs, Mermaid diagrams (boundary, pipeline). |
| `tests/` | pytest suite. Smoke + unit + integration. 136 tests as of 2026-05-04. |

## Five in-boundary hosts (FedRAMP system inventory)

`brisket` (10.10.20.30), `haccp` (10.10.30.25), `dojo` VM (10.10.30.27), `regscale` VM (10.10.30.28), `smokehouse` (10.10.20.10). Defined in `pipelines/cli.py::IN_BOUNDARY_WAZUH_AGENTS`. Five DefectDojo products map them via `pipelines/cli.py::HOST_TO_PRODUCT` (dojo + regscale share a product).

## Source-of-truth chain

```
Wazuh Indexer (live vuln state)
    -> pipelines.sh conmon (ingest)
    -> DefectDojo engagements per product
    -> oscal/poam.json (build-poam)
    -> apply-deviation-requests.py flips state on items matching DR rule table
    -> oscal/poam.json (mutated in place)
    -> render-poam writes poam/POAM-YYYY-MM.xlsx
    -> conmon-submissions/YYYY-MM/ (manual copy of artifacts + scan-evidence refresh)
    -> git commit + push
```

The OSCAL JSON is the source of truth. The xlsx is a render. The Open POA&M Items sheet excludes items in `{Risk Accepted, False Positive, Closed, Operational Requirement}` -- the renderer respects `poam-state` per `pipelines/render/poam.py::EXCLUDED_FROM_OPEN_SHEET`.

## DR taxonomy

| ID | Category | Coverage | Items (May 2026) |
|---|---|---|---|
| RA-0001 | Risk Adjustment | Grafana exposure (compensating controls drop CVSS) | 1 representative |
| FP-0001 | False Positive | Ubuntu ESM tracker lag (NVD vs Canonical timing) | class-based |
| OR-0001 | Operational Requirement | Shared tenancy on brisket | class-based |
| FP-0002 | False Positive | Package installed but code path unreachable (amd64-microcode on Intel hosts, libde265 with no media path, libavahi-* with no daemon) | 43 |
| FP-0003 | False Positive | Multi-binary source package mismatch (qemu-guest-agent CVEs are in qemu-system-x86_64 hypervisor binary, not installed) | 24 |
| OR-0002 | Operational Requirement | Admin-only trusted-input tooling (binutils, vim, busybox, libarchive, libelf, libdw, libxslt, patch, tar, rsync, wget, git) | 304 |

Adding a new DR: write the markdown, add an entry to `DR_RULES` in `runbooks/apply-deviation-requests.py`, re-run apply + render. Idempotent.

## Conventions

- **No em dashes** in any authored content (Brian's voice rule). Use commas, colons, semicolons, parentheses, sentence breaks. Applies to DRs, READMEs, writeups.
- **No Co-Authored-By or Claude attribution** in commit messages.
- **No secrets in tracked files**. `.env` lives at `/c/Projects/.env` (or `~/.env` on POSIX). Never committed.
- **Templates use ASCII hyphens** in product names per ADR 0006 amendment 2026-04-09 (the Plan 1 seed script created products with `-`, not em dashes).
- **GRC tools (DefectDojo, RegScale) stop between demos.** Bring up only for the duration of a cycle. Standard sequence: spinup -> wait for readiness -> clear prior engagements -> run conmon -> apply DRs -> render -> copy artifacts -> commit -> shutdown. See `~/.claude/projects/C--Projects/memory/fedramp_conmon_flow.md` for the full checklist.

## Iterative re-runs in a single day are OK

Each `pipelines.sh conmon` overwrites the per-month submission artifacts. Multiple cycles in one day (one per remediation pass) is the established pattern as of 2026-05-04 (six conmon-related commits in chronological progression). The git history is the audit trail.

**Before each re-run:** clear DefectDojo engagements via `DELETE /api/v2/engagements/<id>/` (cascade-deletes findings). Per ADR 0007 -- the import-scan-pile-up trap. Use a 300s request timeout; cascade delete on a 4,876-finding engagement may take >30s.

## Wazuh fleet baseline (as of 2026-05-04)

- Manager: brisket, v4.14.5 (compose at `/home/bchaplow/docker/wazuh/wazuh-docker/single-node/docker-compose.yml`)
- Indexer + Dashboard: brisket, v4.14.5
- All 15 fleet agents: v4.14.5 (15/15 active)
- Smokehouse agent runs containerized via QNAP Container Station; identity preservation requires `client.keys` persistence to bind mount before recreate (see memory note).

Bumping the manager: edit compose tags, `docker compose pull`, `docker compose up -d`, ~60s service blip, agents queue events to disk and reconnect.

Bumping all agents to match: `PUT /agents/upgrade?agents_list=...` via Wazuh API (single call, Linux + Windows simultaneously, no WinRM/MSI/SSH).

## Weekly apt sweep

`runbooks/conmon-apt-sweep.sh` is deployed to all four in-boundary Ubuntu hosts at `/usr/local/sbin/`, with a cron entry at `/etc/cron.d/conmon-apt-sweep` (Sunday 0400 host-local) and logrotate config at `/etc/logrotate.d/conmon-apt-sweep`. Runs `apt-get update && apt-get upgrade && systemctl restart wazuh-agent`. Skips held packages (Docker / containerd) -- those follow a slower cadence.

Verify each Monday morning: `tail -3 /var/log/conmon-apt-sweep.log` should end with `=== <ts> conmon-apt-sweep END on <host> ===`.

## Test invariants

- 136 pytest tests must pass before any cycle commit.
- `./pipelines.sh ssp-assemble` must succeed (no Trestle YAML errors).
- All OSCAL artifacts schema-valid (SSP 1.2.1, component-def 1.1.2, POA&M 1.1.2).
- POAM xlsx rendering: `Open POA&M Items` sheet starts at row 8 (header rows 1-7 are template metadata + guidance + example).
- IIW xlsx rendering: `Inventory` sheet data starts at row 13.

## ADRs to consult

| ADR | When to read |
|---|---|
| 0005 | PBS backup chain + NFS automount fragility |
| 0006 | Environment realignment, deviation count for ConMon program |
| 0007 | Plan 2 complete; documents DefectDojo import-scan pile-up risk |
| 0009 | Plan 3 complete; SSP authoring lessons |
| 0011 | Plan 4 complete; current portfolio milestone |

## Cross-references

- Parent project map: `/c/Projects/CLAUDE.md` (homelab SOC v3 platform; brisket = primary host)
- Auto-memory index: `~/.claude/projects/C--Projects/memory/MEMORY.md` (search for `fedramp_*`, `wazuh_*`, `feedback_amd64_microcode*`, `feedback_apt_autoremove*`, `feedback_wazuh_api*`)
- `runbooks/monthly-conmon.md` documents the procedure operators follow each cycle.
