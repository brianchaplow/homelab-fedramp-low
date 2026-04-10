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
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cm-04
---

# cm-4 - \[Configuration Management\] Impact Analyses

## Control Statement

Analyze changes to the system to determine potential security and privacy impacts prior to change implementation.

## Control Assessment Objective

- \[CM-04[01]\] changes to the system are analyzed to determine potential security impacts prior to change implementation;

- \[CM-04[02]\] changes to the system are analyzed to determine potential privacy impacts prior to change implementation.

## Control guidance

Organizational personnel with security or privacy responsibilities conduct impact analyses. Individuals conducting impact analyses possess the necessary skills and technical expertise to analyze the changes to systems as well as the security or privacy ramifications. Impact analyses include reviewing security and privacy plans, policies, and procedures to understand control requirements; reviewing system design documentation and operational procedures to understand control implementation and how specific system changes might affect the controls; reviewing the impact of changes on organizational supply chain partners with stakeholders; and determining how potential changes to a system create new risks to the privacy of individuals and the ability of implemented controls to mitigate those risks. Impact analyses also include risk assessments to understand the impact of the changes and determine if additional controls are required.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Security and privacy impact analysis for system changes is performed ad hoc by the system owner through the ADR process. Every architecturally significant change that affects the security posture -- VLAN topology, service port configuration, agent enrollment, backup topology, Phase 14 data pipeline additions -- produces an ADR that explicitly documents security consequences before the change is committed to the baseline. ADR 0003 analyzed the RegScale HTTP-on-80 deviation; ADR 0004 analyzed the DefectDojo HTTP-on-8080 deviation; ADR 0005 identified the security risk of silent backup failure, performed root-cause analysis, and remediated the fstab configuration with `x-systemd.automount` hardening. ADR 0008 contains a pre-execution risk table for all Plan 3 changes. These ADRs provide the pre-implementation impact record that CM-4 requires.

Supporting data points for impact analysis are drawn from Wazuh SCA (Security Configuration Assessment) scans running on all enrolled agents, which surface OS-level hardening gaps from any configuration or package change. The monthly ConMon pipeline (`./pipelines.sh conmon`, ADR 0007) produces a POA&M from Wazuh vulnerability findings (`poam/POAM-2026-04.xlsx`, 8,473 findings) that feeds risk context into change-impact decisions. The Grafana fleet dashboard (`brisket-setup/monitoring/build-infrastructure-fleet.py`) surfaces configuration drift signals -- disk, memory, and service health -- that can trigger manual impact review. The primary gap driving `partial` status is the absence of a formal, documented pre-change impact analysis procedure with defined criteria; the current mechanism is effective but ad hoc.

#### Implementation Status: partial

______________________________________________________________________
