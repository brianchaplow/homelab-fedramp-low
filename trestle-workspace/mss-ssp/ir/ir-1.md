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
  ir-1_prm_1:
    aggregates:
      - ir-01_odp.01
      - ir-01_odp.02
    profile-param-value-origin: organization
  ir-01_odp.01:
    profile-values:
      - system owner; SOC operator
    profile-param-value-origin: organization
  ir-01_odp.02:
    profile-values:
      - system owner; SOC operator
    profile-param-value-origin: organization
  ir-01_odp.03:
    alt-identifier: ir-1_prm_2
    profile-values:
      - annually
    profile-param-value-origin: organization
  ir-01_odp.04:
    alt-identifier: ir-1_prm_3
    profile-values:
      - security incident resulting in an ADR; significant regulatory change
    profile-param-value-origin: organization
  ir-01_odp.05:
    alt-identifier: ir-1_prm_4
    profile-values:
      - annually
    profile-param-value-origin: organization
  ir-01_odp.06:
    alt-identifier: ir-1_prm_5
    profile-values:
      - security incident; runbook gap discovery
    profile-param-value-origin: organization
  ir-01_odp.07:
    alt-identifier: ir-1_prm_6
    profile-values:
      - system owner (Brian Chaplow)
    profile-param-value-origin: organization
  ir-01_odp.08:
    alt-identifier: ir-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ir-01
---

# ir-1 - \[Incident Response\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the incident response policy and the associated incident response controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the incident response policy and procedures; and

- \[c.\] Review and update the current incident response:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[IR-01a.\]

  - \[IR-01a.[01]\] an incident response policy is developed and documented;
  - \[IR-01a.[02]\] the incident response policy is disseminated to [personnel or roles];
  - \[IR-01a.[03]\] incident response procedures to facilitate the implementation of the incident response policy and associated incident response controls are developed and documented;
  - \[IR-01a.[04]\] the incident response procedures are disseminated to [personnel or roles];
  - \[IR-01a.01\]

    - \[IR-01a.01(a)\]

      - \[IR-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses purpose;
      - \[IR-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses scope;
      - \[IR-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses roles;
      - \[IR-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses responsibilities;
      - \[IR-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses management commitment;
      - \[IR-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses coordination among organizational entities;
      - \[IR-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy addresses compliance;

    - \[IR-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] incident response policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[IR-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the incident response policy and procedures;

- \[IR-01c.\]

  - \[IR-01c.01\]

    - \[IR-01c.01[01]\] the current incident response policy is reviewed and updated [frequency];
    - \[IR-01c.01[02]\] the current incident response policy is reviewed and updated following [events];

  - \[IR-01c.02\]

    - \[IR-01c.02[01]\] the current incident response procedures are reviewed and updated [frequency];
    - \[IR-01c.02[02]\] the current incident response procedures are reviewed and updated following [events].

## Control guidance

Incident response policy and procedures address the controls in the IR family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of incident response policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to incident response policy and procedures include assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service maintains a system-level incident response policy embedded in this SSP and in the operational runbooks committed to the homelab-fedramp-low repository. The system owner (Brian Chaplow) serves as the designated official for IR policy development, documentation, and dissemination. The policy covers purpose (detect, contain, eradicate, and recover from incidents affecting in-boundary assets: dojo VMID 201 on pitcrew and regscale VMID 301 on smoker), scope (all 15 Wazuh-enrolled hosts plus Wazuh SIEM on brisket, Shuffle SOAR, TheHive 4 + Cortex 3 on pitcrew LXC 200, Velociraptor DFIR on brisket, and ELK/Arkime on haccp), roles (system owner as policy authority; SOC operator for detection and triage; DFIR operator for endpoint forensics), and compliance with NIST SP 800-53 Rev 5 FedRAMP Low baseline. Policy and procedures are disseminated to the system owner and SOC operator via this SSP, which is version-controlled in the homelab-fedramp-low GitHub repository. The policy is reviewed annually and following any security incident that produces an ADR -- for example, ADR 0005 (PBS backup gap, 2026-04-08) triggered both a procedure update (fstab automount hardening) and a runbook amendment in `runbooks/monthly-conmon.md`. The ADR series (0001 through current) constitutes the living procedure amendment record. A gap exists: no standalone IR policy PDF has been produced outside the SSP; this is an accepted portfolio trade-off documented here.

#### Implementation Status: partial

______________________________________________________________________
