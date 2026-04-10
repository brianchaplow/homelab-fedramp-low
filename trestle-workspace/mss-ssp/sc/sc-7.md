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
  sc-07_odp:
    alt-identifier: sc-7_prm_1
    profile-values:
      - OPNsense inter-VLAN firewall on VP2420 (10.10.10.1); MokerLink L3 port ACLs on TE4 for intra-VLAN microsegmentation; Tailscale mesh for authorized remote administrative access
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sc-07
---

# sc-7 - \[System and Communications Protection\] Boundary Protection

## Control Statement

- \[a.\] Monitor and control communications at the external managed interfaces to the system and at key internal managed interfaces within the system;

- \[b.\] Implement subnetworks for publicly accessible system components that are [Selection: physically; logically] separated from internal organizational networks; and

- \[c.\] Connect to external networks or systems only through managed interfaces consisting of boundary protection devices arranged in accordance with an organizational security and privacy architecture.

## Control Assessment Objective

- \[SC-07a.\]

  - \[SC-07a.[01]\] communications at external managed interfaces to the system are monitored;
  - \[SC-07a.[02]\] communications at external managed interfaces to the system are controlled;
  - \[SC-07a.[03]\] communications at key internal managed interfaces within the system are monitored;
  - \[SC-07a.[04]\] communications at key internal managed interfaces within the system are controlled;

- \[SC-07b.\] subnetworks for publicly accessible system components are [Selection: physically; logically] separated from internal organizational networks;

- \[SC-07c.\] external networks or systems are only connected to through managed interfaces consisting of boundary protection devices arranged in accordance with an organizational security and privacy architecture.

## Control guidance

Managed interfaces include gateways, routers, firewalls, guards, network-based malicious code analysis, virtualization systems, or encrypted tunnels implemented within a security architecture. Subnetworks that are physically or logically separated from internal networks are referred to as demilitarized zones or DMZs. Restricting or prohibiting interfaces within organizational systems includes restricting external web traffic to designated web servers within managed interfaces, prohibiting external traffic that appears to be spoofing internal addresses, and prohibiting internal traffic that appears to be spoofing external addresses. [SP 800-189](#f5edfe51-d1f2-422e-9b27-5d0e90b49c72) provides additional information on source address validation techniques to prevent ingress and egress of traffic with spoofed addresses. Commercial telecommunications services are provided by network components and consolidated management systems shared by customers. These services may also include third party-provided access lines and other service elements. Such services may represent sources of increased risk despite contract security provisions. Boundary protection may be implemented as a common control for all or part of an organizational network such that the boundary to be protected is greater than a system-specific boundary (i.e., an authorization boundary).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

OPNsense on the Protectli VP2420 (10.10.10.1) is the boundary enforcement point for all five VLANs -- VLAN 10 (management), VLAN 20 (SOC infrastructure), VLAN 30 (lab/Proxmox/AD), VLAN 40 (targets -- ISOLATED), and VLAN 50 (IoT) -- via 802.1Q trunk on igc0 to the MokerLink 10G switch. Inter-VLAN firewall rules implement a default-deny posture between security domains: VLAN 40 (targets) carries an explicit DENY outbound rule allowing only established-session return traffic, which enforces full isolation of attack-target workloads from SOC services. VLAN 50 (IoT) is restricted to internet-only egress with no lateral movement to VLANs 10, 20, or 30. All external connectivity traverses OPNsense -- the three documented external connection types are Wazuh agent telemetry inbound on brisket:1514 (TLS), administrative SSH access (key-only), and PBS backup NFS egress to smokehouse -- each constituting a managed interface per the whole-project design §2.4. OPNsense syslog ships firewall events to the Wazuh Manager (brisket) for monitoring and correlation via `wazuh-alerts-*`.

MokerLink L3 port ACL `sear-brisket` (TE4) extends boundary enforcement intra-VLAN on VLAN 20, limiting sear (10.10.20.20) to enumerated Wazuh agent ports (1514, 1515) and OpenSearch (9200) inbound to brisket (10.10.20.30), and explicitly denying all other same-subnet traffic -- this prevents intra-VLAN lateral movement without routing through OPNsense. Tailscale encrypted mesh overlay (WireGuard-based) provides the sole authorized remote management path for administrative access from PITBOSS to in-boundary hosts; all remote management traffic traverses this cryptographic boundary crossing. Suricata IDS on smokehouse monitors the MokerLink SPAN (TE1-TE9 mirrored to TE10/TE11) and ships signatures to Wazuh for boundary event correlation.

#### Implementation Status: implemented

______________________________________________________________________
