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
  pl-04_odp.01:
    alt-identifier: pl-4_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pl-04_odp.02:
    alt-identifier: pl-4_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  pl-04_odp.03:
    alt-identifier: pl-4_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pl-04
---

# pl-4 - \[Planning\] Rules of Behavior

## Control Statement

- \[a.\] Establish and provide to individuals requiring access to the system, the rules that describe their responsibilities and expected behavior for information and system usage, security, and privacy;

- \[b.\] Receive a documented acknowledgment from such individuals, indicating that they have read, understand, and agree to abide by the rules of behavior, before authorizing access to information and the system;

- \[c.\] Review and update the rules of behavior [frequency] ; and

- \[d.\] Require individuals who have acknowledged a previous version of the rules of behavior to read and re-acknowledge [Selection (one or more): [frequency]; when the rules are revised or updated].

## Control Assessment Objective

- \[PL-04a.\]

  - \[PL-04a.[01]\] rules that describe responsibilities and expected behavior for information and system usage, security, and privacy are established for individuals requiring access to the system;
  - \[PL-04a.[02]\] rules that describe responsibilities and expected behavior for information and system usage, security, and privacy are provided to individuals requiring access to the system;

- \[PL-04b.\] before authorizing access to information and the system, a documented acknowledgement from such individuals indicating that they have read, understand, and agree to abide by the rules of behavior is received;

- \[PL-04c.\] rules of behavior are reviewed and updated [frequency];

- \[PL-04d.\] individuals who have acknowledged a previous version of the rules of behavior are required to read and reacknowledge [Selection (one or more): [frequency]; when the rules are revised or updated].

## Control guidance

Rules of behavior represent a type of access agreement for organizational users. Other types of access agreements include nondisclosure agreements, conflict-of-interest agreements, and acceptable use agreements (see [PS-6](#ps-6) ). Organizations consider rules of behavior based on individual user roles and responsibilities and differentiate between rules that apply to privileged users and rules that apply to general users. Establishing rules of behavior for some types of non-organizational users, including individuals who receive information from federal systems, is often not feasible given the large number of such users and the limited nature of their interactions with the systems. Rules of behavior for organizational and non-organizational users can also be established in [AC-8](#ac-8) . The related controls section provides a list of controls that are relevant to organizational rules of behavior. [PL-4b](#pl-4_smt.b) , the documented acknowledgment portion of the control, may be satisfied by the literacy training and awareness and role-based training programs conducted by organizations if such training includes rules of behavior. Documented acknowledgements for rules of behavior include electronic or physical signatures and electronic agreement check boxes or radio buttons.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: pl-4 -->

#### Implementation Status: planned

______________________________________________________________________
