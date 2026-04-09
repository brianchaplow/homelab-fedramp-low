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
  ra-03_odp.01:
    alt-identifier: ra-3_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ra-03_odp.02:
    alt-identifier: ra-3_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ra-03_odp.03:
    alt-identifier: ra-3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ra-03_odp.04:
    alt-identifier: ra-3_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  ra-03_odp.05:
    alt-identifier: ra-3_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ra-03
---

# ra-3 - \[Risk Assessment\] Risk Assessment

## Control Statement

- \[a.\] Conduct a risk assessment, including:

  - \[1.\] Identifying threats to and vulnerabilities in the system;
  - \[2.\] Determining the likelihood and magnitude of harm from unauthorized access, use, disclosure, disruption, modification, or destruction of the system, the information it processes, stores, or transmits, and any related information; and
  - \[3.\] Determining the likelihood and impact of adverse effects on individuals arising from the processing of personally identifiable information;

- \[b.\] Integrate risk assessment results and risk management decisions from the organization and mission or business process perspectives with system-level risk assessments;

- \[c.\] Document risk assessment results in [Selection: security and privacy plans; risk assessment report; [document]];

- \[d.\] Review risk assessment results [frequency];

- \[e.\] Disseminate risk assessment results to [personnel or roles] ; and

- \[f.\] Update the risk assessment [frequency] or when there are significant changes to the system, its environment of operation, or other conditions that may impact the security or privacy state of the system.

## Control Assessment Objective

- \[RA-03a.\]

  - \[RA-03a.01\] a risk assessment is conducted to identify threats to and vulnerabilities in the system;
  - \[RA-03a.02\] a risk assessment is conducted to determine the likelihood and magnitude of harm from unauthorized access, use, disclosure, disruption, modification, or destruction of the system; the information it processes, stores, or transmits; and any related information;
  - \[RA-03a.03\] a risk assessment is conducted to determine the likelihood and impact of adverse effects on individuals arising from the processing of personally identifiable information;

- \[RA-03b.\] risk assessment results and risk management decisions from the organization and mission or business process perspectives are integrated with system-level risk assessments;

- \[RA-03c.\] risk assessment results are documented in [Selection: security and privacy plans; risk assessment report; [document]];

- \[RA-03d.\] risk assessment results are reviewed [frequency];

- \[RA-03e.\] risk assessment results are disseminated to [personnel or roles];

- \[RA-03f.\] the risk assessment is updated [frequency] or when there are significant changes to the system, its environment of operation, or other conditions that may impact the security or privacy state of the system.

## Control guidance

Risk assessments consider threats, vulnerabilities, likelihood, and impact to organizational operations and assets, individuals, other organizations, and the Nation. Risk assessments also consider risk from external parties, including contractors who operate systems on behalf of the organization, individuals who access organizational systems, service providers, and outsourcing entities.

Organizations can conduct risk assessments at all three levels in the risk management hierarchy (i.e., organization level, mission/business process level, or information system level) and at any stage in the system development life cycle. Risk assessments can also be conducted at various steps in the Risk Management Framework, including preparation, categorization, control selection, control implementation, control assessment, authorization, and control monitoring. Risk assessment is an ongoing activity carried out throughout the system development life cycle.

Risk assessments can also address information related to the system, including system design, the intended use of the system, testing results, and supply chain-related information or artifacts. Risk assessments can play an important role in control selection processes, particularly during the application of tailoring guidance and in the earliest phases of capability determination.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: ra-3 -->

#### Implementation Status: planned

______________________________________________________________________
