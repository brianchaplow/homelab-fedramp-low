# Evidence Catalog — SI (System and Information Integrity)

**Family:** SI — System and Information Integrity
**Controls in FedRAMP Rev 5 Low scaffold:** SI-1, SI-2, SI-3, SI-4, SI-5, SI-12
**Catalog date:** 2026-04-09
**Subagent:** SI phase-1 evidence sweep

---

## SI-1 System and Information Integrity Policy and Procedures

- **Status:** implemented
- **Primary mechanism:** `C:\Projects\CLAUDE.md` serves as the system-level SI policy
  document — it defines the authorization boundary, monitoring tool inventory, detection
  rules, and operational cadence (Wazuh, Suricata, Zeek, ELK, OpenCTI). The file is
  git-tracked in the parent workspace and updated at each phase milestone.
- **Supporting mechanisms:** ADRs 0001–0008 record every deviation and policy decision
  made during Plan 1–3 execution; `homelab-fedramp-low/docs/adr/` is the authoritative
  policy-change log. The parent `HomeLab-SOC-v3-Current-vs-Future.md` provides the
  broader architectural intent.
- **Evidence paths:**
  - `C:\Projects\CLAUDE.md` (system-level SI policy; see v3 Migration Status table and
    Service Inventory sections)
  - `homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` (Plan 1 pre-flight — policy
    and scope confirmed before deployment)
  - `homelab-fedramp-low/docs/adr/0008-plan-3-pre-execution-realignment.md` (Plan 3
    pre-execution realignment — authoring cadence and review decisions)
  - `homelab-fedramp-low/runbooks/monthly-conmon.md` (ConMon cycle procedure — SI-related
    monitoring cadence)
- **Set-params (proposed values):**
  - `si-01_odp.01` / `si-01_odp.02` (aggregate: dissemination personnel/roles):
    `["Brian Chaplow (system owner, sole operator)"]`, `organization`
  - `si-01_odp.03` (review frequency for policy): `annually or after any significant
    system change, new phase deployment, or security incident`, `organization`
  - `si-01_odp.04` (review circumstances for policy): `after any significant system
    change, new phase deployment, or ADR-recorded deviation`, `organization`
  - `si-01_odp.05` (review frequency for procedures): `annually or when a new ConMon
    cycle reveals a procedural gap`, `organization`
  - `si-01_odp.06` (review circumstances for procedures): `after a ConMon finding,
    a security incident, or a phase deployment that changes monitoring tooling`,
    `organization`
  - `si-01_odp.07` (designation official): `Brian Chaplow (system owner, sole operator)`,
    `organization`
  - `si-01_odp.08` (policy level — organization/mission/system): `system-level`,
    `organization`
- **Authoring notes:** SI-1 is a policy-and-procedures meta-control. Lead with
  `C:\Projects\CLAUDE.md` as the living system-level SI policy. Second paragraph:
  ADR chain as the policy-change log. Cite `runbooks/monthly-conmon.md` for the
  procedural cadence. Status: implemented (policy exists, is reviewed at each phase
  boundary, and is git-tracked).

---

## SI-2 Flaw Remediation

- **Status:** implemented
- **Primary mechanism:** Wazuh vulnerability detection via the Wazuh Indexer reads the
  `wazuh-states-vulnerabilities-*` OpenSearch index across all 15 in-boundary agents.
  The `pipelines/ingest/wazuh_vulns.py` module pages through all hits (8,471 findings
  across 5 agents in the April 2026 run) and emits normalized `Finding` records mapped
  to SI-2. DefectDojo 2.57.0 on dojo (10.10.30.27) tracks each finding's lifecycle
  against FedRAMP Low SLA windows (Critical 15-day, High 30-day, Moderate 90-day, Low
  180-day).
- **Supporting mechanisms:** The monthly ConMon pipeline (`./pipelines.sh conmon`) re-runs
  ingest → DefectDojo push → POA&M build automatically. `poam/POAM-2026-04.xlsx` is the
  rendered FedRAMP POA&M template (4.9 MB, 8,473 rows, April 2026 cycle). The
  `pipelines/build/oscal_poam.py` OSCAL POA&M builder links each CVE-sourced finding to
  SI-2 in the OSCAL risk catalog. Wazuh SCA (Security Configuration Assessment) scans
  endpoints for configuration flaws; results surface in the Wazuh dashboard on brisket
  (10.10.20.30:5601).
- **Evidence paths:**
  - `homelab-fedramp-low/pipelines/ingest/wazuh_vulns.py` (vuln ingestion — field
    mapping and SI-2 control tag confirmed in module docstring line 39)
  - `homelab-fedramp-low/pipelines/build/oscal_poam.py` (OSCAL POA&M builder — SI-2
    and RA-5 control citations)
  - `homelab-fedramp-low/poam/POAM-2026-04.xlsx` (April 2026 POA&M, 8,473 items)
  - `homelab-fedramp-low/tests/test_wazuh_vulns_ingest.py` (pytest coverage of ingest
    pipeline)
  - `homelab-fedramp-low/runbooks/monthly-conmon.md` (procedure for monthly flaw
    remediation cycle)
  - ADR 0007 (Plan 2 complete — live end-to-end vuln push: 8,471 findings, zero skipped)
  - ADR 0006 Deviation 5 (Wazuh 4.8 REST /vulnerability endpoint removed; pivot to
    indexer-based ingest)
- **Set-params (proposed values):**
  - `si-02_odp` (time period for security-relevant update installation): `within 30 days
    for Critical/High CVEs; within 90 days for Moderate CVEs; within 180 days for Low
    CVEs — aligned with FedRAMP Low ConMon SLA windows tracked in DefectDojo`, `organization`
- **Authoring notes:** SI-2 is the flaw-remediation hero for the ConMon pipeline. Lead
  paragraph: Wazuh Indexer reads `wazuh-states-vulnerabilities-*`, 8,471 findings
  ingested, DefectDojo tracks SLAs. Second paragraph: monthly `./pipelines.sh conmon`
  closes the loop → POA&M. Cite ADR 0007 as the live end-to-end proof. Status:
  implemented (pipeline runs, POA&M generated, DefectDojo holds live findings).

---

## SI-3 Malicious Code Protection

- **Status:** partial
- **Primary mechanism:** Suricata on smokehouse (10.10.20.10, eth4 SPAN) provides
  signature-based malicious code detection at the network boundary. Suricata rule sets
  are maintained under `HomeLab-SOC-v2/configs/suricata/` (`local.rules`,
  `suricata.yaml`, `update.yaml`) and updated via `suricata-update`. Wazuh on brisket
  ingests Suricata `eve.json` alerts via the Wazuh agent on smokehouse, correlating
  malicious traffic signatures against the `wazuh-alerts-*` index. Zeek on haccp
  span0 and smokehouse eth4 provides complementary non-signature protocol-behavior
  detection (JA3/JA4 TLS fingerprinting, anomalous connection patterns) via
  `reference/phase14/zeek/local.zeek`.
- **Supporting mechanisms:** OpenCTI v7 on brisket (10.10.20.30:8080) receives IOC
  feeds from 6 connectors; the IOC sync cron (`0 */6 * * *`) pushes malicious IPs to
  Wazuh CDB lists used in Wazuh detection rules, creating a near-real-time IOC-driven
  blocking layer. The Wazuh ML scorer (`brisket:5002`) applies XGBoost threat scoring
  (PR-AUC 0.9998) as a non-signature behavioral layer. OPNsense firewall provides
  network-entry point blocking on the VLAN boundary.
- **Evidence paths:**
  - `HomeLab-SOC-v2/configs/suricata/suricata.yaml` (Suricata config)
  - `HomeLab-SOC-v2/configs/suricata/local.rules` (local signature rules)
  - `HomeLab-SOC-v2/configs/suricata/update.yaml` (rule-set update config)
  - `reference/phase14/zeek/local.zeek` (Zeek non-signature detection policy on haccp
    span0)
  - `C:\Projects\CLAUDE.md` (OpenCTI IOC sync cron schedules — Service Inventory section)
- **Set-params (proposed values):**
  - `si-03_odp.01` (malicious code protection type — signature/non-signature): `signature-based
    and non-signature-based`, `organization`
  - `si-03_odp.02` (periodic scan frequency): `daily — Suricata continuous + Wazuh SCA
    weekly scan; Wazuh agents perform real-time file monitoring via FIM`, `organization`
  - `si-03_odp.03` (real-time scan location — endpoint/network): `network entry and exit
    points (Suricata on eth4 SPAN, Zeek on span0) and endpoint (Wazuh FIM on 15 agents)`,
    `organization`
  - `si-03_odp.04` (response to detection — block/quarantine/action): `block malicious code
    at the OPNsense firewall via Wazuh CDB-fed ACL rules; send alert to Brian Chaplow via
    Discord #soc-alerts webhook (Shuffle WF1)`, `organization`
  - `si-03_odp.05` (alert personnel): `Brian Chaplow (system owner, sole operator) via
    Discord #soc-alerts`, `organization`
  - `si-03_odp.06` (false-positive handling): `Wazuh deduplication in Shuffle WF1 v2
    suppresses repeated low-confidence alerts; OPNsense ACL blocks are reviewed
    manually when a Discord alert fires`, `organization`
- **Authoring notes:** Status is partial because no endpoint AV agent is installed on
  Linux SOC infrastructure hosts (brisket, haccp, smokehouse). Gap: endpoint-level
  malicious code scanning is network-only. Suricata + Zeek + Wazuh IOC is the
  implemented layer; prose paragraph 2 must name the gap explicitly. Do not claim
  endpoint AV.

---

## SI-4 System Monitoring

- **Status:** implemented
- **Primary mechanism:** Wazuh on brisket (10.10.20.30) aggregates security events
  from all 15 agents across VLANs 10, 20, 30, and 40. The Wazuh manager applies 214
  detection rules with MITRE ATT&CK mapping, shipping alerts to `wazuh-alerts-*`
  in the Wazuh Indexer (OpenSearch on brisket:9200). Suricata on smokehouse eth4 SPAN
  provides signature-based IDS for network-level attack detection. Zeek on haccp span0
  produces JSON protocol-metadata logs (conn, dns, http, ssl, x509) with JA3/JA4 TLS
  fingerprints and community-id correlation, shipped via Filebeat to Logstash on haccp
  and indexed as `logs-zeek.haccp-default-*` in ELK. The Phase 14 Zeek → Logstash
  enrichment pipeline (`reference/phase14/logstash/zeek-enrichment.conf`) applies a
  5-stage enrichment: de-dot → OpenCTI TI lookups → novel-entity tracking
  (`reference/phase14/logstash/ruby/novel_entity.rb`) → tier routing →
  Ollama LLM classification on brisket qwen3:8b. All tier-1 (TI-matched) and tier-2
  (novel-entity) events pass through a shared token-bucket rate limiter
  (`reference/phase14/logstash/ruby/tier2_rate_limit.rb`, cap 10/min) to protect
  the GPU. Arkime on haccp records full PCAP to the 2TB Samsung 990 EVO Plus at
  `/opt/arkime/raw`, enabling post-incident packet replay.
- **Supporting mechanisms:** ELK on haccp (10.10.30.25) runs 214 Kibana detection rules
  and an Elastic ML trial-license auth-anomalies job analyzing DC01/WS01 Windows
  Security events. Velociraptor DFIR on brisket (8889/HTTPS) provides ad-hoc endpoint
  forensic collection across 7 clients. The XGBoost ML scorer on brisket (`brisket:5002`,
  PR-AUC 0.9998) scores individual Wazuh alerts as a behavioral anomaly layer. Shuffle
  WF1 (webhook) receives high-confidence Wazuh alerts and routes them through
  AbuseIPDB enrichment, OPNsense/Cloudflare block, and TheHive case creation.
  WF10 (cron 0530 EST) generates a nightly briefing from the Zeek enrichment pipeline
  output and posts to #morning-briefing via Discord. Grafana on brisket (3000) displays
  the SOC v3 Overview dashboard; the `GPU Thermal Critical — Brisket Above 90C` alert
  (uid=dfihoiidr7k00c) routes to #infrastructure-alerts. The nightly PCAP archival cron
  at 0300 SSH/rsyncs to smokehouse 17TB NAS for long-term retention.
- **Evidence paths:**
  - `C:\Projects\CLAUDE.md` (complete monitoring stack: Wazuh 15 agents, 214 rules,
    Phase 14 pipeline, Arkime, ELK, Velociraptor, ML scorer — Service Inventory section
    and Phase 14 completion notes)
  - `reference/phase14/logstash/zeek-enrichment.conf` (5-stage Zeek enrichment pipeline
    — the monitoring instrumentation core)
  - `reference/phase14/logstash/ruby/tier2_rate_limit.rb` (shared token-bucket rate
    limiter for Ollama classification, tier 1 + tier 2)
  - `reference/phase14/logstash/ruby/novel_entity.rb` (novel-entity tracking in
    `haccp-entities-seen` index)
  - `reference/phase14/zeek/local.zeek` (Zeek policy on haccp span0 — JA3/JA4,
    community-id, log types)
  - `reference/phase14/cron/archive-pcap.sh` (nightly PCAP archival to smokehouse)
  - `brisket-setup/monitoring/prometheus.yml` (Prometheus scrape targets for Grafana)
  - `brisket-setup/monitoring/provisioning/alerting/discord.yml` (Grafana → Discord
    alerting — GPU thermal alert and infrastructure alerts)
  - `brisket-setup/monitoring/build-grafana-alerts.py` (Grafana alert provisioning
    script, GPU thermal alert uid=dfihoiidr7k00c)
  - `reference/phase14/shuffle/wf10-haccp-embed-20260409.json` (WF10 morning briefing
    workflow — monitoring output dissemination)
  - ADR 0008 (Phase 14 thermal hardening 2026-04-08 — documents Ollama rate-limit fix,
    GPU power cap, temp reduction 87C → 63C)
- **Set-params (proposed values):**
  - `si-04_odp.01` (monitoring objectives): `detect attacks and indicators of attack on
    all in-boundary hosts via Wazuh 214-rule policy + Suricata signatures + Zeek protocol
    metadata; detect TI-matched connections via OpenCTI IOC lookup in the Zeek enrichment
    pipeline; detect novel entities via novel_entity.rb; detect unauthorized remote
    connections via Wazuh agent heartbeat and OPNsense syslog`, `organization`
  - `si-04_odp.02` (unauthorized use techniques): `Wazuh MITRE ATT&CK-mapped detection
    rules (214 active), Zeek connection metadata with JA3/JA4 TLS fingerprinting,
    XGBoost ML scorer behavioral scoring (PR-AUC 0.9998), Elastic ML auth-anomalies
    job on Windows Security events`, `organization`
  - `si-04_odp.03` (system monitoring information type for dissemination): `Wazuh
    alert summaries, Zeek enriched connection events, Ollama-classified tier-1/tier-2
    events, daily nightly briefing`, `organization`
  - `si-04_odp.04` (dissemination personnel): `Brian Chaplow (system owner, sole operator)
    via Discord #soc-alerts (WF1), #morning-briefing (WF10), and #infrastructure-alerts
    (Grafana)`, `organization`
  - `si-04_odp.05` (dissemination frequency): `as needed (real-time Discord alerts for
    high-confidence events via Shuffle WF1) and daily (WF10 morning briefing at 0530 EST)`,
    `organization`
  - `si-04_odp.06` (legal opinion on monitoring): `monitoring is conducted on
    infrastructure owned and operated solely by Brian Chaplow; no user privacy interests
    apply — single-operator personal homelab system`, `organization`
- **Authoring notes:** SI-4 is the hero control (whole-project design §4.5). Lead
  paragraph names Wazuh + Suricata + Zeek + ELK + ML scorer together in one dense
  paragraph showing the layered detection stack. Second paragraph covers dissemination
  (WF1 → Discord, WF10 morning briefing, Grafana alerts) and cite Phase 14 thermal
  hardening via CLAUDE.md / ADR 0008 as the auditable incident showing the monitoring
  stack was exercised under load. Cite `zeek-enrichment.conf` and `tier2_rate_limit.rb`
  by path. Status: implemented.

---

## SI-5 Security Alerts, Advisories, and Directives

- **Status:** implemented
- **Primary mechanism:** OpenCTI v7 on brisket (10.10.20.30:8080) aggregates threat
  intelligence from 6 active connectors operating continuously. The IOC sync cron
  (`0 */6 * * *`) pushes current malicious indicators to Wazuh CDB lists on brisket,
  making external threat advisories actionable as detection rules within 6 hours of
  IOC ingestion. A second cron (`15 */6 * * *`) syncs indicators to the
  `opencti-threat-intel` index in ELK on haccp for Kibana correlation.
- **Supporting mechanisms:** The Phase 14 Zeek enrichment pipeline performs live
  OpenCTI TI lookups in Stage 2 of `zeek-enrichment.conf`, matching every observed
  connection against the current IOC set and routing matches to tier-1 processing with
  immediate Ollama classification. Shuffle WF10 (cron 0530 EST) incorporates threat
  intelligence context into the nightly briefing posted to Discord #morning-briefing.
  WF8 (cron 1500 EST) monitors watch-list entities. CISA advisories are manually
  reviewed by Brian Chaplow and actioned within the ConMon cycle cadence; relevant
  findings generate DefectDojo tickets tracked against SI-2.
- **Evidence paths:**
  - `C:\Projects\CLAUDE.md` (OpenCTI 6 connectors, IOC sync cron schedules — Service
    Inventory section under brisket)
  - `reference/phase14/logstash/zeek-enrichment.conf` (Stage 2 OpenCTI TI lookup in
    the enrichment pipeline)
  - `reference/phase14/shuffle/wf10-haccp-embed-20260409.json` (WF10 morning briefing
    with TI context — alert dissemination)
  - ADR 0007 (Plan 2 complete — OpenCTI IOC sync confirmed as live ConMon pipeline
    component)
- **Set-params (proposed values):**
  - `si-05_odp.01` (external organizations for receiving alerts): `CISA US-CERT
    (cisa.gov/uscert), NVD (nvd.nist.gov), OpenCTI connector feeds (AlienVault OTX,
    abuse.ch URLhaus, MISPFeed)`, `organization`
  - `si-05_odp.02` (dissemination personnel/roles/elements): `Brian Chaplow (system
    owner, sole operator)`, `organization`
  - `si-05_odp.03` (dissemination frequency): `continuous via OpenCTI connector polling;
    daily nightly briefing (WF10 0530 EST); ad-hoc when a CISA KEV or critical advisory
    requires immediate action`, `organization`
  - `si-05_odp.04` (implementation time frame): `Critical/High advisories actioned
    within 30 days (aligned with FedRAMP Low High SLA window); Low/Moderate within 90
    days`, `organization`
  - `si-05_odp.05` (degree of noncompliance notification): `Brian Chaplow (sole
    operator) — no external issuing organization applies to this personal homelab system;
    compliance with CISA directives is best-effort`, `organization`
- **Authoring notes:** Lead with OpenCTI 6-connector continuous feed and IOC sync cron.
  Second paragraph: Phase 14 pipeline performs live TI lookups in zeek-enrichment.conf
  Stage 2. Reference `C:\Projects\CLAUDE.md` for the IOC sync cron schedule. Status:
  implemented (OpenCTI connectors live, IOC sync cron live, Phase 14 TI lookup live).

---

## SI-12 Information Management and Retention

- **Status:** implemented
- **Primary mechanism:** Audit and monitoring data retention is enforced at the index
  level: Wazuh Indexer on brisket retains `wazuh-alerts-*` indices for 90 days (aligned
  with the ConMon cycle window); ELK on haccp retains `logs-zeek.haccp-default-*` and
  Arkime PCAP on the 2TB Samsung 990 EVO Plus at `/opt/arkime/raw` with nightly archival
  to smokehouse 17TB NAS via `reference/phase14/cron/archive-pcap.sh`. PBS on smoker
  LXC 300 runs daily and weekly backup jobs of critical VMs (DC01, WS01, TheHive) to
  smokehouse NFS (17TB), providing a system-state retention backstop.
- **Supporting mechanisms:** The ConMon pipeline produces versioned OSCAL artifacts
  per monthly cycle: `oscal/ssp.json`, `oscal/poam.json` (gitignored — regenerated),
  `poam/POAM-2026-04.xlsx` (committed), `inventory/IIW-2026-04.xlsx` (committed).
  Git commit history on `main` branch provides immutable audit trail of policy and
  configuration changes. OSCAL artifacts are tagged per milestone (`plan-2-complete`,
  `plan-3-complete`) for point-in-time retrieval. DefectDojo finding history on dojo
  (10.10.30.27) provides vulnerability lifecycle retention.
- **Evidence paths:**
  - `homelab-fedramp-low/poam/POAM-2026-04.xlsx` (April 2026 POA&M — monthly retained
    submission artifact)
  - `homelab-fedramp-low/inventory/IIW-2026-04.xlsx` (April 2026 IIW — monthly retained
    inventory artifact)
  - `reference/phase14/cron/archive-pcap.sh` (nightly PCAP archival to smokehouse —
    long-term packet retention)
  - `homelab-fedramp-low/oscal/ssp.json` (OSCAL SSP — assembled and retained in git)
  - `homelab-fedramp-low/runbooks/monthly-conmon.md` (ConMon retention procedure)
  - ADR 0005 (PBS backup gap 2026-04-03 to 2026-04-07 — auditable retention-gap
    incident; NFS automount hardening fix applied)
  - ADR 0007 (Plan 2 complete — artifact inventory with sizes and paths confirmed)
  - `C:\Projects\CLAUDE.md` (Phase 11 PBS description: NFS→smokehouse 17TB, daily/weekly
    jobs; Phase 14 PCAP archival cadence)
- **Set-params (proposed values):** SI-12 has no `x-trestle-set-params` ODPs in the
  scaffold (no REPLACE_ME in si-12.md frontmatter) — the control statement has no
  parameterized values. No set-params to fill.
- **Authoring notes:** SI-12 is a retention meta-control. Lead with the index-level
  retention policy (Wazuh 90-day, ELK/Zeek indefinite until disk, PCAP archival to
  smokehouse). Second paragraph: ConMon pipeline monthly artifacts (POA&M xlsx, IIW xlsx)
  committed to git as the primary retention mechanism for OSCAL outputs. Cite ADR 0005
  as the auditable retention-gap incident (PBS backup gap discovered and fixed).
  Status: implemented.

---

## Summary report

| Field | Value |
|---|---|
| `family` | si |
| `controls_cataloged` | 6 (SI-1, SI-2, SI-3, SI-4, SI-5, SI-12) |
| `grep_verifications_performed` | 22 |
| `cites_to_parent_claude_md` | 7 |
| `cites_to_adrs` | 9 (ADR 0001, 0005, 0006, 0007, 0008 — multiple citations) |
| `unresolved_questions` | SI-3: no endpoint AV on Linux hosts — status is partial; SI-04_odp.06 (legal opinion on monitoring) — single-operator homelab justification used; SI-12: zero ODPs in scaffold, confirmed no set-params to fill |
