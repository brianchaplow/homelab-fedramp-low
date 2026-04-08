# Runbook: Restore a Plan 1 VM from PBS

## Scope

Restore `dojo` (VMID 201 on pitcrew) or `regscale` (VMID 301 on smoker)
from a PBS backup snapshot living on PBS LXC 300 (on smoker, NFS-backed
to smokehouse via `10.10.20.10:/pbs-datastore`).

## Prerequisites

- PBS LXC 300 running on smoker (`ssh root@10.10.30.21 'pct status 300'`)
- PBS NFS mount active (see `docs/adr/0005-pbs-backup-gap-and-automount-fix.md`)
- Backup snapshot exists for target VMID (verify via commands below)

## Verify available snapshots

From any host with the PBS CLI installed (or from inside LXC 300):

```bash
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/201/ | tail -5'   # dojo
ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/301/ | tail -5'   # regscale
```

Snapshot directory names are ISO-8601 UTC timestamps like
`2026-04-08T17:26:22Z`.

## Restore dojo (pitcrew)

```bash
ssh root@10.10.30.20

# 1. Stop the broken VM (ignore error if already stopped)
qm stop 201 2>/dev/null || true

# 2. Preserve the config file so you can diff it after restore
cp /etc/pve/qemu-server/201.conf /root/201.conf.pre-restore

# 3. Restore from the PBS snapshot. Use the `pbs-backup:vm/201/<snapshot>`
#    locator that pvesm recognizes. List available snapshots first:
pvesm list pbs-smokehouse --vmid 201 | tail -5

# 4. Pick the desired snapshot (most recent or a specific timestamp) and
#    restore. This rewrites the local-lvm disk in place, so be sure.
qmrestore pbs-smokehouse:backup/vm/201/<ISO-timestamp> 201 --storage local-lvm --force

# 5. Start the VM
qm start 201
```

Wait 60 seconds, then verify:

```bash
ssh ubuntu@10.10.30.27 'uptime && docker compose -f ~/defectdojo/docker-compose.yml ps --format "table {{.Name}}\t{{.Status}}"'
```

Expected: DefectDojo containers (nginx, uwsgi, celeryworker, celerybeat,
postgres, valkey) all `Up`. Run the smoke check from PITBOSS:

```bash
./pipelines.sh smoke-dojo
```

## Restore regscale (smoker)

Same pattern with VMID 301 on `smoker` (10.10.30.21), using the smoker
backup job output location `/mnt/pbs-store/data/vm/301/`:

```bash
ssh root@10.10.30.21
qm stop 301 2>/dev/null || true
cp /etc/pve/qemu-server/301.conf /root/301.conf.pre-restore
pvesm list pbs-smokehouse --vmid 301 | tail -5
qmrestore pbs-smokehouse:backup/vm/301/<ISO-timestamp> 301 --storage local-lvm --force
qm start 301
```

Wait 2 minutes (RegScale SQL Server migration wave takes longer than
DefectDojo), then verify:

```bash
ssh ubuntu@10.10.30.28 'uptime && docker compose -f ~/regscale/docker-compose.yml ps --format "table {{.Name}}\t{{.Status}}"'
./pipelines.sh smoke-regscale
```

Expected: atlas + atlas-db both `Up`, smoke check PASS.

## First-time restore drill

A restore drill should be performed within 7 days of initial Plan 1
completion. Document the drill results in a new ADR:
`docs/adr/NNNN-restore-drill.md`. Capture:

- Snapshot timestamp chosen
- Time-to-restore (from `qmrestore` start to successful smoke check)
- Any manual remediation needed (e.g., re-running
  `deploy/regscale/reset-admin-password.sh` if the restored image doesn't
  reflect the latest password rotation)

## Gotchas

- **Do not run `qm destroy` before `qmrestore`.** `qmrestore --force` rewrites
  the disk in place without destroying the VM entry. Running `destroy` first
  wipes the MAC address, which breaks cloud-init state and the UFW rules
  may not reapply cleanly.
- **MAC address drift.** If you ever see the restored VM come up with a
  different MAC than the original (`BC:24:11:DE:F0:01` for dojo, `:02` for
  regscale), cloud-init has regenerated the NIC. Re-pin the MAC with
  `qm set <VMID> --net0 virtio=<MAC>,bridge=vmbr0`.
- **PBS NFS mount.** If the restore fails with `unable to open chunk store`,
  the NFS mount on PBS LXC 300 has dropped. See
  `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` for the remount
  procedure and the `x-systemd.automount` hardening that should prevent
  this at boot time.
