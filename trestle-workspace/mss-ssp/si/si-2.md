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
  si-02_odp:
    alt-identifier: si-2_prm_1
    profile-values:
      - within 30 days for Critical/High CVEs; within 90 days for Moderate CVEs; within 180 days for Low CVEs -- aligned with FedRAMP Low ConMon SLA windows tracked in DefectDojo
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: si-02
---

# si-2 - \[System and Information Integrity\] Flaw Remediation

## Control Statement

- \[a.\] Identify, report, and correct system flaws;

- \[b.\] Test software and firmware updates related to flaw remediation for effectiveness and potential side effects before installation;

- \[c.\] Install security-relevant software and firmware updates within [time period] of the release of the updates; and

- \[d.\] Incorporate flaw remediation into the organizational configuration management process.

## Control Assessment Objective

- \[SI-02a.\]

  - \[SI-02a.[01]\] system flaws are identified;
  - \[SI-02a.[02]\] system flaws are reported;
  - \[SI-02a.[03]\] system flaws are corrected;

- \[SI-02b.\]

  - \[SI-02b.[01]\] software updates related to flaw remediation are tested for effectiveness before installation;
  - \[SI-02b.[02]\] software updates related to flaw remediation are tested for potential side effects before installation;
  - \[SI-02b.[03]\] firmware updates related to flaw remediation are tested for effectiveness before installation;
  - \[SI-02b.[04]\] firmware updates related to flaw remediation are tested for potential side effects before installation;

- \[SI-02c.\]

  - \[SI-02c.[01]\] security-relevant software updates are installed within [time period] of the release of the updates;
  - \[SI-02c.[02]\] security-relevant firmware updates are installed within [time period] of the release of the updates;

- \[SI-02d.\] flaw remediation is incorporated into the organizational configuration management process.

## Control guidance

The need to remediate system flaws applies to all types of software and firmware. Organizations identify systems affected by software flaws, including potential vulnerabilities resulting from those flaws, and report this information to designated organizational personnel with information security and privacy responsibilities. Organizations consider establishing a controlled patching environment for mission-critical systems. Security-relevant updates include patches, service packs, and malicious code signatures. Organizations also address flaws discovered during assessments, continuous monitoring, incident response activities, and system error handling. By incorporating flaw remediation into configuration management processes, required remediation actions can be tracked and verified.

Organization-defined time periods for updating security-relevant software and firmware may vary based on a variety of risk factors, including the security category of the system, the criticality of the update (i.e., severity of the vulnerability related to the discovered flaw), the organizational risk tolerance, the mission supported by the system, or the threat environment. Some types of flaw remediation may require more testing than other types. Organizations determine the type of testing needed for the specific type of flaw remediation activity under consideration and the types of changes that are to be configuration-managed. Flaw remediation testing addresses both effectiveness of addressing security issues and for potential side effects on functionality, system and system component performance and operations. When implementing remediation activities, organizations consider the order and timing of updates to validate correct execution within the system environment, and to support system and component availability needs (i.e., implementing a staggered deployment strategy). In some situations, organizations may determine that the testing of software or firmware updates is not necessary or practical, such as when implementing simple malicious code signature updates. In testing decisions, organizations consider whether security-relevant software or firmware updates are obtained from authorized sources with appropriate digital signatures.

When implementing remediation activities, organizations consider the order and timing of updates to validate correct execution within the system environment, and to support system and component availability needs (i.e., implementing a staggered deployment strategy). Organizations verify that software and firmware updates come from authorized sources prior to downloading.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

System flaws are identified and tracked using the Wazuh vulnerability detection pipeline. The `pipelines/ingest/wazuh_vulns.py` module pages through the `wazuh-states-vulnerabilities-*` OpenSearch index on brisket (10.10.20.30:9200) across all 15 in-boundary agents, producing normalized Finding records. The April 2026 ConMon cycle ingested 8,471 vulnerability findings across 5 agents. DefectDojo 2.57.0 on dojo (10.10.30.27) receives all findings via the ConMon pipeline and tracks each CVE against FedRAMP Low SLA windows: Critical and High CVEs within 30 days, Moderate within 90 days, Low within 180 days. Security-relevant updates are tested for effectiveness and side effects in the lab environment before rollout to production SOC infrastructure -- the 2026-03-31 fleet patch (kernels, Wazuh 4.14.4, Proxmox alignment) was validated on sear before applying across the fleet. Wazuh SCA performs automated configuration-flaw scanning on all enrolled agents, with results surfaced in the Wazuh Dashboard on brisket.

The monthly ConMon pipeline (`./pipelines.sh conmon`) closes the flaw-remediation loop automatically: ingest from Wazuh Indexer, push to DefectDojo, generate the OSCAL POA&M via `pipelines/build/oscal_poam.py`, and render `poam/POAM-2026-04.xlsx`. ADR 0007 documents the live end-to-end validation of this cycle, confirming 8,471 findings ingested with zero skipped. ADR 0006 Deviation 5 records the pivot from the deprecated Wazuh 4.8 REST vulnerability endpoint to indexer-based ingest -- an example of flaw-remediation procedure incorporated into the configuration management process. Flaw remediation activities are incorporated into the git-tracked configuration baseline, with ADRs serving as the approval mechanism for any deviation from the established remediation cadence.

#### Implementation Status: implemented

______________________________________________________________________
