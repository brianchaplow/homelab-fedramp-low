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
  cp-2_prm_1:
    aggregates:
      - cp-02_odp.01
      - cp-02_odp.02
    profile-param-value-origin: <REPLACE_ME>
  cp-2_prm_2:
    aggregates:
      - cp-02_odp.03
      - cp-02_odp.04
    profile-param-value-origin: <REPLACE_ME>
  cp-2_prm_4:
    aggregates:
      - cp-02_odp.06
      - cp-02_odp.07
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.05:
    alt-identifier: cp-2_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.06:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-02_odp.07:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cp-02
---

# cp-2 - \[Contingency Planning\] Contingency Plan

## Control Statement

- \[a.\] Develop a contingency plan for the system that:

  - \[1.\] Identifies essential mission and business functions and associated contingency requirements;
  - \[2.\] Provides recovery objectives, restoration priorities, and metrics;
  - \[3.\] Addresses contingency roles, responsibilities, assigned individuals with contact information;
  - \[4.\] Addresses maintaining essential mission and business functions despite a system disruption, compromise, or failure;
  - \[5.\] Addresses eventual, full system restoration without deterioration of the controls originally planned and implemented;
  - \[6.\] Addresses the sharing of contingency information; and
  - \[7.\] Is reviewed and approved by [organization-defined personnel or roles];

- \[b.\] Distribute copies of the contingency plan to [organization-defined key contingency personnel (identified by name and/or by role) and organizational elements];

- \[c.\] Coordinate contingency planning activities with incident handling activities;

- \[d.\] Review the contingency plan for the system [frequency];

- \[e.\] Update the contingency plan to address changes to the organization, system, or environment of operation and problems encountered during contingency plan implementation, execution, or testing;

- \[f.\] Communicate contingency plan changes to [organization-defined key contingency personnel (identified by name and/or by role) and organizational elements];

- \[g.\] Incorporate lessons learned from contingency plan testing, training, or actual contingency activities into contingency testing and training; and

- \[h.\] Protect the contingency plan from unauthorized disclosure and modification.

## Control Assessment Objective

- \[CP-02a.\]

  - \[CP-02a.01\] a contingency plan for the system is developed that identifies essential mission and business functions and associated contingency requirements;
  - \[CP-02a.02\]

    - \[CP-02a.02[01]\] a contingency plan for the system is developed that provides recovery objectives;
    - \[CP-02a.02[02]\] a contingency plan for the system is developed that provides restoration priorities;
    - \[CP-02a.02[03]\] a contingency plan for the system is developed that provides metrics;

  - \[CP-02a.03\]

    - \[CP-02a.03[01]\] a contingency plan for the system is developed that addresses contingency roles;
    - \[CP-02a.03[02]\] a contingency plan for the system is developed that addresses contingency responsibilities;
    - \[CP-02a.03[03]\] a contingency plan for the system is developed that addresses assigned individuals with contact information;

  - \[CP-02a.04\] a contingency plan for the system is developed that addresses maintaining essential mission and business functions despite a system disruption, compromise, or failure;
  - \[CP-02a.05\] a contingency plan for the system is developed that addresses eventual, full-system restoration without deterioration of the controls originally planned and implemented;
  - \[CP-02a.06\] a contingency plan for the system is developed that addresses the sharing of contingency information;
  - \[CP-02a.07\]

    - \[CP-02a.07[01]\] a contingency plan for the system is developed that is reviewed by [personnel or roles];
    - \[CP-02a.07[02]\] a contingency plan for the system is developed that is approved by [personnel or roles];

- \[CP-02b.\]

  - \[CP-02b.[01]\] copies of the contingency plan are distributed to [key contingency personnel];
  - \[CP-02b.[02]\] copies of the contingency plan are distributed to [organizational elements];

- \[CP-02c.\] contingency planning activities are coordinated with incident handling activities;

- \[CP-02d.\] the contingency plan for the system is reviewed [frequency];

- \[CP-02e.\]

  - \[CP-02e.[01]\] the contingency plan is updated to address changes to the organization, system, or environment of operation;
  - \[CP-02e.[02]\] the contingency plan is updated to address problems encountered during contingency plan implementation, execution, or testing;

- \[CP-02f.\]

  - \[CP-02f.[01]\] contingency plan changes are communicated to [key contingency personnel];
  - \[CP-02f.[02]\] contingency plan changes are communicated to [organizational elements];

- \[CP-02g.\]

  - \[CP-02g.[01]\] lessons learned from contingency plan testing or actual contingency activities are incorporated into contingency testing;
  - \[CP-02g.[02]\] lessons learned from contingency plan training or actual contingency activities are incorporated into contingency testing and training;

- \[CP-02h.\]

  - \[CP-02h.[01]\] the contingency plan is protected from unauthorized disclosure;
  - \[CP-02h.[02]\] the contingency plan is protected from unauthorized modification.

## Control guidance

Contingency planning for systems is part of an overall program for achieving continuity of operations for organizational mission and business functions. Contingency planning addresses system restoration and implementation of alternative mission or business processes when systems are compromised or breached. Contingency planning is considered throughout the system development life cycle and is a fundamental part of the system design. Systems can be designed for redundancy, to provide backup capabilities, and for resilience. Contingency plans reflect the degree of restoration required for organizational systems since not all systems need to fully recover to achieve the level of continuity of operations desired. System recovery objectives reflect applicable laws, executive orders, directives, regulations, policies, standards, guidelines, organizational risk tolerance, and system impact level.

Actions addressed in contingency plans include orderly system degradation, system shutdown, fallback to a manual mode, alternate information flows, and operating in modes reserved for when systems are under attack. By coordinating contingency planning with incident handling activities, organizations ensure that the necessary planning activities are in place and activated in the event of an incident. Organizations consider whether continuity of operations during an incident conflicts with the capability to automatically disable the system, as specified in [IR-4(5)](#ir-4.5) . Incident response planning is part of contingency planning for organizations and is addressed in the [IR](#ir) (Incident Response) family.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cp-2 -->

#### Implementation Status: planned

______________________________________________________________________
