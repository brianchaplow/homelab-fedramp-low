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
  si-04_odp.01:
    alt-identifier: si-4_prm_1
    profile-values:
      - detect attacks and indicators of attack on all in-boundary hosts via Wazuh 214-rule policy plus Suricata signatures plus Zeek protocol metadata; detect TI-matched connections via OpenCTI IOC lookup in the Zeek enrichment pipeline; detect novel entities via novel_entity.rb; detect unauthorized remote connections via Wazuh agent heartbeat and OPNsense syslog
    profile-param-value-origin: organization
  si-04_odp.02:
    alt-identifier: si-4_prm_2
    profile-values:
      - Wazuh MITRE ATT&CK-mapped detection rules (214 active), Zeek connection metadata with JA3/JA4 TLS fingerprinting, XGBoost ML scorer behavioral scoring (PR-AUC 0.9998), Elastic ML auth-anomalies job on Windows Security events
    profile-param-value-origin: organization
  si-04_odp.03:
    alt-identifier: si-4_prm_3
    profile-values:
      - Wazuh alert summaries, Zeek enriched connection events, Ollama-classified tier-1 and tier-2 events, daily nightly briefing
    profile-param-value-origin: organization
  si-04_odp.04:
    alt-identifier: si-4_prm_4
    profile-values:
      - Brian Chaplow (system owner, sole operator) via Discord #soc-alerts (WF1), #morning-briefing (WF10), and #infrastructure-alerts (Grafana)
    profile-param-value-origin: organization
  si-04_odp.05:
    alt-identifier: si-4_prm_5
    profile-values:
      - as needed (real-time Discord alerts for high-confidence events via Shuffle WF1) and daily (WF10 morning briefing at 0530 EST)
    profile-param-value-origin: organization
  si-04_odp.06:
    alt-identifier: si-4_prm_6
    profile-values:
      - monitoring is conducted on infrastructure owned and operated solely by Brian Chaplow; no user privacy interests apply -- single-operator personal homelab system
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: si-04
---

# si-4 - \[System and Information Integrity\] System Monitoring

## Control Statement

- \[a.\] Monitor the system to detect:

  - \[1.\] Attacks and indicators of potential attacks in accordance with the following monitoring objectives: [monitoring objectives] ; and
  - \[2.\] Unauthorized local, network, and remote connections;

- \[b.\] Identify unauthorized use of the system through the following techniques and methods: [techniques and methods];

- \[c.\] Invoke internal monitoring capabilities or deploy monitoring devices:

  - \[1.\] Strategically within the system to collect organization-determined essential information; and
  - \[2.\] At ad hoc locations within the system to track specific types of transactions of interest to the organization;

- \[d.\] Analyze detected events and anomalies;

- \[e.\] Adjust the level of system monitoring activity when there is a change in risk to organizational operations and assets, individuals, other organizations, or the Nation;

- \[f.\] Obtain legal opinion regarding system monitoring activities; and

- \[g.\] Provide [system monitoring information] to [personnel or roles] [Selection (one or more): as needed; [frequency]].

## Control Assessment Objective

- \[SI-04a.\]

  - \[SI-04a.01\] the system is monitored to detect attacks and indicators of potential attacks in accordance with [monitoring objectives];
  - \[SI-04a.02\]

    - \[SI-04a.02[01]\] the system is monitored to detect unauthorized local connections;
    - \[SI-04a.02[02]\] the system is monitored to detect unauthorized network connections;
    - \[SI-04a.02[03]\] the system is monitored to detect unauthorized remote connections;

- \[SI-04b.\] unauthorized use of the system is identified through [techniques and methods];

- \[SI-04c.\]

  - \[SI-04c.01\] internal monitoring capabilities are invoked or monitoring devices are deployed strategically within the system to collect organization-determined essential information;
  - \[SI-04c.02\] internal monitoring capabilities are invoked or monitoring devices are deployed at ad hoc locations within the system to track specific types of transactions of interest to the organization;

- \[SI-04d.\]

  - \[SI-04d.[01]\] detected events are analyzed;
  - \[SI-04d.[02]\] detected anomalies are analyzed;

- \[SI-04e.\] the level of system monitoring activity is adjusted when there is a change in risk to organizational operations and assets, individuals, other organizations, or the Nation;

- \[SI-04f.\] a legal opinion regarding system monitoring activities is obtained;

- \[SI-04g.\] [system monitoring information] is provided to [personnel or roles] [Selection (one or more): as needed; [frequency]].

## Control guidance

System monitoring includes external and internal monitoring. External monitoring includes the observation of events occurring at external interfaces to the system. Internal monitoring includes the observation of events occurring within the system. Organizations monitor systems by observing audit activities in real time or by observing other system aspects such as access patterns, characteristics of access, and other actions. The monitoring objectives guide and inform the determination of the events. System monitoring capabilities are achieved through a variety of tools and techniques, including intrusion detection and prevention systems, malicious code protection software, scanning tools, audit record monitoring software, and network monitoring software.

Depending on the security architecture, the distribution and configuration of monitoring devices may impact throughput at key internal and external boundaries as well as at other locations across a network due to the introduction of network throughput latency. If throughput management is needed, such devices are strategically located and deployed as part of an established organization-wide security architecture. Strategic locations for monitoring devices include selected perimeter locations and near key servers and server farms that support critical applications. Monitoring devices are typically employed at the managed interfaces associated with controls [SC-7](#sc-7) and [AC-17](#ac-17) . The information collected is a function of the organizational monitoring objectives and the capability of systems to support such objectives. Specific types of transactions of interest include Hypertext Transfer Protocol (HTTP) traffic that bypasses HTTP proxies. System monitoring is an integral part of organizational continuous monitoring and incident response programs, and output from system monitoring serves as input to those programs. System monitoring requirements, including the need for specific types of system monitoring, may be referenced in other controls (e.g., [AC-2g](#ac-2_smt.g), [AC-2(7)](#ac-2.7), [AC-2(12)(a)](#ac-2.12_smt.a), [AC-17(1)](#ac-17.1), [AU-13](#au-13), [AU-13(1)](#au-13.1), [AU-13(2)](#au-13.2), [CM-3f](#cm-3_smt.f), [CM-6d](#cm-6_smt.d), [MA-3a](#ma-3_smt.a), [MA-4a](#ma-4_smt.a), [SC-5(3)(b)](#sc-5.3_smt.b), [SC-7a](#sc-7_smt.a), [SC-7(24)(b)](#sc-7.24_smt.b), [SC-18b](#sc-18_smt.b), [SC-43b](#sc-43_smt.b) ). Adjustments to levels of system monitoring are based on law enforcement information, intelligence information, or other sources of information. The legality of system monitoring activities is based on applicable laws, executive orders, directives, regulations, policies, standards, and guidelines.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service operates a five-layer detection stack covering all in-boundary hosts across VLANs 10, 20, 30, and 40. Layer 1 -- Wazuh on brisket (10.10.20.30) aggregates security events from all 15 enrolled agents (including brisket host, OPNsense syslog, dojo, and regscale) and applies 214 MITRE ATT&CK-mapped detection rules, shipping alerts to `wazuh-alerts-*` in the Wazuh Indexer on brisket:9200. Layer 2 -- Suricata on smokehouse (10.10.20.10, eth4 SPAN) provides signature-based IDS at the network boundary, with rule sets maintained under `HomeLab-SOC-v2/configs/suricata/`. Layer 3 -- Zeek on haccp span0 (`reference/phase14/zeek/local.zeek`) generates JSON protocol-metadata logs (conn, dns, http, ssl, x509) with JA3/JA4 TLS fingerprints and community-id field correlation, shipped via Filebeat to Logstash on haccp and indexed as `logs-zeek.haccp-default-*` in ELK. The Phase 14 Logstash enrichment pipeline (`reference/phase14/logstash/zeek-enrichment.conf`) applies 5 stages: de-dot → OpenCTI TI lookups (Stage 2, live IOC match against all 6 connector feeds) → novel-entity tracking via `novel_entity.rb` (Stage 3, `haccp-entities-seen` index) → tier routing → Ollama LLM classification on brisket qwen3:8b (Stage 5). A shared token-bucket rate limiter (`reference/phase14/logstash/ruby/tier2_rate_limit.rb`, cap 10/min) gates both tier-1 TI-matched and tier-2 novel-entity events to protect the RTX A1000 GPU, which is power-capped to 40W. Layer 4 -- Arkime on haccp records full PCAP to the 2TB Samsung 990 EVO Plus at `/opt/arkime/raw`, with nightly SSH/rsync archival to smokehouse 17TB NAS at 0300 via `reference/phase14/cron/archive-pcap.sh`, enabling post-incident packet replay for any connection observed on span0. Layer 5 -- ELK on haccp (10.10.30.25) runs 214 Kibana detection rules and an Elastic ML trial-license auth-anomalies job analyzing DC01/WS01 Windows Security events for behavioral anomalies. The XGBoost ML scorer on brisket (`brisket:5002`, PR-AUC 0.9998) applies a sixth independent behavioral scoring pass on individual Wazuh alerts. Velociraptor DFIR on brisket (8889/HTTPS) provides ad-hoc endpoint forensic collection across 7 enrolled clients for targeted investigation when monitoring detects a high-confidence indicator.

Monitoring information is disseminated in real time and on a daily schedule. Shuffle WF1 (webhook) receives high-confidence Wazuh alerts, enriches them via AbuseIPDB, routes blocking actions to OPNsense and Cloudflare, creates TheHive cases, and posts to Discord #soc-alerts. WF10 (cron 0530 EST) generates a nightly briefing from the Zeek enrichment pipeline output -- including Ollama classification summaries for tier-1 and tier-2 events -- and posts to Discord #morning-briefing. Grafana on brisket (:3000) displays the SOC v3 Overview dashboard and issues the `GPU Thermal Critical -- Brisket Above 90C` alert (uid=dfihoiidr7k00c) to Discord #infrastructure-alerts when the RTX A1000 exceeds 90C. The auditable proof that the monitoring stack was exercised under real load is ADR 0008: during Phase 14 go-live, the Ollama rate limiter had a defect that allowed tier-1 TI events to bypass the bucket, driving GPU temperature to 87C sustained. The stack detected the thermal event, the Grafana alert fired to #infrastructure-alerts, and the fix -- Stage 3b conditional + shared bucket + 40W power cap -- was implemented and validated, returning temperature to 63C and fan duty to 39%. Monitoring coverage and risk level are reviewed at each ConMon cycle; the level of monitoring activity is adjusted when new attack campaigns, CISA advisories, or POA&M findings increase risk to operations. Monitoring is conducted on infrastructure owned and operated solely by Brian Chaplow -- no external user privacy interests apply.

#### Implementation Status: implemented

______________________________________________________________________
