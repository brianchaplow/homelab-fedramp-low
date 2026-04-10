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
  sort-id: ma-05
---

# ma-5 - \[Maintenance\] Maintenance Personnel

## Control Statement

- \[a.\] Establish a process for maintenance personnel authorization and maintain a list of authorized maintenance organizations or personnel;

- \[b.\] Verify that non-escorted personnel performing maintenance on the system possess the required access authorizations; and

- \[c.\] Designate organizational personnel with required access authorizations and technical competence to supervise the maintenance activities of personnel who do not possess the required access authorizations.

## Control Assessment Objective

- \[MA-05a.\]

  - \[MA-05a.[01]\] a process for maintenance personnel authorization is established;
  - \[MA-05a.[02]\] a list of authorized maintenance organizations or personnel is maintained;

- \[MA-05b.\] non-escorted personnel performing maintenance on the system possess the required access authorizations;

- \[MA-05c.\] organizational personnel with required access authorizations and technical competence is/are designated to supervise the maintenance activities of personnel who do not possess the required access authorizations.

## Control guidance

Maintenance personnel refers to individuals who perform hardware or software maintenance on organizational systems, while [PE-2](#pe-2) addresses physical access for individuals whose maintenance duties place them within the physical protection perimeter of the systems. Technical competence of supervising individuals relates to the maintenance performed on the systems, while having required access authorizations refers to maintenance on and near the systems. Individuals not previously identified as authorized maintenance personnel—such as information technology manufacturers, vendors, systems integrators, and consultants—may require privileged access to organizational systems, such as when they are required to conduct maintenance activities with little or no notice. Based on organizational assessments of risk, organizations may issue temporary credentials to these individuals. Temporary credentials may be for one-time use or for very limited time periods.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service has a single authorized maintenance person: Brian Chaplow (system owner and sole operator). No external maintenance organizations, vendors, or contractors are authorized or hold credentials to any in-boundary component. SSH keys and Tailscale device credentials are held exclusively by the operator. Wazuh agent enrollment (15 active agents as of 2026-04-08) requires operator authentication to the Wazuh manager API on brisket, serving as the access authorization gate. The MA-5c supervision requirement is satisfied trivially -- the operator is both maintainer and supervisor.

#### Implementation Status: implemented

______________________________________________________________________
