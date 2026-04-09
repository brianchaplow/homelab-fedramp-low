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
  ps-06_odp.01:
    alt-identifier: ps-6_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ps-06_odp.02:
    alt-identifier: ps-6_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ps-06
---

# ps-6 - \[Personnel Security\] Access Agreements

## Control Statement

- \[a.\] Develop and document access agreements for organizational systems;

- \[b.\] Review and update the access agreements [frequency] ; and

- \[c.\] Verify that individuals requiring access to organizational information and systems:

  - \[1.\] Sign appropriate access agreements prior to being granted access; and
  - \[2.\] Re-sign access agreements to maintain access to organizational systems when access agreements have been updated or [frequency].

## Control Assessment Objective

- \[PS-06a.\] access agreements are developed and documented for organizational systems;

- \[PS-06b.\] the access agreements are reviewed and updated [frequency];

- \[PS-06c.\]

  - \[PS-06c.01\] individuals requiring access to organizational information and systems sign appropriate access agreements prior to being granted access;
  - \[PS-06c.02\] individuals requiring access to organizational information and systems re-sign access agreements to maintain access to organizational systems when access agreements have been updated or [frequency].

## Control guidance

Access agreements include nondisclosure agreements, acceptable use agreements, rules of behavior, and conflict-of-interest agreements. Signed access agreements include an acknowledgement that individuals have read, understand, and agree to abide by the constraints associated with organizational systems to which access is authorized. Organizations can use electronic signatures to acknowledge access agreements unless specifically prohibited by organizational policy.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ps-6 -->

#### Implementation Status: planned

______________________________________________________________________
