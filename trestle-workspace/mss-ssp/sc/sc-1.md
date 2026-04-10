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
  sc-1_prm_1:
    aggregates:
      - sc-01_odp.01
      - sc-01_odp.02
    profile-param-value-origin: organization
  sc-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  sc-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  sc-01_odp.03:
    alt-identifier: sc-1_prm_2
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  sc-01_odp.04:
    alt-identifier: sc-1_prm_3
    profile-values:
      - annually
    profile-param-value-origin: organization
  sc-01_odp.05:
    alt-identifier: sc-1_prm_4
    profile-values:
      - when a new phase adds infrastructure components or when a security incident reveals a gap
    profile-param-value-origin: organization
  sc-01_odp.06:
    alt-identifier: sc-1_prm_5
    profile-values:
      - annually
    profile-param-value-origin: organization
  sc-01_odp.07:
    alt-identifier: sc-1_prm_6
    profile-values:
      - when a new phase adds infrastructure components or when a security incident reveals a gap
    profile-param-value-origin: organization
  sc-01_odp.08:
    alt-identifier: sc-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sc-01
---

# sc-1 - \[System and Communications Protection\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the system and communications protection policy and the associated system and communications protection controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the system and communications protection policy and procedures; and

- \[c.\] Review and update the current system and communications protection:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[SC-01a.\]

  - \[SC-01a.[01]\] a system and communications protection policy is developed and documented;
  - \[SC-01a.[02]\] the system and communications protection policy is disseminated to [personnel or roles];
  - \[SC-01a.[03]\] system and communications protection procedures to facilitate the implementation of the system and communications protection policy and associated system and communications protection controls are developed and documented;
  - \[SC-01a.[04]\] the system and communications protection procedures are disseminated to [personnel or roles];
  - \[SC-01a.01\]

    - \[SC-01a.01(a)\]

      - \[SC-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses purpose;
      - \[SC-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses scope;
      - \[SC-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses roles;
      - \[SC-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses responsibilities;
      - \[SC-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses management commitment;
      - \[SC-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses coordination among organizational entities;
      - \[SC-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy addresses compliance;

    - \[SC-01a.01(b)\] the [Selection (one or more): organization-level; mission/business-process-level; system-level] system and communications protection policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[SC-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the system and communications protection policy and procedures;

- \[SC-01c.\]

  - \[SC-01c.01\]

    - \[SC-01c.01[01]\] the current system and communications protection policy is reviewed and updated [frequency];
    - \[SC-01c.01[02]\] the current system and communications protection policy is reviewed and updated following [events];

  - \[SC-01c.02\]

    - \[SC-01c.02[01]\] the current system and communications protection procedures are reviewed and updated [frequency];
    - \[SC-01c.02[02]\] the current system and communications protection procedures are reviewed and updated following [events].

## Control guidance

System and communications protection policy and procedures address the controls in the SC family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of system and communications protection policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to system and communications protection policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

System and communications protection policy is documented at the system level across several artifacts that collectively define the MSS SC posture. CLAUDE.md §Network Quick Reference codifies the VLAN architecture, the attack-target-only-on-VLAN-40 mandate, and inter-VLAN isolation conventions that serve as the de facto SC policy for all operators. OPNsense firewall rules and MokerLink L3 ACLs translate those conventions into enforced controls. The ADR series (0001-0008) provides an auditable policy-evolution trail -- each ADR captures the decision rationale when a configuration trade-off or gap is accepted. `runbooks/cert-trust.md` documents the TLS posture rationale and the upgrade path. Brian Chaplow (system owner, sole operator) is the designated official for SC policy management, review, and dissemination. Policy and procedures are reviewed annually and whenever a new phase adds infrastructure components or a security incident reveals a gap.

Gap: no formal standalone SC policy document exists -- policy lives in CLAUDE.md conventions, OPNsense rule comments, and ADR artifacts rather than a dedicated policy document. This is a recognized gap for a single-operator homelab environment; a consolidated SC policy document is a future hardening item. All procedures for implementing SC controls (firewall management, key enrollment, TLS configuration) are captured inline in CLAUDE.md, `reference/network.md`, and per-service runbooks rather than a unified procedures document.

#### Implementation Status: partial

______________________________________________________________________
