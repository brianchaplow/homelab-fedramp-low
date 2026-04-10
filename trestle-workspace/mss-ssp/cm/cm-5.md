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
  sort-id: cm-05
---

# cm-5 - \[Configuration Management\] Access Restrictions for Change

## Control Statement

Define, document, approve, and enforce physical and logical access restrictions associated with changes to the system.

## Control Assessment Objective

- \[CM-05[01]\] physical access restrictions associated with changes to the system are defined and documented;

- \[CM-05[02]\] physical access restrictions associated with changes to the system are approved;

- \[CM-05[03]\] physical access restrictions associated with changes to the system are enforced;

- \[CM-05[04]\] logical access restrictions associated with changes to the system are defined and documented;

- \[CM-05[05]\] logical access restrictions associated with changes to the system are approved;

- \[CM-05[06]\] logical access restrictions associated with changes to the system are enforced.

## Control guidance

Changes to the hardware, software, or firmware components of systems or the operational procedures related to the system can potentially have significant effects on the security of the systems or individuals’ privacy. Therefore, organizations permit only qualified and authorized individuals to access systems for purposes of initiating changes. Access restrictions include physical and logical access controls (see [AC-3](#ac-3) and [PE-3](#pe-3) ), software libraries, workflow automation, media libraries, abstract layers (i.e., changes implemented into external interfaces rather than directly into systems), and change windows (i.e., changes occur only during specified times).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Logical access restrictions for system changes are enforced by SSH key-only authentication to all in-boundary hosts: brisket (primary SOC platform, 10.10.20.30), haccp (ELK + Arkime, 10.10.30.25), and the Proxmox hypervisors pitcrew and smoker. Password-based SSH is disabled on all production hosts via `PasswordAuthentication no` in `/etc/ssh/sshd_config`. All configuration changes flow through git commits from the operator workstation PITBOSS (10.10.10.100), and the GitHub repository (brianchaplow) serves as the access-controlled change approval record -- only the repository owner can push to `main`, providing a logical change authorization gate with commit-level attribution for every change. UFW default-deny is active on GRC VMs dojo (10.10.30.27) and regscale (10.10.30.28), restricting change paths to explicitly permitted SSH and service ports (ADR 0002 §Infrastructure state). Wazuh RBAC restricts who can push SIEM rules, SCA checks, or agent configuration to the Wazuh Dashboard (brisket:5601).

Physical access restrictions are enforced by VLAN microsegmentation on MokerLink: VLAN 40 (targets) is isolated and cannot initiate connections to VLAN 20 (SOC) or VLAN 30 (lab), so only the operator on VLAN 10 (PITBOSS) can reach all segments requiring configuration changes. OPNsense (10.10.10.1) enforces perimeter access control preventing external entities from initiating changes to in-boundary services. Physical access to the 12U rack is restricted to the system owner. The primary gap driving `partial` status is that physical access restrictions are informal -- no documented key-custody procedure or visitor log exists for the home lab rack.

#### Implementation Status: partial

______________________________________________________________________
