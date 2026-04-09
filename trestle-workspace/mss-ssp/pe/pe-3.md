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
  pe-3_prm_9:
    aggregates:
      - pe-03_odp.09
      - pe-03_odp.10
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.01:
    alt-identifier: pe-3_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.02:
    alt-identifier: pe-3_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.03:
    alt-identifier: pe-3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.04:
    alt-identifier: pe-3_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.05:
    alt-identifier: pe-3_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.06:
    alt-identifier: pe-3_prm_6
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.07:
    alt-identifier: pe-3_prm_7
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.08:
    alt-identifier: pe-3_prm_8
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.09:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-03_odp.10:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pe-03
---

# pe-3 - \[Physical and Environmental Protection\] Physical Access Control

## Control Statement

- \[a.\] Enforce physical access authorizations at [entry and exit points] by:

  - \[1.\] Verifying individual access authorizations before granting access to the facility; and
  - \[2.\] Controlling ingress and egress to the facility using [Selection (one or more): [systems or devices]; guards];

- \[b.\] Maintain physical access audit logs for [entry or exit points];

- \[c.\] Control access to areas within the facility designated as publicly accessible by implementing the following controls: [physical access controls];

- \[d.\] Escort visitors and control visitor activity [circumstances];

- \[e.\] Secure keys, combinations, and other physical access devices;

- \[f.\] Inventory [physical access devices] every [frequency] ; and

- \[g.\] Change combinations and keys [organization-defined frequency] and/or when keys are lost, combinations are compromised, or when individuals possessing the keys or combinations are transferred or terminated.

## Control Assessment Objective

- \[PE-03a.\]

  - \[PE-03a.01\] physical access authorizations are enforced at [entry and exit points] by verifying individual access authorizations before granting access to the facility;
  - \[PE-03a.02\] physical access authorizations are enforced at [entry and exit points] by controlling ingress and egress to the facility using [Selection (one or more): [systems or devices]; guards];

- \[PE-03b.\] physical access audit logs are maintained for [entry or exit points];

- \[PE-03c.\] access to areas within the facility designated as publicly accessible are maintained by implementing [physical access controls];

- \[PE-03d.\]

  - \[PE-03d.[01]\] visitors are escorted;
  - \[PE-03d.[02]\] visitor activity is controlled [circumstances];

- \[PE-03e.\]

  - \[PE-03e.[01]\] keys are secured;
  - \[PE-03e.[02]\] combinations are secured;
  - \[PE-03e.[03]\] other physical access devices are secured;

- \[PE-03f.\] [physical access devices] are inventoried [frequency];

- \[PE-03g.\]

  - \[PE-03g.[01]\] combinations are changed [frequency] , when combinations are compromised, or when individuals possessing the combinations are transferred or terminated;
  - \[PE-03g.[02]\] keys are changed [frequency] , when keys are lost, or when individuals possessing the keys are transferred or terminated.

## Control guidance

Physical access control applies to employees and visitors. Individuals with permanent physical access authorizations are not considered visitors. Physical access controls for publicly accessible areas may include physical access control logs/records, guards, or physical access devices and barriers to prevent movement from publicly accessible areas to non-public areas. Organizations determine the types of guards needed, including professional security staff, system users, or administrative staff. Physical access devices include keys, locks, combinations, biometric readers, and card readers. Physical access control systems comply with applicable laws, executive orders, directives, policies, regulations, standards, and guidelines. Organizations have flexibility in the types of audit logs employed. Audit logs can be procedural, automated, or some combination thereof. Physical access points can include facility access points, interior access points to systems that require supplemental access controls, or both. Components of systems may be in areas designated as publicly accessible with organizations controlling access to the components.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: pe-3 -->

#### Implementation Status: planned

______________________________________________________________________
