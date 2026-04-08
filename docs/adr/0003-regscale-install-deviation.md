# ADR 0003 — RegScale CE install path deviation from runbook

## Status

Accepted — 2026-04-08

## Context

Plan 1 Task 15 originally specified a shell-script installer on TLS port 8443
with mandatory `community.regscale.com` signup and a Docker Hub login. As of
2026-04-08, RegScale's actual delivery is a Python-based standalone script
(`standalone_regscale.py`) from the MIT-licensed `github.com/RegScale/community`
repo, pulling publicly accessible Docker images (`regscale/regscale` and
`regscale/regscale-mssql-db`) and serving plain HTTP. No signup or Docker Hub
credentials are required.

The patched plan in `2026-04-07-homelab-fedramp-low-plan-1-infrastructure.md`
called this out as port **81** with Python 3.11 + deadsnakes. Execution
(2026-04-08) revealed three additional discrepancies on top of the
already-patched plan.

## Decisions

### From the patched plan (still correct)

- Use the standalone Python installer from the MIT repo
- Run under Python 3.11 (deadsnakes PPA) since the script does not yet support 3.12
- Skip the regscale.com signup flow entirely — no license key needed for CE

### Discovered at execution time and corrected here

1. **Port is 80, not 81.** The bundled `docker-compose.yml` maps host 80 → atlas:8080. UFW rules updated to allow port 80 from VLANs 10/20/30; the placeholder port 81 rules from Task 14 were deleted.

2. **The Python installer reports a fatal exception that is not actually fatal.** On a 6 GB VM, the SQL Server migration wave races the EF Core distributed lock release and the atlas container exits with `Microsoft.Data.SqlClient.SqlException: A transport-level error has occurred when receiving results from the server. (provider: TCP Provider, error: 35)` during the initial `MigrateAsync` call. The Python wrapper sees this exit and prints `Unexpected error with standalone RegScale instance startup`. **However**, the atlas container's `restart_policy: always` then restarts it; on the second attempt the migration completes and post-startup seeding finishes cleanly. The Python wrapper's exit code is therefore not load-bearing — always wait for HTTP probe + container health to decide whether the install succeeded. `install.sh` swallows the wrapper exit and polls `curl -sf http://127.0.0.1/`.

3. **There is no documented default admin password.** RegScale CE seeds a user (`Email=admin@admin.com`, `UserName=admin`) but:
   - `EmailConfirmed = 0` — login will fail even with the correct password.
   - `PasswordHash` is set to a hashed value not documented in the installer, the GitHub repo, the upstream README, or any env var.
   - There is no `--initial-admin-password` flag, no first-run wizard, and no password-reset endpoint exposed at install time.
   - Login lookup uses `UserName`, not `Email`, even though the row's `Email` is `admin@admin.com` — atlas logs `Username does not exist: admin@admin.com` if you try the email address.
   The only practical way to log into a fresh CE deployment is to overwrite the `PasswordHash` row directly. `deploy/regscale/reset-admin-password.sh` does this:
   - Generates an ASP.NET Identity v3 PBKDF2-HMAC-SHA512 hash (1-byte format marker = 1, 4-byte PRF = 2, 4-byte iter = 100000, 4-byte salt size = 16, 16-byte salt, 32-byte subkey, total 61 bytes, base64 encoded to 84 characters) for the desired password.
   - `UPDATE AspNetUsers SET PasswordHash = ..., EmailConfirmed = 1, AccessFailedCount = 0, LockoutEnd = NULL` `WHERE UserName = 'admin'`.
   - Verifies via `POST /api/authentication/login`.

4. **`sqlcmd` requires `-I` (ANSI QUOTED_IDENTIFIER on)** for any UPDATE that touches AspNetUsers — there's a filtered index on the table that only accepts SET QUOTED_IDENTIFIER ON. Default sqlcmd has it OFF and the UPDATE fails with `Msg 1934`. The reset script passes `-I` explicitly.

5. **Login schema field is `username` (lowercase), credentials POST body uses `username` not `userName`** — though System.Text.Json's case-insensitive matching makes either work in practice.

## Consequences

**Positive:**

- Removes a manual signup step from the runbook; full unattended install possible
- MIT-licensed installer is auditable and redistributable for the portfolio
- Documenting the no-default-password discovery now means the next person hitting RegScale CE has a 30-second answer instead of an hour-long rabbit hole
- The reset-password script is portable to any future RegScale CE deployment (homelab or sandbox), not just this one

**Negative:**

- Plain HTTP on port 80 is acceptable on the lab network but should be fronted with a reverse proxy + TLS before any external exposure (tracked as a future POA&M item in the SSP §SC-8)
- Pinning to Python 3.11 adds a deadsnakes PPA dependency on Ubuntu 24.04. Revisit when RegScale CE supports Python 3.12
- Resetting the password by direct SQL UPDATE means the password is "rotated" outside any audit trail RegScale itself might keep. For the homelab this is fine. In a production deployment this would be a finding worth raising with RegScale.
- The install-time SQL race and the no-default-password issue are both reproducibility risks. Anyone re-running this runbook on a 6 GB VM will see the same fatal-looking-but-not-fatal Python exception, and will need the reset script to log in. Both are fully documented here so the surprise is one-time.

## EULA notes (from ADR 0001)

RegScale CE EULA permits homelab and portfolio use. The only restriction relevant
to this deployment is §2(ii) — no real financial data, no real PHI, no HIPAA/
GLBA/PCI-scope data. The homelab loads only synthetic FedRAMP-Low scope data.

## Verification (as deployed on regscale 2026-04-08)

```
$ curl -s http://10.10.30.28/ -o /dev/null -w '%{http_code}\n'
200

$ curl -s -X POST http://10.10.30.28/api/authentication/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"<REGSCALE_PASSWORD from .env>"}' \
    -o - -w '\n%{http_code}\n' | head -1
{"id":"3f14557b-...","auth_token":"eyJhbG...","expires_in":1440}

$ docker compose ps --format 'table {{.Name}}\t{{.Status}}'
NAME       STATUS
atlas      Up
atlas-db   Up
```

JWT decoded role claim: `GlobalAdmin`. Token TTL: 1440 minutes.
