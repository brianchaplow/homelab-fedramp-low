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
  cp-4_prm_2:
    aggregates:
      - cp-04_odp.02
      - cp-04_odp.03
    profile-param-value-origin: organization
  cp-04_odp.01:
    alt-identifier: cp-4_prm_1
    profile-values:
      - annually
    profile-param-value-origin: organization
  cp-04_odp.02:
    profile-values:
      - tabletop walkthrough and restore drill (qmrestore from PBS snapshot to alternate VMID, verified by smoke check)
    profile-param-value-origin: organization
  cp-04_odp.03:
    profile-values:
      - System Owner (Brian Chaplow)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cp-04
---

# cp-4 - \[Contingency Planning\] Contingency Plan Testing

## Control Statement

- \[a.\] Test the contingency plan for the system [frequency] using the following tests to determine the effectiveness of the plan and the readiness to execute the plan: [organization-defined tests].

- \[b.\] Review the contingency plan test results; and

- \[c.\] Initiate corrective actions, if needed.

## Control Assessment Objective

- \[CP-04a.\]

  - \[CP-04a.[01]\] the contingency plan for the system is tested [frequency];
  - \[CP-04a.[02]\] [tests] are used to determine the effectiveness of the plan;
  - \[CP-04a.[03]\] [tests] are used to determine the readiness to execute the plan;

- \[CP-04b.\] the contingency plan test results are reviewed;

- \[CP-04c.\] corrective actions are initiated, if needed.

## Control guidance

Methods for testing contingency plans to determine the effectiveness of the plans and identify potential weaknesses include checklists, walk-through and tabletop exercises, simulations (parallel or full interrupt), and comprehensive exercises. Organizations conduct testing based on the requirements in contingency plans and include a determination of the effects on organizational operations, assets, and individuals due to contingency operations. Organizations have flexibility and discretion in the breadth, depth, and timelines of corrective actions.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

No formal contingency plan test has been conducted against documented test criteria. The nearest operational analog is documented in ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`): on 2026-04-08, `vzdump` was run against dojo (VMID 201) as a chain-verification step after the NFS remount fix, producing a confirmed snapshot at `vm/201/2026-04-08T17:26:22Z` in 11m11s. This was an operational verification, not a scheduled contingency plan test with predefined success criteria, so it does not satisfy CP-4 on its own.

The planned test method is a tabletop walkthrough combined with a restore drill: `qmrestore` is executed from a current PBS snapshot to an alternate VMID (to avoid disrupting production) and the restored VM is validated by the automated smoke check scripts (`./pipelines.sh smoke-dojo`, `./pipelines.sh smoke-regscale`). The first restore drill is specified in `runbooks/restore-from-pbs.md` §"First-time restore drill" and is owed within 7 days of Plan 1 completion (by 2026-04-15). Test results will be documented in a new ADR (`docs/adr/NNNN-restore-drill.md`). Tests will be repeated annually thereafter. Corrective actions will be captured as ADRs and tracked in the monthly ConMon cycle.

This control is rated `planned` because no annual test record exists; the scheduled restore drill is the first planned test event.

#### Implementation Status: planned

______________________________________________________________________
