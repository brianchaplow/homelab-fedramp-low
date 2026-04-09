# ADR 0006 — Plan 2 Environment and API Realignment

**Date:** 2026-04-09
**Status:** Accepted
**Context:** Plan 2 (OSCAL Foundation + Pipelines) pre-execution critical read

## Decision

Plan 2 was authored 2026-04-07, before Plan 1 executed. Plan 1 execution
(complete 2026-04-08, ADR 0002) produced 9+ deviations that make several
of Plan 2's foundational assumptions wrong in ways that would either
block Task 1 at the config-loader step or cause a silent semantic drift
later. This ADR consolidates every realignment so that downstream Plan 2
tasks can cite "per ADR 0006" when they diverge from the literal plan
text, and so that a future re-read of the plan against this ADR produces
a coherent execution story.

The realignments below were confirmed by a live environment probe on
2026-04-09 before any Plan 2 code was written. Four operator questions
(env var strategy, orchestration home, PBS alerting scope, branch
strategy) were decided up front rather than discovered mid-plan.

## Deviation 1 — Environment: Git Bash on Windows, not WSL

**Plan 2 assumes:** WSL2 Ubuntu on PITBOSS as the execution host. Every
task block is tagged `[wsl]`. Commands use `~/homelab-fedramp-low/`,
`~/.env`, `.venv/bin/activate`, `.venv/bin/pytest`, `python3`.

**Reality:** Plan 1 Task 1 pre-flight (ADR 0001) already noted WSL was
available but the actual execution host is Git Bash on Windows with
Python 3.14 native. The repo lives at `/c/Projects/homelab-fedramp-low`
(`C:\Projects\homelab-fedramp-low`), the env file is `/c/Projects/.env`,
and the venv is at `.venv/Scripts/python.exe`. WSL Ubuntu-22.04 is
available as a secondary path but has not been used for any Plan 1 work.

**Realignment:** All Plan 2 `[wsl]` tags read as `[gitbash]`. The
substitution is mechanical:

| Plan 2 text                       | Actual command                                             |
|-----------------------------------|------------------------------------------------------------|
| `cd ~/homelab-fedramp-low`        | `cd /c/Projects/homelab-fedramp-low`                       |
| `source ~/.env`                   | `set -a; source /c/Projects/.env; set +a`                  |
| `.venv/bin/activate`              | n/a — invoke `.venv/Scripts/python.exe` directly           |
| `.venv/bin/python`                | `.venv/Scripts/python.exe`                                 |
| `.venv/bin/pytest`                | `.venv/Scripts/pytest.exe`                                 |
| `.venv/bin/pip`                   | `.venv/Scripts/pip.exe`                                    |
| `python3 -c '...'`                | `.venv/Scripts/python.exe -c '...'`                        |
| `make <target>`                   | `./pipelines.sh <target>` (see Deviation 2)                |

The `pipelines.sh` entry point already handles venv discovery and env
loading for both POSIX and Git Bash paths (see `pipelines.sh` find_env()
and VENV_PY selection logic), so in practice most invocations reduce to
`./pipelines.sh <subcommand>` regardless of host.

## Deviation 2 — Orchestration: pipelines.sh passthrough, not a rewritten Makefile

**Plan 2 assumes:** Task 14 Step 2 rewrites `Makefile` with a full 60+
line build system containing `install`, `test`, `smoke`, `inventory`,
`render-iiw`, `ingest-findings`, `build-poam`, `render-poam`, `oscal`,
`conmon`, `clean` targets.

**Reality:** ADR 0002 Deviation #9 established that Git Bash on Windows
does not ship `make`, and that `pipelines.sh` is the canonical entry
point. The existing `Makefile` is a thin alias that delegates every
target to `pipelines.sh` so that POSIX systems with make still work.
Overwriting it would break the Plan 1 contract.

**Realignment:** New pipeline commands live in `pipelines/cli.py` as a
Click application with verbose docstrings. `pipelines.sh` grows a
passthrough arm:

```bash
case "$cmd" in
  help|install|clean|smoke|smoke-dojo|smoke-regscale|test)
    # existing and test arm stay explicit (test collides with the
    # POSIX shell builtin)
    ...
    ;;
  *)
    # unknown commands forward to the Click CLI
    load_env
    exec "$VENV_PY" -m pipelines.cli "$cmd" "$@"
    ;;
esac
```

The `Makefile` stays a one-line-per-target forwarder. `./pipelines.sh
help` is updated to enumerate every command, infra and pipeline, so a
new user has a single place to discover capability. The `test` arm
stays explicit in the case statement to avoid any collision with the
POSIX shell `test` builtin.

Rationale for this shape over alternatives (Makefile rewrite;
CLI-only with verbose invocation): it preserves the one-entry-point
invariant from Plan 1, keeps Git Bash and POSIX behavior identical,
and lets Click's `CliRunner` test the orchestration logic in pytest.

## Deviation 3 — Config loader: HTTPS validator scoped to Wazuh only

**Plan 2 assumes:** Task 5's `Config` Pydantic model has a field
validator `must_start_with_https` on `wazuh_api_url`, `defectdojo_url`,
and `regscale_url`, rejecting anything that doesn't begin with
`https://`.

**Reality:** Plan 1 ADR 0003 established RegScale CE serves on
`http://10.10.30.28` (port 80, no TLS wiring). Plan 1 ADR 0004
established DefectDojo 2.57.0 serves on `http://10.10.30.27:8080` (its
bundled nginx container has no cert). Both are deliberate lab-posture
decisions documented in `runbooks/cert-trust.md`. The validator as
written would `ValueError` at startup on every single pipeline
invocation.

**Realignment:** The HTTPS validator applies only to
`wazuh_api_url` and the new `wazuh_indexer_url` (see Deviation 5).
`defectdojo_url` and `regscale_url` are accepted as `http://` without
complaint. The validator becomes:

```python
@field_validator("wazuh_api_url", "wazuh_indexer_url")
@classmethod
def must_start_with_https(cls, v: str) -> str:
    if not v.startswith("https://"):
        raise ValueError(f"Wazuh endpoints must use https://: {v}")
    return v
```

No validator on the DefectDojo or RegScale URLs. The field-level
docstring references this ADR so a future reader understands the
asymmetry.

## Deviation 4 — Wazuh credential surface: hybrid env vars with defaults

**Plan 2 assumes:** Task 5 requires `WAZUH_API_URL`, `WAZUH_API_USER`,
`WAZUH_API_PASS` as three separate environment variables.

**Reality:** `/c/Projects/.env` contains only `WAZUH_API_PASSWORD`.
Parent `CLAUDE.md` convention states the Wazuh API user is always
`wazuh-wui` and the URL is always `https://10.10.20.30:55000` — these
are architectural constants, not configuration. Plan 1 established this
convention and uses it across every touchpoint (smoke scripts, ml-scorer,
Shuffle workflows, Grafana alerts).

**Realignment:** `load_config()` uses hybrid defaults — constants live
in code with comments pointing to this ADR, passwords are required from
env. The env var name for the password matches what already exists in
`.env`:

```python
# Wazuh infrastructure constants — architectural, not configurable
WAZUH_API_URL_DEFAULT     = "https://10.10.20.30:55000"
WAZUH_API_USER_DEFAULT    = "wazuh-wui"
WAZUH_INDEXER_URL_DEFAULT = "https://10.10.20.30:9200"
WAZUH_INDEXER_USER_DEFAULT = "admin"

# Required env vars (no defaults — secrets only)
REQUIRED_ENV_VARS = (
    "WAZUH_API_PASSWORD",
    "WAZUH_INDEXER_PASSWORD",
    "DEFECTDOJO_URL",
    "DEFECTDOJO_API_KEY",
    "REGSCALE_URL",
    "REGSCALE_USERNAME",
    "REGSCALE_PASSWORD",
)
```

A fork targeting a different Wazuh host can still override via env vars
— `os.environ.get("WAZUH_API_URL", WAZUH_API_URL_DEFAULT)` — without
editing any code. Secrets stay in `.env` only.

`WAZUH_INDEXER_PASSWORD` is new to `/c/Projects/.env`. Source of truth
is `/home/bchaplow/docker/wazuh/wazuh-docker/single-node/.env` on
brisket under `INDEXER_PASSWORD` (verified 2026-04-09). Task 1 copies
this into `/c/Projects/.env` as `WAZUH_INDEXER_PASSWORD` before any
pipeline task runs.

## Deviation 5 — Wazuh `/vulnerability` REST endpoint removed

**Plan 2 assumes:** Task 6 `WazuhClient.get_vulnerabilities(agent_id)`
hits `GET /vulnerability/{agent_id}?limit=1000` on the Wazuh API. Task
10's entire `ingest_wazuh_vulns()` pipeline consumes that response,
expecting fields `cve`, `cvss3_score`, `detection_time`, `name`,
`version`, `title`, `severity`, `external_references`.

**Reality:** Wazuh 4.8 rewrote the Vulnerability Detection module and
the agent-scoped REST endpoint was removed. Live probe against the
production manager (Wazuh v4.14.4) on 2026-04-09 with a valid
`wazuh-wui` JWT returned HTTP 404 for every variant:

```
HTTP 404  GET https://10.10.20.30:55000/vulnerability/016?limit=1
HTTP 404  GET https://10.10.20.30:55000/vulnerability
HTTP 404  GET https://10.10.20.30:55000/vulnerability/016/summary/cve
```

The data still exists — in the indexer (OpenSearch), not the API.
Index `wazuh-states-vulnerabilities-wazuh.manager` on the single-node
cluster at `https://10.10.20.30:9200` holds 12,949 documents (8.1 MB,
green health). All agents' vulnerability state is stored in this one
index, keyed by `agent.id` and `agent.name`. Sample document
structure (verified 2026-04-09):

```json
{
  "agent":         { "id": "016", "name": "dojo", "type": "Wazuh", "version": "v4.14.4" },
  "host":          { "os": { "full": "Ubuntu 24.04.4 LTS", ... } },
  "package":       { "name": "linux-image-...", "version": "6.8.0-106.106", "type": "deb" },
  "vulnerability": { "id": "CVE-...", "category": "Packages", "severity": "...",
                     "score": { "base": ... }, "detected_at": "...", ... }
}
```

**Realignment:**

1. **New module** `pipelines/common/wazuh_indexer.py` (Plan 2 Task 6b,
   not in the original plan). A thin OpenSearch client with basic-auth,
   retry-with-backoff, and a single `search_vulnerabilities()` method
   that accepts an agent name filter and returns raw hits with
   paging via `search_after`. TLS verification off (self-signed, same
   posture as Wazuh API per `runbooks/cert-trust.md`).

2. **`pipelines/common/wazuh.py` drops `get_vulnerabilities()`**. The
   REST client keeps `authenticate()`, `list_agents()`,
   `get_syscollector_os()`, `get_syscollector_hardware()`,
   `get_syscollector_packages()`. These endpoints were not affected by
   the 4.8 rewrite and still work.

3. **Task 10 `wazuh_vuln_to_finding()` field mapping is rewritten** to
   match the indexer document schema:

   | Old (REST)                  | New (indexer `_source`)                   |
   |-----------------------------|-------------------------------------------|
   | `raw['cve']`                | `hit['_source']['vulnerability']['id']`   |
   | `raw['cvss3_score']`        | `hit['_source']['vulnerability']['score']['base']` |
   | `raw['detection_time']`     | `hit['_source']['vulnerability']['detected_at']` |
   | `raw['name']` (package)     | `hit['_source']['package']['name']`       |
   | `raw['version']`            | `hit['_source']['package']['version']`    |
   | `raw['severity']`           | `hit['_source']['vulnerability']['severity']` |
   | `raw['title']`              | `hit['_source']['vulnerability']['description']` (truncated) |
   | `raw['external_references']`| `hit['_source']['vulnerability']['reference']` (string, wrapped in list) |

4. **Task 10 control mapping is unchanged.** Every wazuh-vuln finding
   still links to `RA-5` (Vulnerability Scanning) and `SI-2` (Flaw
   Remediation) — these are the controls a 3PAO expects regardless of
   the detection mechanism, and the mapping is semantic, not API-tied.

5. **Test surface adjusts.** The mocked response in
   `tests/test_wazuh_vulns_ingest.py` now mocks
   `WazuhIndexerClient.search_vulnerabilities()` returning a list of
   OpenSearch hits, not a list of REST items.

## Deviation 6 — Wazuh agent IDs 014/015 → 016/017

**Plan 2 assumes:** Dojo is Wazuh agent `014` and regscale is Wazuh
agent `015`. Task 1 Step 2 filters `.id == "014" or .id == "015"` to
verify reachability.

**Reality:** Per ADR 0002, haccp was already agent 014 and brisket
itself was 015 when Plan 1 enrolled the new hosts. Dojo was therefore
assigned `016` and regscale `017`.

**Realignment:** Every Plan 2 reference to agents 014/015 becomes
016/017. This is a mechanical substitution. The overlay.yaml in Task 7
already keys by agent *name* (not id) which is more robust — IDs drift
with enrollment order, names don't.

## Deviation 7 — RegScale CE has no long-lived API key

**Plan 2 assumes:** `REGSCALE_API_KEY` is a long-lived bearer token
that can be set in `.env` and used via `Authorization: Bearer
$REGSCALE_API_KEY` on every pipeline invocation. Task 1 Step 4, Task 5
config requirements, and Task 16 OSCAL push all use this pattern.

**Reality:** Per ADR 0003, RegScale CE only issues 24-hour JWTs via
`POST /api/authentication/login` with body `{"userName": "admin",
"password": "..."}`. The authenticating field is `userName` (not
`Email`). There is no personal access token flow documented in CE.
The 24-hour TTL means unattended runs must re-authenticate per
invocation, which is actually simpler than token rotation.

**Realignment:**

1. **New module** `pipelines/common/regscale.py` — `RegScaleClient`
   with JWT caching, re-auth on 401, retry-with-backoff. Same shape as
   the `WazuhClient` in Task 6. The auth flow mirrors
   `tests/smoke/check_regscale.sh`, which is the source of truth for
   the working login pattern.

2. **Env vars** are `REGSCALE_USERNAME` + `REGSCALE_PASSWORD` (already
   in `.env`), not `REGSCALE_API_KEY`. The config loader requires these.

3. **Task 1 Step 4 verification** is rewritten to demonstrate a full
   round-trip login: POST `/api/authentication/login`, receive JWT, GET
   `/api/seedingStatus` with `Authorization: Bearer <jwt>`, expect 200.
   This is what the smoke check already does, so Task 1 Step 4 reduces
   to `./pipelines.sh smoke-regscale`.

4. **Task 16** uses `RegScaleClient` from its OSCAL push code. No code
   anywhere in `pipelines/` references `REGSCALE_API_KEY`.

The 24-hour JWT TTL is adequate for Plan 2's scope — every pipeline
invocation is a fresh process and gets a fresh token. If a future phase
needs cross-process token sharing (e.g., a long-running webhook), that
would earn its own ADR.

## Deviation 8 — ADR numbering starts at 0006

**Plan 2 assumes:** Task 17 Step 4 writes `docs/adr/0003-pipelines-complete.md`.

**Reality:** ADRs 0001 through 0005 are occupied:
- 0001 — pre-flight and EULA review
- 0002 — Plan 1 deployment complete
- 0003 — RegScale install deviation
- 0004 — DefectDojo install deviation
- 0005 — PBS backup gap and automount fix

**Realignment:** Plan 2 numbering starts at **0006**, which is this
ADR. Further Plan-2-in-flight deviation ADRs (if any are needed beyond
what this ADR already covers) take 0007, 0008, ... sequentially. The
Plan 2 completion ADR lands at whatever number is free when Task 17
runs — likely **0007** if no further deviations surface, higher
otherwise. Plan 2 Task 17 will be updated at execution time to reflect
the actual number, not written against the hard-coded 0003 from the
plan text.

## Deviation 9 — Trestle 4.0.1 CLI drift

**Plan 2 assumes:** Compliance Trestle 3.4+. Uses `trestle create
system-security-plan -o mss-ssp` (Task 4 Step 1), `trestle href add`
(Task 3 Step 3), `trestle profile-resolve` (Task 3 Step 3).

**Reality:** Installed version is Trestle 4.0.1 (verified 2026-04-09,
`.venv/Scripts/python.exe -c "import trestle; print(trestle.__version__)"`).
Trestle 4 has shifted some command surfaces — Task 3 Step 3 and Task 4
Step 1 already anticipate this with fallback paths, but the preferred
path in 4.0.1 is:

- **Catalog/profile import:** `trestle import -f <path> -o <name>`
  (unchanged — verify at execution time)
- **SSP scaffold from profile:** `trestle author ssp-generate -p
  <profile-name> -o <ssp-name>` (use this directly; skip the deprecated
  `trestle create system-security-plan` path)
- **Profile resolution sanity check:** `trestle href` for the assembly
  pointer, then `trestle author profile -n <profile-name>` as the
  canonical 4.x resolution entry point

**Realignment:** Each Trestle subcommand is verified against `trestle
--help` in the corresponding task's Step 1 before use. If a command
shape has drifted further, the task's verification step will surface
it and a follow-up micro-commit documents the adjustment in this ADR's
"Amendments" section.

Also: Trestle 4.0.1 under Python 3.14 emits a `pydantic.v1 not fully
compatible` warning at import time. Imports still work (confirmed
2026-04-09). Task 2 adds a full catalog round-trip test (import ->
validate -> re-serialize -> validate) under 3.14 to prove the warning
is cosmetic at OSCAL schema scale before Plan 2 commits to the stack.

## Deviation 10 — Python 3.12 → 3.10/3.14 (already handled)

**Plan 2 assumes:** Python 3.12 in WSL.

**Reality:** `pyproject.toml` is already relaxed to `requires-python =
">=3.10"` (committed in Plan 1 Task `build: Python project scaffolding
(venv, deps, pipelines.sh, Makefile)`). Runtime environment is Python
3.14 via Git Bash + native Windows, with WSL Ubuntu 22.04's Python 3.10
as a secondary path. No code change needed; this entry exists solely
for Plan 2 text that mentions "Python 3.12" so the reader knows the
discrepancy is already reconciled.

## Deviation 11 — GSA/fedramp-automation repo removed; profile bootstrapped from Trestle plugin XML

**Plan 2 assumes:** Task 3 Step 1 downloads the FedRAMP Rev 5 Low
baseline profile JSON from
`https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LOW-baseline_profile.json`.
Plan 2 even anticipates that GSA "reorganizes their automation repo
periodically" and offers the fallback of searching the repo for the
current path.

**Reality:** The entire `GSA/fedramp-automation` repository is gone as
of 2026-04-09. The `GSA/fedramp-automation` URL returns HTTP 404, no
alternate branches or paths resolve, and the GitHub API's repo
metadata endpoint returns `Not Found`. The FedRAMP GitHub organization
(`FedRAMP/` — confirmed exists) hosts only `community`, `roadmap`,
`docs`, `docs-alpha`, `Marketplace-poc`, `fedramp-marketplace-preview`,
and `join`, plus FRMR documentation. None of these host OSCAL
baselines. NIST's `usnistgov/oscal-content` only hosts NIST-authored
content (catalogs, profiles, examples from SP 800-53), not FedRAMP
baselines. The Wayback Machine has no snapshot of the original
`GSA/fedramp-automation` file URL. Essentially, the canonical URL for
the FedRAMP Rev 5 Low baseline profile JSON no longer exists on the
open internet.

The **upstream content survives** in the
[`oscal-compass/compliance-trestle-fedramp`](https://github.com/oscal-compass/compliance-trestle-fedramp)
plugin repository. That plugin originally consumed GSA's repo as a
git submodule pinned before the delete, and a February 2024 commit
(`feat: updates content and git submodule for FedRAMP Rev5 validation`)
vendored the pinned snapshot into its own tree at
`trestle_fedramp/resources/fedramp-source/content/baselines/rev5/`.
**Only XML versions are in that snapshot** — no JSON peers. Trestle
4.0.1's `trestle import` explicitly refuses XML with
`Unsupported file extension .xml`.

**Realignment:** A one-shot Python bootstrap extractor was used to
read the upstream XML and generate a minimal OSCAL Profile JSON that
imports the local NIST catalog via
`trestle://catalogs/nist-800-53-rev5/catalog.json`. The extractor
preserves:

- Upstream UUID (`512149a6-7f04-4c01-bb1b-78eafd6a950d`)
- Title, version, published, last-modified, oscal-version
- All 156 `<with-id>` control references exactly

It does NOT carry across:

- Party definitions (FedRAMP PMO, JAB) and their contact/address blocks
- Role definitions and responsible-party bindings
- `<set-parameter>` and `<alter>` modify blocks
- Back-matter resources (logos, reference documents)

These omissions are documented in `oscal/profile/SOURCE.md` with the
rationale: they don't affect control coverage, profile resolution, or
SSP scaffolding, and they can be added selectively during Plan 3 (SSP
Authoring) if a specific control needs the FedRAMP-specific prose
text.

**Validation:** The generated profile passes `trestle validate`
(VALID). `trestle author profile-resolve -n fedramp-rev5-low -o
fedramp-rev5-low-resolved` produces a resolved catalog with exactly
156 controls when counted recursively (parents + enhancements),
matching the upstream XML's `<with-id>` count precisely — zero
missing, zero extra. The resolved catalog also passes `trestle
validate`. All acceptance criteria for Plan 2 Task 3 are met.

**Future re-fetch path:** If FedRAMP publishes an updated Rev 5 Low
baseline OSCAL profile at a new canonical location, the extractor can
be pointed at that URL and re-run in ~60 seconds. If a fidelity
upgrade is needed (parties, modify blocks, etc.), the path is to add
`saxonche` as a dev dependency, pull the NIST OSCAL XML-to-JSON XSLT,
and transform the full XML. That would be its own ADR amendment.

## Deferred — PBS backup-failure alerting

ADR 0002 Operator Action Item #2 (wire a Wazuh/Discord alert on PBS
backup failure) is intentionally *not* in Plan 2 scope. The real fix
requires research into PBS log shipping (LXC 300 via smoker, whether
PBS journals surface through the existing Wazuh agent, and which
Shuffle edge owns the Discord fanout) that would widen Plan 2 beyond
its OSCAL focus.

**Interim mitigation inside Plan 2 scope:** Task 1 adds a manual
tripwire to `runbooks/monthly-conmon.md` — a one-line SSH command the
operator runs daily to verify the most recent critical-job snapshot is
under 36 hours old. This is not a proper alert, but it is a tripwire
that keeps the gap visible until the dedicated phase lands.

**Long-term fix:** queued as a standalone follow-up phase. Will own
its own ADR (likely 0008+ depending on how many deviation ADRs
accumulate during Plan 2 execution).

## Branch strategy — direct commits to main

Plan 2 execution commits directly to `main`, same pattern as Plan 1.
No feature branch. Rationale:

- `homelab-fedramp-low` is a solo portfolio repo with no PR/review step
- Plan 1's history is on `main` (`plan-1-complete` tag on main);
  Plan 2 is a continuation of the same linear narrative
- Parent workspace CLAUDE.md sync protocol is main-centric
- Worktree-based isolation is ruled out by the parent workspace's
  established constraint that worktrees don't persist cleanly on
  Windows for agent-driven work
- Every task commit is atomic and verified; `git revert` is available
  as a rollback mechanism if a task fails mid-flight
- `plan-2-complete` tag at Task 17 provides the milestone boundary
  without requiring a merge commit

A reviewer following the portfolio chronologically sees every
deviation and every fix in the order it happened, which is the honest
story we want to tell.

## Consequences

**Positive:**

- Plan 2 tasks can be executed mechanically against the plan text with
  this ADR as the reference for every substitution. No mid-plan
  rediscovery of Plan 1 deviations.
- The Wazuh vuln ingest pivot is a bounded architectural change,
  documented with live probe evidence so a future reader understands
  *why* the code uses OpenSearch instead of the REST API.
- The RegScale JWT client becomes a reusable primitive that any future
  phase touching RegScale CE can depend on.
- The orchestration decision (passthrough from `pipelines.sh` to
  `pipelines/cli.py`) preserves the Plan 1 contract while giving us
  testable Python orchestration — both goals met.
- The HTTPS-validator asymmetry is honest about the lab posture
  without becoming a landmine.

**Negative / accepted:**

- Plan 2 is now 18 substantive tasks instead of 17 (the new Task 6b
  Wazuh Indexer client). Context budget for the execution session is
  meaningfully larger.
- The hybrid env-var approach (constants in code, passwords in `.env`)
  is slightly magic — a reader has to look at `load_config()` to
  discover defaults. Documented in the field-level docstrings.
- RegScale's 24-hour JWT means every pipeline invocation re-auths.
  Acceptable for monthly/daily cadence; would need revisiting if a
  long-running daemon ever touches RegScale.
- Plan 2 scope still does not close the PBS alert gap. The manual
  tripwire is a compromise, not a fix.

**Risks:**

- Further Trestle 4.0.1 CLI drift beyond what Task 2/3/4 anticipate.
  Mitigation: verify each subcommand against `trestle --help` at task
  execution time; document any further drift as ADR amendments below.
- RegScale CE OSCAL import endpoint paths may not match Task 16's
  guesses. Plan 2 Task 16 Step 1 already includes a Swagger discovery
  step; this ADR doesn't change that. If CE exposes no OSCAL import
  API at all, Task 16 falls back to a manual runbook, which is fine.
- Python 3.14 + Trestle 4.0.1 + pydantic.v1 compat warning might be
  more than cosmetic. Task 2 Step 4 catalog round-trip test is the
  early-warning tripwire; if it fails, Plan 2 pauses and we decide
  whether to pin an older Trestle or fall back to WSL Python 3.10.

## Amendments

*(Further deviations discovered during Plan 2 execution that fit this
ADR's scope rather than warranting a separate ADR are appended here
with date + task reference.)*

### 2026-04-09 (Task 2) — Future Python 3.16 tripwire

The OSCAL round-trip tests in `tests/test_oscal_roundtrip.py` pass
cleanly under Python 3.14 + Trestle 4.0.1, confirming Deviation 9's
"cosmetic warning" hypothesis. However, pytest surfaced a *second*
warning category that ADR 0006 didn't anticipate:

```
pydantic/v1/typing.py:77: DeprecationWarning: ForwardRef._evaluate is
a private API and is retained for compatibility, but will be removed
in Python 3.16. Use ForwardRef.evaluate() or typing.evaluate_forward_ref()
instead.
```

This is **not** the same warning as Deviation 9 — it's a Python 3.16
removal warning from `pydantic.v1.typing` using a private
`typing.ForwardRef._evaluate` API. When Python 3.16 releases, this
stops being a warning and becomes an `AttributeError`, at which point
Trestle 4.0.1 + pydantic.v1 will not import at all.

**Impact:** none today (we are on 3.14). Tripwire: the OSCAL round-trip
tests will start failing the moment Python 3.16 arrives on this
workstation. The failure will be fast, loud, and at test-collection
time rather than mid-pipeline.

**Mitigation when it fires:** pin Trestle to whatever version first
removes the pydantic.v1 shim entirely, OR pin Python to 3.15.x until
Trestle does so. The decision should be its own ADR at that time.

### 2026-04-09 (Task 4) — Trestle 4.0.1 `ssp-generate` output path

**Plan 2 assumed:** `trestle author ssp-generate -p fedramp-rev5-low -o
mss-ssp` writes to `trestle-workspace/system-security-plans/mss-ssp/`
(based on the workspace directory layout).

**Reality:** Trestle 4.0.1 writes the markdown scaffold to
`trestle-workspace/mss-ssp/` — a *top-level* directory named after the
SSP, not nested under `system-security-plans/`. The
`system-security-plans/` directory is reserved for assembled OSCAL
JSON artifacts produced by `ssp-assemble`.

**Impact:** trivial. The markdown directory is a human-editable
authoring surface; the assembled JSON path is separate. Task 15 (SSP
assembler wiring) needs to point `ssp-assemble -m mss-ssp` at the
top-level `mss-ssp/` directory, and the assembled output will land
under `trestle-workspace/system-security-plans/mss-ssp/system-security-plan.json`.

### 2026-04-09 (Task 1) — DefectDojo product names use ASCII hyphens

**Plan 2 assumed (Task 14):** `HOST_TO_PRODUCT` dictionary uses em
dashes in product names:

```python
HOST_TO_PRODUCT = {
    "brisket": "MSS Core — brisket",
    "haccp": "MSS Log Analytics — haccp",
    ...
}
```

**Reality:** Plan 1 Task 11's DefectDojo seed script created the
products with ASCII hyphens (`-`), not em dashes (`—`). Queried the
live API during Task 1 pre-flight:

```
id=1  MSS Core - brisket
id=2  MSS Log Analytics - haccp
id=3  MSS Network Sensors - smokehouse
id=4  MSS Boundary Protection - OPNsense
id=5  MSS GRC Tooling - dojo + regscale
```

**Additional finding:** there are **5 products**, not 4 — a **5th
product `MSS Boundary Protection - OPNsense`** exists that Plan 2 Task
14 doesn't map at all. OPNsense inventory (the boundary firewall on
10.10.10.1, documented in `inventory/overlay.yaml` under
`non_agent_assets`) needs to route to product id=4 during Task 14.

**Realignment for Task 14:** `HOST_TO_PRODUCT` uses ASCII hyphens and
adds `opnsense` → `MSS Boundary Protection - OPNsense`. Any unit test
assertions in Task 11/14 that reference product names should be
written against the real strings, not Plan 2's em-dash text.

---

**Next:** Plan 2 Task 1 (Verify Plan 1 done state and capture
environment). Task 1 itself is adjusted per this ADR — see Task 1
execution notes for the specific step substitutions.
