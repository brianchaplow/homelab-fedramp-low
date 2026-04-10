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
  pe-1_prm_1:
    aggregates:
      - pe-01_odp.01
      - pe-01_odp.02
    profile-param-value-origin: organization
  pe-01_odp.01:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  pe-01_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  pe-01_odp.03:
    alt-identifier: pe-1_prm_2
    profile-values:
      - annually and after each plan phase completion or physical infrastructure change
    profile-param-value-origin: organization
  pe-01_odp.04:
    alt-identifier: pe-1_prm_3
    profile-values:
      - plan phase completion, rack rebuild or equipment addition, security incident, or regulatory change
    profile-param-value-origin: organization
  pe-01_odp.05:
    alt-identifier: pe-1_prm_4
    profile-values:
      - annually and after each plan phase completion
    profile-param-value-origin: organization
  pe-01_odp.06:
    alt-identifier: pe-1_prm_5
    profile-values:
      - plan phase completion, new service enrollment, or physical infrastructure change
    profile-param-value-origin: organization
  pe-01_odp.07:
    alt-identifier: pe-1_prm_6
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
  pe-01_odp.08:
    alt-identifier: pe-1_prm_7
    profile-values:
      - Brian Chaplow (system owner)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pe-01
---

# pe-1 - \[Physical and Environmental Protection\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the physical and environmental protection policy and the associated physical and environmental protection controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the physical and environmental protection policy and procedures; and

- \[c.\] Review and update the current physical and environmental protection:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[PE-01a.\]

  - \[PE-01a.[01]\] a physical and environmental protection policy is developed and documented;
  - \[PE-01a.[02]\] the physical and environmental protection policy is disseminated to [personnel or roles];
  - \[PE-01a.[03]\] physical and environmental protection procedures to facilitate the implementation of the physical and environmental protection policy and associated physical and environmental protection controls are developed and documented;
  - \[PE-01a.[04]\] the physical and environmental protection procedures are disseminated to [personnel or roles];
  - \[PE-01a.01\]

    - \[PE-01a.01(a)\]

      - \[PE-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses purpose;
      - \[PE-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses scope;
      - \[PE-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses roles;
      - \[PE-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses responsibilities;
      - \[PE-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses management commitment;
      - \[PE-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses coordination among organizational entities;
      - \[PE-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy addresses compliance;

    - \[PE-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] physical and environmental protection policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[PE-01b.\] the [official] is designated to manage the development, documentation, and disseminate of the physical and environmental protection policy and procedures;

- \[PE-01c.\]

  - \[PE-01c.01\]

    - \[PE-01c.01[01]\] the current physical and environmental protection policy is reviewed and updated [frequency];
    - \[PE-01c.01[02]\] the current physical and environmental protection policy is reviewed and updated following [events];

  - \[PE-01c.02\]

    - \[PE-01c.02[01]\] the current physical and environmental protection procedures are reviewed and updated [frequency];
    - \[PE-01c.02[02]\] the current physical and environmental protection procedures are reviewed and updated following [events].

## Control guidance

Physical and environmental protection policy and procedures address the controls in the PE family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of physical and environmental protection policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to physical and environmental protection policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service operates in a private residence with Brian Chaplow (system owner and sole operator) as the designated official responsible for physical and environmental protection policy. The policy exists as a distributed set of artifacts: this SSP document, ADR 0001 (pre-flight and EULA), ADR 0002 (Plan 1 deployment completion), ADR 0005 (PBS backup gap and automount fix -- documenting a physical rack reboot event and its downstream impact), and ADR 0008 (Plan 3 pre-execution realignment). The whole-project design document explicitly acknowledges the PE family as partial (residential homelab substitutes homeowner access control for enterprise physical security) and the rack build design spec records the physical environment specification including equipment placement, power architecture, airflow, and cable management. Policy review is event-driven: at each plan phase boundary and after any physical infrastructure change. The sole dissemination audience is the system owner.

This implementation is partial rather than not-applicable because policy artifacts genuinely exist across the ADR corpus and design documents, but no standalone formal enterprise-grade PE policy document has been produced for a single-operator residential system. The gap is formality of document structure, not absence of policy intent. The whole-project design §PE honest-gaps row documents this limitation as intentional: "Partial -- homelab rack locks + camera." This SSP and its associated ADRs collectively constitute the PE policy record for the Managed SOC Service; they address purpose, scope, roles, responsibilities, and compliance consistent with the FedRAMP Rev 5 Low baseline for a private-residence homelab context.

#### Implementation Status: partial

______________________________________________________________________
