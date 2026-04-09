# Proxmox VM Deployment Runbook

This directory contains the VM configs for the two new VMs created in
Plan 1: `dojo` (DefectDojo) on pitcrew and `regscale` (RegScale CE) on
smoker.

## Files

| File | Purpose |
|---|---|
| `dojo-vm-config.yaml` | DefectDojo host VM config + deviation notes (VMID 201 on pitcrew) |
| `regscale-vm-config.yaml` | RegScale CE host VM config + deviation notes (VMID 301 on smoker) |

## Network assignments

| VM | IP | VLAN | Proxmox host | VMID | MAC |
|---|---|---|---|---|---|
| dojo | 10.10.30.27 | 30 (untagged) | pitcrew (10.10.30.20) | 201 | BC:24:11:DE:F0:01 |
| regscale | 10.10.30.28 | 30 (untagged) | smoker (10.10.30.21) | 301 | BC:24:11:DE:F0:02 |

Both hosts run Proxmox VE 9.1.6. Neither is part of a cluster (no corosync),
which is why VMID 201 and 301 can coexist — one on each node, they never
conflict because there is no shared cluster VMID namespace.

## Resource reservations

Each VM: 4 vCPU / 6 GB RAM / 40 GB disk, `local-lvm` thin storage.

PBS backups:

- **dojo (VMID 201)** added to the existing daily critical backup job on
  pitcrew (`1da17d50-2183-4592-946b-47e956174e0a`, schedule `02:00`,
  storage `pbs-smokehouse`) alongside DC01/WS01/TheHive.
- **regscale (VMID 301)** gets a **new** daily backup job on smoker
  (`851dfd63-cbf4-464a-b394-0cc985de3810`, schedule `02:30`,
  storage `pbs-smokehouse`). The 02:30 offset from pitcrew's 02:00
  avoids PBS datastore contention at the nightly window. The existing
  weekly target-VM job on smoker (Sun 03:00) is untouched.

## Deviations applied to both VMs (from ADR 0001 pre-flight)

These four deviations were applied to both dojo and regscale during
`qm create`. Hard-code them in any future recreation:

1. **No VLAN tag on net0.** `vmbr0` on both pitcrew and smoker is VLAN 30
   untagged. Adding `tag=30` double-tags the frames and breaks network
   connectivity. Use `virtio=<MAC>,bridge=vmbr0` with no tag.
2. **Pin the MAC upfront.** `virtio=BC:24:11:DE:F0:01` for dojo,
   `BC:24:11:DE:F0:02` for regscale. Editing net0 after the fact churns
   the MAC and permanently breaks cloud-init's NIC identity.
3. **Modern boot syntax.** `qm set <VMID> --boot "order=scsi0"` — the
   legacy `--boot c --bootdisk scsi0` is silently accepted by Proxmox
   9.1.6 but produces a VM that hangs at the serial console and never
   boots into Linux.
4. **Ubuntu 24.04 cloud image uses `eth0`, not `ens18`.** Any
   verification command that `ip addr show dev <iface>` must use `eth0`.

## To recreate from scratch

Both VMs follow the same pattern. From the respective Proxmox host as
root:

```bash
# 1. Download Ubuntu 24.04 cloud image if missing
cd /var/lib/vz/template/iso
[ -f noble-server-cloudimg-amd64.img ] || \
  wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# 2. Create the VM (substitute VMID, NAME, MAC per the table above)
qm create <VMID> \
  --name <NAME> \
  --memory 6144 \
  --cores 4 \
  --cpu host \
  --net0 virtio=<MAC>,bridge=vmbr0 \
  --ostype l26 \
  --scsihw virtio-scsi-single \
  --agent enabled=1

# 3. Import the cloud image as scsi0
qm importdisk <VMID> /var/lib/vz/template/iso/noble-server-cloudimg-amd64.img local-lvm
qm set <VMID> --scsi0 local-lvm:vm-<VMID>-disk-0,discard=on,ssd=1
qm resize <VMID> scsi0 +38G

# 4. Cloud-init drive + boot order
qm set <VMID> --ide2 local-lvm:cloudinit
qm set <VMID> --boot "order=scsi0"
qm set <VMID> --serial0 socket --vga serial0

# 5. Cloud-init static IP + SSH keys from the host's /etc/pve/priv/authorized_keys
TMPKEY=$(mktemp)
cat /etc/pve/priv/authorized_keys > $TMPKEY
qm set <VMID> \
  --ipconfig0 "ip=<VM_IP>/24,gw=10.10.30.1" \
  --nameserver "10.10.10.1" \
  --searchdomain "local" \
  --ciuser ubuntu \
  --cipassword "$(openssl rand -base64 24)" \
  --sshkey "$TMPKEY"
rm -f $TMPKEY

# 6. Start
qm start <VMID>
```

Then, once SSH is reachable, install the **QEMU Guest Agent package** inside
the VM. The `--agent enabled=1` flag above only wires up the virtio-serial
device on the hypervisor side; the guest still needs the agent daemon
running to respond to `guest-ping` and `fs-freeze`. Without it, vzdump
snapshots are taken without freezing the filesystem (still works, just
not strictly crash-consistent), and you'll see warnings like:

```
VM <VMID> qga command 'guest-ping' failed - got timeout
skipping guest-agent 'fs-freeze', agent configured but not running?
```

Install on the guest:

```bash
# On the VM, as ubuntu:
sudo apt-get install -y qemu-guest-agent
# Ubuntu 24.04 socket-activates the unit — no systemctl enable needed,
# just start it and reboot-on-install is fine too:
sudo systemctl start qemu-guest-agent
```

Then verify from the Proxmox host:

```bash
qm agent <VMID> ping && echo OK
```

Then continue with the service-specific runbook:

- dojo: `deploy/defectdojo/README.md`
- regscale: `deploy/regscale/README.md`

## Rollback

To tear a VM down and start over:

```bash
qm stop <VMID> 2>/dev/null || true
qm destroy <VMID> --purge
```

PBS snapshots for the VM are NOT deleted by `qm destroy --purge` — they
remain in the datastore and can be used with `qmrestore` (see
`runbooks/restore-from-pbs.md`).
