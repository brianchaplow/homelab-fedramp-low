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
  at-1_prm_1:
    aggregates:
      - at-01_odp.01
      - at-01_odp.02
    profile-param-value-origin: organization
  at-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  at-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  at-01_odp.03:
    alt-identifier: at-1_prm_2
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  at-01_odp.04:
    alt-identifier: at-1_prm_3
    profile-values:
      - annually or when a new ADR records a scope or architecture change
    profile-param-value-origin: organization
  at-01_odp.05:
    alt-identifier: at-1_prm_4
    profile-values:
      - new ADR filing, phase completion, or architecture change
    profile-param-value-origin: organization
  at-01_odp.06:
    alt-identifier: at-1_prm_5
    profile-values:
      - annually or when a new ADR records a scope or architecture change
    profile-param-value-origin: organization
  at-01_odp.07:
    alt-identifier: at-1_prm_6
    profile-values:
      - new ADR filing, phase completion, or architecture change
    profile-param-value-origin: organization
  at-01_odp.08:
    alt-identifier: at-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: at-01
---

# at-1 - \[Awareness and Training\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the awareness and training policy and the associated awareness and training controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the awareness and training policy and procedures; and

- \[c.\] Review and update the current awareness and training:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[AT-01a.\]

  - \[AT-01a.[01]\] an awareness and training policy is developed and documented; 
  - \[AT-01a.[02]\] the awareness and training policy is disseminated to [personnel or roles];
  - \[AT-01a.[03]\] awareness and training procedures to facilitate the implementation of the awareness and training policy and associated access controls are developed and documented;
  - \[AT-01a.[04]\] the awareness and training procedures are disseminated to [personnel or roles].
  - \[AT-01a.01\]

    - \[AT-01a.01(a)\]

      - \[AT-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses purpose;
      - \[AT-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses scope;
      - \[AT-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses roles;
      - \[AT-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses responsibilities;
      - \[AT-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses management commitment;
      - \[AT-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses coordination among organizational entities;
      - \[AT-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy addresses compliance; and

    - \[AT-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] awareness and training policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines; and

- \[AT-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the awareness and training policy and procedures;

- \[AT-01c.\]

  - \[AT-01c.01\]

    - \[AT-01c.01[01]\] the current awareness and training policy is reviewed and updated [frequency];
    - \[AT-01c.01[02]\] the current awareness and training policy is reviewed and updated following [events];

  - \[AT-01c.02\]

    - \[AT-01c.02[01]\] the current awareness and training procedures are reviewed and updated [frequency];
    - \[AT-01c.02[02]\] the current awareness and training procedures are reviewed and updated following [events].

## Control guidance

Awareness and training policy and procedures address the controls in the AT family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of awareness and training policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to awareness and training policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

This SSP (`trestle-workspace/mss-ssp/`) serves as the system-level awareness and training policy for the MSS homelab. It addresses purpose, scope, roles, responsibilities, and compliance expectations for a single-operator personal system. No separate policy document is needed; the SSP combined with the `homelab-fedramp-low` git history and ADR chain (ADRs 0001--0008) constitutes the policy and procedure record. Brian Chaplow is designated as the sole person responsible for developing, documenting, and disseminating all awareness and training material.

Policy is reviewed annually and whenever a new ADR records a scope or architecture change. The `runbooks/monthly-conmon.md` defines the ConMon review cadence, and the `C:/Projects/CLAUDE.md` project ledger (last updated 2026-04-08) provides an observable last-review timestamp. The policy gap is that this document is embedded in the SSP rather than a standalone policy artifact; NIST guidance explicitly permits this consolidation, making the status partial rather than not-applicable.

#### Implementation Status: partial

______________________________________________________________________
