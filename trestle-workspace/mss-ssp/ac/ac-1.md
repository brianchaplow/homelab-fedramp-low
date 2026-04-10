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
  ac-1_prm_1:
    aggregates:
      - ac-01_odp.01
      - ac-01_odp.02
    profile-param-value-origin: organization
  ac-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  ac-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  ac-01_odp.03:
    alt-identifier: ac-1_prm_2
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  ac-01_odp.04:
    alt-identifier: ac-1_prm_3
    profile-values:
      - plan phase completion, new service enrollment, security incident, or regulatory change
    profile-param-value-origin: organization
  ac-01_odp.05:
    alt-identifier: ac-1_prm_4
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  ac-01_odp.06:
    alt-identifier: ac-1_prm_5
    profile-values:
      - plan phase completion, new service enrollment, or deviation requiring an ADR
    profile-param-value-origin: organization
  ac-01_odp.07:
    alt-identifier: ac-1_prm_6
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
  ac-01_odp.08:
    alt-identifier: ac-1_prm_7
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ac-01
---

# ac-1 - \[Access Control\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the access control policy and the associated access controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the access control policy and procedures; and

- \[c.\] Review and update the current access control:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[AC-01a.\]

  - \[AC-01a.[01]\] an access control policy is developed and documented;
  - \[AC-01a.[02]\] the access control policy is disseminated to [personnel or roles];
  - \[AC-01a.[03]\] access control procedures to facilitate the implementation of the access control policy and associated controls are developed and documented;
  - \[AC-01a.[04]\] the access control procedures are disseminated to [personnel or roles];
  - \[AC-01a.01\]

    - \[AC-01a.01(a)\]

      - \[AC-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses purpose;
      - \[AC-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses scope;
      - \[AC-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses roles;
      - \[AC-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses responsibilities;
      - \[AC-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses management commitment;
      - \[AC-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses coordination among organizational entities;
      - \[AC-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy addresses compliance;

    - \[AC-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] access control policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[AC-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the access control policy and procedures;

- \[AC-01c.\]

  - \[AC-01c.01\]

    - \[AC-01c.01[01]\] the current access control policy is reviewed and updated [frequency];
    - \[AC-01c.01[02]\] the current access control policy is reviewed and updated following [events];

  - \[AC-01c.02\]

    - \[AC-01c.02[01]\] the current access control procedures are reviewed and updated [frequency];
    - \[AC-01c.02[02]\] the current access control procedures are reviewed and updated following [events].

## Control guidance

Access control policy and procedures address the controls in the AC family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of access control policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies reflecting the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to access control policy and procedures include assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service access control policy is embodied across three artifact layers. The system-level VLAN segmentation rules, SSH key-only conventions, credential handling requirements, and authorized attack targets are established in `CLAUDE.md` (the canonical system policy reference) and enforced through OPNsense inter-VLAN firewall rules and MokerLink switch ACLs. Procedural artifacts are distributed across service-specific deployment READMEs (`deploy/defectdojo/README.md`, `deploy/regscale/README.md`) and TLS posture runbooks (`runbooks/cert-trust.md`). Architectural access decisions that deviate from secure defaults are recorded and approved as ADRs -- ADR 0001 (EULA and pre-flight decisions), ADR 0002 (Plan 1 deployment completion and operator action items), and ADR 0008 (Plan 3 pre-execution realignment including the implementation status rubric) collectively constitute the access control policy and procedure record for this system. Brian Chaplow, as system owner and sole operator, is the designated official for managing and updating this policy. Policy and procedures are reviewed annually and after each plan phase completion, and are updated when a plan phase concludes, a new service is enrolled, a security incident occurs, or a deviation warrants an ADR.

The gap driving `partial` status is the absence of a formal HR-style dissemination step -- in a single-operator personal system, the policy author and the sole recipient are the same individual. No external review, approval, or acknowledgment workflow exists for this policy. ADR 0008 §Pre-execution decisions item 5 documents the implementation status rubric applied throughout Plan 3, establishing that this gap is acknowledged and accepted for a single-operator homelab boundary. Cross-reference IA-1 for the same pattern applied to the identification and authentication family.

#### Implementation Status: partial

______________________________________________________________________
