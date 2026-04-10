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
  sort-id: ir-04
---

# ir-4 - \[Incident Response\] Incident Handling

## Control Statement

- \[a.\] Implement an incident handling capability for incidents that is consistent with the incident response plan and includes preparation, detection and analysis, containment, eradication, and recovery;

- \[b.\] Coordinate incident handling activities with contingency planning activities;

- \[c.\] Incorporate lessons learned from ongoing incident handling activities into incident response procedures, training, and testing, and implement the resulting changes accordingly; and

- \[d.\] Ensure the rigor, intensity, scope, and results of incident handling activities are comparable and predictable across the organization.

## Control Assessment Objective

- \[IR-04a.\]

  - \[IR-04a.[01]\] an incident handling capability for incidents is implemented that is consistent with the incident response plan;
  - \[IR-04a.[02]\] the incident handling capability for incidents includes preparation;
  - \[IR-04a.[03]\] the incident handling capability for incidents includes detection and analysis;
  - \[IR-04a.[04]\] the incident handling capability for incidents includes containment;
  - \[IR-04a.[05]\] the incident handling capability for incidents includes eradication;
  - \[IR-04a.[06]\] the incident handling capability for incidents includes recovery;

- \[IR-04b.\] incident handling activities are coordinated with contingency planning activities;

- \[IR-04c.\]

  - \[IR-04c.[01]\] lessons learned from ongoing incident handling activities are incorporated into incident response procedures, training, and testing;
  - \[IR-04c.[02]\] the changes resulting from the incorporated lessons learned are implemented accordingly;

- \[IR-04d.\]

  - \[IR-04d.[01]\] the rigor of incident handling activities is comparable and predictable across the organization;
  - \[IR-04d.[02]\] the intensity of incident handling activities is comparable and predictable across the organization;
  - \[IR-04d.[03]\] the scope of incident handling activities is comparable and predictable across the organization;
  - \[IR-04d.[04]\] the results of incident handling activities are comparable and predictable across the organization.

## Control guidance

Organizations recognize that incident response capabilities are dependent on the capabilities of organizational systems and the mission and business processes being supported by those systems. Organizations consider incident response as part of the definition, design, and development of mission and business processes and systems. Incident-related information can be obtained from a variety of sources, including audit monitoring, physical access monitoring, and network monitoring; user or administrator reports; and reported supply chain events. An effective incident handling capability includes coordination among many organizational entities (e.g., mission or business owners, system owners, authorizing officials, human resources offices, physical security offices, personnel security offices, legal departments, risk executive [function], operations personnel, procurement offices). Suspected security incidents include the receipt of suspicious email communications that can contain malicious code. Suspected supply chain incidents include the insertion of counterfeit hardware or malicious code into organizational systems or system components. For federal agencies, an incident that involves personally identifiable information is considered a breach. A breach results in unauthorized disclosure, the loss of control, unauthorized acquisition, compromise, or a similar occurrence where a person other than an authorized user accesses or potentially accesses personally identifiable information or an authorized user accesses or potentially accesses such information for other than authorized purposes.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service implements all five NIST incident handling phases through an integrated toolchain. Preparation: Wazuh SIEM on brisket (15 enrolled agents covering all in-boundary and supporting hosts) provides continuous monitoring; Shuffle SOAR WF1 v2 receives Wazuh alerts via webhook, performs AbuseIPDB enrichment, executes Cloudflare IP blocks, creates TheHive 4 cases on pitcrew LXC 200, and posts to Discord #soc-alerts via the `$discord_webhook` variable; Velociraptor v0.75.3 on brisket (7 enrolled DFIR clients) provides pre-staged endpoint forensics; PBS LXC 300 on smoker delivers daily snapshots of in-boundary VMs (dojo, regscale, DC01, WS01, TheHive) to smokehouse 17TB NFS. Detection and analysis: Zeek on haccp span0 (USB 2.5GbE, promiscuous, JA3/JA4/community-id enrichment) ships logs via Filebeat --> Logstash 5-stage pipeline to ELK (haccp ES 8.17); XGBoost ML Scorer on brisket:5002 (PR-AUC 0.9998) scores network flows; TheHive 4 + Cortex 3 (5 analyzers) structures case management and automated indicator analysis. Containment: Shuffle WF1 blocks offending IPs via Cloudflare API; OPNsense and MokerLink ACL enforce VLAN 40 isolation of target systems. Eradication: Velociraptor hunts across 7 enrolled clients enable process termination, file removal, and persistence mechanism identification; Wazuh active response executes remediation scripts on agents. Recovery: PBS same-day rollback (daily job at 02:00); restore procedure documented in `runbooks/restore-from-pbs.md`. ADR 0005 (PBS backup gap, 2026-04-08) is the canonical real end-to-end incident: detected during Plan 1 Task 12, root-cause analyzed, contained via manual remount, eradicated via fstab automount hardening, and recovered with confirmed backup on 2026-04-09. Lessons learned are captured as ADRs and reflected in `runbooks/monthly-conmon.md`. Known gaps: PBS backup-failure alerting (Wazuh --> Discord) is pending (Plan 1 Task 20); Shuffle WF4 (automated Velociraptor triage) is not yet deployed.

#### Implementation Status: implemented

______________________________________________________________________
