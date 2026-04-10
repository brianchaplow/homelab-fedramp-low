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
  sort-id: sa-02
---

# sa-2 - \[System and Services Acquisition\] Allocation of Resources

## Control Statement

- \[a.\] Determine the high-level information security and privacy requirements for the system or system service in mission and business process planning;

- \[b.\] Determine, document, and allocate the resources required to protect the system or system service as part of the organizational capital planning and investment control process; and

- \[c.\] Establish a discrete line item for information security and privacy in organizational programming and budgeting documentation.

## Control Assessment Objective

- \[SA-02a.\]

  - \[SA-02a.[01]\] the high-level information security requirements for the system or system service are determined in mission and business process planning;
  - \[SA-02a.[02]\] the high-level privacy requirements for the system or system service are determined in mission and business process planning;

- \[SA-02b.\]

  - \[SA-02b.[01]\] the resources required to protect the system or system service are determined and documented as part of the organizational capital planning and investment control process;
  - \[SA-02b.[02]\] the resources required to protect the system or system service are allocated as part of the organizational capital planning and investment control process;

- \[SA-02c.\]

  - \[SA-02c.[01]\] a discrete line item for information security is established in organizational programming and budgeting documentation;
  - \[SA-02c.[02]\] a discrete line item for privacy is established in organizational programming and budgeting documentation.

## Control guidance

Resource allocation for information security and privacy includes funding for system and services acquisition, sustainment, and supply chain-related risks throughout the system development life cycle.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Security and privacy resource requirements for the Managed SOC Service are determined at the hardware level and documented in `inventory/overlay.yaml` (each in-boundary host's hardware model, function, and EOL date) and in `oscal/component-definition.json` (OSCAL-native resource inventory for all 7 in-boundary components). The MSS platform runs on personally-owned hardware: Lenovo ThinkStation P3 Tiny Gen 2 (brisket -- Ultra 9 285 / 64 GB, primary SOC platform), Lenovo ThinkStation P340 Tiny (haccp -- i7-10700T / 32 GB, ELK + Arkime; pitcrew -- i7-10700T / 32 GB, Proxmox host), and QNAP TVS-871 (smokehouse -- i7-4790S / 16 GB, sensors + NFS backup). The GRC tooling tier (dojo, regscale) is allocated 4 vCPU / 6 GB RAM / 40 GB disk per VM as documented in `deploy/proxmox/dojo-vm-config.yaml` and `deploy/proxmox/regscale-vm-config.yaml` and in ADR 0002. The `inventory/IIW-2026-04.xlsx` (FedRAMP IIW, April 2026) enumerates all 7 in-boundary assets as the capital allocation reference.

This control is partial because formal capital planning and investment control (CPIC) processes do not exist for a single-operator homelab -- there is no organizational budget cycle, investment board, or discrete security line item in programming documents. Hardware was procured and resource allocation is documented post-hoc in overlay.yaml and the OSCAL component-definition rather than through a pre-acquisition CPIC review. EOL dates in overlay.yaml serve as the lifecycle planning anchor for future replacement decisions.

#### Implementation Status: partial

______________________________________________________________________
