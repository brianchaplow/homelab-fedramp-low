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
  si-05_odp.01:
    alt-identifier: si-5_prm_1
    profile-values:
      - CISA US-CERT (cisa.gov/uscert), NVD (nvd.nist.gov), OpenCTI connector feeds (AlienVault OTX, abuse.ch URLhaus, MISPFeed)
    profile-param-value-origin: organization
  si-05_odp.02:
    alt-identifier: si-5_prm_2
    profile-values:
      - Brian Chaplow (system owner, sole operator)
    profile-param-value-origin: organization
  si-05_odp.03:
    alt-identifier: si-5_prm_3
    profile-values:
      - continuous via OpenCTI connector polling; daily nightly briefing (WF10 0530 EST); ad-hoc when a CISA KEV or critical advisory requires immediate action
    profile-param-value-origin: organization
  si-05_odp.04:
    alt-identifier: si-5_prm_4
    profile-values:
      - Critical/High advisories actioned within 30 days aligned with FedRAMP Low High SLA window; Low/Moderate within 90 days
    profile-param-value-origin: organization
  si-05_odp.05:
    alt-identifier: si-5_prm_5
    profile-values:
      - Brian Chaplow (sole operator) -- no external issuing organization applies to this personal homelab system; compliance with CISA directives is best-effort
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: si-05
---

# si-5 - \[System and Information Integrity\] Security Alerts, Advisories, and Directives

## Control Statement

- \[a.\] Receive system security alerts, advisories, and directives from [external organizations] on an ongoing basis;

- \[b.\] Generate internal security alerts, advisories, and directives as deemed necessary;

- \[c.\] Disseminate security alerts, advisories, and directives to: [Selection (one or more): [personnel or roles]; [elements]; [external organizations]] ; and

- \[d.\] Implement security directives in accordance with established time frames, or notify the issuing organization of the degree of noncompliance.

## Control Assessment Objective

- \[SI-05a.\] system security alerts, advisories, and directives are received from [external organizations] on an ongoing basis;

- \[SI-05b.\] internal security alerts, advisories, and directives are generated as deemed necessary;

- \[SI-05c.\] security alerts, advisories, and directives are disseminated to [Selection (one or more): [personnel or roles]; [elements]; [external organizations]];

- \[SI-05d.\] security directives are implemented in accordance with established time frames or if the issuing organization is notified of the degree of noncompliance.

## Control guidance

The Cybersecurity and Infrastructure Security Agency (CISA) generates security alerts and advisories to maintain situational awareness throughout the Federal Government. Security directives are issued by OMB or other designated organizations with the responsibility and authority to issue such directives. Compliance with security directives is essential due to the critical nature of many of these directives and the potential (immediate) adverse effects on organizational operations and assets, individuals, other organizations, and the Nation should the directives not be implemented in a timely manner. External organizations include supply chain partners, external mission or business partners, external service providers, and other peer or supporting organizations.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Security alerts, advisories, and directives are received on an ongoing basis through OpenCTI v7 on brisket (10.10.20.30:8080), which aggregates threat intelligence from 6 active connectors -- including AlienVault OTX, abuse.ch URLhaus, and MISPFeed -- operating on continuous polling schedules. The IOC sync cron (`0 */6 * * *`) pushes current malicious indicators to Wazuh CDB lists on brisket, making external threat advisories directly actionable as detection rule inputs within 6 hours of IOC ingestion. A complementary cron (`15 */6 * * *`) syncs indicators to the `opencti-threat-intel` index in ELK on haccp (10.10.30.25:9200) for Kibana correlation. CISA US-CERT advisories and NVD CVE feeds are monitored manually by Brian Chaplow on an ongoing basis; CISA Known Exploited Vulnerability (KEV) entries are treated as Critical/High priority and actioned within 30 days aligned with the FedRAMP Low High SLA window tracked in DefectDojo.

The Phase 14 Zeek enrichment pipeline performs live OpenCTI TI lookups in Stage 2 of `reference/phase14/logstash/zeek-enrichment.conf`, matching every observed network connection against the current IOC set in real time and routing matches to tier-1 processing with immediate Ollama qwen3:8b classification. This transforms external threat intelligence into in-line detection within the monitoring pipeline. Internal security alerts are generated by Shuffle WF10 (cron 0530 EST), which produces a nightly briefing incorporating threat intelligence context from the Zeek enrichment output and posts it to Discord #morning-briefing. Shuffle WF8 (cron 1500 EST) monitors watch-list entities. Security directives are implemented within established time frames; relevant findings are tracked as DefectDojo tickets linked to the monthly POA&M cycle via `pipelines/build/oscal_poam.py`.

#### Implementation Status: implemented

______________________________________________________________________
