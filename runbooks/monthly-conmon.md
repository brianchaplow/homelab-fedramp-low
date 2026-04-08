# Runbook: Monthly ConMon Cycle

## Scope

Run the monthly FedRAMP Low Continuous Monitoring cycle on the homelab
system: ingest scan outputs, update the POA&M, regenerate the IIW, and
produce the submission package.

## Status

**STUB — Plan 1 complete, Plan 2 pipelines pending.**

This runbook will be filled in once Plan 2 implements the OSCAL pipelines.
Until then, the only action taken for the monthly cycle is a smoke check:

```bash
cd /c/Projects/homelab-fedramp-low
./pipelines.sh smoke
```

Expected: both DefectDojo and RegScale CE reachable, JWT round-trips.

## Prerequisites (when Plan 2 lands)

- All Plan 1 infrastructure verified and green (`./pipelines.sh smoke`)
- All Plan 2 pipelines installed and callable
- `/c/Projects/.env` has: `DEFECTDOJO_API_KEY`, `REGSCALE_PASSWORD`,
  `WAZUH_API_PASSWORD`, `DEFECTDOJO_URL`, `REGSCALE_URL`
- The dojo and regscale VMs are both backing up daily to PBS (see
  `docs/adr/0005` for the backup chain)

## Procedure (to be filled in after Plan 2)

Planned outline, subject to refinement during Plan 2:

1. **Ingest:** Pull the last 30 days of vulnerability findings from Wazuh
   into DefectDojo via the DefectDojo API
2. **Triage:** Run the DefectDojo SLA engine against the FedRAMP Low ConMon
   SLA (30/90/180/365 days per severity)
3. **POA&M update:** Export any findings past or approaching SLA into the
   `FedRAMP-POAM-Template-Rev5.xlsx` master POA&M file
4. **OSCAL generate:** Use compliance-trestle to regenerate
   `system-security-plan.json` and `assessment-results.json` from the
   updated POA&M state
5. **Reg sync:** Push the new POA&M rows and OSCAL artifacts into RegScale CE
   via the JWT-authenticated API
6. **Package:** Zip the submission package (OSCAL JSON + filled POA&M +
   IIW + month-over-month delta) into `submissions/YYYY-MM/`
7. **Commit:** Create a signed git commit tagged `conmon-YYYY-MM` with the
   submission folder

## Temporary: Smoke-only mode

Until steps 1-7 above are implemented, run only the smoke check on or
near the first of each month to confirm infrastructure is healthy:

```bash
cd /c/Projects/homelab-fedramp-low
./pipelines.sh smoke
```

Expected:

```
DefectDojo OK at http://10.10.30.27:8080 (api=403 login=200)
RegScale OK at http://10.10.30.28 (root=200 login=200 seedingstatus=200, JWT round-trips)
All smoke checks passed.
```

## Backup verification

Also confirm both VMs have been backing up daily:

```bash
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/201/ | tail -5'
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/301/ | tail -5'
```

Expected: a snapshot for each of the last 3 calendar days.

## Follow-up TODO captured from Plan 1 Task 12 discovery

**Wire a Wazuh/Discord alert on PBS backup job failure.** The 5-day gap
documented in ADR 0005 went unnoticed because the only notification
target was `mail-to-root` on the PBS LXC, which nobody reads. A Plan 2
sub-task should:

- Add a Wazuh custom rule tailing PBS log file or the Proxmox backup job
  API endpoint (`/cluster/backup-info/not-backed-up`)
- Route to Shuffle WF that posts to `$discord_webhook_infra`
- Acceptance: deliberately break the PBS mount, wait for next backup
  window, confirm the Discord alert fires
