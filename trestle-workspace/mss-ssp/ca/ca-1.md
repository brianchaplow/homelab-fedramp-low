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
  ca-1_prm_1:
    aggregates:
      - ca-01_odp.01
      - ca-01_odp.02
    profile-param-value-origin: organization
  ca-01_odp.01:
    profile-values:
      - system owner (Brian Chaplow)
    profile-param-value-origin: organization
  ca-01_odp.02:
    profile-values:
      - system owner (Brian Chaplow)
    profile-param-value-origin: organization
  ca-01_odp.03:
    alt-identifier: ca-1_prm_2
    profile-values:
      - system owner (Brian Chaplow)
    profile-param-value-origin: organization
  ca-01_odp.04:
    alt-identifier: ca-1_prm_3
    profile-values:
      - annually
    profile-param-value-origin: organization
  ca-01_odp.05:
    alt-identifier: ca-1_prm_4
    profile-values:
      - significant system change; security incident; regulatory update
    profile-param-value-origin: organization
  ca-01_odp.06:
    alt-identifier: ca-1_prm_5
    profile-values:
      - annually
    profile-param-value-origin: organization
  ca-01_odp.07:
    alt-identifier: ca-1_prm_6
    profile-values:
      - significant system change; security incident
    profile-param-value-origin: organization
  ca-01_odp.08:
    alt-identifier: ca-1_prm_7
    profile-values:
      - significant system change; security incident
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-01
---

# ca-1 - \[Assessment, Authorization, and Monitoring\] Policy and Procedures

## Control Statement

- \[a.\] Develop, document, and disseminate to [organization-defined personnel or roles]:

  - \[1.\] [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy that:

    - \[(a)\] Addresses purpose, scope, roles, responsibilities, management commitment, coordination among organizational entities, and compliance; and
    - \[(b)\] Is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines; and

  - \[2.\] Procedures to facilitate the implementation of the assessment, authorization, and monitoring policy and the associated assessment, authorization, and monitoring controls;

- \[b.\] Designate an [official] to manage the development, documentation, and dissemination of the assessment, authorization, and monitoring policy and procedures; and

- \[c.\] Review and update the current assessment, authorization, and monitoring:

  - \[1.\] Policy [frequency] and following [events] ; and
  - \[2.\] Procedures [frequency] and following [events].

## Control Assessment Objective

- \[CA-01a.\]

  - \[CA-01a.[01]\] an assessment, authorization, and monitoring policy is developed and documented;
  - \[CA-01a.[02]\] the assessment, authorization, and monitoring policy is disseminated to [personnel or roles];
  - \[CA-01a.[03]\] assessment, authorization, and monitoring procedures to facilitate the implementation of the assessment, authorization, and monitoring policy and associated assessment, authorization, and monitoring controls are developed and documented;
  - \[CA-01a.[04]\] the assessment, authorization, and monitoring procedures are disseminated to [personnel or roles];
  - \[CA-01a.01\]

    - \[CA-01a.01(a)\]

      - \[CA-01a.01(a)[01]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses purpose;
      - \[CA-01a.01(a)[02]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses scope;
      - \[CA-01a.01(a)[03]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses roles;
      - \[CA-01a.01(a)[04]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses responsibilities;
      - \[CA-01a.01(a)[05]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses management commitment;
      - \[CA-01a.01(a)[06]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses coordination among organizational entities;
      - \[CA-01a.01(a)[07]\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy addresses compliance;

    - \[CA-01a.01(b)\] the [Selection (one or more): organization-level; mission/business process-level; system-level] assessment, authorization, and monitoring policy is consistent with applicable laws, executive orders, directives, regulations, policies, standards, and guidelines;

- \[CA-01b.\] the [official] is designated to manage the development, documentation, and dissemination of the assessment, authorization, and monitoring policy and procedures;

- \[CA-01c.\]

  - \[CA-01c.01\]

    - \[CA-01c.01[01]\] the current assessment, authorization, and monitoring policy is reviewed and updated [frequency];
    - \[CA-01c.01[02]\] the current assessment, authorization, and monitoring policy is reviewed and updated following [events];

  - \[CA-01c.02\]

    - \[CA-01c.02[01]\] the current assessment, authorization, and monitoring procedures are reviewed and updated [frequency];
    - \[CA-01c.02[02]\] the current assessment, authorization, and monitoring procedures are reviewed and updated following [events].

## Control guidance

Assessment, authorization, and monitoring policy and procedures address the controls in the CA family that are implemented within systems and organizations. The risk management strategy is an important factor in establishing such policies and procedures. Policies and procedures contribute to security and privacy assurance. Therefore, it is important that security and privacy programs collaborate on the development of assessment, authorization, and monitoring policy and procedures. Security and privacy program policies and procedures at the organization level are preferable, in general, and may obviate the need for mission- or system-specific policies and procedures. The policy can be included as part of the general security and privacy policy or be represented by multiple policies that reflect the complex nature of organizations. Procedures can be established for security and privacy programs, for mission or business processes, and for systems, if needed. Procedures describe how the policies or controls are implemented and can be directed at the individual or role that is the object of the procedure. Procedures can be documented in system security and privacy plans or in one or more separate documents. Events that may precipitate an update to assessment, authorization, and monitoring policy and procedures include assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines. Simply restating controls does not constitute an organizational policy or procedure.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

This SSP (`oscal/ssp.json`, assembled from `trestle-workspace/mss-ssp/`) serves as the system-level assessment, authorization, and monitoring policy document for the Managed SOC Service (MSS) homelab boundary. It addresses purpose (FedRAMP Low ConMon portfolio demonstrating continuous monitoring capability), scope (7 in-boundary components per `oscal/component-definition.json`: brisket, haccp, smokehouse, dojo, regscale, OPNsense, MokerLink), roles (system owner = Brian Chaplow), responsibilities (sole operator), and compliance (FedRAMP Rev 5 Low baseline, NIST SP 800-53 Rev 5). The SSP is disseminated to the system owner and is the authoritative policy artifact for the portfolio.

The ConMon procedures are documented in `runbooks/monthly-conmon.md`, which describes the monthly `./pipelines.sh conmon` cycle: ingest-findings from Wazuh, build OSCAL POA&M, render IIW and POA&M xlsx, and report results. Plan 3 SSP authoring constitutes the initial documentation event; annual review cadence starts from Plan 3 completion.

The ADR series (`docs/adr/0001` through `docs/adr/0008`) provides the change-event record: each ADR is filed at a significant system change or deviation discovery event, which serves as the "following events" trigger for policy and procedure review. `docs/adr/0008-plan-3-pre-execution-realignment.md` documents the pre-execution critical read (2026-04-09) as the first formal policy review event. Annual review is the established cadence going forward; the next review will occur no later than 2027-04-09 or following the next significant system change, whichever comes first.

CA-1 is partially implemented: SSP prose and runbook are authored during Plan 3; formal calendar-scheduled annual review has not yet been established for future cycles. The policy content is complete; the scheduling mechanism for future reviews is the named gap.

#### Implementation Status: partial

______________________________________________________________________
