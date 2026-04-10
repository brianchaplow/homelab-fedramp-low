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
  sort-id: ia-08.02
---

# ia-8.2 - \[Identification and Authentication\] Acceptance of External Authenticators

## Control Statement

- \[(a)\] Accept only external authenticators that are NIST-compliant; and

- \[(b)\] Document and maintain a list of accepted external authenticators.

## Control Assessment Objective

- \[IA-08(02)(a)\] only external authenticators that are NIST-compliant are accepted;

- \[IA-08(02)(b)\]

  - \[IA-08(02)(b)[01]\] a list of accepted external authenticators is documented;
  - \[IA-08(02)(b)[02]\] a list of accepted external authenticators is maintained.

## Control guidance

Acceptance of only NIST-compliant external authenticators applies to organizational systems that are accessible to the public (e.g., public-facing websites). External authenticators are issued by nonfederal government entities and are compliant with [SP 800-63B](#e59c5a7c-8b1f-49ca-8de0-6ee0882180ce) . Approved external authenticators meet or exceed the minimum Federal Government-wide technical, security, privacy, and organizational maturity requirements. Meeting or exceeding Federal requirements allows Federal Government relying parties to trust external authenticators in connection with an authentication transaction at a specified authenticator assurance level.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

IA-8(2) is not applicable to the Managed SOC Service. The system does not accept any external authenticators from non-federal identity providers. All authentication is internal: SSH keys issued by the operator, service passwords managed in `.env`, and Tailscale device keys issued through the operator's Tailscale account. No OAuth, SAML, or federated identity provider integrations are in use within the FedRAMP Low boundary, and no external authenticators from any source are accepted.

#### Implementation Status: not-applicable

______________________________________________________________________
