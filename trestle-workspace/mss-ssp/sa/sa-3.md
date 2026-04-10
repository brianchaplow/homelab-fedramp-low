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
  sa-03_odp:
    alt-identifier: sa-3_prm_1
    profile-values:
      - GSD phased lifecycle (Plan 1 through Plan 4) with pre-execution realignment ADRs as security gate records, per-phase design specs incorporating security requirements, and post-phase completion ADRs as done-criteria verification
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sa-03
---

# sa-3 - \[System and Services Acquisition\] System Development Life Cycle

## Control Statement

- \[a.\] Acquire, develop, and manage the system using [system-development life cycle] that incorporates information security and privacy considerations;

- \[b.\] Define and document information security and privacy roles and responsibilities throughout the system development life cycle;

- \[c.\] Identify individuals having information security and privacy roles and responsibilities; and

- \[d.\] Integrate the organizational information security and privacy risk management process into system development life cycle activities.

## Control Assessment Objective

- \[SA-03a.\]

  - \[SA-03a.[01]\] the system is acquired, developed, and managed using [system-development life cycle] that incorporates information security considerations;
  - \[SA-03a.[02]\] the system is acquired, developed, and managed using [system-development life cycle] that incorporates privacy considerations;

- \[SA-03b.\]

  - \[SA-03b.[01]\] information security roles and responsibilities are defined and documented throughout the system development life cycle;
  - \[SA-03b.[02]\] privacy roles and responsibilities are defined and documented throughout the system development life cycle;

- \[SA-03c.\]

  - \[SA-03c.[01]\] individuals with information security roles and responsibilities are identified;
  - \[SA-03c.[02]\] individuals with privacy roles and responsibilities are identified;

- \[SA-03d.\]

  - \[SA-03d.[01]\] organizational information security risk management processes are integrated into system development life cycle activities;
  - \[SA-03d.[02]\] organizational privacy risk management processes are integrated into system development life cycle activities.

## Control guidance

A system development life cycle process provides the foundation for the successful development, implementation, and operation of organizational systems. The integration of security and privacy considerations early in the system development life cycle is a foundational principle of systems security engineering and privacy engineering. To apply the required controls within the system development life cycle requires a basic understanding of information security and privacy, threats, vulnerabilities, adverse impacts, and risk to critical mission and business functions. The security engineering principles in [SA-8](#sa-8) help individuals properly design, code, and test systems and system components. Organizations include qualified personnel (e.g., senior agency information security officers, senior agency officials for privacy, security and privacy architects, and security and privacy engineers) in system development life cycle processes to ensure that established security and privacy requirements are incorporated into organizational systems. Role-based security and privacy training programs can ensure that individuals with key security and privacy roles and responsibilities have the experience, skills, and expertise to conduct assigned system development life cycle activities.

The effective integration of security and privacy requirements into enterprise architecture also helps to ensure that important security and privacy considerations are addressed throughout the system life cycle and that those considerations are directly related to organizational mission and business processes. This process also facilitates the integration of the information security and privacy architectures into the enterprise architecture, consistent with the risk management strategy of the organization. Because the system development life cycle involves multiple organizations, (e.g., external suppliers, developers, integrators, service providers), acquisition and supply chain risk management functions and controls play significant roles in the effective management of the system during the life cycle.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS is acquired, developed, and managed using the GSD (Get Stuff Done) phased lifecycle framework: Plan 1 (infrastructure deployment, ADR 0002), Plan 2 (OSCAL pipelines, ADR 0007), Plan 3 (SSP authoring, ADR 0008/0009), and Plan 4+ (ConMon cycles). Each Plan has a design spec (e.g., `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` §4, Gates 1-5) and an implementation plan that incorporates security and privacy considerations explicitly. Pre-execution realignment ADRs (ADR 0006 for Plan 2, ADR 0008 for Plan 3) document risk identification and mitigation decisions made before each phase executes -- the formal security gate record. Brian Chaplow is the single individual identified as holding all information security and privacy roles (system owner, operator, developer, assessor) as documented in `C:\Projects\CLAUDE.md`. Each phase begins with a Gate 1 regression check (`./pipelines.sh smoke` + pytest suite) that confirms security-relevant infrastructure is healthy before new work starts.

This control is partial because the GSD framework is informal -- no NIST SP 800-64 process was explicitly adopted, role separation beyond the single operator does not exist, and no formal privacy impact assessment process has been documented. The phase/plan/gate structure integrates security at every stage and is the nearest operational equivalent of a formal SDLC for a single-operator system. Cross-reference SA-8 (engineering principles applied during design) and SA-5 (system documentation as SDLC output).

#### Implementation Status: partial

______________________________________________________________________
