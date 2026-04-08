# DefectDojo Deployment — `dojo` VM

## Target

- VM: `dojo` (Proxmox VMID 201 on pitcrew)
- IP: 10.10.30.27
- OS: Ubuntu 24.04 LTS (kernel 6.8.0-107-generic after first upgrade)
- Resources: 4 vCPU / 6 GB RAM / 40 GB disk
- Version: DefectDojo 2.57.0 (pinned)
- Docker: 29.4.0 + Compose v5.1.1

## Install

```bash
# On dojo VM as the ubuntu user (member of docker group)
git clone https://github.com/DefectDojo/django-DefectDojo.git ~/defectdojo
cd ~/defectdojo
git checkout 2.57.0          # pin to a release; do not track master
./docker/setEnv.sh release   # release mode = no override symlink
docker compose build
docker compose up -d
# Wait ~90s, then:
docker compose logs initializer 2>&1 | grep 'Admin password'
# Capture the admin password and store on PITBOSS in /c/Projects/.env
# as DEFECTDOJO_ADMIN_PASS. This is the ONLY time it is printed.
```

## Containers in a healthy 2.57.0 deployment

```
defectdojo-nginx-1           Up
defectdojo-uwsgi-1           Up
defectdojo-celeryworker-1    Up
defectdojo-celerybeat-1      Up
defectdojo-postgres-1        Up
defectdojo-valkey-1          Up
```

Note: 2.57.0 replaced Redis with **Valkey** as the Celery broker / cache.
If a future upgrade reintroduces Redis, `docker compose ps` will reflect it;
operationally there is no functional difference for ConMon workloads.

## Verify

```bash
curl -s http://10.10.30.27:8080/api/v2/user_profile/ -o /dev/null -w '%{http_code}\n'
# Expected: 403 (service up, unauthenticated request rejected)

curl -s http://10.10.30.27:8080/login -o /dev/null -w '%{http_code}\n'
# Expected: 200 (login page renders)
```

## Admin

- Initial admin username: `admin`
- Initial admin password: see `/c/Projects/.env` on PITBOSS (`DEFECTDOJO_ADMIN_PASS`)
- URL: **http://10.10.30.27:8080/** (HTTP, not HTTPS — see ADR 0004 for rationale)

## Why HTTP in a ConMon demo?

DefectDojo 2.57.0 upstream `docker-compose.yml` publishes two ports:

- `8080` — nginx serving HTTP
- `8443` — published by Docker, but the bundled nginx container ships
  without a TLS cert or listen directive, so the port is effectively unused

A real FedRAMP-Low deployment would front DefectDojo with a TLS-terminating
reverse proxy (ALB, nginx, Traefik) holding a CA-signed cert. In this homelab
the tool is reached only from trusted VLANs (10/20/30) via IP; adding a
self-signed cert would create a false sense of security without demonstrating
any new ConMon concept. The writeup in Plan 4 calls this out as an explicit
"in production, do X" control trade-off — a more useful portfolio artifact
than a self-signed-cert workaround.

## Version pinning rationale

Pinned to 2.57.0 (released 2026-04-06). Why pin rather than track master:

1. Reproducibility — anyone re-running this runbook gets the same stack.
2. Deliberate upgrades — version bumps are ConMon-tracked events, not accidents.
3. Rollback — if 2.57.0 has a regression, fall back one tag before deep debugging.

## Deviation from original runbook

The original Plan 1 Task 8 referenced `./dc-up.sh postgres-redis`, a convenience
wrapper that existed in older DefectDojo releases but was removed before 2.57.0.
The profile-based naming (`postgres-redis`, `mysql-rabbitmq`) is also gone —
DefectDojo standardized on a single PostgreSQL + Valkey stack. The current flow
is `setEnv.sh release` + `docker compose build` + `docker compose up -d`
against the canonical `docker-compose.yml`. See
`docs/adr/0004-defectdojo-install-deviation.md`.
