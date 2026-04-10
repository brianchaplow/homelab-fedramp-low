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
  ps-1_prm_1:
    aggregates:
      - ps-01_odp.01
      - ps-01_odp.02
    profile-param-value-origin: organization
  ps-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  ps-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  ps-01_odp.03:
    alt-identifier: ps-1_prm_2
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
  ps-01_odp.04:
    alt-identifier: ps-1_prm_3
    profile-values:
      - annually and after each plan phase completion or security incident
    profile-param-value-origin: organization
  ps-01_odp.05:
    alt-identifier: ps-1_prm_4
    profile-values:
      - plan phase completion, new service enrollment, security incident, or regulatory change
    profile-param-value-origin: organization
  ps-01_odp.06:
    alt-identifier: ps-1_prm_5
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  ps-01_odp.07:
    alt-identifier: ps-1_prm_6
    profile-values:
      - plan phase completion, new service enrollment, or deviation requiring an ADR
    profile-param-value-origin: organization
  ps-01_odp.08:
    alt-identifier: ps-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ps-01
---

# ps-1 - \[Personnel Security\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the personnel security policy and the associated personnel security controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the personnel security policy and procedures; and

- \[c.\] Review and update the current personnel security:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[PS-01a.\]

  - \[PS-01a.[01]\] a personnel security policy is developed and documented;
  - \[PS-01a.[02]\] the personnel security policy is disseminated to [personnel or roles];
  - \[PS-01a.[03]\] personnel security procedures to facilitate the implementation of the personnel security policy and associated personnel security controls are developed and documented;
  - \[PS-01a.[04]\] the personnel security procedures are disseminated to [personnel or roles];
  - \[PS-01a.01\]

    - \[PS-01a.01(a)\]

      - \[PS-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses purpose;
      - \[PS-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses scope;
      - \[PS-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses roles;
      - \[PS-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses responsibilities;
      - \[PS-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses management commitment;
      - \[PS-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses coordination among organizational entities;
      - \[PS-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy addresses compliance;

    - \[PS-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] personnel security policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[PS-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the personnel security policy and procedures;

- \[PS-01c.\]

  - \[PS-01c.01\]

    - \[PS-01c.01[01]\] the current personnel security policy is reviewed and updated [frequency];
    - \[PS-01c.01[02]\] the current personnel security policy is reviewed and updated following [events];

  - \[PS-01c.02\]

    - \[PS-01c.02[01]\] the current personnel security procedures are reviewed and updated [frequency];
    - \[PS-01c.02[02]\] the current personnel security procedures are reviewed and updated following [events].

## Control guidance

Personnel security policy and procedures for the controls in the PS family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on their development. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission level or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies reflecting the complex nature of organizations. Procedures can be established for security and privacy programs, for mission/business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to personnel security policy and procedures include, but are not limited to, assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS personnel security policy is documented at the system level. The CLAUDE.md policy document (`/c/Projects/CLAUDE.md`) establishes the single-operator access model, credential conventions, SSH key-only authentication requirements, and the attack-boundary rule (all attacks must target VLAN 40 only). This SSP -- together with ADR 0001 (preflight/EULA analysis), ADR 0002 (Plan 1 deployment completion), and ADR 0008 (Plan 3 pre-execution realignment) -- collectively constitutes the personnel security policy and procedure record for the MSS boundary. Brian Chaplow serves as the sole designated official for policy development, documentation, and dissemination. Policy is reviewed annually and following each plan phase completion or security incident; procedures are reviewed on the same cadence and whenever a deviation requires an ADR.

The gap relative to a multi-person organization is acknowledged: no formal HR-style policy publication process exists and no designated separate policy official is possible for a single-operator system. Brian Chaplow performs all policy, management, and compliance roles simultaneously. Dissemination is therefore internal to a single role, and the review cycle is event-driven via ADR authoring rather than calendar-driven via a policy committee. This constitutes a partial implementation -- policy artifacts exist and are actively maintained, but the formal multi-role dissemination model presupposed by PS-1 does not apply.

#### Implementation Status: partial

______________________________________________________________________
