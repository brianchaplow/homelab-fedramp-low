# Runbook: Monthly ConMon Cycle

## Scope

Run the monthly FedRAMP Low Continuous Monitoring cycle on the homelab
system: ingest scan outputs, update the POA&M, regenerate the IIW, and
produce the submission package.

## Status

**STUB -- Plan 1 complete, Plan 2 pipelines IN PROGRESS as of 2026-04-09.**

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
- `/c/Projects/.env` has: `DEFECTDOJO_API_KEY`, `DEFECTDOJO_URL`,
  `REGSCALE_USERNAME`, `REGSCALE_PASSWORD`, `REGSCALE_URL`,
  `WAZUH_API_PASSWORD`, `WAZUH_INDEXER_PASSWORD`
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

## Daily PBS backup tripwire (interim -- run once per day)

Until the proper Wazuh/Discord alert is wired (see "Follow-up TODO"
below), the operator runs this one-line check each morning as a
tripwire. It will catch a silent PBS failure within 24 hours, which is
the gap that originally let ADR 0005's 5-day backup hole go unnoticed.

```bash
ssh root@10.10.30.21 "pct exec 300 -- find /mnt/pbs-store/data/vm -maxdepth 2 -name '*2026*' -mtime -2 -printf '%T+  %p\n' 2>/dev/null | sort -r | head -10"
```

Expected: at least one snapshot per day for each of VM 100 (DC01), VM
101 (WS01), VM 200 (TheHive), VM 201 (dojo), VM 301 (regscale). If any
VM has no snapshot under 36 hours old, investigate immediately -- PBS
has silently stopped backing up that host.

A faster one-liner that just alarms if anything is stale:

```bash
ssh root@10.10.30.21 "pct exec 300 -- bash -c 'for vm in 100 101 200 201 301; do latest=\$(ls -t /mnt/pbs-store/data/vm/\$vm 2>/dev/null | head -1); age=\$(find /mnt/pbs-store/data/vm/\$vm/\$latest -maxdepth 0 -mmin +2160 2>/dev/null); [ -n \"\$age\" ] && echo \"STALE: vm \$vm latest=\$latest\" || echo \"ok: vm \$vm\"; done'"
```

Expected: five `ok: vm <id>` lines. Any `STALE:` line is a fault.

## Backup verification (monthly)

Once per month during the ConMon cycle, also confirm the full snapshot
cadence for the GRC VMs:

```bash
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/201/ | tail -5'
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/301/ | tail -5'
```

Expected: a snapshot for each of the last 3 calendar days.

## Follow-up TODO -- proper PBS alert wiring (deferred per ADR 0006)

**Wire a Wazuh/Discord alert on PBS backup job failure.** The 5-day gap
documented in ADR 0005 went unnoticed because the only notification
target was `mail-to-root` on the PBS LXC, which nobody reads.

This was originally queued for Plan 2 but deferred out of scope per ADR
0006 §"Deferred -- PBS backup-failure alerting" because the real fix
requires dedicated research into PBS log shipping (LXC 300 via smoker,
whether PBS journals surface through the existing Wazuh agent, and
which Shuffle edge owns the Discord fanout) that would widen Plan 2
beyond its OSCAL focus.

The daily tripwire above is the interim mitigation until a dedicated
follow-up phase lands. When that phase executes, it should:

- Add a Wazuh custom rule tailing the PBS log file or the Proxmox
  backup job API endpoint (`/cluster/backup-info/not-backed-up`)
- Route to a Shuffle workflow that posts to `$discord_webhook_infra`
- Acceptance: deliberately break the PBS mount, wait for the next
  backup window, confirm the Discord alert fires
- Earn its own ADR at whatever number is free at that time
