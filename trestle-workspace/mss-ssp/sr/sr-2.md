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
  sr-02_odp.01:
    alt-identifier: sr-2_prm_1
    profile-values:
      - All in-boundary hardware components (brisket -- Lenovo ThinkStation P3 Tiny Gen 2; haccp, pitcrew, smoker -- Lenovo ThinkStation P340 Tiny; OPNsense -- Protectli VP2420; MokerLink 10G08410GSM) and all in-boundary software services documented in inventory/overlay.yaml
    profile-param-value-origin: organization
  sr-02_odp.02:
    alt-identifier: sr-2_prm_2
    profile-values:
      - annually or after a significant hardware acquisition or change event
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-02
---

# sr-2 - \[Supply Chain Risk Management\] Supply Chain Risk Management Plan

## Control Statement

- \[a.\] Develop a plan for managing supply chain risks associated with the research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal of the following systems, system components or system services: [systems, system components, or system services];

- \[b.\] Review and update the supply chain risk management plan [frequency] or as required, to address threat, organizational or environmental changes; and

- \[c.\] Protect the supply chain risk management plan from unauthorized disclosure and modification.

## Control Assessment Objective

- \[SR-02a.\]

  - \[SR-02a.[01]\] a plan for managing supply chain risks is developed;
  - \[SR-02a.[02]\] the supply chain risk management plan addresses risks associated with the research and development of [systems, system components, or system services];
  - \[SR-02a.[03]\] the supply chain risk management plan addresses risks associated with the design of [systems, system components, or system services];
  - \[SR-02a.[04]\] the supply chain risk management plan addresses risks associated with the manufacturing of [systems, system components, or system services];
  - \[SR-02a.[05]\] the supply chain risk management plan addresses risks associated with the acquisition of [systems, system components, or system services];
  - \[SR-02a.[06]\] the supply chain risk management plan addresses risks associated with the delivery of [systems, system components, or system services];
  - \[SR-02a.[07]\] the supply chain risk management plan addresses risks associated with the integration of [systems, system components, or system services];
  - \[SR-02a.[08]\] the supply chain risk management plan addresses risks associated with the operation and maintenance of [systems, system components, or system services];
  - \[SR-02a.[09]\] the supply chain risk management plan addresses risks associated with the disposal of [systems, system components, or system services];

- \[SR-02b.\] the supply chain risk management plan is reviewed and updated [frequency] or as required to address threat, organizational, or environmental changes;

- \[SR-02c.\]

  - \[SR-02c.[01]\] the supply chain risk management plan is protected from unauthorized disclosure;
  - \[SR-02c.[02]\] the supply chain risk management plan is protected from unauthorized modification.

## Control guidance

The dependence on products, systems, and services from external providers, as well as the nature of the relationships with those providers, present an increasing level of risk to an organization. Threat actions that may increase security or privacy risks include unauthorized production, the insertion or use of counterfeits, tampering, theft, insertion of malicious software and hardware, and poor manufacturing and development practices in the supply chain. Supply chain risks can be endemic or systemic within a system element or component, a system, an organization, a sector, or the Nation. Managing supply chain risk is a complex, multifaceted undertaking that requires a coordinated effort across an organization to build trust relationships and communicate with internal and external stakeholders. Supply chain risk management (SCRM) activities include identifying and assessing risks, determining appropriate risk response actions, developing SCRM plans to document response actions, and monitoring performance against plans. The SCRM plan (at the system-level) is implementation specific, providing policy implementation, requirements, constraints and implications. It can either be stand-alone, or incorporated into system security and privacy plans. The SCRM plan addresses managing, implementation, and monitoring of SCRM controls and the development/sustainment of systems across the SDLC to support mission and business functions.

Because supply chains can differ significantly across and within organizations, SCRM plans are tailored to the individual program, organizational, and operational contexts. Tailored SCRM plans provide the basis for determining whether a technology, service, system component, or system is fit for purpose, and as such, the controls need to be tailored accordingly. Tailored SCRM plans help organizations focus their resources on the most critical mission and business functions based on mission and business requirements and their risk environment. Supply chain risk management plans include an expression of the supply chain risk tolerance for the organization, acceptable supply chain risk mitigation strategies or controls, a process for consistently evaluating and monitoring supply chain risk, approaches for implementing and communicating the plan, a description of and justification for supply chain risk mitigation measures taken, and associated roles and responsibilities. Finally, supply chain risk management plans address requirements for developing trustworthy, secure, privacy-protective, and resilient system components and systems, including the application of the security design principles implemented as part of life cycle-based systems security engineering processes (see [SA-8](#sa-8)).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS informal SCRM plan is embedded in this SSP and supported by the hardware inventory at `inventory/overlay.yaml`. All hardware was acquired new from established US primary vendors -- Lenovo ThinkStation units purchased directly from Lenovo, the Protectli VP2420 from protectli.com (manufacturer direct), and the MokerLink 10G08410GSM through Amazon Business. No gray-market or refurbished hardware was used. This direct-from-vendor posture is the primary acquisition-phase risk control.

Integration and operations risk is managed through the COTS-only software policy: all services (Wazuh, ELK, DefectDojo, RegScale, Shuffle, TheHive, Velociraptor, Caldera, OpenCTI, Arkime) are installed from official distribution channels (vendor-signed apt repositories or official Docker Hub images). Wazuh syscollector continuously inventories installed packages on all in-boundary agents, providing ongoing software component tracking. The 2026-04-07 rack consolidation drive swaps (haccp 2TB Samsung 990 EVO Plus PCAP drive, pitcrew +512GB, smoker +1TB) were performed by the System Owner directly from new purchased hardware -- no third-party handling.

The SCRM plan record -- comprising this SSP, `inventory/overlay.yaml`, `inventory/IIW-2026-04.xlsx`, and relevant ADRs -- is protected from unauthorized disclosure and modification by GitHub repository access controls and the git commit history. Secrets are stored in `.env` (gitignored, never committed). The plan is reviewed annually and after any significant hardware acquisition or major environmental change.

The gap at this stage is the absence of a stand-alone formal SCRM plan document; the plan is distributed across this SSP and inventory artifacts rather than consolidated in a single document. This gap is acknowledged and accepted at the partial rating.

#### Implementation Status: partial

______________________________________________________________________
