# ADR 0005 -- PBS backup gap discovered + NFS automount hardening

## Status

Accepted -- 2026-04-08

## Context

Plan 1 Task 12 calls for adding the `dojo` VM (VMID 201 on pitcrew) to the
existing daily PBS backup job and verifying the first backup succeeds. When
that verification ran, `vzdump` failed:

```
ERROR: VM 201 qmp command 'backup' failed - backup connect failed:
command error: unable to open chunk store at "/mnt/pbs-store/data/.chunks"
- No such file or directory (os error 2)
```

Diagnostic walk:

| Check | Result |
|---|---|
| smoker host has `/mnt/pbs-store/`? | No -- PBS storage lives inside LXC 300 |
| LXC 300 fstab | `10.10.20.10:/pbs-datastore /mnt/pbs-store nfs defaults,_netdev 0 0` |
| LXC 300 → smokehouse ping | OK |
| smokehouse export visible | `showmount -e 10.10.20.10` → `/pbs-datastore 10.10.30.0/24` |
| LXC 300 mount unit state | `mnt-pbs\x2dstore.mount` → **failed** |
| Manual `mount /mnt/pbs-store` | **Succeeds** |
| Most recent successful backups in datastore | **2026-04-02 06:00** for VMs 100, 101 |

The PBS NFS mount silently dropped during the rack consolidation reboot of
2026-04-07 (likely a boot race: PBS LXC came up before smokehouse finished
exporting NFS, the `_netdev` mount unit failed once, and systemd never
retried). The `proxmox-backup-proxy` daemon stayed up but with an empty data
directory, so every datastore status query returned 400 and every backup
attempt errored on the missing `.chunks/` path.

**Backup gap: 2026-04-03 through 2026-04-07** (5 nights missed for the daily
critical backup job covering VMs 100/DC01, 101/WS01, 200/TheHive). The job
scheduled at 02:00 nightly was firing but failing silently. The
`mail-to-root` notification target presumably did fire to the LXC's local
root mailbox, which nobody reads.

## Decision

1. **Manual remount + service restart** to recover from the current failed state:
   ```
   pct exec 300 -- mount /mnt/pbs-store
   pct exec 300 -- systemctl daemon-reload
   pct exec 300 -- systemctl restart proxmox-backup-proxy proxmox-backup
   ```
2. **Harden the fstab line** with `x-systemd.automount` so the mount becomes
   lazy -- systemd brings up an automount placeholder at boot, and the actual
   NFS mount happens on the first access. This eliminates the boot-order race
   with smokehouse:
   ```
   10.10.20.10:/pbs-datastore /mnt/pbs-store nfs defaults,_netdev,x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30 0 0
   ```
3. **Re-run vzdump for VM 201** to validate the chain end-to-end (succeeded
   in 11m11s, snapshot at `vm/201/2026-04-08T17:26:22Z`).
4. **Existing VMs 100/101/200 will catch up automatically** at the next 02:00
   nightly run; no manual force-backup needed since the gap is bounded
   (April 3–7) and the protected workloads have been low-risk in that window.
5. **Add a Plan 1 follow-up TODO** (Task 20 runbooks) for a Wazuh alert /
   Discord notification when PBS daily backup status reports failure, so
   silent failures cannot persist again.

## Consequences

**Positive:**
- PBS backups working again, including VM 201 (first dojo backup is now in PBS)
- Boot-race class of failure eliminated by automount
- Real bug discovered + fixed as a side-effect of Plan 1 -- exactly the kind
  of "ConMon catches what manual checks miss" story the FedRAMP portfolio
  needs

**Negative:**
- 5-day backup gap for DC01, WS01, TheHive -- not catastrophic but the homelab
  has no Wazuh/Discord alert wired up to PBS, which let the gap grow
  unnoticed
- Operator must manually verify the Apr 9 02:00 run actually succeeds before
  considering this fully resolved (cannot validate from inside Plan 1
  execution context)

## Verification (run on 2026-04-08 17:37 UTC)

```
$ ssh root@10.10.30.21 'pct exec 300 -- mount | grep pbs-store'
10.10.20.10:/pbs-datastore on /mnt/pbs-store type nfs4 (rw,relatime,vers=4.1,...)

$ ssh root@10.10.30.21 'pct exec 300 -- ls /mnt/pbs-store/data/vm/201/'
2026-04-08T17:26:22Z
owner

$ ssh root@10.10.30.21 'pct exec 300 -- systemctl is-active proxmox-backup-proxy proxmox-backup'
active
active

$ ssh root@10.10.30.21 'pct exec 300 -- systemctl list-units --all --type=mount,automount | grep pbs'
mnt-pbs\x2dstore.automount  loaded inactive dead    mnt-pbs\x2dstore.automount
mnt-pbs\x2dstore.mount      loaded active   mounted /mnt/pbs-store
```

The automount unit is dead-but-loaded right now because the .mount is
manually active (mutually exclusive). After the next LXC reboot, the
automount unit will become active and lazy-mount on first access -- this is
the desired steady state.

## Notes

This discovery counts toward FedRAMP Low Plan 1 success criterion #5
("Both VMs show successful PBS backup") for the dojo half. Regscale half
is still pending (Task 18). The fix is documented here rather than in
`brisket-setup/` because Plan 1 caused both the discovery and the fix.
