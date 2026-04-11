# ADR 0002 -- Plan 1 Deployment Complete

**Date:** 2026-04-08
**Status:** Accepted
**Context:** Plan 1 Infrastructure Deployment completion

## Decision

Declare Plan 1 complete. Every done-criterion from the design spec §7.10
is verified below. Every deviation encountered during execution is
captured in its own ADR so the runbooks remain trustworthy for a
re-deployment.

## Deployment Done Criteria (from design spec §7.10)

| Criterion | Actual | Status |
|---|---|---|
| DefectDojo login page loads | `http://10.10.30.27:8080/login` → 200 (HTTP not HTTPS -- see ADR 0004) | PASS |
| RegScale CE login page loads | `http://10.10.30.28/` → 200 (HTTP port 80 not HTTPS 8443 -- see ADR 0003) | PASS |
| Wazuh dashboard shows new agents active | Agents **016 dojo** and **017 regscale** both `active`, keepalive flowing (plan said 014/015 -- haccp and brisket were already 014/015) | PASS |
| `./pipelines.sh smoke` returns healthy | Both DefectDojo and RegScale PASS end-to-end (root=200, login=200, authenticated probe=200) | PASS |
| Both VMs show successful PBS backup | VM 201 (dojo) snapshot `2026-04-08T17:26:22Z`, VM 301 (regscale) snapshot `2026-04-08T21:08:15Z`, both verified in `/mnt/pbs-store/data/vm/` | PASS |
| Both VMs appear in Wazuh syscollector | dojo + regscale: hostname, os=Ubuntu 24.04.4 LTS, kernel=6.8.0-107-generic, cpu=i7-10700T (4 cores), ram=6067424 KB, all present in `/syscollector/*/os` and `/syscollector/*/hardware` | PASS |
| `deploy/` committed + pushed | All artifacts on `origin/main` at github.com/brianchaplow/homelab-fedramp-low | PASS |

## Smoke check output (2026-04-08 final run)

```
DefectDojo OK at http://10.10.30.27:8080 (api=403 login=200)
RegScale OK at http://10.10.30.28 (root=200 login=200 seedingstatus=200, JWT round-trips)
All smoke checks passed.
```

## Additional artifacts in the repo

- `deploy/proxmox/dojo-vm-config.yaml`, `deploy/proxmox/regscale-vm-config.yaml` -- Proxmox VM configs with deviation notes
- `deploy/defectdojo/README.md` -- pinned to DefectDojo 2.57.0, HTTP-on-8080 documented
- `deploy/defectdojo/post-install.sh` -- idempotent + reconciling seed script (5 MSS products, FedRAMP Low ConMon SLA 30/90/180/365)
- `deploy/regscale/install.sh` -- wraps the MIT `standalone_regscale.py`, swallows the non-fatal Python wrapper exit, HTTP-polls for readiness
- `deploy/regscale/reset-admin-password.sh` -- generates ASP.NET Identity v3 PBKDF2-HMAC-SHA512 hash and UPDATEs `AspNetUsers` directly (no shipped default password)
- `deploy/regscale/README.md` -- documents the port 80 / UserName=admin / no-default-password realities
- `tests/smoke/check_defectdojo.sh`, `tests/smoke/check_regscale.sh` -- smoke checks
- `pyproject.toml` + `pipelines.sh` + `Makefile` -- Python venv scaffold, canonical entry point `./pipelines.sh smoke`
- `pipelines/__init__.py` -- stub package, Plan 2 fills it in
- `runbooks/restore-from-pbs.md`, `runbooks/cert-trust.md`, `runbooks/monthly-conmon.md` (stub) -- operational runbooks
- `docs/adr/0001-preflight-and-eula.md` -- pre-flight results + RegScale CE EULA analysis
- `docs/adr/0003-regscale-install-deviation.md` -- RegScale port / wrapper exit / admin password discoveries
- `docs/adr/0004-defectdojo-install-deviation.md` -- DefectDojo 2.57.0 setEnv flow + Valkey + HTTP on 8080
- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` -- PBS 5-day backup gap discovery + automount fix

## Infrastructure state (end of Plan 1)

| Host | IP | VMID | Node | Role |
|---|---|---|---|---|
| dojo | 10.10.30.27 | 201 | pitcrew | DefectDojo 2.57.0 on Docker, Wazuh agent 016 |
| regscale | 10.10.30.28 | 301 | smoker | RegScale CE (atlas + mssql) on Docker, Wazuh agent 017 |

Both VMs: Ubuntu 24.04.4 LTS, kernel 6.8.0-107-generic, 4 vCPU / 6 GB RAM / 40 GB disk, eth0 on VLAN 30 untagged, UFW default-deny with VLAN-scoped allows on SSH + service port, unattended-upgrades active.

## Summary of deviations encountered during execution

Nine distinct deviations were discovered during Plan 1 execution beyond the pre-flight ones documented in ADR 0001. All are captured in dedicated ADRs or in-repo artifacts:

1. **DefectDojo 2.57.0 uses Valkey instead of Redis** (ADR 0004) -- container name changed from `defectdojo-redis-1` to `defectdojo-valkey-1`. Functionally identical.
2. **DefectDojo 2.57.0 serves HTTP on 8080, not HTTPS** (ADR 0004) -- the bundled nginx container has no TLS cert wired in. Port 8443 is published but unused. Corrected URL + UFW rules.
3. **`/api/v2/sla_configurations/?name=` does not actually filter** (commit 81c585b + seed script comment) -- returns all rows. Seed script switched to client-side jq exact-match, plus reconciling PATCH for products already attached to the wrong SLA.
4. **dojo is Wazuh agent 016, not 014** -- haccp (014) and brisket (015) were already enrolled. regscale became 017. Documented in ADR 0002.
5. **RegScale CE serves on port 80, not 81** (ADR 0003) -- bundled compose maps host 80 → atlas:8080. UFW rules corrected at runtime from 81 to 80.
6. **The RegScale Python wrapper reports a fatal exception that isn't fatal** (ADR 0003) -- SQL Server migration race on first pass, atlas container's `restart_policy: always` retries and succeeds on second pass. `install.sh` uses HTTP probe instead of wrapper exit code to determine success.
7. **RegScale CE has no documented default admin password** (ADR 0003) -- seeds `Email=admin@admin.com, UserName=admin` with `EmailConfirmed=0` and an undocumented hash. `reset-admin-password.sh` generates a proper ASP.NET Identity v3 PBKDF2-HMAC-SHA512 hash and UPDATEs the row directly. Login lookup uses `UserName` not `Email` -- using the email address returns `Username does not exist`.
8. **PBS NFS mount silently failed during 2026-04-07 rack reboot** (ADR 0005) -- discovered during Task 12 backup verification. 5-day backup gap Apr 3–7 for VMs 100/101/200 (DC01, WS01, TheHive). Fixed with `x-systemd.automount` fstab hardening.
9. **No `make` in Git Bash on Windows** -- Git for Windows does not ship make. `pipelines.sh` is the canonical entry point; the Makefile is a thin alias for POSIX systems that do have make.

## Operator action items deferred to Plan 2 or beyond

1. **Verify the 2026-04-09 02:00 PBS nightly run succeeds** for VMs 100/101/200 -- this closes the 5-day backup gap from ADR 0005. If it fails, the automount unit didn't trigger as expected.
2. **Wire a Wazuh/Discord alert on PBS backup job failure** -- the 5-day gap went unnoticed because `mail-to-root` on the PBS LXC is the only notification target. Plan 2 follow-up captured in `runbooks/monthly-conmon.md`.
3. **Restore drill within 7 days of Plan 1 completion** -- `runbooks/restore-from-pbs.md` describes the procedure. Should produce `docs/adr/0006-restore-drill.md` with time-to-restore and any manual remediation.
4. **Reverse-proxy + TLS posture** -- both tools are HTTP-only. Plan 4 writeup treats this as a deliberate portfolio trade-off (SC-8), and `runbooks/cert-trust.md` describes the upgrade path if a production-adjacent posture is desired later.
5. **RegScale long-lived API key** -- Plan 1 uses JWT tokens (24h TTL) via `/api/authentication/login`. If unattended Plan 2 pipelines need longer-lived credentials, investigate RegScale CE's personal access token flow.
6. **Python 3.14 + pydantic.v1 compat warning** -- Trestle 4.0.1 warns that `pydantic.v1` is not fully compatible with Python 3.14. Plan 2 should verify all trestle code paths run cleanly in this environment or pin an older trestle that uses pydantic v2 natively.

## Next

**Plan 2: OSCAL Foundation + Pipelines.** The pipeline code that consumes the now-running DefectDojo and RegScale CE, reading Wazuh vulnerabilities from the brisket manager API and emitting OSCAL assessment-results via compliance-trestle.

---

## Plan 2 start (2026-04-09)

Plan 2 (OSCAL Foundation + Pipelines) started 2026-04-09 after a critical
read of the Plan 2 plan file against this ADR surfaced ten substantive
deviations and required a pre-execution realignment. All deviations are
consolidated in **ADR 0006 -- Plan 2 Environment and API Realignment**,
which is the canonical reference every downstream Plan 2 task cites
when it diverges from the literal plan text.

Key pre-execution findings:

- Wazuh `/vulnerability/{agent_id}` REST endpoint was removed in 4.8+
  (confirmed HTTP 404 on the live manager at v4.14.4). Task 6 `WazuhClient`
  drops `get_vulnerabilities()`; new Task 6b builds a
  `WazuhIndexerClient` that queries the `wazuh-states-vulnerabilities-*`
  index directly (12,949 docs, indexer green at 10.10.20.30:9200).
- RegScale CE has no long-lived API key -- only 24h JWTs. Plan 2's
  `REGSCALE_API_KEY` references are all rewritten to use a
  `RegScaleClient` that re-auths per invocation.
- Plan 2's HTTPS validator in `Config` would reject the real DefectDojo
  and RegScale URLs (both HTTP per ADRs 0003/0004). Scoped to Wazuh
  endpoints only.
- Plan 2's `[wsl]` tags and `~/homelab-fedramp-low` paths reflect a
  WSL assumption that was never real for this workstation. Every
  command rewrites to Git Bash conventions.
- Plan 2 Task 14 would have rewritten `Makefile` with a full build
  system. Preserving the Plan 1 pipelines.sh-canonical contract: new
  pipeline commands live in `pipelines/cli.py`, `pipelines.sh` grows a
  passthrough arm for unknown commands, `Makefile` stays a thin alias.
- Plan 2 assumed Wazuh agents 014/015 for dojo/regscale. Reality per
  Plan 1 is 016/017 (haccp and brisket were already 014/015).
- Plan 2 Task 17 would have written ADR 0003 (already taken). Plan 2's
  numbering starts at 0006 (this realignment ADR) and the completion
  ADR lands at whatever number is free at Task 17.

Four operator questions decided up front: hybrid env var defaults
(constants in code, passwords in `.env`); `pipelines/cli.py` Click app
with `pipelines.sh` passthrough (verbose docstrings, `test` arm stays
explicit); PBS alert deferred to a dedicated follow-up phase (interim
manual tripwire added to `runbooks/monthly-conmon.md`); direct commits
to `main` matching Plan 1's pattern.

**Plan 1 operator TODO status (re-checked 2026-04-09):**

1. ✅ 2026-04-09 02:00 PBS run successfully closed the 5-day backup gap
   -- verified via `pct exec 300 -- ls /mnt/pbs-store/data/vm/` on smoker.
   VM 100 (DC01) @ 02:00, VM 101 (WS01) @ 02:03, VM 201 (dojo) @ 02:08,
   VM 301 (regscale) @ 02:30; VM 200 (TheHive) caught by the weekly job
   at 06:45. ADR 0005 automount fix held.
2. 🔴 Wazuh/Discord PBS alert -- **deferred out of Plan 2 per ADR 0006**.
   Interim manual tripwire added to `runbooks/monthly-conmon.md` §"Daily
   PBS backup tripwire" during Plan 2 Task 1.
3. 🔴 Restore drill -- independent of Plan 2, still owed within 7 days.
4. ⚠️ Reverse-proxy / TLS posture -- no change; documented as a portfolio
   trade-off for Plan 4 writeup (SC-8).
5. ✅ RegScale long-lived API key investigation -- **resolved by ADR 0006**:
   the 24h JWT is sufficient (each pipeline invocation re-auths).
6. ✅ Trestle 4.0.1 under Python 3.14 -- imports verified, cosmetic
   pydantic.v1 warning only. Task 2 adds an OSCAL catalog round-trip
   test as an early-warning tripwire before Plan 2 commits to the stack.
