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
  sr-03_odp.01:
    alt-identifier: sr-3_prm_1
    profile-values:
      - All in-boundary hardware and software components inventoried in inventory/overlay.yaml and inventory/IIW-2026-04.xlsx
    profile-param-value-origin: organization
  sr-03_odp.02:
    alt-identifier: sr-3_prm_2
    profile-values:
      - System Owner (Brian Chaplow) -- sole supply chain personnel
    profile-param-value-origin: organization
  sr-03_odp.03:
    alt-identifier: sr-3_prm_3
    profile-values:
      - direct-from-vendor hardware purchasing; official-channel-only software installation; Wazuh syscollector continuous package inventory; pinned software versions in pyproject.toml and deploy README files
    profile-param-value-origin: organization
  sr-03_odp.04:
    alt-identifier: sr-3_prm_4
    profile-values:
      - security and privacy plans
    profile-param-value-origin: organization
  sr-03_odp.05:
    alt-identifier: sr-3_prm_5
    profile-values:
      - physical inspection of hardware components at receipt and during rack builds
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-03
---

# sr-3 - \[Supply Chain Risk Management\] Supply Chain Controls and Processes

## Control Statement

- \[a.\] Establish a process or processes to identify and address weaknesses or deficiencies in the supply chain elements and processes of [system or system component] in coordination with [supply chain personnel];

- \[b.\] Employ the following controls to protect against supply chain risks to the system, system component, or system service and to limit the harm or consequences from supply chain-related events: [supply chain controls] ; and

- \[c.\] Document the selected and implemented supply chain processes and controls in [Selection (one or more): security and privacy plans; supply chain risk management plan; [document]].

## Control Assessment Objective

- \[SR-03a.\]

  - \[SR-03a.[01]\] a process or processes is/are established to identify and address weaknesses or deficiencies in the supply chain elements and processes of [system or system component];
  - \[SR-03a.[02]\] the process or processes to identify and address weaknesses or deficiencies in the supply chain elements and processes of [system or system component] is/are coordinated with [supply chain personnel];

- \[SR-03b.\] [supply chain controls] are employed to protect against supply chain risks to the system, system component, or system service and to limit the harm or consequences from supply chain-related events;

- \[SR-03c.\] the selected and implemented supply chain processes and controls are documented in [Selection (one or more): security and privacy plans; supply chain risk management plan; [document]].

## Control guidance

Supply chain elements include organizations, entities, or tools employed for the research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal of systems and system components. Supply chain processes include hardware, software, and firmware development processes; shipping and handling procedures; personnel security and physical security programs; configuration management tools, techniques, and measures to maintain provenance; or other programs, processes, or procedures associated with the development, acquisition, maintenance and disposal of systems and system components. Supply chain elements and processes may be provided by organizations, system integrators, or external providers. Weaknesses or deficiencies in supply chain elements or processes represent potential vulnerabilities that can be exploited by adversaries to cause harm to the organization and affect its ability to carry out its core missions or business functions. Supply chain personnel are individuals with roles and responsibilities in the supply chain.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The System Owner (Brian Chaplow) serves as the sole supply chain coordination point for all in-boundary hardware and software components. Supply chain weaknesses are identified through two primary channels: (1) Wazuh vulnerability scanning via the `wazuh-states-vulnerabilities-*` index, which surfaces CVE-level component risk for all in-boundary agents and feeds the monthly POA&M cycle (`poam/POAM-2026-04.xlsx`, 8,473 findings); and (2) ad-hoc monitoring of vendor security advisories through public channels. Identified weaknesses are addressed through the ConMon remediation workflow (`runbooks/monthly-conmon.md`).

The primary supply chain controls employed are: (a) direct-from-vendor hardware purchasing -- all Lenovo ThinkStation units purchased directly from Lenovo, Protectli VP2420 from protectli.com, MokerLink switch through Amazon Business, with no gray-market or refurbished hardware; (b) official-channel-only software installation -- all services installed from vendor-signed apt repositories (`packages.wazuh.com`, `artifacts.elastic.co`) or official Docker Hub images; (c) Wazuh syscollector continuous package inventory on all in-boundary agents, providing the operational SBOM analog (queryable at `https://10.10.20.30:55000/syscollector/{agent_id}/packages` and normalized via `pipelines/ingest/inventory.py`); (d) software version pinning -- DefectDojo 2.57.0 (`deploy/defectdojo/README.md`), Trestle 4.0.1 (`pyproject.toml`), Wazuh 4.14.4 per Service Inventory; and (e) physical inspection of hardware at receipt and during rack builds (see SR-10).

The gap is the absence of a formal written weakness-identification procedure and a structured SBOM in SPDX or CycloneDX format. Wazuh syscollector is the operational substitute for the SBOM gap. The selected controls are documented in this SSP (`inventory/overlay.yaml`, `inventory/IIW-2026-04.xlsx`).

#### Implementation Status: partial

______________________________________________________________________
