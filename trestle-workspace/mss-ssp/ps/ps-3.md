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
  ps-3_prm_1:
    aggregates:
      - ps-03_odp.01
      - ps-03_odp.02
    profile-param-value-origin: organization
  ps-03_odp.01:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  ps-03_odp.02:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ps-03
---

# ps-3 - \[Personnel Security\] Personnel Screening

## Control Statement

- \[a.\] Screen individuals prior to authorizing access to the system; and

- \[b.\] Rescreen individuals in accordance with [organization-defined conditions requiring rescreening and, where rescreening is so indicated, the frequency of rescreening].

## Control Assessment Objective

- \[PS-03a.\] individuals are screened prior to authorizing access to the system;

- \[PS-03b.\]

  - \[PS-03b.[01]\] individuals are rescreened in accordance with [conditions requiring rescreening];
  - \[PS-03b.[02]\] where rescreening is so indicated, individuals are rescreened [frequency].

## Control guidance

Personnel screening and rescreening activities reflect applicable laws, executive orders, directives, regulations, policies, standards, guidelines, and specific criteria established for the risk designations of assigned positions. Examples of personnel screening include background investigations and agency checks. Organizations may define different rescreening conditions and frequencies for personnel accessing systems based on types of information processed, stored, or transmitted by the systems.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. MSS is a single-operator personal system; there is only one individual with access -- Brian Chaplow -- and no organizational hiring process through which a pre-access screening requirement or rescreening schedule could be triggered. Access to in-boundary systems is technically enforced via SSH key-only authentication with no external accounts provisioned, which means the control's intent (limiting access to vetted individuals) is achieved architecturally rather than through a personnel screening process.

#### Implementation Status: not-applicable

______________________________________________________________________
