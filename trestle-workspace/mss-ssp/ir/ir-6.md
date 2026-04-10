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
  ir-06_odp.01:
    alt-identifier: ir-6_prm_1
    profile-values:
      - 1 hour
    profile-param-value-origin: organization
  ir-06_odp.02:
    alt-identifier: ir-6_prm_2
    profile-values:
      - system owner (Brian Chaplow); US-CERT/CISA for production-scope incidents
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ir-06
---

# ir-6 - \[Incident Response\] Incident Reporting

## Control Statement

- \[a.\] Require personnel to report suspected incidents to the organizational incident response capability within [time period] ; and

- \[b.\] Report incident information to [authorities].

## Control Assessment Objective

- \[IR-06a.\] personnel is/are required to report suspected incidents to the organizational incident response capability within [time period];

- \[IR-06b.\] incident information is reported to [authorities].

## Control guidance

The types of incidents reported, the content and timeliness of the reports, and the designated reporting authorities reflect applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Incident information can inform risk assessments, control effectiveness assessments, security requirements for acquisitions, and selection criteria for technology products.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service is a single-operator system; the system owner (Brian Chaplow) is simultaneously the personnel required to report suspected incidents and the organizational IR capability receiving the report. Reporting is operationalized through automated notification: Wazuh forwards alerts to Shuffle WF1 v2 via webhook within seconds of detection; WF1 posts an enriched summary to Discord #soc-alerts via `$discord_webhook` and creates a TheHive case within minutes -- satisfying the "report to organizational IR capability within 1 hour" requirement for this system. Infrastructure-layer incidents (e.g., GPU thermal events on brisket, service availability failures) route to Discord #infrastructure-alerts via the Grafana alerting integration using `$discord_webhook_infra`. Nightly briefing WF10 (cron 0530 via `$discord_webhook_briefing`) posts a daily review to #morning-briefing, ensuring the operator is notified even when no real-time alert fires. ADR 0005 (PBS backup gap, 2026-04-08) demonstrates the reporting mechanism for incidents discovered outside the automated alerting path: the operator detected the 5-day backup gap during manual verification (Plan 1 Task 12), self-reported via the ADR record, and notified the IR capability by opening a TheHive case and committing the ADR to the repository within 1 hour of discovery. External reporting to US-CERT/CISA is not operationally applicable at the homelab portfolio scope; this system is not a federal information system subject to FISMA mandatory reporting. If elevated to production FedRAMP scope, significant incident reporting to US-CERT within 1 hour of discovery would be required per FedRAMP ConMon guidance.

#### Implementation Status: implemented

______________________________________________________________________
