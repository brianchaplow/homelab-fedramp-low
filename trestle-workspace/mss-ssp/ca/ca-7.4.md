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
  sort-id: ca-07.04
---

# ca-7.4 - \[Assessment, Authorization, and Monitoring\] Risk Monitoring

## Control Statement

Ensure risk monitoring is an integral part of the continuous monitoring strategy that includes the following:

- \[(a)\] Effectiveness monitoring;

- \[(b)\] Compliance monitoring; and

- \[(c)\] Change monitoring.

## Control Assessment Objective

risk monitoring is an integral part of the continuous monitoring strategy;

- \[CA-07(04)(a)\] effectiveness monitoring is included in risk monitoring;

- \[CA-07(04)(b)\] compliance monitoring is included in risk monitoring;

- \[CA-07(04)(c)\] change monitoring is included in risk monitoring.

## Control guidance

Risk monitoring is informed by the established organizational risk tolerance. Effectiveness monitoring determines the ongoing effectiveness of the implemented risk response measures. Compliance monitoring verifies that required risk response measures are implemented. It also verifies that security and privacy requirements are satisfied. Change monitoring identifies changes to organizational systems and environments of operation that may affect security and privacy risk.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Risk monitoring is integral to the ConMon strategy implemented in CA-7, operating across all three required dimensions.

**Effectiveness monitoring.** Wazuh (brisket, 15 agents) provides continuous real-time telemetry; agent connectivity gaps surface in the Wazuh Dashboard (brisket:5601) within minutes of failure. `./pipelines.sh conmon` re-ingests all open findings each cycle and recomputes SLA due dates in `pipelines/build/oscal_poam.py` -- findings that have passed their SLA window are automatically flagged in `poam/POAM-2026-04.xlsx` as overdue, providing a direct measure of remediation effectiveness. The test suite (136 tests in `tests/`) provides automated assertion of pipeline effectiveness on every invocation; a regression in any pipeline module causes test failure before the POA&M is published. Grafana (brisket:3000) monitors GPU thermal headroom, agent health, and service-level indicators, with the "GPU Thermal Critical -- Brisket Above 90C" alert (uid=dfihoiidr7k00c) as a live example of infrastructure effectiveness monitoring producing a response action (power cap applied 2026-04-08, GPU temperature reduced from 87C to 63C).

**Compliance monitoring.** DefectDojo SLA enforcement (10.10.30.27:8080) applies FedRAMP Low ConMon SLA windows (Critical=15, High=30, Medium=90, Low=180 days per `pipelines/build/oscal_poam.py` `SLA_DAYS`) to all findings across 5 MSS products, seeded via `deploy/defectdojo/post-install.sh`. The FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`, 156 `<with-id>` references) defines the compliance boundary; each `./pipelines.sh ssp-assemble` run validates that all authored control prose maps to a defined FedRAMP Low control. OSCAL 1.1.2 schema validation (`trestle validate`) runs against all 5 OSCAL artifacts (catalog, profile, component-definition, SSP, POA&M) per ADR 0007, providing automated compliance verification of the artifact set.

**Change monitoring.** The ADR series (`docs/adr/0001` through `docs/adr/0008`) records every significant system change: infrastructure deployment (Plan 1, ADR 0002), OSCAL pipeline build (Plan 2, ADR 0007), NFS boot-race fix (ADR 0005), SLA correction (ADR 0006), and Plan 3 pre-execution realignment (ADR 0008). Wazuh syscollector captures installed package sets and hardware configuration for all 15 agents in `wazuh-states-*` indices; changes in OS version or packages surface on next agent check-in. The `wazuh-states-vulnerabilities-*` index tracks per-CVE state per agent -- new CVEs appearing since the last ingest run represent change events. Git commit log in `github.com/brianchaplow/homelab-fedramp-low` tracks every pipeline code change. PBS daily backups (smoker LXC 300 to smokehouse NFS) provide change indicator for VM availability; the ADR 0005 boot-race event is a documented example of change monitoring detecting a backup gap and driving a compensating control change.

#### Implementation Status: implemented

______________________________________________________________________
