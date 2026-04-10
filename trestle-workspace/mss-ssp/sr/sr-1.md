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
  sr-1_prm_1:
    aggregates:
      - sr-01_odp.01
      - sr-01_odp.02
    profile-param-value-origin: organization
  sr-01_odp.01:
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  sr-01_odp.02:
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  sr-01_odp.03:
    alt-identifier: sr-1_prm_2
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
  sr-01_odp.04:
    alt-identifier: sr-1_prm_3
    profile-values:
      - annually
    profile-param-value-origin: organization
  sr-01_odp.05:
    alt-identifier: sr-1_prm_4
    profile-values:
      - significant hardware acquisition, vendor compromise notification, or major system change
    profile-param-value-origin: organization
  sr-01_odp.06:
    alt-identifier: sr-1_prm_5
    profile-values:
      - annually
    profile-param-value-origin: organization
  sr-01_odp.07:
    alt-identifier: sr-1_prm_6
    profile-values:
      - significant hardware acquisition, vendor compromise notification, or major system change
    profile-param-value-origin: organization
  sr-01_odp.08:
    alt-identifier: sr-1_prm_7
    profile-values:
      - system-level
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-01
---

# sr-1 - \[Supply Chain Risk Management\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the supply chain risk management policy and the associated supply chain risk management controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the supply chain risk management policy and procedures; and

- \[c.\] Review and update the current supply chain risk management:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[SR-01a.\]

  - \[SR-01a.[01]\] a supply chain risk management policy is developed and documented;
  - \[SR-01a.[02]\] the supply chain risk management policy is disseminated to [personnel or roles];
  - \[SR-01a.[03]\] supply chain risk management procedures to facilitate the implementation of the supply chain risk management policy and the associated supply chain risk management controls are developed and documented;
  - \[SR-01a.[04]\] the supply chain risk management procedures are disseminated to [personnel or roles].
  - \[SR-01a.01\]

    - \[SR-01a.01(a)\]

      - \[SR-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses purpose;
      - \[SR-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses scope;
      - \[SR-01a.01(a)[03]\] [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses roles;
      - \[SR-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses responsibilities;
      - \[SR-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses management commitment;
      - \[SR-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses coordination among organizational entities;
      - \[SR-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy addresses compliance.

    - \[SR-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] supply chain risk management policy is consistent with applicable laws, Executive Orders, directives, regulations, policies, standards, and guidelines;

- \[SR-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the supply chain risk management policy and procedures;

- \[SR-01c.\]

  - \[SR-01c.01\]

    - \[SR-01c.01[01]\] the current supply chain risk management policy is reviewed and updated [frequency];
    - \[SR-01c.01[02]\] the current supply chain risk management policy is reviewed and updated following [events];

  - \[SR-01c.02\]

    - \[SR-01c.02[01]\] the current supply chain risk management procedures are reviewed and updated [frequency];
    - \[SR-01c.02[02]\] the current supply chain risk management procedures are reviewed and updated following [events].

## Control guidance

Supply chain risk management policy and procedures address the controls in the SR family as well as supply chain-related controls in other families that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of supply chain risk management policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to supply chain risk management policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS supply chain risk management policy is documented at the system level within this SSP. The System Owner (Brian Chaplow) holds all SCRM roles for this single-operator homelab -- purchaser, integrator, operator, and disposer -- and serves as the sole designated official responsible for developing, maintaining, and disseminating the policy and procedures. This single-operator structure collapses the multi-person SCRM team concept into one accountable role.

The policy scope covers all in-boundary hardware and software components: the Lenovo ThinkStation P3 Tiny Gen 2 (brisket), three Lenovo ThinkStation P340 Tiny units (haccp, pitcrew, smoker), the Protectli VP2420 (OPNsense firewall), the MokerLink 10G08410GSM switch, and all in-boundary software services listed in `inventory/overlay.yaml`. The policy is consistent with NIST SP 800-161r1 (supply chain risk management practices) and the FedRAMP Rev 5 Low baseline. The policy and supporting procedures are embedded in this SSP and reviewed annually and following any significant hardware acquisition, vendor compromise notification, or major system change.

#### Implementation Status: planned

______________________________________________________________________
