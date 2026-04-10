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
  at-04_odp:
    alt-identifier: at-4_prm_1
    profile-values:
      - indefinitely while the GitHub repository is active -- git history is immutable and retained at github.com/brianchaplow/homelab-fedramp-low
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: at-04
---

# at-4 - \[Awareness and Training\] Training Records

## Control Statement

- \[a.\] Document and monitor information security and privacy training activities, including security and privacy awareness training and specific role-based security and privacy training; and

- \[b.\] Retain individual training records for [time period].

## Control Assessment Objective

- \[AT-04a.\]

  - \[AT-04a.[01]\] information security and privacy training activities, including security and privacy awareness training and specific role-based security and privacy training, are documented;
  - \[AT-04a.[02]\] information security and privacy training activities, including security and privacy awareness training and specific role-based security and privacy training, are monitored;

- \[AT-04b.\] individual training records are retained for [time period].

## Control guidance

Documentation for specialized training may be maintained by individual supervisors at the discretion of the organization. The National Archives and Records Administration provides guidance on records retention for federal agencies.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The `homelab-fedramp-low` git repository on GitHub (`github.com/brianchaplow/homelab-fedramp-low`) serves as the training record for this system. Every ADR filed documents a learning event: a deviation discovered, a technology evaluated, a decision made under real operational conditions. The git commit log provides immutable, timestamped evidence of when each learning event occurred and what decision followed. Eight ADRs filed between 2026-04-08 and 2026-04-09 (ADRs 0001--0008) and the `C:/Projects/CLAUDE.md` phase-completion ledger (Phases 1--14, with dates) constitute the operator's training activity record. Retention is indefinite while the repository remains active; no data-retention cutoff is imposed in a personal homelab context.

The gap is the absence of a dedicated training-monitoring mechanism that would alert on overdue training. The control requires "document AND monitor"; git history satisfies "document" but monitoring of training currency is manual and not automated.

#### Implementation Status: partial

______________________________________________________________________
