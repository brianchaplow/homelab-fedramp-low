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
  si-05_odp.01:
    alt-identifier: si-5_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-05_odp.02:
    alt-identifier: si-5_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-05_odp.03:
    alt-identifier: si-5_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-05_odp.04:
    alt-identifier: si-5_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-05_odp.05:
    alt-identifier: si-5_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: si-05
---

# si-5 - \[System and Information Integrity\] Security Alerts, Advisories, and Directives

## Control Statement

- \[a.\] Receive system security alerts, advisories, and directives from [external organizations] on an ongoing basis;

- \[b.\] Generate internal security alerts, advisories, and directives as deemed necessary;

- \[c.\] Disseminate security alerts, advisories, and directives to: [Selection (one or more): [personnel or roles]; [elements]; [external organizations]] ; and

- \[d.\] Implement security directives in accordance with established time frames, or notify the issuing organization of the degree of noncompliance.

## Control Assessment Objective

- \[SI-05a.\] system security alerts, advisories, and directives are received from [external organizations] on an ongoing basis;

- \[SI-05b.\] internal security alerts, advisories, and directives are generated as deemed necessary;

- \[SI-05c.\] security alerts, advisories, and directives are disseminated to [Selection (one or more): [personnel or roles]; [elements]; [external organizations]];

- \[SI-05d.\] security directives are implemented in accordance with established time frames or if the issuing organization is notified of the degree of noncompliance.

## Control guidance

The Cybersecurity and Infrastructure Security Agency (CISA) generates security alerts and advisories to maintain situational awareness throughout the Federal Government. Security directives are issued by OMB or other designated organizations with the responsibility and authority to issue such directives. Compliance with security directives is essential due to the critical nature of many of these directives and the potential (immediate) adverse effects on organizational operations and assets, individuals, other organizations, and the Nation should the directives not be implemented in a timely manner. External organizations include supply chain partners, external mission or business partners, external service providers, and other peer or supporting organizations.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: si-5 -->

#### Implementation Status: planned

______________________________________________________________________
