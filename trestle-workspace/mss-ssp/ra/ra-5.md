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
  ra-5_prm_1:
    aggregates:
      - ra-05_odp.01
      - ra-05_odp.02
    profile-param-value-origin: organization
  ra-05_odp.01:
    profile-values:
      - continuously (Wazuh vulnerability detector runs on agent check-in) and monthly (full ConMon pipeline via ./pipelines.sh conmon)
    profile-param-value-origin: organization
  ra-05_odp.02:
    profile-values:
      - Wazuh syscollector collects package inventory on agent check-in; the vulnerability detector cross-references NVD; results are stored in wazuh-states-vulnerabilities-* and ingested monthly via pipelines/ingest/wazuh_vulns.py
    profile-param-value-origin: organization
  ra-05_odp.03:
    alt-identifier: ra-5_prm_2
    profile-values:
      - Critical 15 days; High 30 days; Medium 90 days; Low 180 days -- per FedRAMP Low ConMon SLA windows, enforced in pipelines/build/oscal_poam.py SLA_DAYS dict
    profile-param-value-origin: organization
  ra-05_odp.04:
    alt-identifier: ra-5_prm_3
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ra-05
---

# ra-5 - \[Risk Assessment\] Vulnerability Monitoring and Scanning

## Control Statement

- \[a.\] Monitor and scan for vulnerabilities in the system and hosted applications [organization-defined frequency and/or randomly in accordance with organization-defined process] and when new vulnerabilities potentially affecting the system are identified and reported;

- \[b.\] Employ vulnerability monitoring tools and techniques that facilitate interoperability among tools and automate parts of the vulnerability management process by using standards for:

  - \[1.\] Enumerating platforms, software flaws, and improper configurations;
  - \[2.\] Formatting checklists and test procedures; and
  - \[3.\] Measuring vulnerability impact;

- \[c.\] Analyze vulnerability scan reports and results from vulnerability monitoring;

- \[d.\] Remediate legitimate vulnerabilities [response times] in accordance with an organizational assessment of risk;

- \[e.\] Share information obtained from the vulnerability monitoring process and control assessments with [personnel or roles] to help eliminate similar vulnerabilities in other systems; and

- \[f.\] Employ vulnerability monitoring tools that include the capability to readily update the vulnerabilities to be scanned.

## Control Assessment Objective

- \[RA-05a.\]

  - \[RA-05a.[01]\] systems and hosted applications are monitored for vulnerabilities [frequency and/or randomly in accordance with organization-defined process] and when new vulnerabilities potentially affecting the system are identified and reported;
  - \[RA-05a.[02]\] systems and hosted applications are scanned for vulnerabilities [frequency and/or randomly in accordance with organization-defined process] and when new vulnerabilities potentially affecting the system are identified and reported;

- \[RA-05b.\] vulnerability monitoring tools and techniques are employed to facilitate interoperability among tools;

  - \[RA-05b.01\] vulnerability monitoring tools and techniques are employed to automate parts of the vulnerability management process by using standards for enumerating platforms, software flaws, and improper configurations;
  - \[RA-05b.02\] vulnerability monitoring tools and techniques are employed to facilitate interoperability among tools and to automate parts of the vulnerability management process by using standards for formatting checklists and test procedures;
  - \[RA-05b.03\] vulnerability monitoring tools and techniques are employed to facilitate interoperability among tools and to automate parts of the vulnerability management process by using standards for measuring vulnerability impact;

- \[RA-05c.\] vulnerability scan reports and results from vulnerability monitoring are analyzed;

- \[RA-05d.\] legitimate vulnerabilities are remediated [response times] in accordance with an organizational assessment of risk;

- \[RA-05e.\] information obtained from the vulnerability monitoring process and control assessments is shared with [personnel or roles] to help eliminate similar vulnerabilities in other systems;

- \[RA-05f.\] vulnerability monitoring tools that include the capability to readily update the vulnerabilities to be scanned are employed.

## Control guidance

Security categorization of information and systems guides the frequency and comprehensiveness of vulnerability monitoring (including scans). Organizations determine the required vulnerability monitoring for system components, ensuring that the potential sources of vulnerabilities—such as infrastructure components (e.g., switches, routers, guards, sensors), networked printers, scanners, and copiers—are not overlooked. The capability to readily update vulnerability monitoring tools as new vulnerabilities are discovered and announced and as new scanning methods are developed helps to ensure that new vulnerabilities are not missed by employed vulnerability monitoring tools. The vulnerability monitoring tool update process helps to ensure that potential vulnerabilities in the system are identified and addressed as quickly as possible. Vulnerability monitoring and analyses for custom software may require additional approaches, such as static analysis, dynamic analysis, binary analysis, or a hybrid of the three approaches. Organizations can use these analysis approaches in source code reviews and in a variety of tools, including web-based application scanners, static analysis tools, and binary analyzers.

Vulnerability monitoring includes scanning for patch levels; scanning for functions, ports, protocols, and services that should not be accessible to users or devices; and scanning for flow control mechanisms that are improperly configured or operating incorrectly. Vulnerability monitoring may also include continuous vulnerability monitoring tools that use instrumentation to continuously analyze components. Instrumentation-based tools may improve accuracy and may be run throughout an organization without scanning. Vulnerability monitoring tools that facilitate interoperability include tools that are Security Content Automated Protocol (SCAP)-validated. Thus, organizations consider using scanning tools that express vulnerabilities in the Common Vulnerabilities and Exposures (CVE) naming convention and that employ the Open Vulnerability Assessment Language (OVAL) to determine the presence of vulnerabilities. Sources for vulnerability information include the Common Weakness Enumeration (CWE) listing and the National Vulnerability Database (NVD). Control assessments, such as red team exercises, provide additional sources of potential vulnerabilities for which to scan. Organizations also consider using scanning tools that express vulnerability impact by the Common Vulnerability Scoring System (CVSS).

Vulnerability monitoring includes a channel and process for receiving reports of security vulnerabilities from the public at-large. Vulnerability disclosure programs can be as simple as publishing a monitored email address or web form that can receive reports, including notification authorizing good-faith research and disclosure of security vulnerabilities. Organizations generally expect that such research is happening with or without their authorization and can use public vulnerability disclosure channels to increase the likelihood that discovered vulnerabilities are reported directly to the organization for remediation.

Organizations may also employ the use of financial incentives (also known as "bug bounties" ) to further encourage external security researchers to report discovered vulnerabilities. Bug bounty programs can be tailored to the organization’s needs. Bounties can be operated indefinitely or over a defined period of time and can be offered to the general public or to a curated group. Organizations may run public and private bounties simultaneously and could choose to offer partially credentialed access to certain participants in order to evaluate security vulnerabilities from privileged vantage points.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Wazuh 4.14.4 on brisket provides continuous vulnerability monitoring for all 5 in-boundary agents via its built-in vulnerability detector module. The detector's syscollector component collects installed package inventories on each agent check-in and cross-references them against the National Vulnerability Database (NVD) and vendor-specific advisories, storing results in the `wazuh-states-vulnerabilities-*` index on the Wazuh OpenSearch indexer (brisket:9200). A live probe on 2026-04-09 confirmed 12,949 documents across 5 agents: brisket 2,804, haccp 1,899, regscale 1,861, dojo 1,861, smokehouse 46. Each document carries CVE identifier, CVSS base score (v2/v3/v4), Wazuh severity label (Critical/High/Medium/Low), detected_at timestamp, affected package name and version, and NVD reference URLs. This satisfies RA-5b's interoperability requirements: platforms and software flaws are enumerated via CVE, vulnerability impact is measured via CVSS, and the NVD feed provides standards-based checklist alignment. Zeek on haccp span0 and Suricata on smokehouse eth4 provide complementary network-level scanning -- detecting active exploitation attempts, lateral movement, and misconfigured services that host-based scanners miss. OpenCTI v7 on brisket syncs threat indicators from 6 connectors to Wazuh CDB lists every 6 hours (cron `0 */6 * * *`), implementing RA-5f by continuously extending the IOC-based detection surface without operator action.

The vulnerability pipeline (`pipelines/ingest/wazuh_vulns.py`) normalizes every indexer hit into a Finding schema (`pipelines/common/schemas.py`: cve, cvss_score, severity, affected_host, affected_package, related_controls) and pushes 8,471 findings to DefectDojo 2.57.0 on dojo via `pipelines/push/defectdojo.py`. DefectDojo tracks remediation state per finding (Open, In Progress, Completed, False Positive, Deviated) and enforces FedRAMP Low SLA windows via `pipelines/build/oscal_poam.py`: Critical 15 days, High 30 days, Medium 90 days, Low 180 days (corrected from wrong baseline values per ADR 0006 Amendment Task 12). The OSCAL POA&M (`poam/POAM-2026-04.xlsx`, 8,473 rows) is the vulnerability scan report artifact satisfying RA-5c (analysis of scan results) and RA-5d (remediation with response times). Vulnerability information is shared with Brian Chaplow as sole operator via the monthly ConMon pipeline run and Discord briefing (WF10, cron 0530 EST).

#### Implementation Status: implemented

______________________________________________________________________
