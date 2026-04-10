---
x-trestle-add-props: []
  # Add or modify control properties here
  # Properties may be at the control or part level
  # Add control level properties like this:
  #   - name: ac1_new_prop
  #     value: new property value
  #
  # Add properties to a statement part like this, where "b." is the label of the target statement part
  #   - name: ac1_new_prop
  #     value: new property value
  #     smt-part: b.
  #
x-trestle-set-params:
  # You may set values for parameters in the assembled SSP by adding
  #
  # ssp-values:
  #   - value 1
  #   - value 2
  #
  # below a section of values:
  # The values list refers to the values in the resolved profile catalog, and the ssp-values represent new values
  # to be placed in SetParameters of the SSP.
  #
  cp-09_odp.01:
    alt-identifier: cp-9_prm_1
    profile-values:
      - dojo (VMID 201 on pitcrew), regscale (VMID 301 on smoker), DC01 (VMID 100 on pitcrew), WS01 (VMID 101 on pitcrew), TheHive (VMID 200 on pitcrew)
    profile-param-value-origin: organization
  cp-09_odp.02:
    alt-identifier: cp-9_prm_2
    profile-values:
      - daily (02:00 pitcrew job; 02:30 smoker job)
    profile-param-value-origin: organization
  cp-09_odp.03:
    alt-identifier: cp-9_prm_3
    profile-values:
      - daily (same PBS jobs; vzdump captures full VM image including OS, middleware, and application layers)
    profile-param-value-origin: organization
  cp-09_odp.04:
    alt-identifier: cp-9_prm_4
    profile-values:
      - per-commit push to origin/main (ad-hoc); Git history serves as the versioned documentation backup
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cp-09
---

# cp-9 - \[Contingency Planning\] System Backup

## Control Statement

- \[a.\] Conduct backups of user-level information contained in [system components] [frequency];

- \[b.\] Conduct backups of system-level information contained in the system [frequency];

- \[c.\] Conduct backups of system documentation, including security- and privacy-related documentation [frequency] ; and

- \[d.\] Protect the confidentiality, integrity, and availability of backup information.

## Control Assessment Objective

- \[CP-09a.\] backups of user-level information contained in [system components] are conducted [frequency];

- \[CP-09b.\] backups of system-level information contained in the system are conducted [frequency];

- \[CP-09c.\] backups of system documentation, including security- and privacy-related documentation are conducted [frequency];

- \[CP-09d.\]

  - \[CP-09d.[01]\] the confidentiality of backup information is protected;
  - \[CP-09d.[02]\] the integrity of backup information is protected;
  - \[CP-09d.[03]\] the availability of backup information is protected.

## Control guidance

System-level information includes system state information, operating system software, middleware, application software, and licenses. User-level information includes information other than system-level information. Mechanisms employed to protect the integrity of system backups include digital signatures and cryptographic hashes. Protection of system backup information while in transit is addressed by [MP-5](#mp-5) and [SC-8](#sc-8) . System backups reflect the requirements in contingency plans as well as other organizational requirements for backing up information. Organizations may be subject to laws, executive orders, directives, regulations, or policies with requirements regarding specific categories of information (e.g., personal health information). Organizational personnel consult with the senior agency official for privacy and legal counsel regarding such requirements.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The backup infrastructure for this system is implemented and operational. Proxmox Backup Server (PBS) runs as LXC 300 on smoker (10.10.30.21) with NFS-backed storage to smokehouse (`10.10.20.10:/pbs-datastore`, 17TB available). Two daily vzdump snapshot jobs cover all five in-scope VMs: the pitcrew job (UUID `1da17d50-2183-4592-946b-47e956174e0a`) runs at 02:00 and covers DC01 (VMID 100), WS01 (VMID 101), TheHive (VMID 200), and dojo (VMID 201); the smoker job (UUID `851dfd63-cbf4-464a-b394-0cc985de3810`) runs at 02:30 and covers regscale (VMID 301). A supplemental weekly job runs Sundays at 03:00 covering target VMs. vzdump captures crash-consistent qemu image chunks across all layers (OS, middleware, application data), satisfying both user-level and system-level backup requirements at the same daily frequency.

System documentation backup is provided by the Git repository (`github.com/brianchaplow/homelab-fedramp-low`) with per-commit pushes to `origin/main`. All in-repo documentation, OSCAL artifacts, and runbooks are version-controlled; the `plan-2-complete` tag confirms the repository state at Plan 2 close.

The auditable backup failure record is ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`): during the 2026-04-07 rack consolidation reboot, a boot-race caused the PBS NFS mount to fail silently, creating a 5-day gap (2026-04-03 through 2026-04-07) for DC01, WS01, and TheHive. The fix -- fstab hardening to `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30` -- eliminates the boot-order race class. The gap was closed by the 02:00 run on 2026-04-09.

This control is rated `partial` due to three open gaps: NFS backup transport is unencrypted (CP-9.d.01 confidentiality gap, documented as a portfolio trade-off in `runbooks/cert-trust.md`); no automated PBS failure alert is wired to Wazuh/Discord (the ADR 0005 gap went undetected for 5 nights; interim manual tripwire active per `runbooks/monthly-conmon.md`); and brisket (bare metal) and haccp (bare metal) have no VM-level PBS backup job.

#### Implementation Status: partial

______________________________________________________________________
