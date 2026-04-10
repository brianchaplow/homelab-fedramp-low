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
  ca-05_odp:
    alt-identifier: ca-5_prm_1
    profile-values:
      - monthly (each ConMon cycle)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-05
---

# ca-5 - \[Assessment, Authorization, and Monitoring\] Plan of Action and Milestones

## Control Statement

- \[a.\] Develop a plan of action and milestones for the system to document the planned remediation actions of the organization to correct weaknesses or deficiencies noted during the assessment of the controls and to reduce or eliminate known vulnerabilities in the system; and

- \[b.\] Update existing plan of action and milestones [frequency] based on the findings from control assessments, independent audits or reviews, and continuous monitoring activities.

## Control Assessment Objective

- \[CA-05a.\] a plan of action and milestones for the system is developed to document the planned remediation actions of the organization to correct weaknesses or deficiencies noted during the assessment of the controls and to reduce or eliminate known vulnerabilities in the system;

- \[CA-05b.\] existing plan of action and milestones are updated [frequency] based on the findings from control assessments, independent audits or reviews, and continuous monitoring activities.

## Control guidance

Plans of action and milestones are useful for any type of organization to track planned remedial actions. Plans of action and milestones are required in authorization packages and subject to federal reporting requirements established by OMB.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The POA&M pipeline is implemented and live-verified as of the April 2026 ConMon cycle. `pipelines/build/oscal_poam.py` is the OSCAL POA&M builder: it reads DefectDojo findings via `DefectDojoClient.list_findings()`, maps each finding to an OSCAL 1.1.2 POA&M item, and assigns a FedRAMP Low SLA-based scheduled completion date. SLA windows are Critical=15 days, High=30 days, Medium/Moderate=90 days, Low=180 days -- values corrected from the original plan text (30/90/180/365) to the actual FedRAMP ConMon Strategy Guide values per ADR 0006 Amendment Task 12.

The April 2026 POA&M output is `poam/POAM-2026-04.xlsx` (4.9 MB, 8,473 rows in FedRAMP Rev 5 POA&M template format using `templates/FedRAMP-POAM-Template-Rev5.xlsx`). Data populates the "Open POA&M Items" sheet starting at row 8. Internal DefectDojo `Medium` severity is mapped to `Moderate` for the FedRAMP template dropdown. `False Positive` findings set the FP column to Yes. The OSCAL source is `oscal/poam.json` (16.8 MB), gitignored and regenerated on each ConMon run.

The full monthly cycle is orchestrated by `./pipelines.sh conmon` (`pipelines/cli.py` `conmon` command): ingest-findings (Wazuh vulnerability scan data) -- push to DefectDojo -- build OSCAL POA&M -- render IIW xlsx -- render POA&M xlsx. DefectDojo SLA enforcement (`http://10.10.30.27:8080`) provides early warning for findings approaching or past SLA across all 5 MSS products, seeded via `deploy/defectdojo/post-install.sh`. The live April 2026 run is documented in ADR 0007 §"Done criteria." Update frequency is monthly, aligned with the FedRAMP ConMon Strategy Guide requirement; `./pipelines.sh conmon` is the update mechanism.

#### Implementation Status: implemented

______________________________________________________________________
