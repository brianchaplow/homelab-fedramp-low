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
  sort-id: ra-07
---

# ra-7 - \[Risk Assessment\] Risk Response

## Control Statement

Respond to findings from security and privacy assessments, monitoring, and audits in accordance with organizational risk tolerance.

## Control Assessment Objective

- \[RA-07[01]\] findings from security assessments are responded to in accordance with organizational risk tolerance;

- \[RA-07[02]\] findings from privacy assessments are responded to in accordance with organizational risk tolerance;

- \[RA-07[03]\] findings from monitoring are responded to in accordance with organizational risk tolerance;

- \[RA-07[04]\] findings from audits are responded to in accordance with organizational risk tolerance.

## Control guidance

Organizations have many options for responding to risk including mitigating risk by implementing new controls or strengthening existing controls, accepting risk with appropriate justification or rationale, sharing or transferring risk, or avoiding risk. The risk tolerance of the organization influences risk response decisions and actions. Risk response addresses the need to determine an appropriate response to risk before generating a plan of action and milestones entry. For example, the response may be to accept risk or reject risk, or it may be possible to mitigate the risk immediately so that a plan of action and milestones entry is not needed. However, if the risk response is to mitigate the risk, and the mitigation cannot be completed immediately, a plan of action and milestones entry is generated.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Risk findings are responded to through a structured pipeline that closes the loop between identification and documented response. Wazuh 4.14.4 identifies vulnerabilities and stores them in `wazuh-states-vulnerabilities-*`; `pipelines/ingest/wazuh_vulns.py` normalizes them into Finding records with FedRAMP SLA due-dates; DefectDojo 2.57.0 on dojo tracks remediation state (Open, In Progress, Completed, False Positive, Deviated) per finding; `pipelines/build/oscal_poam.py` builds the OSCAL POA&M with SLA-driven scheduled-completion dates using the `_finding_state()` state mapping (priority: false-positive > risk-accepted > mitigated > active > closed). Each DefectDojo state change constitutes a documented risk response decision in accordance with organizational risk tolerance. The OSCAL POA&M (`poam/POAM-2026-04.xlsx`, 8,473 rows) is the formal risk response record, and the monthly `./pipelines.sh conmon` run is the recurring mechanism that processes new findings and updates existing response records.

ADR 0005 is the archetypal RA-7 example: a PBS backup gap (2026-04-03 to 2026-04-07) was identified via monitoring during Plan 1 Task 12, assessed as limited-impact (5-day gap, no data loss, acceptable for the ConMon cycle), remediated (NFS automount hardening with `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30`), and a follow-up TODO was captured in Plan 1 Task 20 (PBS Wazuh/Discord alert). ADR 0006 Amendment Task 12 is a second example: SLA window values in `oscal_poam.py` were wrong (30/90/180/365 days), the risk was assessed as incorrect due-dates propagating to the POA&M, and the response was immediate correction to FedRAMP-correct values (Critical 15d, High 30d, Medium 90d, Low 180d). Both examples demonstrate the full RA-7 cycle: finding -- assessment -- response -- documentation.

#### Implementation Status: implemented

______________________________________________________________________
