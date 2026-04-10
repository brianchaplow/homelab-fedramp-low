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
  mp-2_prm_1:
    aggregates:
      - mp-02_odp.01
      - mp-02_odp.03
    profile-param-value-origin: organization
  mp-2_prm_2:
    aggregates:
      - mp-02_odp.02
      - mp-02_odp.04
    profile-param-value-origin: organization
  mp-02_odp.01:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  mp-02_odp.02:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  mp-02_odp.03:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
  mp-02_odp.04:
    profile-values:
      - not-applicable - single-operator personal system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: mp-02
---

# mp-2 - \[Media Protection\] Media Access

## Control Statement

Restrict access to [organization-defined types of digital and/or non-digital media] to [organization-defined personnel or roles].

## Control Assessment Objective

- \[MP-02[01]\] access to [types of digital media] is restricted to [personnel or roles];

- \[MP-02[02]\] access to [types of non-digital media] is restricted to [personnel or roles].

## Control guidance

System media includes digital and non-digital media. Digital media includes flash drives, diskettes, magnetic tapes, external or removable hard disk drives (e.g., solid state, magnetic), compact discs, and digital versatile discs. Non-digital media includes paper and microfilm. Denying access to patient medical records in a community hospital unless the individuals seeking access to such records are authorized healthcare providers is an example of restricting access to non-digital media. Limiting access to the design specifications stored on compact discs in the media library to individuals on the system development team is an example of restricting access to digital media.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

MP-2 is not applicable to the MSS. The boundary contains no removable digital media (no USB flash drives, external hard drives, optical discs, or diskettes) and no non-digital media (no paper records or microfilm) participating in any in-boundary data flow. All storage is permanently installed: brisket and haccp use internally mounted NVMe drives (haccp boot drive WD SN720 2TB on nvme1n1; PCAP drive Samsung 990 EVO Plus 2TB on nvme0n1); smokehouse uses internal SATA drives as the NFS backup target. The 2026-04-07 rack consolidation involved three drive swaps performed by the sole operator as one-time hardware installations -- after installation all drives became permanent internal storage. Because no removable or non-digital media exists in the boundary, the access restriction requirement of MP-2 has no subjects to apply to.

#### Implementation Status: not-applicable

______________________________________________________________________
