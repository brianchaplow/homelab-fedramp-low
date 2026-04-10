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
  ca-02_odp.01:
    alt-identifier: ca-2_prm_1
    profile-values:
      - annually (aligned with FedRAMP ConMon annual assessment)
    profile-param-value-origin: organization
  ca-02_odp.02:
    alt-identifier: ca-2_prm_2
    profile-values:
      - system owner (Brian Chaplow)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-02
---

# ca-2 - \[Assessment, Authorization, and Monitoring\] Control Assessments

## Control Statement

- \[a.\] Select the appropriate assessor or assessment team for the type of assessment to be conducted;

- \[b.\] Develop a control assessment plan that describes the scope of the assessment including:

  - \[1.\] Controls and control enhancements under assessment;
  - \[2.\] Assessment procedures to be used to determine control effectiveness; and
  - \[3.\] Assessment environment, assessment team, and assessment roles and responsibilities;

- \[c.\] Ensure the control assessment plan is reviewed and approved by the authorizing official or designated representative prior to conducting the assessment;

- \[d.\] Assess the controls in the system and its environment of operation [assessment frequency] to determine the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting established security and privacy requirements;

- \[e.\] Produce a control assessment report that document the results of the assessment; and

- \[f.\] Provide the results of the control assessment to [individuals or roles].

## Control Assessment Objective

- \[CA-02a.\] an appropriate assessor or assessment team is selected for the type of assessment to be conducted;

- \[CA-02b.\]

  - \[CA-02b.01\] a control assessment plan is developed that describes the scope of the assessment, including controls and control enhancements under assessment;
  - \[CA-02b.02\] a control assessment plan is developed that describes the scope of the assessment, including assessment procedures to be used to determine control effectiveness;
  - \[CA-02b.03\]

    - \[CA-02b.03[01]\] a control assessment plan is developed that describes the scope of the assessment, including the assessment environment;
    - \[CA-02b.03[02]\] a control assessment plan is developed that describes the scope of the assessment, including the assessment team;
    - \[CA-02b.03[03]\] a control assessment plan is developed that describes the scope of the assessment, including assessment roles and responsibilities;

- \[CA-02c.\] the control assessment plan is reviewed and approved by the authorizing official or designated representative prior to conducting the assessment;

- \[CA-02d.\]

  - \[CA-02d.[01]\] controls are assessed in the system and its environment of operation [assessment frequency] to determine the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting established security requirements;
  - \[CA-02d.[02]\] controls are assessed in the system and its environment of operation [assessment frequency] to determine the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting established privacy requirements;

- \[CA-02e.\] a control assessment report is produced that documents the results of the assessment;

- \[CA-02f.\] the results of the control assessment are provided to [individuals or roles].

## Control guidance

Organizations ensure that control assessors possess the required skills and technical expertise to develop effective assessment plans and to conduct assessments of system-specific, hybrid, common, and program management controls, as appropriate. The required skills include general knowledge of risk management concepts and approaches as well as comprehensive knowledge of and experience with the hardware, software, and firmware system components implemented.

Organizations assess controls in systems and the environments in which those systems operate as part of initial and ongoing authorizations, continuous monitoring, FISMA annual assessments, system design and development, systems security engineering, privacy engineering, and the system development life cycle. Assessments help to ensure that organizations meet information security and privacy requirements, identify weaknesses and deficiencies in the system design and development process, provide essential information needed to make risk-based decisions as part of authorization processes, and comply with vulnerability mitigation procedures. Organizations conduct assessments on the implemented controls as documented in security and privacy plans. Assessments can also be conducted throughout the system development life cycle as part of systems engineering and systems security engineering processes. The design for controls can be assessed as RFPs are developed, responses assessed, and design reviews conducted. If a design to implement controls and subsequent implementation in accordance with the design are assessed during development, the final control testing can be a simple confirmation utilizing previously completed control assessment and aggregating the outcomes.

Organizations may develop a single, consolidated security and privacy assessment plan for the system or maintain separate plans. A consolidated assessment plan clearly delineates the roles and responsibilities for control assessment. If multiple organizations participate in assessing a system, a coordinated approach can reduce redundancies and associated costs.

Organizations can use other types of assessment activities, such as vulnerability scanning and system monitoring, to maintain the security and privacy posture of systems during the system life cycle. Assessment reports document assessment results in sufficient detail, as deemed necessary by organizations, to determine the accuracy and completeness of the reports and whether the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting requirements. Assessment results are provided to the individuals or roles appropriate for the types of assessments being conducted. For example, assessments conducted in support of authorization decisions are provided to authorizing officials, senior agency officials for privacy, senior agency information security officers, and authorizing official designated representatives.

To satisfy annual assessment requirements, organizations can use assessment results from the following sources: initial or ongoing system authorizations, continuous monitoring, systems engineering processes, or system development life cycle activities. Organizations ensure that assessment results are current, relevant to the determination of control effectiveness, and obtained with the appropriate level of assessor independence. Existing control assessment results can be reused to the extent that the results are still valid and can also be supplemented with additional assessments as needed. After the initial authorizations, organizations assess controls during continuous monitoring. Organizations also establish the frequency for ongoing assessments in accordance with organizational continuous monitoring strategies. External audits, including audits by external entities such as regulatory agencies, are outside of the scope of [CA-2](#ca-2).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The assessor for this homelab system is Brian Chaplow (system owner and sole operator). The assessment plan is embedded in the SSP and `runbooks/monthly-conmon.md`: scope is the FedRAMP Rev 5 Low baseline applied to 7 in-boundary components (brisket, haccp, smokehouse, dojo, regscale, OPNsense, MokerLink); assessment procedures are the `./pipelines.sh conmon` pipeline subcommands; assessment environment is the Wazuh SIEM (brisket, 10.10.20.30) and DefectDojo (dojo, 10.10.30.27:8080).

The primary assessment mechanism is automated: `pipelines/ingest/wazuh_vulns.py` ingests all open vulnerability findings from the `wazuh-states-vulnerabilities-*` index via the Wazuh Indexer (OpenSearch at `https://10.10.20.30:9200`), using `search_after` pagination to capture the full finding set. The live April 2026 run produced 8,471 findings across 5 in-boundary agents (brisket 2,804; haccp 1,899; regscale 1,861; dojo 1,861; smokehouse 46) per ADR 0007 Task 10.

The assessment report is `poam/POAM-2026-04.xlsx` (4.9 MB, 8,473 rows in FedRAMP Rev 5 POA&M template format), produced by `pipelines/render/poam.py` and rendered from `oscal/poam.json` (16.8 MB OSCAL 1.1.2 POA&M). DefectDojo (`http://10.10.30.27:8080`) hosts findings across 5 products -- MSS Core (brisket), MSS Log Analytics (haccp), MSS Network Sensors (smokehouse), MSS GRC Tooling (dojo + regscale) -- with engagement "ConMon 2026-04" serving as the assessment scope record. The assessment report and DefectDojo findings are provided to the system owner (Brian Chaplow). Assessment frequency is annual for full SSP review; monthly for vulnerability scan ingestion via `./pipelines.sh conmon`.

CA-2 is partially implemented: the assessment artifact (POA&M) and pipeline are operational and live-verified per ADR 0007. A formal written assessment plan as a standalone document distinct from the SSP has not been produced; the SSP and `runbooks/monthly-conmon.md` together serve this function for the homelab scope.

#### Implementation Status: partial

______________________________________________________________________
