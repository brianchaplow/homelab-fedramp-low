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
  sort-id: ir-05
---

# ir-5 - \[Incident Response\] Incident Monitoring

## Control Statement

Track and document incidents.

## Control Assessment Objective

- \[IR-05[01]\] incidents are tracked;

- \[IR-05[02]\] incidents are documented.

## Control guidance

Documenting incidents includes maintaining records about each incident, the status of the incident, and other pertinent information necessary for forensics as well as evaluating incident details, trends, and handling. Incident information can be obtained from a variety of sources, including network monitoring, incident reports, incident response teams, user complaints, supply chain partners, audit monitoring, physical access monitoring, and user and administrator reports. [IR-4](#ir-4) provides information on the types of incidents that are appropriate for monitoring.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service tracks and documents incidents through two complementary mechanisms. Automated tracking via TheHive 4 (pitcrew LXC 200, 10.10.30.22:9000): Shuffle WF1 v2 automatically creates a TheHive case for every Wazuh alert that passes the dedup filter, capturing alert timestamp, source IP (AbuseIPDB-enriched), Cloudflare block status, Wazuh rule ID and description, and severity. Cortex 3 (5 analyzers) runs automated indicator analysis and records results as case observables; the TheHive case lifecycle (New --> In Progress --> Resolved) provides the audit trail. Documented incident records via the ADR series: significant incidents affecting operational posture, configuration, or procedures are captured as Architecture Decision Records in `docs/adr/`. ADR 0005 (PBS backup gap, 2026-04-08) demonstrates the full documentation chain -- the incident was detected during Plan 1 Task 12 when the operator noticed the PBS NFS mount to smokehouse had not re-established after the 2026-04-07 rack consolidation reboot, covering a 5-day backup gap (2026-04-03 through 2026-04-07) for the daily critical job (DC01, WS01, TheHive). The ADR records root cause (boot-race: PBS LXC 300 came up before smokehouse finished exporting NFS; `_netdev` mount unit failed once and was never retried), remediation (manual remount, service restart, fstab hardened with `x-systemd.automount` options), and follow-up (Plan 1 Task 20: PBS backup alerting). ELK/Zeek logs on haccp ES (`logs-zeek.haccp-default-*`) and Arkime PCAP archive on `/opt/arkime/raw/` (daily SSH/rsync to smokehouse at 03:00) provide the tamper-evident network event record for forensic correlation.

#### Implementation Status: implemented

______________________________________________________________________
