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
  sort-id: ra-05.11
---

# ra-5.11 - \[Risk Assessment\] Public Disclosure Program

## Control Statement

Establish a public reporting channel for receiving reports of vulnerabilities in organizational systems and system components.

## Control Assessment Objective

a public reporting channel is established for receiving reports of vulnerabilities in organizational systems and system components.

## Control guidance

The reporting channel is publicly discoverable and contains clear language authorizing good-faith research and the disclosure of vulnerabilities to the organization. The organization does not condition its authorization on an expectation of indefinite non-disclosure to the public by the reporting entity but may request a specific time period to properly remediate the vulnerability.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. The Managed SOC Service is a single-operator personal portfolio system with no public-facing attack surface. All in-boundary hosts reside on private VLAN 20 (10.10.20.0/24) and VLAN 30 (10.10.30.0/24) with no inbound internet access -- OPNsense on the perimeter firewall (10.10.10.1) blocks all unsolicited inbound connections by default, and no public IP addresses are assigned to any in-boundary MSS host. Remote access is restricted to the operator via Tailscale VPN. There is no web application, API endpoint, or service exposed to external researchers from which vulnerabilities could be discovered and reported. A public disclosure channel would have no mechanism to receive reports and no scope to authorize good-faith research against private homelab infrastructure.

The operator's GCP VM (external, Tailscale 100.125.40.97) hosts public-facing websites (brianchaplow.com, bytesbourbonbbq.com) but those are explicitly out-of-boundary assets per `inventory/overlay.yaml` (reason: "Customer asset on GCP") and are not part of the MSS system boundary. The not-applicable determination holds for the current system boundary and would be revisited if any in-boundary service were exposed to the internet in a future phase.

#### Implementation Status: not-applicable

______________________________________________________________________
