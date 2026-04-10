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
  ia-05_odp.01:
    alt-identifier: ia-5_prm_1
    profile-values:
      - "SSH keys: rotate on suspected compromise or personnel change. Service passwords: rotate on operational events (rebuild, suspected compromise). No calendar interval enforced."
    profile-param-value-origin: organization
  ia-05_odp.02:
    alt-identifier: ia-5_prm_2
    profile-values:
      - Suspected compromise; service rebuild or credential reset; personnel change; security incident
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ia-05
---

# ia-5 - \[Identification and Authentication\] Authenticator Management

## Control Statement

Manage system authenticators by:

- \[a.\] Verifying, as part of the initial authenticator distribution, the identity of the individual, group, role, service, or device receiving the authenticator;

- \[b.\] Establishing initial authenticator content for any authenticators issued by the organization;

- \[c.\] Ensuring that authenticators have sufficient strength of mechanism for their intended use;

- \[d.\] Establishing and implementing administrative procedures for initial authenticator distribution, for lost or compromised or damaged authenticators, and for revoking authenticators;

- \[e.\] Changing default authenticators prior to first use;

- \[f.\] Changing or refreshing authenticators [time period by authenticator type] or when [events] occur;

- \[g.\] Protecting authenticator content from unauthorized disclosure and modification;

- \[h.\] Requiring individuals to take, and having devices implement, specific controls to protect authenticators; and

- \[i.\] Changing authenticators for group or role accounts when membership to those accounts changes.

## Control Assessment Objective

- \[IA-05a.\] system authenticators are managed through the verification of the identity of the individual, group, role, service, or device receiving the authenticator as part of the initial authenticator distribution;

- \[IA-05b.\] system authenticators are managed through the establishment of initial authenticator content for any authenticators issued by the organization;

- \[IA-05c.\] system authenticators are managed to ensure that authenticators have sufficient strength of mechanism for their intended use;

- \[IA-05d.\] system authenticators are managed through the establishment and implementation of administrative procedures for initial authenticator distribution; lost, compromised, or damaged authenticators; and the revocation of authenticators;

- \[IA-05e.\] system authenticators are managed through the change of default authenticators prior to first use;

- \[IA-05f.\] system authenticators are managed through the change or refreshment of authenticators [time period by authenticator type] or when [events] occur;

- \[IA-05g.\] system authenticators are managed through the protection of authenticator content from unauthorized disclosure and modification;

- \[IA-05h.\]

  - \[IA-05h.[01]\] system authenticators are managed through the requirement for individuals to take specific controls to protect authenticators;
  - \[IA-05h.[02]\] system authenticators are managed through the requirement for devices to implement specific controls to protect authenticators;

- \[IA-05i.\] system authenticators are managed through the change of authenticators for group or role accounts when membership to those accounts changes.

## Control guidance

Authenticators include passwords, cryptographic devices, biometrics, certificates, one-time password devices, and ID badges. Device authenticators include certificates and passwords. Initial authenticator content is the actual content of the authenticator (e.g., the initial password). In contrast, the requirements for authenticator content contain specific criteria or characteristics (e.g., minimum password length). Developers may deliver system components with factory default authentication credentials (i.e., passwords) to allow for initial installation and configuration. Default authentication credentials are often well known, easily discoverable, and present a significant risk. The requirement to protect individual authenticators may be implemented via control [PL-4](#pl-4) or [PS-6](#ps-6) for authenticators in the possession of individuals and by controls [AC-3](#ac-3), [AC-6](#ac-6) , and [SC-28](#sc-28) for authenticators stored in organizational systems, including passwords stored in hashed or encrypted formats or files containing encrypted or hashed passwords accessible with administrator privileges.

Systems support authenticator management by organization-defined settings and restrictions for various authenticator characteristics (e.g., minimum password length, validation time window for time synchronous one-time tokens, and number of allowed rejections during the verification stage of biometric authentication). Actions can be taken to safeguard individual authenticators, including maintaining possession of authenticators, not sharing authenticators with others, and immediately reporting lost, stolen, or compromised authenticators. Authenticator management includes issuing and revoking authenticators for temporary access when no longer needed.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Authenticator management for the Managed SOC Service covers the full lifecycle of SSH keys and service passwords, with some documented gaps.

SSH key pairs are generated by the operator on the PITBOSS workstation using ED25519 or RSA-4096, both of which provide sufficient cryptographic strength for their intended use. Initial distribution is performed by the operator directly (identity verified implicitly -- single-operator model). No shared private keys are used. Default authenticators are changed before first use on every service: RegScale CE ships with an undocumented default password hash; `deploy/regscale/reset-admin-password.sh` replaces the default with a PBKDF2-HMAC-SHA512 hash (100,000 iterations, 16-byte salt, 32-byte subkey) before the service is placed in use, per ADR 0003. DefectDojo, TheHive, Cortex, and Velociraptor either require first-run admin setup or have no usable default credential; defaults are changed at deployment per ADR 0004 and platform runbooks. All service passwords are stored exclusively in `/c/Projects/.env` (gitignored) on the operator workstation; no credential appears in committed code or documentation artifacts.

Authenticator revocation is manual -- SSH keys are removed from `authorized_keys` and service passwords are changed in the platform on operational events (suspected compromise, service rebuild, or personnel change). No calendar-based rotation schedule is enforced for SSH keys or service passwords; rotation is event-driven. No automated tool tracks authenticator age. The absence of a formal rotation schedule and automated revocation mechanism are the documented gaps that contribute to the partial status.

#### Implementation Status: partial

______________________________________________________________________
