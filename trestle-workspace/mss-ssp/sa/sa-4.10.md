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
  sort-id: sa-04.10
---

# sa-4.10 - \[System and Services Acquisition\] Use of Approved PIV Products

## Control Statement

Employ only information technology products on the FIPS 201-approved products list for Personal Identity Verification (PIV) capability implemented within organizational systems.

## Control Assessment Objective

only information technology products on the FIPS 201-approved products list for the Personal Identity Verification (PIV) capability implemented within organizational systems are employed.

## Control guidance

Products on the FIPS 201-approved products list meet NIST requirements for Personal Identity Verification (PIV) of Federal Employees and Contractors. PIV cards are used for multi-factor authentication in systems and organizations.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

This control is not applicable to the Managed SOC Service. The MSS is a single-operator homelab pilot that does not implement Personal Identity Verification (PIV) capability, issue PIV credentials, or process PIV card authentication in any service workflow. No PIV-capable hardware is deployed within the authorization boundary. Authentication is via SSH key pairs on all Linux hosts, individual service account passwords stored in a gitignored `.env` file, and Tailscale node certificates for remote access. The FIPS 201 Approved Products List is not applicable to this deployment.

#### Implementation Status: not-applicable

______________________________________________________________________
