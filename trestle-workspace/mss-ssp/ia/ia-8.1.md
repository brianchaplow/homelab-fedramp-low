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
  sort-id: ia-08.01
---

# ia-8.1 - \[Identification and Authentication\] Acceptance of PIV Credentials from Other Agencies

## Control Statement

Accept and electronically verify Personal Identity Verification-compliant credentials from other federal agencies.

## Control Assessment Objective

- \[IA-08(01)[01]\] Personal Identity Verification-compliant credentials from other federal agencies are accepted;

- \[IA-08(01)[02]\] Personal Identity Verification-compliant credentials from other federal agencies are electronically verified.

## Control guidance

Acceptance of Personal Identity Verification (PIV) credentials from other federal agencies applies to both logical and physical access control systems. PIV credentials are those credentials issued by federal agencies that conform to FIPS Publication 201 and supporting guidelines. The adequacy and reliability of PIV card issuers are addressed and authorized using [SP 800-79-2](#10963761-58fc-4b20-b3d6-b44a54daba03).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

IA-8(1) is not applicable to the Managed SOC Service. The system is a private homelab with no federal agency interconnections and no PIV infrastructure. No federal users from other agencies access this system, and no PIV-compliant credential issuance or verification capability is deployed or planned.

#### Implementation Status: not-applicable

______________________________________________________________________
