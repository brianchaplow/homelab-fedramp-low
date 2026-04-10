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
  cm-02_odp.01:
    alt-identifier: cm-2_prm_1
    profile-values:
      - monthly
    profile-param-value-origin: organization
  cm-02_odp.02:
    alt-identifier: cm-2_prm_2
    profile-values:
      - when a new phase adds infrastructure, after a rack or cable change, after a host reimage, or when an ADR records a configuration-drift incident
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cm-02
---

# cm-2 - \[Configuration Management\] Baseline Configuration

## Control Statement

- \[a.\] Develop, document, and maintain under configuration control, a current baseline configuration of the system; and

- \[b.\] Review and update the baseline configuration of the system:

  - \[1.\] [frequency];
  - \[2.\] When required due to [circumstances] ; and
  - \[3.\] When system components are installed or upgraded.

## Control Assessment Objective

- \[CM-02a.\]

  - \[CM-02a.[01]\] a current baseline configuration of the system is developed and documented;
  - \[CM-02a.[02]\] a current baseline configuration of the system is maintained under configuration control;

- \[CM-02b.\]

  - \[CM-02b.01\] the baseline configuration of the system is reviewed and updated [frequency];
  - \[CM-02b.02\] the baseline configuration of the system is reviewed and updated when required due to [circumstances];
  - \[CM-02b.03\] the baseline configuration of the system is reviewed and updated when system components are installed or upgraded.

## Control guidance

Baseline configurations for systems and system components include connectivity, operational, and communications aspects of systems. Baseline configurations are documented, formally reviewed, and agreed-upon specifications for systems or configuration items within those systems. Baseline configurations serve as a basis for future builds, releases, or changes to systems and include security and privacy control implementations, operational procedures, information about system components, network topology, and logical placement of components in the system architecture. Maintaining baseline configurations requires creating new baselines as organizational systems change over time. Baseline configurations of systems reflect the current enterprise architecture.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service maintains its baseline configuration as git-tracked code across four public and private repositories: `homelab-soc-portfolio` (every SOC config checked in), `HomeLab-SOC-v2` (legacy configs retained for delta analysis), `brisket-setup/` (v3 platform install and monitoring configs), and `reference/phase14/` (Zeek baseline for the haccp data foundation). Every configuration change is a git commit with an ADR when the change is architecturally significant; every change is therefore attributable, reviewable, and rollback-able. The baseline is reviewed on the monthly ConMon cycle (`./pipelines.sh conmon`) and whenever a new phase adds infrastructure, a host is reimaged, or an ADR records a configuration-drift incident.

The baseline is supported by PBS (Proxmox Backup Server on smoker LXC 300) with daily snapshots to smokehouse 17TB NFS as the recovery backstop, and by Wazuh agent syscollector which captures each host's installed package set and configuration drift for indexer-side review. The auditable example of baseline drift being caught and fixed is homelab-fedramp-low ADR 0005: the PBS automount regression during the 2026-04-07 rack consolidation was detected, fixed, and the fix was itself encoded as a baseline change (fstab `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30`) -- the full cycle from drift to detection to remediation to baseline update.

#### Implementation Status: implemented

______________________________________________________________________
