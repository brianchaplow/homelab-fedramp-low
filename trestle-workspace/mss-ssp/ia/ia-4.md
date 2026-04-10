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
  ia-04_odp.01:
    alt-identifier: ia-4_prm_1
    profile-values:
      - System owner (Brian Chaplow)
    profile-param-value-origin: organization
  ia-04_odp.02:
    alt-identifier: ia-4_prm_2
    profile-values:
      - Indefinite -- retired identifiers are never reassigned within this system boundary
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ia-04
---

# ia-4 - \[Identification and Authentication\] Identifier Management

## Control Statement

Manage system identifiers by:

- \[a.\] Receiving authorization from [personnel or roles] to assign an individual, group, role, service, or device identifier;

- \[b.\] Selecting an identifier that identifies an individual, group, role, service, or device;

- \[c.\] Assigning the identifier to the intended individual, group, role, service, or device; and

- \[d.\] Preventing reuse of identifiers for [time period].

## Control Assessment Objective

- \[IA-04a.\] system identifiers are managed by receiving authorization from [personnel or roles] to assign to an individual, group, role, or device identifier;

- \[IA-04b.\] system identifiers are managed by selecting an identifier that identifies an individual, group, role, service, or device;

- \[IA-04c.\] system identifiers are managed by assigning the identifier to the intended individual, group, role, service, or device;

- \[IA-04d.\] system identifiers are managed by preventing reuse of identifiers for [time period].

## Control guidance

Common device identifiers include Media Access Control (MAC) addresses, Internet Protocol (IP) addresses, or device-unique token identifiers. The management of individual identifiers is not applicable to shared system accounts. Typically, individual identifiers are the usernames of the system accounts assigned to those individuals. In such instances, the account management activities of [AC-2](#ac-2) use account names provided by [IA-4](#ia-4) . Identifier management also addresses individual identifiers not necessarily associated with system accounts. Preventing the reuse of identifiers implies preventing the assignment of previously used individual, group, role, service, or device identifiers to different individuals, groups, roles, services, or devices.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Identifier management for the Managed SOC Service is governed by operator convention and documented in `CLAUDE.md` and `inventory/overlay.yaml`. The system owner (Brian Chaplow) is the sole authority for assigning identifiers to any subject within the boundary.

For host OS accounts, each in-boundary host carries a named OS account -- `bchaplow` on brisket and haccp, `butcher` on sear, `root` on smoker (key-only), and similarly named accounts on dojo and regscale. Account creation requires an explicit operator decision; the account name identifies the role and is never reassigned. Wazuh agent identifiers are assigned sequentially by the Wazuh Manager at enrollment time. IDs 001 through 017 are in use across 15 active agents plus the OPNsense syslog source. Agent IDs are never reassigned to different hosts after enrollment -- a policy documented in ADR 0006 Deviation 6, which also establishes that agent names (stable host names: `brisket`, `haccp`, `smokehouse`, `dojo`, `regscale`, etc.) are the preferred stable identifiers in pipeline code and `inventory/overlay.yaml`. Service account identifiers (Wazuh `admin` and `wazuh-wui`, Shuffle `admin`, OpenCTI `admin@opencti.local`, TheHive `admin@thehive.local` and `socadmin@thehive.local`, Cortex `admin` and `socadmin@SOC`, Velociraptor `admin`, DefectDojo `admin`, RegScale `admin`) are tied to a defined role and are retired -- not reassigned -- when the associated service is decommissioned. DefectDojo product IDs (1 through 5) were assigned at seed time and are not reused. Identifier reuse is prevented indefinitely -- no previously used identifier is assigned to a different subject within the system boundary.

#### Implementation Status: implemented

______________________________________________________________________
