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
  au-05_odp.01:
    alt-identifier: au-5_prm_1
    profile-values:
      - Brian Chaplow (system owner, sole operator) via Discord #infrastructure-alerts
    profile-param-value-origin: organization
  au-05_odp.02:
    alt-identifier: au-5_prm_2
    profile-values:
      - within 15 minutes (Grafana alert evaluation window plus Discord delivery)
    profile-param-value-origin: organization
  au-05_odp.03:
    alt-identifier: au-5_prm_3
    profile-values:
      - overwrite oldest record
    profile-param-value-origin: inherited
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: au-05
---

# au-5 - \[Audit and Accountability\] Response to Audit Logging Process Failures

## Control Statement

- \[a.\] Alert [personnel or roles] within [time period] in the event of an audit logging process failure; and

- \[b.\] Take the following additional actions: [additional actions].

## Control Assessment Objective

- \[AU-05a.\] [personnel or roles] are alerted in the event of an audit logging process failure within [time period];

- \[AU-05b.\] [additional actions] are taken in the event of an audit logging process failure.

## Control guidance

Audit logging process failures include software and hardware errors, failures in audit log capturing mechanisms, and reaching or exceeding audit log storage capacity. Organization-defined actions include overwriting oldest audit records, shutting down the system, and stopping the generation of audit records. Organizations may choose to define additional actions for audit logging process failures based on the type of failure, the location of the failure, the severity of the failure, or a combination of such factors. When the audit logging process failure is related to storage, the response is carried out for the audit log storage repository (i.e., the distinct system component where the audit logs are stored), the system on which the audit logs reside, the total audit log storage capacity of the organization (i.e., all audit log storage repositories combined), or all three. Organizations may decide to take no additional actions after alerting designated roles or personnel.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Grafana Unified Alerting on brisket provides the primary failure-notification mechanism for audit log storage exhaustion. Four alert rules defined in `build-grafana-alerts.py` route to Discord `#infrastructure-alerts` via the `$discord_webhook_infra` Shuffle variable: "Disk Critical -- Usage Above 90%" fires when any monitored host's primary volume exceeds 90% utilization; "Service Down" fires when a Blackbox HTTP probe detects a monitored service unreachable; "Host Unreachable" fires when an ICMP probe fails; and "GPU Thermal Critical -- Brisket Above 90C" (uid=dfihoiidr7k00c) fires when GPU temperature threatens the Logstash/Ollama enrichment pipeline. All four alert evaluation windows are 2-5 minutes, delivering Discord notification to the operator within 15 minutes of detection. When disk capacity approaches saturation, the FedRAMP-mandated additional action is overwrite-oldest-record -- for Arkime PCAP this is enforced automatically by the `freeSpaceG=100` config parameter; for OpenSearch indices no automated overwrite is configured (gap: operator must manually manage index deletion or implement ILM).

The gap with respect to AU-5 is that Wazuh indexer health, Filebeat pipeline status, and Logstash pipeline errors are not currently subjects of dedicated alerting. This gap became visible during homelab-fedramp-low ADR 0005, which documents that a 5-day PBS backup failure went undetected because no targeted alert existed for that subsystem -- the same failure mode applies to audit pipelines. Plan 1 Task 20 captured a ConMon follow-up to wire a Wazuh/Discord alert on PBS backup status; an equivalent alert for Logstash pipeline errors and OpenSearch indexer availability is in the ConMon roadmap. Until that gap is closed, this control is assessed as partial.

#### Implementation Status: partial

______________________________________________________________________
