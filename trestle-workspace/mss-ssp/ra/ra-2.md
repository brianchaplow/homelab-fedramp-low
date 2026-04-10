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
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ra-02
---

# ra-2 - \[Risk Assessment\] Security Categorization

## Control Statement

- \[a.\] Categorize the system and information it processes, stores, and transmits;

- \[b.\] Document the security categorization results, including supporting rationale, in the security plan for the system; and

- \[c.\] Verify that the authorizing official or authorizing official designated representative reviews and approves the security categorization decision.

## Control Assessment Objective

- \[RA-02a.\] the system and the information it processes, stores, and transmits are categorized;

- \[RA-02b.\] the security categorization results, including supporting rationale, are documented in the security plan for the system;

- \[RA-02c.\] the authorizing official or authorizing official designated representative reviews and approves the security categorization decision.

## Control guidance

Security categories describe the potential adverse impacts or negative consequences to organizational operations, organizational assets, and individuals if organizational information and systems are compromised through a loss of confidentiality, integrity, or availability. Security categorization is also a type of asset loss characterization in systems security engineering processes that is carried out throughout the system development life cycle. Organizations can use privacy risk assessments or privacy impact assessments to better understand the potential adverse effects on individuals. [CNSSI 1253](#4e4fbc93-333d-45e6-a875-de36b878b6b9) provides additional guidance on categorization for national security systems.

Organizations conduct the security categorization process as an organization-wide activity with the direct involvement of chief information officers, senior agency information security officers, senior agency officials for privacy, system owners, mission and business owners, and information owners or stewards. Organizations consider the potential adverse impacts to other organizations and, in accordance with [USA PATRIOT](#13f0c39d-eaf7-417a-baef-69a041878bb5) and Homeland Security Presidential Directives, potential national-level adverse impacts.

Security categorization processes facilitate the development of inventories of information assets and, along with [CM-8](#cm-8) , mappings to specific system components where information is processed, stored, or transmitted. The security categorization process is revisited throughout the system development life cycle to ensure that the security categories remain accurate and relevant.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service is categorized as FIPS 199 Low across all three security objectives -- Confidentiality Low, Integrity Low, and Availability Low. This categorization is consistent with the system's purpose: a portfolio-demonstration ConMon environment with no PII, no production customer data, and no life-safety functions. The FedRAMP Low baseline was explicitly selected at project inception and documented in ADR 0001 (`docs/adr/0001-preflight-and-eula.md`). The FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) operationalizes the categorization by selecting exactly 156 controls appropriate for Low-impact systems, and the OSCAL SSP (`oscal/ssp.json`) carries the system identifier `managed-soc-service` throughout. The security categorization decision has been reviewed and approved by Brian Chaplow as the authorizing official and sole operator.

The IIW (`inventory/IIW-2026-04.xlsx`) records 7 in-boundary components -- brisket, haccp, smokehouse, dojo VM, regscale VM, pitcrew, and smoker -- all classified as Low-impact assets. Supporting rationale for the Low categorization: the system processes no classified or sensitive data, hosts no public-facing services on in-boundary hosts, and is not in the operational path of any mission-critical function. Loss of confidentiality, integrity, or availability of the MSS homelab would result in limited adverse effect on operator operations and no effect on any external party. The categorization is reviewed at each annual ConMon cycle and whenever a new phase adds in-boundary infrastructure.

#### Implementation Status: implemented

______________________________________________________________________
