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
  sc-05_odp.01:
    alt-identifier: sc-5_prm_2
    profile-values:
      - volumetric network floods, connection exhaustion, intra-VLAN lateral flooding from compromised VMs
    profile-param-value-origin: organization
  sc-05_odp.02:
    alt-identifier: sc-5_prm_1
    profile-values:
      - limit
    profile-param-value-origin: organization
  sc-05_odp.03:
    alt-identifier: sc-5_prm_3
    profile-values:
      - OPNsense stateful packet filtering for external volumetric events; MokerLink port ACL for intra-VLAN flooding; Suricata IDS for signature detection
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sc-05
---

# sc-5 - \[System and Communications Protection\] Denial-of-service Protection

## Control Statement

- \[a.\] [Selection: protect against; limit] the effects of the following types of denial-of-service events: [types of denial-of-service events] ; and

- \[b.\] Employ the following controls to achieve the denial-of-service objective: [controls by type of denial-of-service event].

## Control Assessment Objective

- \[SC-05a.\] the effects of [types of denial-of-service events] are [Selection: protect against; limit];

- \[SC-05b.\] [controls by type of denial-of-service event] are employed to achieve the denial-of-service protection objective.

## Control guidance

Denial-of-service events may occur due to a variety of internal and external causes, such as an attack by an adversary or a lack of planning to support organizational needs with respect to capacity and bandwidth. Such attacks can occur across a wide range of network protocols (e.g., IPv4, IPv6). A variety of technologies are available to limit or eliminate the origination and effects of denial-of-service events. For example, boundary protection devices can filter certain types of packets to protect system components on internal networks from being directly affected by or the source of denial-of-service attacks. Employing increased network capacity and bandwidth combined with service redundancy also reduces the susceptibility to denial-of-service events.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

OPNsense on the Protectli VP2420 (10.10.10.1) provides the primary DoS mitigation layer for the MSS boundary. Stateful packet inspection limits connection flooding from external sources; inter-VLAN rules deny inbound traffic from VLAN 40 (targets), preventing compromised lab VMs from flooding SOC infrastructure; and VLAN 50 (IoT) is restricted to internet-only egress with no lateral movement permitted. MokerLink port-bound ACLs (TE4 `sear-brisket`) limit intra-VLAN flooding between SOC components on VLAN 20 without routing through OPNsense. Suricata IDS running on smokehouse eth4 (SPAN of TE1-TE9) detects volumetric signatures and ships eve.json alerts to `wazuh-alerts-*` for correlation. The combined effect is that the MSS can limit the impact of volumetric and lateral flooding events from in-boundary sources.

Gap: no cloud-based DoS scrubbing service or dedicated anti-DDoS appliance is deployed. A sustained high-volume external flood would rely on Verizon upstream throttling as the only upstream mitigation; the MSS itself has no BGP-based blackholing or scrubbing capability. This is an accepted trade-off for a homelab environment with no public-facing services in boundary. Status is partial -- the deployed controls limit the effects of the enumerated DoS event types but do not fully protect against sustained external volumetric attacks.

#### Implementation Status: partial

______________________________________________________________________
