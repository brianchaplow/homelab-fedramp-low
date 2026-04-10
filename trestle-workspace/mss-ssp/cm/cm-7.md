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
  cm-7_prm_2:
    aggregates:
      - cm-07_odp.02
      - cm-07_odp.03
      - cm-07_odp.04
      - cm-07_odp.05
      - cm-07_odp.06
    profile-param-value-origin: organization
  cm-07_odp.01:
    alt-identifier: cm-7_prm_1
    profile-values:
      - SOC monitoring (Wazuh SIEM, Zeek, Suricata, Arkime PCAP, ELK analytics), SOAR automation (Shuffle), DFIR (Velociraptor), threat intelligence (OpenCTI), GRC/ConMon (DefectDojo, RegScale), ML-based scoring (ml-scorer), LLM enrichment (Ollama)
    profile-param-value-origin: organization
  cm-07_odp.02:
    profile-values:
      - all functions not listed in CLAUDE.md §Service Inventory; VLAN 40 target traffic to VLAN 20/30 (MokerLink ACL)
    profile-param-value-origin: organization
  cm-07_odp.03:
    profile-values:
      - all ports not explicitly published in docker-compose.yml or opened by UFW on in-boundary hosts
    profile-param-value-origin: organization
  cm-07_odp.04:
    profile-values:
      - Telnet; unencrypted FTP to/from SOC infrastructure hosts; peer-to-peer file sharing protocols
    profile-param-value-origin: organization
  cm-07_odp.05:
    profile-values:
      - all software not documented in CLAUDE.md §Service Inventory or homelab-soc-portfolio git repository
    profile-param-value-origin: organization
  cm-07_odp.06:
    profile-values:
      - remote desktop protocols on SOC infrastructure hosts; unauthenticated management services
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cm-07
---

# cm-7 - \[Configuration Management\] Least Functionality

## Control Statement

- \[a.\] Configure the system to provide only [mission-essential capabilities] ; and

- \[b.\] Prohibit or restrict the use of the following functions, ports, protocols, software, and/or services: [organization-defined prohibited or restricted functions, system ports, protocols, software, and/or services].

## Control Assessment Objective

- \[CM-07a.\] the system is configured to provide only [mission-essential capabilities];

- \[CM-07b.\]

  - \[CM-07b.[01]\] the use of [functions] is prohibited or restricted;
  - \[CM-07b.[02]\] the use of [ports] is prohibited or restricted;
  - \[CM-07b.[03]\] the use of [protocols] is prohibited or restricted;
  - \[CM-07b.[04]\] the use of [software] is prohibited or restricted;
  - \[CM-07b.[05]\] the use of [services] is prohibited or restricted.

## Control guidance

Systems provide a wide variety of functions and services. Some of the functions and services routinely provided by default may not be necessary to support essential organizational missions, functions, or operations. Additionally, it is sometimes convenient to provide multiple services from a single system component, but doing so increases risk over limiting the services provided by that single component. Where feasible, organizations limit component functionality to a single function per component. Organizations consider removing unused or unnecessary software and disabling unused or unnecessary physical and logical ports and protocols to prevent unauthorized connection of components, transfer of information, and tunneling. Organizations employ network scanning tools, intrusion detection and prevention systems, and end-point protection technologies, such as firewalls and host-based intrusion detection systems, to identify and prevent the use of prohibited functions, protocols, ports, and services. Least functionality can also be achieved as part of the fundamental design and development of the system (see [SA-8](#sa-8), [SC-2](#sc-2) , and [SC-3](#sc-3)).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The system is configured to provide only mission-essential SOC capabilities. Each in-boundary host runs only the services required for its designated role: brisket (10.10.20.30) runs Wazuh Manager/Indexer/Dashboard, Prometheus, Grafana, Shuffle SOAR, Velociraptor, ML Scorer, Ollama, and OpenCTI -- no unrelated services. haccp (10.10.30.25) runs ELK, Arkime, and Logstash exclusively. dojo (10.10.30.27) runs DefectDojo and its Valkey dependency; regscale (10.10.30.28) runs RegScale CE and its MSSQL dependency. The canonical mission-essential service list per host is defined in CLAUDE.md §Service Inventory, which serves as the operational baseline definition -- any service not listed is not approved. Docker container isolation ensures that each service is confined to its own namespace with no host-network exposure beyond explicitly published ports (`brisket-setup/monitoring/docker-compose.yml`).

Prohibited functions and traffic paths are enforced at multiple layers. OPNsense (10.10.10.1) enforces perimeter restrictions blocking all non-essential inbound access. MokerLink L3 ACL isolates VLAN 40 (targets, 10.10.40.0/24) from VLAN 20 (SOC) and VLAN 30 (lab), preventing target-originated traffic from reaching SOC infrastructure. UFW default-deny on dojo and regscale blocks all ports not explicitly opened. Prometheus scrape targets (`brisket-setup/monitoring/prometheus.yml`) and Zeek loaded-scripts (`reference/phase14/zeek/local.zeek`) are explicitly enumerated -- no wildcard discovery or default plugin activation. Wazuh SCA checks validate that enrolled agents do not expose unnecessary running services or open ports. The primary gap driving `partial` status is the absence of a committed prohibited-ports/protocols list as a formal configuration document separate from CLAUDE.md prose.

#### Implementation Status: partial

______________________________________________________________________
