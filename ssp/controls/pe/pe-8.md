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
  pe-08_odp.01:
    alt-identifier: pe-8_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-08_odp.02:
    alt-identifier: pe-8_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pe-08_odp.03:
    alt-identifier: pe-8_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pe-08
---

# pe-8 - \[Physical and Environmental Protection\] Visitor Access Records

## Control Statement

- \[a.\] Maintain visitor access records to the facility where the system resides for [time period];

- \[b.\] Review visitor access records [frequency] ; and

- \[c.\] Report anomalies in visitor access records to [personnel].

## Control Assessment Objective

- \[PE-08a.\] visitor access records for the facility where the system resides are maintained for [time period];

- \[PE-08b.\] visitor access records are reviewed [frequency];

- \[PE-08c.\] visitor access records anomalies are reported to [personnel].

## Control guidance

Visitor access records include the names and organizations of individuals visiting, visitor signatures, forms of identification, dates of access, entry and departure times, purpose of visits, and the names and organizations of individuals visited. Access record reviews determine if access authorizations are current and are still required to support organizational mission and business functions. Access records are not required for publicly accessible areas.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: pe-8 -->

#### Implementation Status: planned

______________________________________________________________________
