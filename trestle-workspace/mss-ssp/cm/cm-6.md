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
  cm-06_odp.01:
    alt-identifier: cm-6_prm_1
    profile-values:
      - Ubuntu 24.04 LTS vendor defaults with unattended-upgrades, UFW default-deny, SSH PasswordAuthentication disabled, Docker least-privilege port publication
    profile-param-value-origin: organization
  cm-06_odp.02:
    alt-identifier: cm-6_prm_2
    profile-values:
      - DefectDojo 2.57.0 on dojo (HTTP-on-8080 per ADR 0004); RegScale CE on regscale (HTTP-on-80 per ADR 0003)
    profile-param-value-origin: organization
  cm-06_odp.03:
    alt-identifier: cm-6_prm_3
    profile-values:
      - no publicly trusted TLS certificate available for LAN-only services; reverse-proxy upgrade path documented in runbooks/cert-trust.md for future Plan 4
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: cm-06
---

# cm-6 - \[Configuration Management\] Configuration Settings

## Control Statement

- \[a.\] Establish and document configuration settings for components employed within the system that reflect the most restrictive mode consistent with operational requirements using [common secure configurations];

- \[b.\] Implement the configuration settings;

- \[c.\] Identify, document, and approve any deviations from established configuration settings for [system components] based on [operational requirements] ; and

- \[d.\] Monitor and control changes to the configuration settings in accordance with organizational policies and procedures.

## Control Assessment Objective

- \[CM-06a.\] configuration settings that reflect the most restrictive mode consistent with operational requirements are established and documented for components employed within the system using [common secure configurations];

- \[CM-06b.\] the configuration settings documented in CM-06a are implemented;

- \[CM-06c.\]

  - \[CM-06c.[01]\] any deviations from established configuration settings for [system components] are identified and documented based on [operational requirements];
  - \[CM-06c.[02]\] any deviations from established configuration settings for [system components] are approved;

- \[CM-06d.\]

  - \[CM-06d.[01]\] changes to the configuration settings are monitored in accordance with organizational policies and procedures;
  - \[CM-06d.[02]\] changes to the configuration settings are controlled in accordance with organizational policies and procedures.

## Control guidance

Configuration settings are the parameters that can be changed in the hardware, software, or firmware components of the system that affect the security and privacy posture or functionality of the system. Information technology products for which configuration settings can be defined include mainframe computers, servers, workstations, operating systems, mobile devices, input/output devices, protocols, and applications. Parameters that impact the security posture of systems include registry settings; account, file, or directory permission settings; and settings for functions, protocols, ports, services, and remote connections. Privacy parameters are parameters impacting the privacy posture of systems, including the parameters required to satisfy other privacy controls. Privacy parameters include settings for access controls, data processing preferences, and processing and retention permissions. Organizations establish organization-wide configuration settings and subsequently derive specific configuration settings for systems. The established settings become part of the configuration baseline for the system.

Common secure configurations (also known as security configuration checklists, lockdown and hardening guides, and security reference guides) provide recognized, standardized, and established benchmarks that stipulate secure configuration settings for information technology products and platforms as well as instructions for configuring those products or platforms to meet operational requirements. Common secure configurations can be developed by a variety of organizations, including information technology product developers, manufacturers, vendors, federal agencies, consortia, academia, industry, and other organizations in the public and private sectors.

Implementation of a common secure configuration may be mandated at the organization level, mission and business process level, system level, or at a higher level, including by a regulatory agency. Common secure configurations include the United States Government Configuration Baseline [USGCB](#98498928-3ca3-44b3-8b1e-f48685373087) and security technical implementation guides (STIGs), which affect the implementation of [CM-6](#cm-6) and other controls such as [AC-19](#ac-19) and [CM-7](#cm-7) . The Security Content Automation Protocol (SCAP) and the defined standards within the protocol provide an effective method to uniquely identify, track, and control configuration settings.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Configuration settings for in-boundary components reflect the most restrictive mode consistent with SOC operational requirements. All Ubuntu 24.04 VMs (dojo, regscale) are deployed with `unattended-upgrades` active for automated security patching, UFW default-deny with explicit service allowances, and SSH `PasswordAuthentication no` -- establishing a hardened OS baseline without requiring a named CIS Benchmark profile. Docker on brisket uses explicit port publications only (`brisket-setup/monitoring/docker-compose.yml`); no containers expose host-network mode or wildcard bindings. The Zeek configuration (`reference/phase14/zeek/local.zeek`) explicitly names every loaded package -- no default Zeek plugins are active beyond the pinned baseline. Prometheus scrape targets (`brisket-setup/monitoring/prometheus.yml`) are enumerated explicitly with no wildcard service discovery.

Deviations from secure-by-default settings are documented and approved via ADRs: DefectDojo 2.57.0 on dojo runs HTTP-on-8080 rather than HTTPS (ADR 0004), and RegScale CE on regscale runs HTTP-on-80 (ADR 0003). Both deviations are justified by the absence of a publicly trusted TLS certificate for LAN-only services; a reverse-proxy upgrade path is documented in `runbooks/cert-trust.md` for Plan 4. Wazuh SCA checks on all enrolled agents continuously validate OS hardening settings and surface deviations in the Wazuh Dashboard (brisket:5601); findings feed the monthly POA&M via `pipelines/ingest/wazuh_vulns.py`. The primary gap driving `partial` status is the absence of a named configuration standard (CIS Benchmark or STIG) formally adopted and mapped to the system.

#### Implementation Status: partial

______________________________________________________________________
