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
  ia-08.04_odp:
    alt-identifier: ia-8.4_prm_1
    profile-values:
      - SSH (RFC 4251-4256, ED25519/RSA-4096); JWT (RFC 7519, role-claim based); TLS 1.2/1.3 (RFC 5246/8446)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ia-08.04
---

# ia-8.4 - \[Identification and Authentication\] Use of Defined Profiles

## Control Statement

Conform to the following profiles for identity management [identity management profiles].

## Control Assessment Objective

there is conformance with [identity management profiles] for identity management.

## Control guidance

Organizations define profiles for identity management based on open identity management standards. To ensure that open identity management standards are viable, robust, reliable, sustainable, and interoperable as documented, the Federal Government assesses and scopes the standards and technology implementations against applicable laws, executive orders, directives, policies, regulations, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service partially conforms to defined identity management profiles through its use of standard, open protocols for authentication and identity. No formal FICAM-compliant or federated identity profile is adopted as a system-level standard -- the system uses per-service native authentication without a unified identity fabric, which is the source of the partial status.

Implemented protocol conformance: SSH access to all in-boundary hosts conforms to the SSH protocol standard (RFC 4251 through 4256); accepted key types are ED25519 and RSA-4096, aligning with NIST SP 800-207 guidance on key strength. JSON Web Token (JWT) authentication for the Wazuh API and RegScale CE conforms to RFC 7519; JWTs carry role claims (`GlobalAdmin` for RegScale per ADR 0003) used for authorization decisions. HTTPS services (Wazuh Dashboard, Shuffle SOAR, Velociraptor) use TLS 1.2 and TLS 1.3 per RFC 5246 and RFC 8446. No formal identity management profile document listing accepted profiles and their conformance requirements exists, no unified IdP or federation standard has been adopted, and no SP 800-63B Authenticator Assurance Level designations have been formally assigned to each service. These are the gaps contributing to the partial status and are planned remediation items in future ConMon cycles.

#### Implementation Status: partial

______________________________________________________________________
