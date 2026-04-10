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
  ia-05.01_odp.01:
    alt-identifier: ia-5.1_prm_1
    profile-values:
      - annually or when a compromise is suspected
    profile-param-value-origin: organization
  ia-05.01_odp.02:
    alt-identifier: ia-5.1_prm_2
    profile-values:
      - minimum 12 characters; must not appear in known-breach wordlists; stored as bcrypt or argon2 hash; no complexity character-class requirements beyond length
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ia-05.01
---

# ia-5.1 - \[Identification and Authentication\] Password-based Authentication

## Control Statement

For password-based authentication:

- \[(a)\] Maintain a list of commonly-used, expected, or compromised passwords and update the list [frequency] and when organizational passwords are suspected to have been compromised directly or indirectly;

- \[(b)\] Verify, when users create or update passwords, that the passwords are not found on the list of commonly-used, expected, or compromised passwords in IA-5(1)(a);

- \[(c)\] Transmit passwords only over cryptographically-protected channels;

- \[(d)\] Store passwords using an approved salted key derivation function, preferably using a keyed hash;

- \[(e)\] Require immediate selection of a new password upon account recovery;

- \[(f)\] Allow user selection of long passwords and passphrases, including spaces and all printable characters;

- \[(g)\] Employ automated tools to assist the user in selecting strong password authenticators; and

- \[(h)\] Enforce the following composition and complexity rules: [composition and complexity rules].

## Control Assessment Objective

- \[IA-05(01)(a)\] for password-based authentication, a list of commonly used, expected, or compromised passwords is maintained and updated [frequency] and when organizational passwords are suspected to have been compromised directly or indirectly;

- \[IA-05(01)(b)\] for password-based authentication when passwords are created or updated by users, the passwords are verified not to be found on the list of commonly used, expected, or compromised passwords in IA-05(01)(a);

- \[IA-05(01)(c)\] for password-based authentication, passwords are only transmitted over cryptographically protected channels;

- \[IA-05(01)(d)\] for password-based authentication, passwords are stored using an approved salted key derivation function, preferably using a keyed hash;

- \[IA-05(01)(e)\] for password-based authentication, immediate selection of a new password is required upon account recovery;

- \[IA-05(01)(f)\] for password-based authentication, user selection of long passwords and passphrases is allowed, including spaces and all printable characters;

- \[IA-05(01)(g)\] for password-based authentication, automated tools are employed to assist the user in selecting strong password authenticators;

- \[IA-05(01)(h)\] for password-based authentication, [composition and complexity rules] are enforced.

## Control guidance

Password-based authentication applies to passwords regardless of whether they are used in single-factor or multi-factor authentication. Long passwords or passphrases are preferable over shorter passwords. Enforced composition rules provide marginal security benefits while decreasing usability. However, organizations may choose to establish certain rules for password generation (e.g., minimum character length for long passwords) under certain circumstances and can enforce this requirement in IA-5(1)(h). Account recovery can occur, for example, in situations when a password is forgotten. Cryptographically protected passwords include salted one-way cryptographic hashes of passwords. The list of commonly used, compromised, or expected passwords includes passwords obtained from previous breach corpuses, dictionary words, and repetitive or sequential characters. The list includes context-specific words, such as the name of the service, username, and derivatives thereof.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service enforces password-based authentication strength through multiple layers, though the system favors key-based authentication wherever possible to reduce reliance on passwords entirely. For SSH access to every in-boundary host (brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, regscale), password authentication is disabled in `sshd_config`; only key-based authentication is accepted. For service-level authentication (Wazuh dashboard, Shuffle, OpenCTI, TheHive, RegScale, DefectDojo), passwords are stored exclusively in `/c/Projects/.env` (gitignored) on PITBOSS and are rotated when operational events require it.

Password complexity and strength requirements for the services that still accept passwords follow each service's default policy. The Wazuh dashboard and indexer use the bundled password policy shipped in the `wazuh-docker/single-node` stack; Shuffle and TheHive enforce their own minimums. No passwords are stored in plaintext in any committed file -- the `.env` convention means secret rotation is a single-file edit followed by service restart, and every code file and documentation artifact references secrets by env-var name (see parent CLAUDE.md "Credentials" section conventions).

#### Implementation Status: implemented

______________________________________________________________________
