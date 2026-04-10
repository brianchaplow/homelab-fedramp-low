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
  sr-02.01_odp.01:
    alt-identifier: sr-2.1_prm_1
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  sr-02.01_odp.02:
    alt-identifier: sr-2.1_prm_2
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-02.01
---

# sr-2.1 - \[Supply Chain Risk Management\] Establish SCRM Team

## Control Statement

Establish a supply chain risk management team consisting of [personnel, roles and responsibilities] to lead and support the following SCRM activities: [supply chain risk management activities].

## Control Assessment Objective

a supply chain risk management team consisting of [personnel, roles and responsibilities] is established to lead and support [supply chain risk management activities].

## Control guidance

To implement supply chain risk management plans, organizations establish a coordinated, team-based approach to identify and assess supply chain risks and manage these risks by using programmatic and technical mitigation techniques. The team approach enables organizations to conduct an analysis of their supply chain, communicate with internal and external partners or stakeholders, and gain broad consensus regarding the appropriate resources for SCRM. The SCRM team consists of organizational personnel with diverse roles and responsibilities for leading and supporting SCRM activities, including risk executive, information technology, contracting, information security, privacy, mission or business, legal, supply chain and logistics, acquisition, business continuity, and other relevant functions. Members of the SCRM team are involved in various aspects of the SDLC and, collectively, have an awareness of and provide expertise in acquisition processes, legal practices, vulnerabilities, threats, and attack vectors, as well as an understanding of the technical aspects and dependencies of systems. The SCRM team can be an extension of the security and privacy risk management processes or be included as part of an organizational risk management team.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. MSS is a single-operator personal homelab system. Brian Chaplow (System Owner) is the only person associated with this system in any supply chain capacity -- purchaser, integrator, operator, and disposer. There are no personnel resources to constitute a dedicated multi-person SCRM team; all SCRM roles are consolidated under the System Owner. A formal SCRM team with role differentiation across acquisition, legal, logistics, information security, and business continuity functions is not feasible or appropriate at this scale.

The System Owner maintains awareness of supply chain risks through professional background (27 years military service, cybersecurity program context, FedRAMP ConMon portfolio development) and applies informal single-operator SCRM mitigations: direct-from-vendor hardware purchasing, official-channel software installation, and apt GPG key verification. These practices implement the anti-counterfeit and provenance intent of the control without a formal team structure.

#### Implementation Status: not-applicable

______________________________________________________________________
