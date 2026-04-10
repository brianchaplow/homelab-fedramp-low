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
  ca-03_odp.01:
    alt-identifier: ca-3_prm_1
    profile-values:
      - information exchange security agreements (documented in SSP and CLAUDE.md)
    profile-param-value-origin: organization
  ca-03_odp.02:
    alt-identifier: ca-3_prm_2
    profile-values:
      - this SSP (external connections section); CLAUDE.md Network Quick Reference
    profile-param-value-origin: organization
  ca-03_odp.03:
    alt-identifier: ca-3_prm_3
    profile-values:
      - annually; following significant system or network change
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-03
---

# ca-3 - \[Assessment, Authorization, and Monitoring\] Information Exchange

## Control Statement

- \[a.\] Approve and manage the exchange of information between the system and other systems using [Selection (one or more): interconnection security agreements; information exchange security agreements; memoranda of understanding or agreement; service level agreements; user agreements; non-disclosure agreements; [type of agreement]];

- \[b.\] Document, as part of each exchange agreement, the interface characteristics, security and privacy requirements, controls, and responsibilities for each system, and the impact level of the information communicated; and

- \[c.\] Review and update the agreements [frequency].

## Control Assessment Objective

- \[CA-03a.\] the exchange of information between the system and other systems is approved and managed using [Selection (one or more): interconnection security agreements; information exchange security agreements; memoranda of understanding or agreement; service level agreements; user agreements; non-disclosure agreements; [type of agreement]];

- \[CA-03b.\]

  - \[CA-03b.[01]\] the interface characteristics are documented as part of each exchange agreement;
  - \[CA-03b.[02]\] security requirements are documented as part of each exchange agreement;
  - \[CA-03b.[03]\] privacy requirements are documented as part of each exchange agreement;
  - \[CA-03b.[04]\] controls are documented as part of each exchange agreement;
  - \[CA-03b.[05]\] responsibilities for each system are documented as part of each exchange agreement;
  - \[CA-03b.[06]\] the impact level of the information communicated is documented as part of each exchange agreement;

- \[CA-03c.\] agreements are reviewed and updated [frequency].

## Control guidance

System information exchange requirements apply to information exchanges between two or more systems. System information exchanges include connections via leased lines or virtual private networks, connections to internet service providers, database sharing or exchanges of database transaction information, connections and exchanges with cloud services, exchanges via web-based services, or exchanges of files via file transfer protocols, network protocols (e.g., IPv4, IPv6), email, or other organization-to-organization communications. Organizations consider the risk related to new or increased threats that may be introduced when systems exchange information with other systems that may have different security and privacy requirements and controls. This includes systems within the same organization and systems that are external to the organization. A joint authorization of the systems exchanging information, as described in [CA-6(1)](#ca-6.1) or [CA-6(2)](#ca-6.2) , may help to communicate and reduce risk.

Authorizing officials determine the risk associated with system information exchange and the controls needed for appropriate risk mitigation. The types of agreements selected are based on factors such as the impact level of the information being exchanged, the relationship between the organizations exchanging information (e.g., government to government, government to business, business to business, government or business to service provider, government or business to individual), or the level of access to the organizational system by users of the other system. If systems that exchange information have the same authorizing official, organizations need not develop agreements. Instead, the interface characteristics between the systems (e.g., how the information is being exchanged. how the information is protected) are described in the respective security and privacy plans. If the systems that exchange information have different authorizing officials within the same organization, the organizations can develop agreements or provide the same information that would be provided in the appropriate agreement type from [CA-3a](#ca-3_smt.a) in the respective security and privacy plans for the systems. Organizations may incorporate agreement information into formal contracts, especially for information exchanges established between federal agencies and nonfederal organizations (including service providers, contractors, system developers, and system integrators). Risk considerations include systems that share the same networks.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS homelab boundary has four categories of external information exchange, all documented in `CLAUDE.md` (the authoritative whole-project design reference) and this SSP. Agreement type for all external exchanges is information exchange security agreement, documented in prose in this SSP and in `CLAUDE.md` §"Network Quick Reference" and `reference/network.md`.

The first category is the Tailscale overlay network (outbound/bidirectional). Hosts with Tailscale connectivity: brisket (TS 100.124.139.56), smokehouse (TS 100.110.112.98), sear (TS 100.86.67.91), haccp (TS 100.74.16.82), smoker (TS 100.77.138.24), PITBOSS (TS 100.126.10.19), GCP VM (TS 100.125.40.97). Protocol: WireGuard-based mesh VPN. Traffic is encrypted in transit. Information communicated: SSH management sessions and pipeline invocations from PITBOSS. Impact: low (management traffic only). Responsibility: Tailscale, Inc. operates the coordination plane; each node is owned by Brian Chaplow.

The second category is the GCP VM Wazuh agent (agent 009) reporting from an external IP to brisket Wazuh Manager (10.10.20.30:1514/1515). Interface: OSSEC protocol over Tailscale WireGuard tunnel. Information communicated: security events and syslog. Impact: low.

The third category is the PBS LXC 300 (10.10.30.24) NFS mount to smokehouse (10.10.20.10) over the VLAN 30 to VLAN 20 routed path. Interface: NFSv3/v4 over TCP. Information: VM backup data including ConMon artifacts. Impact: moderate (backup loss creates recovery gap). Hardened per ADR 0005: fstab uses `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30` to prevent boot-race failures.

The fourth category is the OPNsense syslog feed (514/UDP) to Wazuh Manager (in-boundary, VLAN 10 to VLAN 20). Interface: syslog UDP. Information: firewall events. Impact: low.

Agreements are reviewed annually and following significant network or component changes. HTTP-only posture for DefectDojo and RegScale is a known gap acknowledged in ADR 0002 and ADR 0003; SC-8 addresses the mitigations. Formal written ISAs do not exist; this SSP prose serves as the agreement documentation for the homelab scope.

#### Implementation Status: partial

______________________________________________________________________
