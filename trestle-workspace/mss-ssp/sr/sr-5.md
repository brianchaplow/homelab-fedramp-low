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
  sr-05_odp:
    alt-identifier: sr-5_prm_1
    profile-values:
      - (1) COTS-only software preference with open-source bias for auditability; (2) direct-from-vendor hardware purchasing from primary US distributors; (3) official-channel software installation via vendor-signed apt repos and official Docker Hub images; (4) Wazuh syscollector continuous package inventory as operational SBOM analog; (5) pinned software versions in deploy README files and pyproject.toml
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-05
---

# sr-5 - \[Supply Chain Risk Management\] Acquisition Strategies, Tools, and Methods

## Control Statement

Employ the following acquisition strategies, contract tools, and procurement methods to protect against, identify, and mitigate supply chain risks: [strategies, tools, and methods].

## Control Assessment Objective

- \[SR-05[01]\] [strategies, tools, and methods] are employed to protect against supply chain risks;

- \[SR-05[02]\] [strategies, tools, and methods] are employed to identify supply chain risks;

- \[SR-05[03]\] [strategies, tools, and methods] are employed to mitigate supply chain risks.

## Control guidance

The use of the acquisition process provides an important vehicle to protect the supply chain. There are many useful tools and techniques available, including obscuring the end use of a system or system component, using blind or filtered buys, requiring tamper-evident packaging, or using trusted or controlled distribution. The results from a supply chain risk assessment can guide and inform the strategies, tools, and methods that are most applicable to the situation. Tools and techniques may provide protections against unauthorized production, theft, tampering, insertion of counterfeits, insertion of malicious software or backdoors, and poor development practices throughout the system development life cycle. Organizations also consider providing incentives for suppliers who implement controls, promote transparency into their processes and security and privacy practices, provide contract language that addresses the prohibition of tainted or counterfeit components, and restrict purchases from untrustworthy suppliers. Organizations consider providing training, education, and awareness programs for personnel regarding supply chain risk, available mitigation strategies, and when the programs should be employed. Methods for reviewing and protecting development plans, documentation, and evidence are commensurate with the security and privacy requirements of the organization. Contracts may specify documentation protection requirements.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS acquisition strategy employs five layered methods to protect against, identify, and mitigate supply chain risks.

First, the entire software stack is open-source COTS: Wazuh (Apache 2.0), ELK (Elastic License 2.0), DefectDojo (BSD 3-Clause), RegScale CE (proprietary CE license reviewed in ADR 0001), Shuffle (Apache 2.0), TheHive + Cortex (AGPL), Velociraptor (AGPLv3), Caldera (Apache 2.0), OpenCTI (Apache 2.0), and Arkime (Apache 2.0). Open-source preference reduces counterfeit software risk because source code is publicly auditable. Hardware is commodity x86 compute (Lenovo ThinkStation Tiny line) and network appliances (Protectli VP2420, MokerLink 10G08410GSM) -- widely deployed COTS platforms with established supply chains.

Second, software is installed exclusively from official distribution channels: vendor-signed apt repositories (`packages.wazuh.com` for Wazuh, `artifacts.elastic.co` for ELK) with apt GPG key verification at install time, and official Docker Hub images (e.g., `defectdojo/defectdojo-django`, `wazuh/wazuh-manager`). No unofficial builds, pirated software, or unverified images are used.

Third, all hardware was purchased new from primary US vendors -- Lenovo units directly from Lenovo, Protectli VP2420 from protectli.com, MokerLink through Amazon Business -- with no gray-market or third-party refurbisher involvement.

Fourth, Wazuh syscollector provides continuous installed-package inventory on all in-boundary agents. This is the operational SBOM analog, ingestible via `pipelines/ingest/inventory.py` and reflected in `inventory/IIW-2026-04.xlsx`.

Fifth, software versions are pinned: DefectDojo 2.57.0 (`deploy/defectdojo/README.md`), Trestle 4.0.1 (`pyproject.toml`). Remaining gaps are Docker image digest pinning (images pulled by tag, not digest) and a formal SPDX/CycloneDX SBOM. These gaps are acknowledged and accepted at the partial rating.

#### Implementation Status: partial

______________________________________________________________________
