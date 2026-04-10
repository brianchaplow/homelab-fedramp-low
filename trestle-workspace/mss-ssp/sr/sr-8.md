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
  sr-08_odp.01:
    alt-identifier: sr-8_prm_1
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  sr-08_odp.02:
    alt-identifier: sr-8_prm_2
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sr-08
---

# sr-8 - \[Supply Chain Risk Management\] Notification Agreements

## Control Statement

Establish agreements and procedures with entities involved in the supply chain for the system, system component, or system service for the [Selection (one or more): notification of supply chain compromises; [results of assessments or audits]].

## Control Assessment Objective

agreements and procedures are established with entities involved in the supply chain for the system, system components, or system service for [Selection (one or more): notification of supply chain compromises; [results of assessments or audits]].

## Control guidance

The establishment of agreements and procedures facilitates communications among supply chain entities. Early notification of compromises and potential compromises in the supply chain that can potentially adversely affect or have adversely affected organizational systems or system components is essential for organizations to effectively respond to such incidents. The results of assessments or audits may include open-source information that contributed to a decision or result and could be used to help the supply chain entity resolve a concern or improve its processes.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. MSS is a single-operator homelab with no external supply chain partners with whom formal bilateral notification agreements can be established. The system's hardware vendors (Lenovo, Protectli, MokerLink) and software vendors (Wazuh, Elastic, et al.) are commercial entities that do not enter into individualized notification agreements with end-user homelab operators.

Supply chain compromise notifications from these vendors are received through public channels: vendor security advisories, CVE feeds monitored via Wazuh's `wazuh-states-vulnerabilities-*` index (ingestible via `pipelines/ingest/wazuh_vulns.py`), and public mailing lists. The April 2026 POA&M (`poam/POAM-2026-04.xlsx`, 8,473 findings across 5 agents) is the evidence that supply chain vulnerability data is being actively consumed and tracked. This public-channel monitoring is the operational substitute for bilateral notification agreements, but it does not constitute a formal agreement in the control's sense.

#### Implementation Status: not-applicable

______________________________________________________________________
