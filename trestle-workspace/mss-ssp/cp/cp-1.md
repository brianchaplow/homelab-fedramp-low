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
  cp-1_prm_1:
    aggregates:
      - cp-01_odp.01
      - cp-01_odp.02
    profile-param-value-origin: organization
  cp-01_odp.01:
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  cp-01_odp.02:
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  cp-01_odp.03:
    alt-identifier: cp-1_prm_2
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  cp-01_odp.04:
    alt-identifier: cp-1_prm_3
    profile-values:
      - annually
    profile-param-value-origin: organization
  cp-01_odp.05:
    alt-identifier: cp-1_prm_4
    profile-values:
      - significant system change, security incident, or external audit finding
    profile-param-value-origin: organization
  cp-01_odp.06:
    alt-identifier: cp-1_prm_5
    profile-values:
      - annually
    profile-param-value-origin: organization
  cp-01_odp.07:
    alt-identifier: cp-1_prm_6
    profile-values:
      - significant system change, security incident, or external audit finding
    profile-param-value-origin: organization
  cp-01_odp.08:
    alt-identifier: cp-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cp-01
---

# cp-1 - \[Contingency Planning\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the contingency planning policy and the associated contingency planning controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the contingency planning policy and procedures; and

- \[c.\] Review and update the current contingency planning:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[CP-01a.\]

  - \[CP-01a.[01]\] a contingency planning policy is developed and documented;
  - \[CP-01a.[02]\] the contingency planning policy is disseminated to [personnel or roles];
  - \[CP-01a.[03]\] contingency planning procedures to facilitate the implementation of the contingency planning policy and associated contingency planning controls are developed and documented;
  - \[CP-01a.[04]\] the contingency planning procedures are disseminated to [personnel or roles];
  - \[CP-01a.01\]

    - \[CP-01a.01(a)\]

      - \[CP-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses purpose;
      - \[CP-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses scope;
      - \[CP-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses roles;
      - \[CP-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses responsibilities;
      - \[CP-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses management commitment;
      - \[CP-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses coordination among organizational entities;
      - \[CP-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy addresses compliance;

    - \[CP-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] contingency planning policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[CP-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the contingency planning policy and procedures;

- \[CP-01c.\]

  - \[CP-01c.01\]

    - \[CP-01c.01[01]\] the current contingency planning policy is reviewed and updated [frequency];
    - \[CP-01c.01[02]\] the current contingency planning policy is reviewed and updated following [events];

  - \[CP-01c.02\]

    - \[CP-01c.02[01]\] the current contingency planning procedures are reviewed and updated [frequency];
    - \[CP-01c.02[02]\] the current contingency planning procedures are reviewed and updated following [events].

## Control guidance

Contingency planning policy and procedures address the controls in the CP family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of contingency planning policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to contingency planning policy and procedures include assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

No formal standalone contingency planning policy document has been authored for this system. The contingency policy posture is captured at the system level through three artifacts: ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`) records the reactive decision to harden the PBS NFS automount after a 5-day backup gap was discovered during the 2026-04-07 rack consolidation reboot; `runbooks/restore-from-pbs.md` establishes recovery procedures for the two in-boundary GRC VMs (dojo and regscale); and `runbooks/monthly-conmon.md` specifies the interim manual PBS backup tripwire maintained until automated Wazuh alerting is wired. The system owner (Brian Chaplow) is the sole designated official responsible for development, documentation, and dissemination of contingency planning policy and procedures.

This SSP document serves as the policy artifact for CP-1 purposes, binding the system-level contingency planning requirements to the mechanisms described above. The policy will be reviewed annually and following any significant system change, security incident, or external audit finding. No organizational elements or additional personnel exist in this single-operator homelab; dissemination is self-referential to the system owner role.

This control is rated `planned` because no dedicated CP policy document predates this SSP authoring cycle. The SSP narrative constitutes the policy record going forward; procedures exist in the runbook corpus.

#### Implementation Status: planned

______________________________________________________________________
