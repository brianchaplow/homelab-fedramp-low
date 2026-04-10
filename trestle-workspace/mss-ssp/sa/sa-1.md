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
  sa-1_prm_1:
    aggregates:
      - sa-01_odp.01
      - sa-01_odp.02
    profile-param-value-origin: organization
  sa-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  sa-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  sa-01_odp.03:
    alt-identifier: sa-1_prm_2
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  sa-01_odp.04:
    alt-identifier: sa-1_prm_3
    profile-values:
      - plan phase completion, new service enrollment, vendor support-end announcement, or significant change request
    profile-param-value-origin: organization
  sa-01_odp.05:
    alt-identifier: sa-1_prm_4
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  sa-01_odp.06:
    alt-identifier: sa-1_prm_5
    profile-values:
      - plan phase completion, new service deployment, or deviation requiring an ADR
    profile-param-value-origin: organization
  sa-01_odp.07:
    alt-identifier: sa-1_prm_6
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
  sa-01_odp.08:
    alt-identifier: sa-1_prm_7
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sa-01
---

# sa-1 - \[System and Services Acquisition\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the system and services acquisition policy and the associated system and services acquisition controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the system and services acquisition policy and procedures; and

- \[c.\] Review and update the current system and services acquisition:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[SA-01a.\]

  - \[SA-01a.[01]\] a system and services acquisition policy is developed and documented;
  - \[SA-01a.[02]\] the system and services acquisition policy is disseminated to [personnel or roles];
  - \[SA-01a.[03]\] system and services acquisition procedures to facilitate the implementation of the system and services acquisition policy and associated system and services acquisition controls are developed and documented;
  - \[SA-01a.[04]\] the system and services acquisition procedures are disseminated to [personnel or roles];
  - \[SA-01a.01\]

    - \[SA-01a.01(a)\]

      - \[SA-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses purpose;
      - \[SA-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses scope;
      - \[SA-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses roles;
      - \[SA-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses responsibilities;
      - \[SA-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses management commitment;
      - \[SA-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses coordination among organizational entities;
      - \[SA-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy addresses compliance;

    - \[SA-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] system and services acquisition policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[SA-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the system and services acquisition policy and procedures;

- \[SA-01c.\]

  - \[SA-01c.01\]

    - \[SA-01c.01[01]\] the system and services acquisition policy is reviewed and updated [frequency];
    - \[SA-01c.01[02]\] the current system and services acquisition policy is reviewed and updated following [events];

  - \[SA-01c.02\]

    - \[SA-01c.02[01]\] the current system and services acquisition procedures are reviewed and updated [frequency];
    - \[SA-01c.02[02]\] the current system and services acquisition procedures are reviewed and updated following [events].

## Control guidance

System and services acquisition policy and procedures address the controls in the SA family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of system and services acquisition policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to system and services acquisition policy and procedures include assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service acquisition policy is documented across this SSP, ADR 0001 (EULA/pre-flight review, serving as the acquisition policy record for RegScale CE), ADR 0008 (Plan 3 pre-execution realignment, codifying authoring policy and implementation-status rubric), and the parent `C:\Projects\CLAUDE.md` (acquisition conventions: open-source stack preference, COTS vendor list, no hardcoded secrets, attack-scope boundaries). The designated policy official is Brian Chaplow (system owner, sole operator). Procedures are documented in per-service deploy READMEs (`deploy/defectdojo/README.md`, `deploy/regscale/README.md`) and in `runbooks/cert-trust.md` for TLS posture decisions. Policy and procedures are reviewed annually and after each plan phase completion; events triggering an off-cycle review include new service enrollment, vendor support-end announcements, or any deviation requiring an ADR.

This control is partial because no formal dissemination process exists beyond the single operator who both produces and consumes the policy -- a structural limitation of a single-operator system. All policy artifacts are accessible to the sole operator at all times; the gap is the absence of a multi-party dissemination record. Cross-reference SA-3 (the ADR/plan workflow is the closest analog to a formal SDLC incorporating acquisition policy decisions).

#### Implementation Status: partial

______________________________________________________________________
