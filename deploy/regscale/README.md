# RegScale Community Edition Deployment — `regscale` VM

## Target

- VM: `regscale` (Proxmox VMID 301 on smoker)
- IP: 10.10.30.28
- OS: Ubuntu 24.04 LTS (kernel 6.8.0-107-generic after first upgrade)
- Resources: 4 vCPU / 6 GB RAM / 40 GB disk
- Endpoint: **http://10.10.30.28:80** (plain HTTP, lab-only — see ADR 0003)
- Database: SQL Server 2022 in `atlas-db` container (port 1433, sa creds in `~/regscale/atlas.env`)
- Application: `regscale/regscale:latest` in `atlas` container (host port 80 → container 8080)

## Prerequisites

- Docker Engine installed (Task 7-style block)
- Python 3.11 from deadsnakes PPA (the standalone installer requires <= 3.11)
- 6+ GB RAM (SQL Server needs ~1 GB just to start; migrations need headroom)
- No regscale.com signup, no Docker Hub login, no license key — CE is fully open

## Install

```bash
./deploy/regscale/install.sh
```

Then set the admin password (no shipped default — see "Admin password" below):

```bash
# On regscale VM, with REGSCALE_DB_SA_PASSWORD and REGSCALE_PASSWORD in env
./deploy/regscale/reset-admin-password.sh
```

## Verify

```bash
# Health: root page renders the SPA shell
curl -s http://10.10.30.28/ -o /dev/null -w '%{http_code}\n'
# Expected: 200

# Auth: /api/authentication/login issues a JWT
curl -s -X POST http://10.10.30.28/api/authentication/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<REGSCALE_PASSWORD from .env>"}' \
  -w '\n%{http_code}\n'
# Expected: 200, JSON body with "auth_token" field
```

## Admin

- Initial admin username: `admin` (NOT an email — RegScale CE looks up by `UserName`, not `Email`, even though the row's `Email` is `admin@admin.com`)
- Initial admin password: see `/c/Projects/.env` on PITBOSS (`REGSCALE_PASSWORD`)
- URL: **http://10.10.30.28/** (HTTP, port 80 — see ADR 0003)
- JWT contains role `GlobalAdmin`, expires in 1440 minutes (24 hours)

## Why HTTP and why direct DB password reset?

**Plain HTTP on lab subnet only.** The bundled compose file binds `0.0.0.0:80→atlas:8080`. There is no TLS termination in the container — a real FedRAMP-Low deployment would front this with a reverse proxy (Caddy / nginx / Traefik) holding a CA-signed cert. Documented in the SSP as a deferred control trade-off (SC-8).

**Admin password reset via SQL.** RegScale CE seeds an admin user with `EmailConfirmed=0` and a hashed password that is **not** documented in the public repo, the installer log, or any env var. There is no first-run wizard, no `--initial-admin-password` flag, and no password reset endpoint. The only practical way to log in is `reset-admin-password.sh`, which generates an ASP.NET Identity v3 PBKDF2-HMAC-SHA512 hash and `UPDATE`s the row directly. See ADR 0003 for the full reasoning.

## Source

- Installer: https://github.com/RegScale/community (MIT license)
- Docker images:
  - `regscale/regscale:latest` (the application; Docker Hub, public, 100K+ pulls)
  - `regscale/regscale-mssql-db:latest` (SQL Server 2022 with seeded schema)
- EULA: https://regscale.com/community-edition-license-agreement/
  (full text captured in `docs/adr/0001-preflight-and-eula.md`)

## Operational notes

- **Port 80 not 81 not 8443.** The bundled compose maps host 80 → container 8080. UFW rules and `~/.env REGSCALE_URL` updated accordingly.
- **Python 3.11 pinned.** Ubuntu 24.04 ships 3.12 which `standalone_regscale.py` does not yet support.
- **Container restart_policy: always.** This is what saves the install: the Python wrapper crashes during the initial migration race, but atlas restarts and retries the migration successfully on the second pass. The wrapper's exit code does not reflect the true state of the deployment — always check container health and HTTP probe instead.
- **EmailConfirmed=0 by default.** The seeded admin has `EmailConfirmed=0`, which alone would prevent login even with the correct password. `reset-admin-password.sh` flips this to 1.
- **Tenant password policy (from `tenants.json`):** PasswordLength=12, must include upper/lower/digit/symbol. Pick a `REGSCALE_PASSWORD` that satisfies this.

## Deviation record

See `docs/adr/0003-regscale-install-deviation.md` for the full deviation
from the original Plan 1 Task 15 assumptions and the install-time discoveries.
