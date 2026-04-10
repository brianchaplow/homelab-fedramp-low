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
  sort-id: ac-03
---

# ac-3 - \[Access Control\] Access Enforcement

## Control Statement

Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.

## Control Assessment Objective

approved authorizations for logical access to information and system resources are enforced in accordance with applicable access control policies.

## Control guidance

Access control policies control access between active entities or subjects (i.e., users or processes acting on behalf of users) and passive entities or objects (i.e., devices, files, records, domains) in organizational systems. In addition to enforcing authorized access at the system level and recognizing that systems can host many applications and services in support of mission and business functions, access enforcement mechanisms can also be employed at the application and service level to provide increased information security and privacy. In contrast to logical access controls that are implemented within the system, physical access controls are addressed by the controls in the Physical and Environmental Protection ( [PE](#pe) ) family.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Access enforcement is implemented through three complementary layers that together enforce the approved authorization model across all MSS boundary components. At the network perimeter, OPNsense inter-VLAN firewall rules block unauthorized lateral movement between VLANs 10 (management), 20 (SOC infrastructure), 30 (lab), 40 (targets -- isolated), and 50 (IoT); VLAN 40 is configured default-deny inbound from VLANs 20 and 30 so that attack targets cannot initiate connections to SOC services. At the intra-VLAN layer, MokerLink switch ACL `sear-brisket` (TE4) enforces microsegmentation between sear (10.10.20.20) and brisket (10.10.20.30) with a stateless 9-rule bidirectional ACL permitting only enumerated ports and explicitly denying all others; the full rule table with packet-flow verification results is documented in `/c/Projects/reference/network.md`. At the host layer, UFW on all in-boundary Linux hosts (brisket, haccp, smokehouse, dojo, regscale) enforces default-deny ingress with VLAN-scoped explicit allows for each service port -- dojo and regscale UFW rules are documented in ADR 0002 §Infrastructure state. SSH key-only authentication reinforces the access model at the protocol layer; no password-based SSH is permitted on any in-boundary host. Service-level RBAC adds a fourth enforcement point: Wazuh differentiates admin vs. read-only roles, OpenCTI enforces admin vs. analyst scopes, and TheHive distinguishes platform-admin from org-admin. Cross-reference SC-7 for boundary protection and AC-17 for the remote access enforcement path.

#### Implementation Status: implemented

______________________________________________________________________
