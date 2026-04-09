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
    profile-param-value-origin: <REPLACE_ME>
  at-2_prm_2:
    aggregates:
      - at-02_odp.03
      - at-02_odp.04
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.05:
    alt-identifier: at-2_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.06:
    alt-identifier: at-2_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  at-02_odp.07:
    alt-identifier: at-2_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
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

<!-- Add implementation prose for the main This System component for control: at-2 -->

#### Implementation Status: planned

______________________________________________________________________
