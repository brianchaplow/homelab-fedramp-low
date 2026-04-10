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
  at-2_prm_1:
    aggregates:
      - at-02_odp.01
      - at-02_odp.02
    profile-param-value-origin: organization
  at-2_prm_2:
    aggregates:
      - at-02_odp.03
      - at-02_odp.04
    profile-param-value-origin: organization
  at-02_odp.01:
    profile-values:
      - continuous -- operator reviews WF10 morning briefing daily and reviews Wazuh and OpenCTI alerts as part of normal SOC operations
    profile-param-value-origin: organization
  at-02_odp.02:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  at-02_odp.03:
    profile-values:
      - new phase completion, significant security incident, new CVE class introduced to the environment
    profile-param-value-origin: organization
  at-02_odp.04:
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  at-02_odp.05:
    alt-identifier: at-2_prm_3
    profile-values:
      - daily WF10 morning briefing (Discord #morning-briefing), OpenCTI IOC sync every 6 hours, Grafana threat-intel dashboard review, ADR authoring as incident-learning record
    profile-param-value-origin: organization
  at-02_odp.06:
    alt-identifier: at-2_prm_4
    profile-values:
      - continuously via OpenCTI connector feeds and ADR filings
    profile-param-value-origin: organization
  at-02_odp.07:
    alt-identifier: at-2_prm_5
    profile-values:
      - new security incident, new phase adding in-boundary components, significant CVE advisory
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: at-02
---

# at-2 - \[Awareness and Training\] Literacy Training and Awareness

## Control Statement

- \[a.\] Provide security and privacy literacy training to system users (including managers, senior executives, and contractors):

  - \[1.\] As part of initial training for new users and [organization-defined frequency] thereafter; and
  - \[2.\] When required by system changes or following [organization-defined events];

- \[b.\] Employ the following techniques to increase the security and privacy awareness of system users [awareness techniques];

- \[c.\] Update literacy training and awareness content [frequency] and following [events] ; and

- \[d.\] Incorporate lessons learned from internal or external security incidents or breaches into literacy training and awareness techniques.

## Control Assessment Objective

- \[AT-02a.\]

  - \[AT-02a.01\]

    - \[AT-02a.01[01]\] security literacy training is provided to system users (including managers, senior executives, and contractors) as part of initial training for new users;
    - \[AT-02a.01[02]\] privacy literacy training is provided to system users (including managers, senior executives, and contractors) as part of initial training for new users;
    - \[AT-02a.01[03]\] security literacy training is provided to system users (including managers, senior executives, and contractors) [frequency] thereafter;
    - \[AT-02a.01[04]\] privacy literacy training is provided to system users (including managers, senior executives, and contractors) [frequency] thereafter;

  - \[AT-02a.02\]

    - \[AT-02a.02[01]\] security literacy training is provided to system users (including managers, senior executives, and contractors) when required by system changes or following [events];
    - \[AT-02a.02[02]\] privacy literacy training is provided to system users (including managers, senior executives, and contractors) when required by system changes or following [events];

- \[AT-02b.\] [awareness techniques] are employed to increase the security and privacy awareness of system users;

- \[AT-02c.\]

  - \[AT-02c.[01]\] literacy training and awareness content is updated [frequency];
  - \[AT-02c.[02]\] literacy training and awareness content is updated following [events];

- \[AT-02d.\] lessons learned from internal or external security incidents or breaches are incorporated into literacy training and awareness techniques.

## Control guidance

Organizations provide basic and advanced levels of literacy training to system users, including measures to test the knowledge level of users. Organizations determine the content of literacy training and awareness based on specific organizational requirements, the systems to which personnel have authorized access, and work environments (e.g., telework). The content includes an understanding of the need for security and privacy as well as actions by users to maintain security and personal privacy and to respond to suspected incidents. The content addresses the need for operations security and the handling of personally identifiable information.

Awareness techniques include displaying posters, offering supplies inscribed with security and privacy reminders, displaying logon screen messages, generating email advisories or notices from organizational officials, and conducting awareness events. Literacy training after the initial training described in [AT-2a.1](#at-2_smt.a.1) is conducted at a minimum frequency consistent with applicable laws, directives, regulations, and policies. Subsequent literacy training may be satisfied by one or more short ad hoc sessions and include topical information on recent attack schemes, changes to organizational security and privacy policies, revised security and privacy expectations, or a subset of topics from the initial training. Updating literacy training and awareness content on a regular basis helps to ensure that the content remains relevant. Events that may precipitate an update to literacy training and awareness content include, but are not limited to, assessment or audit findings, security incidents or breaches, or changes in applicable laws, executive orders, directives, regulations, policies, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The operator maintains continuous security literacy through active operation of the MSS homelab SOC -- reviewing Wazuh alerts from 15 agents, enriching OpenCTI v7 indicators via 6 connectors (MITRE ATT&CK, AbuseIPDB, threat feeds), and receiving the WF10 morning briefing (Shuffle cron 0530 EST, Discord `#morning-briefing`) summarizing the prior night's Zeek network activity from the Phase 14 pipeline. The OpenCTI IOC sync cron (`0 */6 * * *`) pushes current threat indicators to Wazuh CDB lists and the haccp `opencti-threat-intel` ELK index, providing live awareness of active IOCs. ADR 0005 (PBS backup gap detection and automount fix) is a concrete example of applied security awareness: the operator independently identified, diagnosed, and resolved a security-relevant configuration failure.

The gap is the absence of a formal training completion attestation or scheduled course. Awareness is continuous and operationally driven rather than time-bounded with a recorded completion date. This makes the status partial -- the substance of awareness exists and is current, but no LMS record is generated.

#### Implementation Status: partial

______________________________________________________________________
