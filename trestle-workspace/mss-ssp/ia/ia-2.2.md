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
  sort-id: ia-02.02
---

# ia-2.2 - \[Identification and Authentication\] Multi-factor Authentication to Non-privileged Accounts

## Control Statement

Implement multi-factor authentication for access to non-privileged accounts.

## Control Assessment Objective

multi-factor authentication for access to non-privileged accounts is implemented.

## Control guidance

Multi-factor authentication requires the use of two or more different factors to achieve authentication. The authentication factors are defined as follows: something you know (e.g., a personal identification number [PIN]), something you have (e.g., a physical authenticator such as a cryptographic private key), or something you are (e.g., a biometric). Multi-factor authentication solutions that feature physical authenticators include hardware authenticators that provide time-based or challenge-response outputs and smart cards such as the U.S. Government Personal Identity Verification card or the DoD Common Access Card. In addition to authenticating users at the system level, organizations may also employ authentication mechanisms at the application level, at their discretion, to provide increased information security. Regardless of the type of access (i.e., local, network, remote), non-privileged accounts are authenticated using multi-factor options appropriate for the level of risk. Organizations can provide additional security measures, such as additional or more rigorous authentication mechanisms, for specific types of access.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Multi-factor authentication is not currently implemented for non-privileged account access to any in-boundary service in the Managed SOC Service. This is a documented gap with the same posture as IA-2(1).

SSH key authentication is used for all host access, constituting a single cryptographic factor. No second factor -- TOTP, hardware token, PIV, or biometric -- is paired with SSH keys or any service console. The `socadmin@thehive.local` and `socadmin@SOC` accounts in TheHive and Cortex represent lower-privilege operator roles and are also single-factor (named account with password). In a single-operator homelab boundary, the distinction between privileged and non-privileged accounts is largely nominal -- the operator holds admin credentials for all services -- but the non-privileged accounts equally lack a second authentication factor.

MFA for non-privileged accounts is a planned remediation item, linked to the same initiative as IA-2(1). Until remediated, this control is partial -- the gap is documented, the risk is accepted under the lab posture, and a future ConMon cycle will address MFA implementation across all service tiers.

#### Implementation Status: partial

______________________________________________________________________
