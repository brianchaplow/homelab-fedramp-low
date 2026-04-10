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
  ca-09_odp.01:
    alt-identifier: ca-9_prm_1
    profile-values:
      - all VLAN 20 and VLAN 30 components listed in CLAUDE.md All Hosts table
    profile-param-value-origin: organization
  ca-09_odp.02:
    alt-identifier: ca-9_prm_2
    profile-values:
      - component decommission; security incident requiring isolation; unauthorized connection detected
    profile-param-value-origin: organization
  ca-09_odp.03:
    alt-identifier: ca-9_prm_3
    profile-values:
      - annually; following significant network or component change
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-09
---

# ca-9 - \[Assessment, Authorization, and Monitoring\] Internal System Connections

## Control Statement

- \[a.\] Authorize internal connections of [system components] to the system;

- \[b.\] Document, for each internal connection, the interface characteristics, security and privacy requirements, and the nature of the information communicated;

- \[c.\] Terminate internal system connections after [conditions] ; and

- \[d.\] Review [frequency] the continued need for each internal connection.

## Control Assessment Objective

- \[CA-09a.\] internal connections of [system components] to the system are authorized;

- \[CA-09b.\]

  - \[CA-09b.[01]\] for each internal connection, the interface characteristics are documented;
  - \[CA-09b.[02]\] for each internal connection, the security requirements are documented;
  - \[CA-09b.[03]\] for each internal connection, the privacy requirements are documented;
  - \[CA-09b.[04]\] for each internal connection, the nature of the information communicated is documented;

- \[CA-09c.\] internal system connections are terminated after [conditions];

- \[CA-09d.\] the continued need for each internal connection is reviewed [frequency].

## Control guidance

Internal system connections are connections between organizational systems and separate constituent system components (i.e., connections between components that are part of the same system) including components used for system development. Intra-system connections include connections with mobile devices, notebook and desktop computers, tablets, printers, copiers, facsimile machines, scanners, sensors, and servers. Instead of authorizing each internal system connection individually, organizations can authorize internal connections for a class of system components with common characteristics and/or configurations, including printers, scanners, and copiers with a specified processing, transmission, and storage capability or smart phones and tablets with a specific baseline configuration. The continued need for an internal system connection is reviewed from the perspective of whether it provides support for organizational missions or business functions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Internal connections are authorized and documented through three mechanisms: `CLAUDE.md` §"All Hosts" (authoritative inventory with IP, VLAN, and role for each component), `oscal/component-definition.json` (OSCAL-format inventory of 7 in-boundary components: brisket, haccp, smokehouse, dojo, regscale, OPNsense, MokerLink), and `reference/network.md` (detailed topology, OPNsense interface configuration, firewall rules, and MokerLink ACL table).

Key internal connections, authorized and documented: Wazuh agents (15 total) to Manager (brisket:1514/1515) via OSSEC encrypted protocol carrying security events and syscollector data across VLAN 20/30/10; Filebeat (smokehouse) to Logstash (brisket:5044) carrying Zeek logs via Beat protocol on VLAN 20; Fleet agents (haccp) to Elasticsearch (haccp:9200) via HTTPS on VLAN 30 local; Logstash (haccp) to OpenCTI (brisket:8080) via HTTP/REST for TI lookups across VLAN 30 to VLAN 20; Logstash (haccp) to Ollama (brisket:11434) via HTTP for LLM classification with token-bucket rate limit (10 req/min) across VLAN 30 to VLAN 20; PBS LXC 300 (10.10.30.24) to smokehouse NFS (10.10.20.10) via NFSv3/v4 TCP carrying VM backup data, hardened per ADR 0005 with `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30`; dojo (10.10.30.27) and regscale (10.10.30.28) Wazuh agents 016/017 to brisket Manager across VLAN 30 to VLAN 20, authorized per Plan 1 ADR 0002; PITBOSS (10.10.10.100) to pipeline endpoints via SSH/Git Bash for pipeline invocations on management VLAN 10 to VLAN 20. MokerLink mirror sessions 1+2 (TE1-TE9 to TE10/TE11) feed haccp `span0` and smokehouse `eth4` as authorized read-only SPAN -- not routable connections.

Enforcement is by MokerLink L3 switch ACL (10.10.10.2) for inter-VLAN routing authorization, and OPNsense firewall (10.10.10.1) for inter-VLAN policy. VLAN 40 targets are isolated with no routing path to production VLANs except through explicit OPNsense rules for the Caldera C2 path.

Termination conditions are implemented: OpenCTI LXC 202 (10.10.30.26) is a documented decommission example -- connection terminated after Phase 12 migration to brisket Docker, autostart disabled. Shuffle WF1 v2 provides an immediate connection termination path via OPNsense block through `$cf_api_token` and `$cf_account_id` workflow variables. Connection need is reviewed annually and following significant network or component changes.

#### Implementation Status: implemented

______________________________________________________________________
