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
  pe-08_odp.01:
    alt-identifier: pe-8_prm_1
    profile-values:
      - not-applicable -- single-operator personal system; no visitors admitted to facility
    profile-param-value-origin: organization
  pe-08_odp.02:
    alt-identifier: pe-8_prm_2
    profile-values:
      - not-applicable -- single-operator personal system; no visitor access records generated
    profile-param-value-origin: organization
  pe-08_odp.03:
    alt-identifier: pe-8_prm_3
    profile-values:
      - not-applicable -- single-operator personal system; no visitor access records generated
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pe-08
---

# pe-8 - \[Physical and Environmental Protection\] Visitor Access Records

## Control Statement

- \[a.\] Maintain visitor access records to the facility where the system resides for [time period];

- \[b.\] Review visitor access records [frequency] ; and

- \[c.\] Report anomalies in visitor access records to [personnel].

## Control Assessment Objective

- \[PE-08a.\] visitor access records for the facility where the system resides are maintained for [time period];

- \[PE-08b.\] visitor access records are reviewed [frequency];

- \[PE-08c.\] visitor access records anomalies are reported to [personnel].

## Control guidance

Visitor access records include the names and organizations of individuals visiting, visitor signatures, forms of identification, dates of access, entry and departure times, purpose of visits, and the names and organizations of individuals visited. Access record reviews determine if access authorizations are current and are still required to support organizational mission and business functions. Access records are not required for publicly accessible areas.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

This control is not applicable. The Managed SOC Service operates in a private residence with Brian Chaplow as the sole operator and sole occupant of the equipment room. No visitors are admitted to the facility where the system resides. Because no visitor access occurs, visitor access records are not generated, not maintained, and not reviewed -- there is no gap to document, only an absence of applicability. This N/A determination is consistent with PE-2 (access authorizations: single-entry list) and PE-3 (physical access control: no visitor escort procedure because no visitors are admitted). The whole-project design §PE honest-gaps row acknowledges the residential single-operator context that underlies all PE N/A determinations.

#### Implementation Status: not-applicable

______________________________________________________________________
