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
  sort-id: ia-02.12
---

# ia-2.12 - \[Identification and Authentication\] Acceptance of PIV Credentials

## Control Statement

Accept and electronically verify Personal Identity Verification-compliant credentials.

## Control Assessment Objective

Personal Identity Verification-compliant credentials are accepted and electronically verified.

## Control guidance

Acceptance of Personal Identity Verification (PIV)-compliant credentials applies to organizations implementing logical access control and physical access control systems. PIV-compliant credentials are those credentials issued by federal agencies that conform to FIPS Publication 201 and supporting guidance documents. The adequacy and reliability of PIV card issuers are authorized using [SP 800-79-2](#10963761-58fc-4b20-b3d6-b44a54daba03) . Acceptance of PIV-compliant credentials includes derived PIV credentials, the use of which is addressed in [SP 800-166](#e8552d48-cf41-40aa-8b06-f45f7fb4706c) . The DOD Common Access Card (CAC) is an example of a PIV credential.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

IA-2(12) is not applicable to the Managed SOC Service. The system is a private homelab with no federal PIV infrastructure. PIV issuance requires federal agency sponsorship; the system owner holds no PIV card and no PIV issuance authority. No PIV card readers, middleware (e.g., OpenSC), or PIV-aware identity providers are deployed in the boundary.

#### Implementation Status: not-applicable

______________________________________________________________________
