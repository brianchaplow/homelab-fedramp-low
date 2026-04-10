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
  ra-03.01_odp.01:
    alt-identifier: ra-3.1_prm_1
    profile-values:
      - all 5 in-boundary hardware assets (brisket, haccp, smokehouse, dojo VM, regscale VM) and all open-source software stacks (Wazuh 4.14.4, ELK 8.17, DefectDojo 2.57.0, RegScale CE, Trestle 4.0.1)
    profile-param-value-origin: organization
  ra-03.01_odp.02:
    alt-identifier: ra-3.1_prm_2
    profile-values:
      - annually
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ra-03.01
---

# ra-3.1 - \[Risk Assessment\] Supply Chain Risk Assessment

## Control Statement

- \[(a)\] Assess supply chain risks associated with [systems, system components, and system services] ; and

- \[(b)\] Update the supply chain risk assessment [frequency] , when there are significant changes to the relevant supply chain, or when changes to the system, environments of operation, or other conditions may necessitate a change in the supply chain.

## Control Assessment Objective

- \[RA-03(01)(a)\] supply chain risks associated with [systems, system components, and system services] are assessed;

- \[RA-03(01)(b)\] the supply chain risk assessment is updated [frequency] , when there are significant changes to the relevant supply chain, or when changes to the system, environments of operation, or other conditions may necessitate a change in the supply chain.

## Control guidance

Supply chain-related events include disruption, use of defective components, insertion of counterfeits, theft, malicious development practices, improper delivery practices, and insertion of malicious code. These events can have a significant impact on the confidentiality, integrity, or availability of a system and its information and, therefore, can also adversely impact organizational operations (including mission, functions, image, or reputation), organizational assets, individuals, other organizations, and the Nation. The supply chain-related events may be unintentional or malicious and can occur at any point during the system life cycle. An analysis of supply chain risk can help an organization identify systems or components for which additional supply chain risk mitigations are required.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Supply chain risk for the MSS homelab is assessed informally through hardware procurement provenance and software version-pinning practices documented in the ADR chain. All 5 in-boundary hosts are Lenovo ThinkStation P340 Tiny or QNAP commercial off-the-shelf (COTS) hardware sourced from US vendors, reducing counterfeit and malicious hardware insertion risk. Software stack versions are pinned by ADR record: Trestle 4.0.1 (ADR 0006 Deviation 9), DefectDojo 2.57.0 (ADR 0004), and RegScale CE (ADR 0003) are frozen at known-good versions with Proxmox VM snapshots providing rollback capability. The `inventory/overlay.yaml` records hardware model, asset tags, and end-of-life dates for all in-boundary hosts -- brisket 2029-04, haccp 2028-04, smokehouse 2027-12 -- providing a hardware lifecycle visibility artifact. The `wazuh-states-vulnerabilities-*` index captures the installed package set for each agent, enabling detection of unauthorized software supply chain changes on a continuous basis.

The partial status reflects genuine scope limits: no formal vendor contracts, no hardware SBOM, no third-party supply chain attestation process, and no software composition analysis (SCA) tool. These gaps are expected for a single-operator portfolio lab with no vendor relationships. The supply chain assessment is reviewed annually aligned with the hardware end-of-life review cadence in `inventory/overlay.yaml`, and when a significant change to the relevant supply chain or system environment is recorded in an ADR.

#### Implementation Status: partial

______________________________________________________________________
