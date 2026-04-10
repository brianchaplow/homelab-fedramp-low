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
  cp-03_odp.01:
    alt-identifier: cp-3_prm_1
    profile-values:
      - within 30 days of assuming contingency responsibility
    profile-param-value-origin: organization
  cp-03_odp.02:
    alt-identifier: cp-3_prm_2
    profile-values:
      - annually
    profile-param-value-origin: organization
  cp-03_odp.03:
    alt-identifier: cp-3_prm_3
    profile-values:
      - annually
    profile-param-value-origin: organization
  cp-03_odp.04:
    alt-identifier: cp-3_prm_4
    profile-values:
      - system change affecting backup or recovery procedures, contingency activation, or audit finding
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cp-03
---

# cp-3 - \[Contingency Planning\] Contingency Training

## Control Statement

- \[a.\] Provide contingency training to system users consistent with assigned roles and responsibilities:

  - \[1.\] Within [time period] of assuming a contingency role or responsibility;
  - \[2.\] When required by system changes; and
  - \[3.\] [frequency] thereafter; and

- \[b.\] Review and update contingency training content [frequency] and following [events].

## Control Assessment Objective

- \[CP-03a.\]

  - \[CP-03a.01\] contingency training is provided to system users consistent with assigned roles and responsibilities within [time period] of assuming a contingency role or responsibility;
  - \[CP-03a.02\] contingency training is provided to system users consistent with assigned roles and responsibilities when required by system changes;
  - \[CP-03a.03\] contingency training is provided to system users consistent with assigned roles and responsibilities [frequency] thereafter;

- \[CP-03b.\]

  - \[CP-03b.[01]\] the contingency plan training content is reviewed and updated [frequency];
  - \[CP-03b.[02]\] the contingency plan training content is reviewed and updated following [events].

## Control guidance

Contingency training provided by organizations is linked to the assigned roles and responsibilities of organizational personnel to ensure that the appropriate content and level of detail is included in such training. For example, some individuals may only need to know when and where to report for duty during contingency operations and if normal duties are affected; system administrators may require additional training on how to establish systems at alternate processing and storage sites; and organizational officials may receive more specific training on how to conduct mission-essential functions in designated off-site locations and how to establish communications with other governmental entities for purposes of coordination on contingency-related activities. Training for contingency roles or responsibilities reflects the specific continuity requirements in the contingency plan. Events that may precipitate an update to contingency training content include, but are not limited to, contingency plan testing or an actual contingency (lessons learned), assessment or audit findings, security incidents or breaches, or changes in laws, executive orders, directives, regulations, policies, standards, and guidelines. At the discretion of the organization, participation in a contingency plan test or exercise, including lessons learned sessions subsequent to the test or exercise, may satisfy contingency plan training requirements.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

No formal contingency training program, curriculum, or training records exist for this system. The system is a single-operator homelab in which the system owner (Brian Chaplow) both designs and executes all contingency procedures, collapsing the typical trainer/trainee distinction. Contingency familiarity is maintained through direct authorship and hands-on operation of the recovery procedures documented in `runbooks/restore-from-pbs.md` and the backup monitoring tripwire in `runbooks/monthly-conmon.md`. These documents function as self-paced operator reference material, but they do not constitute training delivery in the CP-3 sense -- no formal acknowledgment, delivery record, or training completion artifact exists.

The planned training approach treats the annual review of contingency runbooks (restore-from-pbs.md, monthly-conmon.md) and any executed restore drills (per `runbooks/restore-from-pbs.md` §"First-time restore drill") as the training event for the sole contingency role. Training content will be reviewed annually and following any system change affecting backup or recovery procedures, any contingency activation, or any audit finding. Initial training on assumption of the contingency role is defined as within 30 days.

This control is rated `planned` because no training delivery record or acknowledgment artifact exists; the runbook review and restore drill are the planned mechanism to formally satisfy CP-3.

#### Implementation Status: planned

______________________________________________________________________
