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
  ca-06_odp:
    alt-identifier: ca-6_prm_1
    profile-values:
      - annually; following significant security change
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-06
---

# ca-6 - \[Assessment, Authorization, and Monitoring\] Authorization

## Control Statement

- \[a.\] Assign a senior official as the authorizing official for the system;

- \[b.\] Assign a senior official as the authorizing official for common controls available for inheritance by organizational systems;

- \[c.\] Ensure that the authorizing official for the system, before commencing operations:

  - \[1.\] Accepts the use of common controls inherited by the system; and
  - \[2.\] Authorizes the system to operate;

- \[d.\] Ensure that the authorizing official for common controls authorizes the use of those controls for inheritance by organizational systems;

- \[e.\] Update the authorizations [frequency].

## Control Assessment Objective

- \[CA-06a.\] a senior official is assigned as the authorizing official for the system;

- \[CA-06b.\] a senior official is assigned as the authorizing official for common controls available for inheritance by organizational systems;

- \[CA-06c.\]

  - \[CA-06c.01\] before commencing operations, the authorizing official for the system accepts the use of common controls inherited by the system;
  - \[CA-06c.02\] before commencing operations, the authorizing official for the system authorizes the system to operate;

- \[CA-06d.\] the authorizing official for common controls authorizes the use of those controls for inheritance by organizational systems;

- \[CA-06e.\] the authorizations are updated [frequency].

## Control guidance

Authorizations are official management decisions by senior officials to authorize operation of systems, authorize the use of common controls for inheritance by organizational systems, and explicitly accept the risk to organizational operations and assets, individuals, other organizations, and the Nation based on the implementation of agreed-upon controls. Authorizing officials provide budgetary oversight for organizational systems and common controls or assume responsibility for the mission and business functions supported by those systems or common controls. The authorization process is a federal responsibility, and therefore, authorizing officials must be federal employees. Authorizing officials are both responsible and accountable for security and privacy risks associated with the operation and use of organizational systems. Nonfederal organizations may have similar processes to authorize systems and senior officials that assume the authorization role and associated responsibilities.

Authorizing officials issue ongoing authorizations of systems based on evidence produced from implemented continuous monitoring programs. Robust continuous monitoring programs reduce the need for separate reauthorization processes. Through the employment of comprehensive continuous monitoring processes, the information contained in authorization packages (i.e., security and privacy plans, assessment reports, and plans of action and milestones) is updated on an ongoing basis. This provides authorizing officials, common control providers, and system owners with an up-to-date status of the security and privacy posture of their systems, controls, and operating environments. To reduce the cost of reauthorization, authorizing officials can leverage the results of continuous monitoring processes to the maximum extent possible as the basis for rendering reauthorization decisions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Brian Chaplow (system owner and sole operator) is assigned as the authorizing official (AO) for the MSS homelab system. This is the maximum level of independence feasible for a single-person portfolio system; the AO role and system owner role are held by the same individual, which is the honest state for this scope.

This SSP (`oscal/ssp.json`, assembled from `trestle-workspace/mss-ssp/`) constitutes the authorization package. It documents the system boundary (7 in-boundary components per `oscal/component-definition.json`), the complete FedRAMP Rev 5 Low control implementation, and the POA&M (`poam/POAM-2026-04.xlsx`, 8,473 items). Plan 3 SSP authoring is the authorization event -- a completed SSP with realistic Tier-1-grade implementation prose, live-verified CA-7 ConMon pipeline, and passing test suite (136 tests) represents the ATO artifact for portfolio purposes.

ADR 0009 (planned, to be filed at Plan 3 Gate 5) will serve as the formal self-authorization decision record. ADR 0008 §"Authoritative Plan 3 artifacts" explicitly identifies ADR 0009 as the "Plan 3 completion" ADR filed at Gate 5; that ADR will capture the AO's acceptance of risk and authorization to operate. No common controls are inherited from a shared services provider; this system is standalone and all controls are system-specific. Authorization updates are performed annually and following any significant security change, leveraging the monthly ConMon cycle results as the evidentiary basis.

A real FedRAMP authorization requires a federally-delegated AO and a FedRAMP-authorized 3PAO. This homelab treats the system owner as AO and the automated test suite plus SSP as the equivalent of a 3PAO assessment package, per the explicit portfolio scope documented in `README.md`. ADR 0009 has not been filed (pending Plan 3 Gate 5); the authorization event has not yet formally occurred.

#### Implementation Status: planned

______________________________________________________________________
