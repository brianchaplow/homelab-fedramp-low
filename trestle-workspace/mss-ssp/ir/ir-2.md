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
  ir-02_odp.01:
    alt-identifier: ir-2_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ir-02_odp.02:
    alt-identifier: ir-2_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ir-02_odp.03:
    alt-identifier: ir-2_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ir-02_odp.04:
    alt-identifier: ir-2_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ir-02
---

# ir-2 - \[Incident Response\] Incident Response Training

## Control Statement

- \[a.\] Provide incident response training to system users consistent with assigned roles and responsibilities:

  - \[1.\] Within [time period] of assuming an incident response role or responsibility or acquiring system access;
  - \[2.\] When required by system changes; and
  - \[3.\] [frequency] thereafter; and

- \[b.\] Review and update incident response training content [frequency] and following [events].

## Control Assessment Objective

- \[IR-02a.\]

  - \[IR-02a.01\] incident response training is provided to system users consistent with assigned roles and responsibilities within [time period] of assuming an incident response role or responsibility or acquiring system access;
  - \[IR-02a.02\] incident response training is provided to system users consistent with assigned roles and responsibilities when required by system changes;
  - \[IR-02a.03\] incident response training is provided to system users consistent with assigned roles and responsibilities [frequency] thereafter;

- \[IR-02b.\]

  - \[IR-02b.[01]\] incident response training content is reviewed and updated [frequency];
  - \[IR-02b.[02]\] incident response training content is reviewed and updated following [events].

## Control guidance

Incident response training is associated with the assigned roles and responsibilities of organizational personnel to ensure that the appropriate content and level of detail are included in such training. For example, users may only need to know who to call or how to recognize an incident; system administrators may require additional training on how to handle incidents; and incident responders may receive more specific training on forensics, data collection techniques, reporting, system recovery, and system restoration. Incident response training includes user training in identifying and reporting suspicious activities from external and internal sources. Incident response training for users may be provided as part of [AT-2](#at-2) or [AT-3](#at-3) . Events that may precipitate an update to incident response training content include, but are not limited to, incident response plan testing or response to an actual incident (lessons learned), assessment or audit findings, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ir-2 -->

#### Implementation Status: planned

______________________________________________________________________
