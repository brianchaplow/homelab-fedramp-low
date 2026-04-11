# ADR 0004 -- DefectDojo install path deviation from runbook

## Status

Accepted -- 2026-04-08

## Context

Plan 1 Task 8 originally called `./dc-up.sh postgres-redis`. That script and
its profile-based naming were removed in DefectDojo 2.57.0 (latest release,
2026-04-06). The upstream repo now uses a canonical `docker-compose.yml` plus
a `docker/setEnv.sh` helper that manages an optional `docker-compose.override.yml`
symlink based on environment (`dev`, `unit_tests`, `unit_tests_cicd`,
`integration_tests`, `release`).

A secondary change in 2.57.0: the Celery broker / cache service was swapped
from **Redis** to **Valkey** (the community fork of Redis created after the
2024 license change). `docker compose ps` now shows `defectdojo-valkey-1` in
place of `defectdojo-redis-1`. This is transparent to Celery and uwsgi but
affects anyone grepping for container names in the runbook.

A third discovery at execution time: nginx inside the 2.57.0 container serves
**HTTP on 8080** only. The compose file publishes port 8443 as well, but the
bundled nginx container ships without a TLS cert or `listen 8443 ssl;`
directive, so that port is effectively unused. The original plan assumed
`https://...:8080/` as the URL -- this was wrong on two counts (wrong scheme
and wrong port). Corrected URL: `http://10.10.30.27:8080/`.

## Decision

- Pin to tag `2.57.0` for reproducibility
- Use `./docker/setEnv.sh release` to select release mode (removes any override symlink)
- Use direct `docker compose build` + `docker compose up -d` against the canonical compose file
- No manual `.env.prod` copy -- the `initializer` container handles seeding
- Admin password still captured from `docker compose logs initializer | grep 'Admin password'`
- Document the valkey rename in `deploy/defectdojo/README.md` so the runbook reader is not surprised
- Accept HTTP-only on 8080 for the homelab; explicitly call out in the
  portfolio writeup that a real FedRAMP-Low deployment would front
  DefectDojo with a TLS-terminating reverse proxy

## Consequences

**Positive:**
- Matches current upstream patterns exactly; no brittle wrapper dependencies
- Pinning to a release tag makes the deployment reproducible
- `setEnv.sh release` is a documented upstream entry point, not a workaround

**Negative:**
- Version upgrade is now a deliberate operation (`git fetch && git checkout <newtag>`)
  rather than a clone-tracks-master pattern -- but this is desirable for ConMon
- No rollback shortcut if 2.57.0 has regressions in this environment; operator
  must fall back one tag manually

## Verification (as deployed on dojo 2026-04-08)

```
$ docker compose ps --format 'table {{.Name}}\t{{.Status}}'
NAME                        STATUS
defectdojo-celerybeat-1     Up
defectdojo-celeryworker-1   Up
defectdojo-nginx-1          Up
defectdojo-postgres-1       Up
defectdojo-uwsgi-1          Up
defectdojo-valkey-1         Up

$ git -C ~/defectdojo describe --tags
2.57.0
```

## Notes

This deviation was caught during co-work pre-flight verification, not during
execution. ADR timestamp matches the upstream release date. The Redis → Valkey
service-name change was discovered at execution time and added to this ADR
before the Plan 1 commit.
