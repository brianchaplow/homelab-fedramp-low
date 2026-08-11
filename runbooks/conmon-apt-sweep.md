# PATCH-01 weekly core-node patch sweep

## Scope and current state

This is the repository design for hardening the weekly Ubuntu patch sweep on
the two core SOC nodes:

- `haccp`: ELK, Fleet, Logstash, Arkime, and the Wazuh agent
- `brisket`: Wazuh, Shuffle, OpenCTI, Velociraptor, Grafana, the ML scorer,
  Prometheus blackbox probes, and the Wazuh agent

The repository changes do not install package holds, deploy files, change live
cron, refresh APT metadata, upgrade packages, or restart services. The legacy
`runbooks/conmon-apt-sweep.cron` is intentionally inert. Install exactly one
host-specific cron file only after completing the staged procedure below.

The older dojo and regscale sweep deployments are outside PATCH-01. Do not
replace their scripts with this core-node revision until meaningful host gates
are designed and tested for those workloads.

## Safety contract

`conmon-apt-sweep.sh` fails closed unless every condition below is true:

1. It is running as root on `haccp` or `brisket`, and the optional cron host
   assertion matches the actual short hostname.
2. It acquires a non-blocking local `flock` for the full run.
3. The root filesystem and Docker data filesystem each have at least 5 GiB
   free.
4. Docker and containerd are active, and the following installed packages are
   all explicitly held:

   - `docker-ce`
   - `docker-ce-cli`
   - `docker-ce-rootless-extras`
   - `containerd.io`
   - `docker-buildx-plugin`
   - `docker-compose-plugin`

5. The APT transaction simulation succeeds, contains no removals, and contains
   no install, configure, or removal action for a protected runtime package.
6. The host-specific PRE health gate passes before any package upgrade.
7. The real transaction uses `apt-get upgrade --no-remove`, refuses held-package
   changes, keeps existing configuration files, and sets `NEEDRESTART_MODE=l`.
   The wrapper does not issue a service restart command.
8. Protected package versions and the Docker/containerd daemon PIDs are
   identical before and after the transaction.
9. The same host-specific health gate passes after the transaction.

Only after step 9 does the script atomically replace:

```text
/var/lib/conmon-apt-sweep/last-clean-completion
```

The file contains one UTC epoch value. A failure never creates or refreshes
the heartbeat, and a preflight-only run never publishes it. An `END` log marker
therefore means all postchecks and heartbeat publication completed. A `FAILED`
marker or stale heartbeat is an actionable sweep failure.

The script does not reboot the host. Kernel updates remain pending until a
separately approved maintenance window.

## Health gates

### haccp

The PRE and POST gates require:

- Docker and containerd active and queryable
- `elk-es01-1`, `elk-kibana-1`, `elk-logstash-1`, and
  `elk-fleet-server-1` running, with no unhealthy/starting Docker health state
- authenticated Elasticsearch cluster state of green or yellow, using the
  credential already inside the Elasticsearch container so it is not exposed
  in the host process list or log
- Kibana returning HTTP 200 or 302 over its local HTTP endpoint
- `arkimecapture`, `arkimeviewer`, and `wazuh-agent` active

### brisket

The PRE and POST gates require Docker, containerd, and `wazuh-agent`, plus the
documented local responses for Wazuh Dashboard/API, Shuffle, OpenCTI,
Velociraptor, Grafana, and the ML scorer. The final end-to-end gate queries
Prometheus for `probe_success == 0` and requires an empty result.

These checks establish the named capabilities at the host boundary. They do
not prove end-to-end event delivery through every downstream workflow. Keep
the broader detection-canary and off-host sentinel observation requirements
separate.

## Serial canary schedule

The proposed schedules are 24 hours apart:

| Stage | Host | Repository cron file | Schedule |
|---|---|---|---|
| Canary | haccp | `conmon-apt-sweep.haccp.cron` | Sunday 04:00 host-local |
| Promoted | brisket | `conmon-apt-sweep.brisket.cron` | Monday 04:00 host-local |

Do not enable both schedules together during initial rollout. Promote brisket
only after haccp produces a clean heartbeat, a clean `END` marker, passing
post-health evidence, and a full observation period through the following
day. The initial observed BEGIN/END timestamps are the non-overlap proof.

The 24-hour separation is a blast-radius control, not a distributed lock. An
off-host monitor must treat a stale or failed haccp heartbeat as a stop signal
for the next brisket window. Until that alert-to-suppression path is automated,
the operator must disable or defer the brisket cron before its Monday window
when the haccp canary is not clean.

## Repository validation

These checks are isolated. The regression harness substitutes every APT,
systemd, Docker, disk, hostname, and HTTP interaction:

```bash
bash -n runbooks/conmon-apt-sweep.sh runbooks/test-conmon-apt-sweep.sh
bash runbooks/test-conmon-apt-sweep.sh
git ls-files --eol -- \
  runbooks/conmon-apt-sweep.sh \
  runbooks/test-conmon-apt-sweep.sh \
  'runbooks/conmon-apt-sweep*.cron'
git diff --check
```

The harness covers successful haccp and brisket profiles, missing holds,
protected-package simulation, APT failure, low disk, lock contention, runtime
version/PID change, host mismatch, host-specific health failures, post-upgrade
health failure, stale-heartbeat preservation, and no-heartbeat preflight mode.

## Remaining deployment procedure

All commands in this section are future operator actions. They have not been
run by this repository change.

1. Record the reviewed Git revision and SHA-256 of the script and three cron
   files in the PATCH-01 evidence record.
2. On haccp, confirm the six packages are installed. Apply the holds explicitly:

   ```bash
   sudo apt-mark hold docker-ce docker-ce-cli docker-ce-rootless-extras \
     containerd.io docker-buildx-plugin docker-compose-plugin
   ```

3. Copy the reviewed script to `/usr/local/sbin/conmon-apt-sweep.sh` with mode
   `0750 root:root`. Verify the live SHA-256 matches the reviewed source.
4. Run the read-only control path before scheduling:

   ```bash
   sudo /usr/local/sbin/conmon-apt-sweep.sh \
     --expected-host haccp --preflight-only
   ```

   Confirm `PREFLIGHT PASS`, no `END` marker, no new heartbeat, and no package
   or service state change.
5. Install `conmon-apt-sweep.haccp.cron` as
   `/etc/cron.d/conmon-apt-sweep` with mode `0644 root:root`. Validate with the
   system cron parser available on the host. Do not manually invoke the live
   upgrade merely to accelerate evidence collection.
6. Observe the next natural haccp run. Preserve the BEGIN/END timestamps, APT
   simulation, hold assertions, unchanged package versions/PIDs, PRE/POST gate
   results, heartbeat epoch, and off-host monitoring state.
7. Observe haccp through the following day. If any gate, service, ingestion,
   or heartbeat check is not clean, do not promote brisket.
8. Repeat steps 2 through 4 on brisket with `--expected-host brisket`.
9. Only after the haccp canary evidence is accepted, install
   `conmon-apt-sweep.brisket.cron` on brisket. Observe its next natural Monday
   run and preserve the same evidence set.
10. Compare haccp END and brisket BEGIN timestamps to prove the first runs did
    not overlap. Keep the schedules disabled if that evidence is ambiguous.
11. Add both heartbeats to the off-host liveness/DMS monitor with an SLA that
    tolerates one missed weekly run, then observe at least two natural cycles
    before closing PATCH-01.

Any future container-runtime update is a separate maintenance change. Remove
holds only inside that approved window, perform its own dry run and service
impact review, and restore all six holds before re-enabling this sweep.
