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
  ps-04_odp.01:
    alt-identifier: ps-4_prm_1
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  ps-04_odp.02:
    alt-identifier: ps-4_prm_2
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ps-04
---

# ps-4 - \[Personnel Security\] Personnel Termination

## Control Statement

Upon termination of individual employment:

- \[a.\] Disable system access within [time period];

- \[b.\] Terminate or revoke any authenticators and credentials associated with the individual;

- \[c.\] Conduct exit interviews that include a discussion of [information security topics];

- \[d.\] Retrieve all security-related organizational system-related property; and

- \[e.\] Retain access to organizational information and systems formerly controlled by terminated individual.

## Control Assessment Objective

- \[PS-04a.\] upon termination of individual employment, system access is disabled within [time period];

- \[PS-04b.\] upon termination of individual employment, any authenticators and credentials are terminated or revoked;

- \[PS-04c.\] upon termination of individual employment, exit interviews that include a discussion of [information security topics] are conducted;

- \[PS-04d.\] upon termination of individual employment, all security-related organizational system-related property is retrieved;

- \[PS-04e.\] upon termination of individual employment, access to organizational information and systems formerly controlled by the terminated individual are retained.

## Control guidance

System property includes hardware authentication tokens, system administration technical manuals, keys, identification cards, and building passes. Exit interviews ensure that terminated individuals understand the security constraints imposed by being former employees and that proper accountability is achieved for system-related property. Security topics at exit interviews include reminding individuals of nondisclosure agreements and potential limitations on future employment. Exit interviews may not always be possible for some individuals, including in cases related to the unavailability of supervisors, illnesses, or job abandonment. Exit interviews are important for individuals with security clearances. The timely execution of termination actions is essential for individuals who have been terminated for cause. In certain situations, organizations consider disabling the system accounts of individuals who are being terminated prior to the individuals being notified.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. MSS is a single-operator personal system; there are no employees, no employer-employee relationships, and no termination events possible. The sole operator, Brian Chaplow, owns all system access, and termination of the operator's access would be equivalent to decommissioning the system itself rather than executing a personnel security action.

#### Implementation Status: not-applicable

______________________________________________________________________
