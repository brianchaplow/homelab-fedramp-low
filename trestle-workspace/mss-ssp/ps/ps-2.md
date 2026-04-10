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
  ps-02_odp:
    alt-identifier: ps-2_prm_1
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ps-02
---

# ps-2 - \[Personnel Security\] Position Risk Designation

## Control Statement

- \[a.\] Assign a risk designation to all organizational positions;

- \[b.\] Establish screening criteria for individuals filling those positions; and

- \[c.\] Review and update position risk designations [frequency].

## Control Assessment Objective

- \[PS-02a.\] a risk designation is assigned to all organizational positions;

- \[PS-02b.\] screening criteria are established for individuals filling organizational positions;

- \[PS-02c.\] position risk designations are reviewed and updated [frequency].

## Control guidance

Position risk designations reflect Office of Personnel Management (OPM) policy and guidance. Proper position designation is the foundation of an effective and consistent suitability and personnel security program. The Position Designation System (PDS) assesses the duties and responsibilities of a position to determine the degree of potential damage to the efficiency or integrity of the service due to misconduct of an incumbent of a position and establishes the risk level of that position. The PDS assessment also determines if the duties and responsibilities of the position present the potential for position incumbents to bring about a material adverse effect on national security and the degree of that potential effect, which establishes the sensitivity level of a position. The results of the assessment determine what level of investigation is conducted for a position. Risk designations can guide and inform the types of authorizations that individuals receive when accessing organizational information and information systems. Position screening criteria include explicit information security role appointment requirements. Parts 1400 and 731 of Title 5, Code of Federal Regulations, establish the requirements for organizations to evaluate relevant covered positions for a position sensitivity and position risk designation commensurate with the duties and responsibilities of those positions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Not applicable. MSS is a single-operator personal system; there are no organizational positions to designate, no OPM Position Designation System model to apply, and no screening criteria to establish, because Brian Chaplow is the sole operator holding all roles simultaneously with no employer-employee relationship in scope.

#### Implementation Status: not-applicable

______________________________________________________________________
