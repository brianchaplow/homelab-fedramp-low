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
  sort-id: ma-04
---

# ma-4 - \[Maintenance\] Nonlocal Maintenance

## Control Statement

- \[a.\] Approve and monitor nonlocal maintenance and diagnostic activities;

- \[b.\] Allow the use of nonlocal maintenance and diagnostic tools only as consistent with organizational policy and documented in the security plan for the system;

- \[c.\] Employ strong authentication in the establishment of nonlocal maintenance and diagnostic sessions;

- \[d.\] Maintain records for nonlocal maintenance and diagnostic activities; and

- \[e.\] Terminate session and network connections when nonlocal maintenance is completed.

## Control Assessment Objective

- \[MA-04a.\]

  - \[MA-04a.[01]\] nonlocal maintenance and diagnostic activities are approved;
  - \[MA-04a.[02]\] nonlocal maintenance and diagnostic activities are monitored;

- \[MA-04b.\]

  - \[MA-04b.[01]\] the use of nonlocal maintenance and diagnostic tools are allowed only as consistent with organizational policy;
  - \[MA-04b.[02]\] the use of nonlocal maintenance and diagnostic tools are documented in the security plan for the system;

- \[MA-04c.\] strong authentication is employed in the establishment of nonlocal maintenance and diagnostic sessions;

- \[MA-04d.\] records for nonlocal maintenance and diagnostic activities are maintained;

- \[MA-04e.\]

  - \[MA-04e.[01]\] session connections are terminated when nonlocal maintenance is completed;
  - \[MA-04e.[02]\] network connections are terminated when nonlocal maintenance is completed.

## Control guidance

Nonlocal maintenance and diagnostic activities are conducted by individuals who communicate through either an external or internal network. Local maintenance and diagnostic activities are carried out by individuals who are physically present at the system location and not communicating across a network connection. Authentication techniques used to establish nonlocal maintenance and diagnostic sessions reflect the network access requirements in [IA-2](#ia-2) . Strong authentication requires authenticators that are resistant to replay attacks and employ multi-factor authentication. Strong authenticators include PKI where certificates are stored on a token protected by a password, passphrase, or biometric. Enforcing requirements in [MA-4](#ma-4) is accomplished, in part, by other controls. [SP 800-63B](#e59c5a7c-8b1f-49ca-8de0-6ee0882180ce) provides additional guidance on strong authentication and authenticators.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

All remote maintenance sessions to in-boundary hosts use Tailscale VPN (WireGuard device-key authentication) before any SSH connection is established, satisfying the strong authentication requirement. Remote sessions to brisket (100.124.139.56), haccp (100.74.16.82), smoker (100.77.138.24), and sear (100.86.67.91) all traverse the Tailscale mesh. Wazuh on brisket logs all SSH authentication events from each agent host, providing the session audit trail. Sessions terminate when the SSH connection closes -- no persistent tunnels remain open after maintenance completes. ADR 0005 documents a concrete nonlocal maintenance session record.

#### Implementation Status: implemented

______________________________________________________________________
