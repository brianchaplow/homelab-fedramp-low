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
  mp-1_prm_1:
    aggregates:
      - mp-01_odp.01
      - mp-01_odp.02
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.03:
    alt-identifier: mp-1_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.04:
    alt-identifier: mp-1_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.05:
    alt-identifier: mp-1_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.06:
    alt-identifier: mp-1_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.07:
    alt-identifier: mp-1_prm_6
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  mp-01_odp.08:
    alt-identifier: mp-1_prm_7
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: mp-01
---

# mp-1 - \[Media Protection\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the media protection policy and the associated media protection controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the media protection policy and procedures; and

- \[c.\] Review and update the current media protection:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[MP-01a.\]

  - \[MP-01a.[01]\] a media protection policy is developed and documented;
  - \[MP-01a.[02]\] the media protection policy is disseminated to [personnel or roles];
  - \[MP-01a.[03]\] media protection procedures to facilitate the implementation of the media protection policy and associated media protection controls are developed and documented;
  - \[MP-01a.[04]\] the media protection procedures are disseminated to [personnel or roles];
  - \[MP-01a.01\]

    - \[MP-01a.01(a)\]

      - \[MP-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses purpose;
      - \[MP-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses scope;
      - \[MP-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses roles;
      - \[MP-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses responsibilities;
      - \[MP-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses management commitment;
      - \[MP-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy addresses coordination among organizational entities;
      - \[MP-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] media protection policy compliance;

    - \[MP-01a.01(b)\] the media protection policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[MP-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the media protection policy and procedures.

- \[MP-01c.\]

  - \[MP-01c.01\]

    - \[MP-01c.01[01]\] the current media protection policy is reviewed and updated [frequency];
    - \[MP-01c.01[02]\] the current media protection policy is reviewed and updated following [events];

  - \[MP-01c.02\]

    - \[MP-01c.02[01]\] the current media protection procedures are reviewed and updated [frequency];
    - \[MP-01c.02[02]\] the current media protection procedures are reviewed and updated following [events].

## Control guidance

Media protection policy and procedures address the controls in the MP family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of media protection policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to media protection policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: mp-1 -->

#### Implementation Status: planned

______________________________________________________________________
