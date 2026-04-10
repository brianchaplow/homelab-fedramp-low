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
  au-06_odp.01:
    alt-identifier: au-6_prm_1
    profile-values:
      - at least weekly
    profile-param-value-origin: inherited
  au-06_odp.02:
    alt-identifier: au-6_prm_2
    profile-values:
      - MITRE ATT&CK technique detections, rule.level >= 8 alerts, novel entity detections (tier2_novel), threat-intel matches (tier1_ti_match), authentication failures exceeding 5 attempts, and scan/reconnaissance signatures from Suricata
    profile-param-value-origin: organization
  au-06_odp.03:
    alt-identifier: au-6_prm_3
    profile-values:
      - Brian Chaplow (system owner, sole operator) via Discord #soc-alerts and #morning-briefing
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: au-06
---

# au-6 - \[Audit and Accountability\] Audit Record Review, Analysis, and Reporting

## Control Statement

- \[a.\] Review and analyze system audit records [frequency] for indications of [inappropriate or unusual activity] and the potential impact of the inappropriate or unusual activity;

- \[b.\] Report findings to [personnel or roles] ; and

- \[c.\] Adjust the level of audit record review, analysis, and reporting within the system when there is a change in risk based on law enforcement information, intelligence information, or other credible sources of information.

## Control Assessment Objective

- \[AU-06a.\] system audit records are reviewed and analyzed [frequency] for indications of [inappropriate or unusual activity] and the potential impact of the inappropriate or unusual activity;

- \[AU-06b.\] findings are reported to [personnel or roles];

- \[AU-06c.\] the level of audit record review, analysis, and reporting within the system is adjusted when there is a change in risk based on law enforcement information, intelligence information, or other credible sources of information.

## Control guidance

Audit record review, analysis, and reporting covers information security- and privacy-related logging performed by organizations, including logging that results from the monitoring of account usage, remote access, wireless connectivity, mobile device connection, configuration settings, system component inventory, use of maintenance tools and non-local maintenance, physical access, temperature and humidity, equipment delivery and removal, communications at system interfaces, and use of mobile code or Voice over Internet Protocol (VoIP). Findings can be reported to organizational entities that include the incident response team, help desk, and security or privacy offices. If organizations are prohibited from reviewing and analyzing audit records or unable to conduct such activities, the review or analysis may be carried out by other organizations granted such authority. The frequency, scope, and/or depth of the audit record review, analysis, and reporting may be adjusted to meet organizational needs based on new information received.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Audit record review and analysis is automated at twice-daily frequency via Shuffle WF2 (watch digest, cron 0600/1800 EST), which queries `wazuh-alerts-4.x-*` on OpenSearch for the preceding 12-hour window, correlates results against MITRE ATT&CK technique identifiers, requests an Ollama (qwen3:8b) threat assessment, and delivers the structured summary to Discord `#soc-alerts` via `$discord_webhook`. The FedRAMP baseline requires review "at least weekly" -- actual practice is twice-daily, exceeding that floor by more than 14x. Additionally, Shuffle WF10 (nightly briefing, cron 0530 EST) queries both `wazuh-alerts-*` and `logs-zeek.haccp-default-*` to produce an Ollama-generated comprehensive threat briefing delivered to Discord `#morning-briefing`. On-demand review is available at any time through Wazuh Dashboard (brisket:5601) and Kibana (haccp:5601). The `generate-attack-layer.py` script queries both stacks to produce a MITRE ATT&CK Navigator JSON layer for cross-stack technique coverage reporting, satisfying the AU-6 reporting requirement at the technique level.

ADR 0005 documents the most concrete real-world AU-6 example in this system's history: during homelab-fedramp-low Plan 1 Task 12, manual audit log review discovered that PBS LXC 300 had lost its NFS mount to smokehouse during the 2026-04-07 rack consolidation -- a backup gap from 2026-04-03 through 2026-04-07 that no automated alert had surfaced. The detection occurred through log analysis (reviewing Proxmox backup job output manually), triggering the fix documented in ADR 0005 and the ConMon follow-up for a dedicated PBS backup status alert. This example demonstrates that the AU-6 review process is operational and capable of detecting security-relevant failures that evade other detection paths. In this single-operator system, the provider and consumer coordination requirement resolves to the operator reviewing and acting on all findings.

#### Implementation Status: implemented

______________________________________________________________________
