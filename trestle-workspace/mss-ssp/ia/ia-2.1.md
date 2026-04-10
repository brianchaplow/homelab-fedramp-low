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
  sort-id: ia-02.01
---

# ia-2.1 - \[Identification and Authentication\] Multi-factor Authentication to Privileged Accounts

## Control Statement

Implement multi-factor authentication for access to privileged accounts.

## Control Assessment Objective

multi-factor authentication is implemented for access to privileged accounts.

## Control guidance

Multi-factor authentication requires the use of two or more different factors to achieve authentication. The authentication factors are defined as follows: something you know (e.g., a personal identification number [PIN]), something you have (e.g., a physical authenticator such as a cryptographic private key), or something you are (e.g., a biometric). Multi-factor authentication solutions that feature physical authenticators include hardware authenticators that provide time-based or challenge-response outputs and smart cards such as the U.S. Government Personal Identity Verification (PIV) card or the Department of Defense (DoD) Common Access Card (CAC). In addition to authenticating users at the system level (i.e., at logon), organizations may employ authentication mechanisms at the application level, at their discretion, to provide increased security. Regardless of the type of access (i.e., local, network, remote), privileged accounts are authenticated using multi-factor options appropriate for the level of risk. Organizations can add additional security measures, such as additional or more rigorous authentication mechanisms, for specific types of access.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Multi-factor authentication is not currently implemented for privileged account access to any in-boundary service in the Managed SOC Service. This is a documented gap.

SSH access to all in-boundary hosts -- brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, and regscale -- uses private key authentication (something you have) as the sole factor. While SSH key authentication is cryptographically stronger than password-only authentication and satisfies replay resistance (see IA-2(8)), it constitutes single-factor authentication under NIST SP 800-63B. A private key replaces the password; it does not add a second factor on top of a password or biometric. Under SP 800-63B, SSH key-only access is a single-factor cryptographic authenticator at AAL2, which does not satisfy the MFA requirement for privileged accounts. Similarly, Tailscale device authentication uses WireGuard keys (device-bound cryptographic factor) without a required second factor.

No TOTP, hardware token, PIV card, or push-notification MFA is wired to any privileged service console -- Wazuh Dashboard, Shuffle SOAR, OpenCTI, Velociraptor, or the Wazuh API. MFA implementation is a planned remediation item tracked in the FedRAMP Low ConMon program. Until remediated, this control is partial -- the gap is acknowledged and the risk accepted under the homelab boundary posture documented in this SSP.

#### Implementation Status: partial

______________________________________________________________________
