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
  sa-8_prm_1:
    aggregates:
      - sa-08_odp.01
      - sa-08_odp.02
    profile-param-value-origin: organization
  sa-08_odp.01:
    profile-values:
      - defense-in-depth (three enforcement layers -- OPNsense inter-VLAN firewall plus MokerLink switch ACL plus UFW host firewall); least privilege (SSH key auth on all Linux hosts, UFW default-deny, service-specific accounts with minimum permissions); separation of concerns (GRC tooling tier isolated from SOC operational tier across Proxmox hosts); security-first design (Wazuh SCA CIS Ubuntu 24.04 benchmark validated on every new VM at first run); open design (all security configurations git-tracked and ADR-documented)
    profile-param-value-origin: organization
  sa-08_odp.02:
    profile-values:
      - OSCAL-as-source-of-truth (machine-readable schema-validated artifacts eliminate format drift and make security state auditable); no-PII-processed scope (no personal data stored or processed eliminates a class of privacy engineering requirements)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sa-08
---

# sa-8 - \[System and Services Acquisition\] Security and Privacy Engineering Principles

## Control Statement

Apply the following systems security and privacy engineering principles in the specification, design, development, implementation, and modification of the system and system components: [organization-defined systems security and privacy engineering principles].

## Control Assessment Objective

- \[SA-08[01]\] [systems security engineering principles] are applied in the specification of the system and system components;

- \[SA-08[02]\] [systems security engineering principles] are applied in the design of the system and system components;

- \[SA-08[03]\] [systems security engineering principles] are applied in the development of the system and system components;

- \[SA-08[04]\] [systems security engineering principles] are applied in the implementation of the system and system components;

- \[SA-08[05]\] [systems security engineering principles] are applied in the modification of the system and system components;

- \[SA-08[06]\] [privacy engineering principles] are applied in the specification of the system and system components;

- \[SA-08[07]\] [privacy engineering principles] are applied in the design of the system and system components;

- \[SA-08[08]\] [privacy engineering principles] are applied in the development of the system and system components;

- \[SA-08[09]\] [privacy engineering principles] are applied in the implementation of the system and system components;

- \[SA-08[10]\] [privacy engineering principles] are applied in the modification of the system and system components.

## Control guidance

Systems security and privacy engineering principles are closely related to and implemented throughout the system development life cycle (see [SA-3](#sa-3) ). Organizations can apply systems security and privacy engineering principles to new systems under development or to systems undergoing upgrades. For existing systems, organizations apply systems security and privacy engineering principles to system upgrades and modifications to the extent feasible, given the current state of hardware, software, and firmware components within those systems.

The application of systems security and privacy engineering principles helps organizations develop trustworthy, secure, and resilient systems and reduces the susceptibility to disruptions, hazards, threats, and the creation of privacy problems for individuals. Examples of system security engineering principles include: developing layered protections; establishing security and privacy policies, architecture, and controls as the foundation for design and development; incorporating security and privacy requirements into the system development life cycle; delineating physical and logical security boundaries; ensuring that developers are trained on how to build secure software; tailoring controls to meet organizational needs; and performing threat modeling to identify use cases, threat agents, attack vectors and patterns, design patterns, and compensating controls needed to mitigate risk.

Organizations that apply systems security and privacy engineering concepts and principles can facilitate the development of trustworthy, secure systems, system components, and system services; reduce risk to acceptable levels; and make informed risk management decisions. System security engineering principles can also be used to protect against certain supply chain risks, including incorporating tamper-resistant hardware into a design.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Security and privacy engineering principles are applied throughout the MSS specification, design, and implementation. The most concrete evidence is the three-layer defense-in-depth network architecture: OPNsense handles inter-VLAN firewall policy (VLAN 40 isolated targets, VLAN 30 lab hosts, VLAN 20 SOC infrastructure); MokerLink L3 ACL enforces switch-level east-west segmentation; UFW default-deny on each host with explicit allows for required service ports only. Least privilege is applied at every layer: SSH key-only authentication on all Linux hosts, service accounts provisioned with minimum required permissions, and no shared credentials between services (all secrets in a gitignored `.env`). The separation-of-concerns principle is expressed structurally: the GRC tooling tier (dojo on pitcrew, regscale on smoker) is isolated from the SOC operational tier (brisket, haccp, smokehouse) across separate Proxmox hypervisors. The security-first design principle is operationalized by the Wazuh SCA module running the CIS Ubuntu 24.04 benchmark on every new VM at first run, as specified in the whole-project design spec (`docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §7.9). The open-design principle is enforced by the git-tracked configuration-as-code posture: all security configurations are committed, ADR-documented, and auditable.

This control is partial because no formal systems security engineering methodology (e.g., NIST SP 800-160) was explicitly adopted, and formal privacy engineering methodology beyond OSCAL-as-source-of-truth and the no-PII-processed scope is not documented. The principles above are applied in practice through the whole-project design spec and the ADR record, but not under a named framework. Cross-reference SA-3 (SDLC -- engineering principles applied throughout the lifecycle) and SC-7 (boundary protection -- the primary engineering artifact).

#### Implementation Status: partial

______________________________________________________________________
