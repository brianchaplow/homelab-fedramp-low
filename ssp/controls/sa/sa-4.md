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
  sa-04_odp.01:
    alt-identifier: sa-4_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  sa-04_odp.02:
    alt-identifier: sa-4_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sa-04
---

# sa-4 - \[System and Services Acquisition\] Acquisition Process

## Control Statement

Include the following requirements, descriptions, and criteria, explicitly or by reference, using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service:

- \[a.\] Security and privacy functional requirements;

- \[b.\] Strength of mechanism requirements;

- \[c.\] Security and privacy assurance requirements;

- \[d.\] Controls needed to satisfy the security and privacy requirements.

- \[e.\] Security and privacy documentation requirements;

- \[f.\] Requirements for protecting security and privacy documentation;

- \[g.\] Description of the system development environment and environment in which the system is intended to operate;

- \[h.\] Allocation of responsibility or identification of parties responsible for information security, privacy, and supply chain risk management; and

- \[i.\] Acceptance criteria.

## Control Assessment Objective

- \[SA-04a.\]

  - \[SA-04a.[01]\] security functional requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04a.[02]\] privacy functional requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04b.\] strength of mechanism requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04c.\]

  - \[SA-04c.[01]\] security assurance requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04c.[02]\] privacy assurance requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04d.\]

  - \[SA-04d.[01]\] controls needed to satisfy the security requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04d.[02]\] controls needed to satisfy the privacy requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04e.\]

  - \[SA-04e.[01]\] security documentation requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04e.[02]\] privacy documentation requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04f.\]

  - \[SA-04f.[01]\] requirements for protecting security documentation, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04f.[02]\] requirements for protecting privacy documentation, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04g.\] the description of the system development environment and environment in which the system is intended to operate, requirements, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;

- \[SA-04h.\]

  - \[SA-04h.[01]\] the allocation of responsibility or identification of parties responsible for information security requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service;
  - \[SA-04h.[02]\] the allocation of responsibility or identification of parties responsible for privacy requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]];
  - \[SA-04h.[03]\] the allocation of responsibility or identification of parties responsible for supply chain risk management requirements, descriptions, and criteria are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]];

- \[SA-04i.\] acceptance criteria requirements and descriptions are included explicitly or by reference using [Selection (one or more): standardized contract language; [contract language]] in the acquisition contract for the system, system component, or system service.

## Control guidance

Security and privacy functional requirements are typically derived from the high-level security and privacy requirements described in [SA-2](#sa-2) . The derived requirements include security and privacy capabilities, functions, and mechanisms. Strength requirements associated with such capabilities, functions, and mechanisms include degree of correctness, completeness, resistance to tampering or bypass, and resistance to direct attack. Assurance requirements include development processes, procedures, and methodologies as well as the evidence from development and assessment activities that provide grounds for confidence that the required functionality is implemented and possesses the required strength of mechanism. [SP 800-160-1](#e3cc0520-a366-4fc9-abc2-5272db7e3564) describes the process of requirements engineering as part of the system development life cycle.

Controls can be viewed as descriptions of the safeguards and protection capabilities appropriate for achieving the particular security and privacy objectives of the organization and for reflecting the security and privacy requirements of stakeholders. Controls are selected and implemented in order to satisfy system requirements and include developer and organizational responsibilities. Controls can include technical, administrative, and physical aspects. In some cases, the selection and implementation of a control may necessitate additional specification by the organization in the form of derived requirements or instantiated control parameter values. The derived requirements and control parameter values may be necessary to provide the appropriate level of implementation detail for controls within the system development life cycle.

Security and privacy documentation requirements address all stages of the system development life cycle. Documentation provides user and administrator guidance for the implementation and operation of controls. The level of detail required in such documentation is based on the security categorization or classification level of the system and the degree to which organizations depend on the capabilities, functions, or mechanisms to meet risk response expectations. Requirements can include mandated configuration settings that specify allowed functions, ports, protocols, and services. Acceptance criteria for systems, system components, and system services are defined in the same manner as the criteria for any organizational acquisition or procurement.

Organizations can determine other requirements that support security and operations, to include responsibilities for the organization and developer, and notification and timing requirements for support, maintenance and updates.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: sa-4 -->

#### Implementation Status: planned

______________________________________________________________________
