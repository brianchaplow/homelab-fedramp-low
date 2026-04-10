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
  at-3_prm_1:
    aggregates:
      - at-03_odp.01
      - at-03_odp.02
    profile-param-value-origin: organization
  at-03_odp.01:
    profile-values:
      - Brian Chaplow -- system owner, ISSO, system administrator, SOC analyst, incident responder, vulnerability manager, assessment coordinator (all roles held by sole operator)
    profile-param-value-origin: organization
  at-03_odp.02:
    profile-values:
      - Brian Chaplow (sole operator)
    profile-param-value-origin: organization
  at-03_odp.03:
    alt-identifier: at-3_prm_2
    profile-values:
      - continuous -- operational homelab activity serves as ongoing role-based training
    profile-param-value-origin: organization
  at-03_odp.04:
    alt-identifier: at-3_prm_3
    profile-values:
      - updated with each new phase completion or ADR filing
    profile-param-value-origin: organization
  at-03_odp.05:
    alt-identifier: at-3_prm_4
    profile-values:
      - new phase, new in-boundary component, security incident requiring new role skill
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: at-03
---

# at-3 - \[Awareness and Training\] Role-based Training

## Control Statement

- \[a.\] Provide role-based security and privacy training to personnel with the following roles and responsibilities: [organization-defined roles and responsibilities]:

  - \[1.\] Before authorizing access to the system, information, or performing assigned duties, and [frequency] thereafter; and
  - \[2.\] When required by system changes;

- \[b.\] Update role-based training content [frequency] and following [events] ; and

- \[c.\] Incorporate lessons learned from internal or external security incidents or breaches into role-based training.

## Control Assessment Objective

- \[AT-03a.\]

  - \[AT-03a.01\]

    - \[AT-03a.01[01]\] role-based security training is provided to [roles and responsibilities] before authorizing access to the system, information, or performing assigned duties;
    - \[AT-03a.01[02]\] role-based privacy training is provided to [roles and responsibilities] before authorizing access to the system, information, or performing assigned duties;
    - \[AT-03a.01[03]\] role-based security training is provided to [roles and responsibilities] [frequency] thereafter;
    - \[AT-03a.01[04]\] role-based privacy training is provided to [roles and responsibilities] [frequency] thereafter;

  - \[AT-03a.02\]

    - \[AT-03a.02[01]\] role-based security training is provided to personnel with assigned security roles and responsibilities when required by system changes;
    - \[AT-03a.02[02]\] role-based privacy training is provided to personnel with assigned security roles and responsibilities when required by system changes;

- \[AT-03b.\]

  - \[AT-03b.[01]\] role-based training content is updated [frequency];
  - \[AT-03b.[02]\] role-based training content is updated following [events];

- \[AT-03c.\] lessons learned from internal or external security incidents or breaches are incorporated into role-based training.

## Control guidance

Organizations determine the content of training based on the assigned roles and responsibilities of individuals as well as the security and privacy requirements of organizations and the systems to which personnel have authorized access, including technical training specifically tailored for assigned duties. Roles that may require role-based training include senior leaders or management officials (e.g., head of agency/chief executive officer, chief information officer, senior accountable official for risk management, senior agency information security officer, senior agency official for privacy), system owners; authorizing officials; system security officers; privacy officers; acquisition and procurement officials; enterprise architects; systems engineers; software developers; systems security engineers; privacy engineers; system, network, and database administrators; auditors; personnel conducting configuration management activities; personnel performing verification and validation activities; personnel with access to system-level software; control assessors; personnel with contingency planning and incident response duties; personnel with privacy management responsibilities; and personnel with access to personally identifiable information.

Comprehensive role-based training addresses management, operational, and technical roles and responsibilities covering physical, personnel, and technical controls. Role-based training also includes policies, procedures, tools, methods, and artifacts for the security and privacy roles defined. Organizations provide the training necessary for individuals to fulfill their responsibilities related to operations and supply chain risk management within the context of organizational security and privacy programs. Role-based training also applies to contractors who provide services to federal agencies. Types of training include web-based and computer-based training, classroom-style training, and hands-on training (including micro-training). Updating role-based training on a regular basis helps to ensure that the content remains relevant and effective. Events that may precipitate an update to role-based training content include, but are not limited to, assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

All roles in the MSS homelab -- system owner, ISSO, system administrator, SOC analyst, incident responder, vulnerability manager, and assessment coordinator -- are held by a single person: Brian Chaplow. Role-based training is fulfilled through operational mastery and self-directed study specific to each role. As system administrator, the operator maintains 15 Wazuh agents, manages Proxmox VMs, and resolves infrastructure failures (ADR 0005 PBS automount fix, ADR 0003 RegScale install deviation). As SOC analyst, the operator reviews Wazuh alerts, tunes detection rules, and operates the Phase 14 Zeek + Logstash enrichment pipeline daily. As ISSO and assessment coordinator, the operator authored this SSP, built the OSCAL ConMon pipelines (Plan 2), and executed 130 tests across the FedRAMP Low ConMon program.

The gap is the absence of a formal pre-access role-based training attestation; the operator self-authorizes, so there is no distinct authorization event to tie a training record to. The ADR chain (ADRs 0001--0008) and the 14-phase homelab build history constitute the auditable record of role-specific competence acquired under real operational conditions.

#### Implementation Status: partial

______________________________________________________________________
