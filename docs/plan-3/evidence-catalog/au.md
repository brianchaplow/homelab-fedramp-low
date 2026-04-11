# AU -- Audit and Accountability Evidence Catalog

**Family:** AU -- Audit and Accountability
**Controls:** AU-1, AU-2, AU-3, AU-4, AU-5, AU-6, AU-8, AU-9, AU-11, AU-12
**Produced by:** Plan 3 Phase 1 evidence-catalog subagent
**Date:** 2026-04-09
**FedRAMP profile source:** `trestle-workspace/profiles/fedramp-rev5-low/profile.json`
  (no `modify` section -- baseline-mandated values come from `.tmp/fedramp-low-profile.xml`)

---

## FedRAMP Baseline-Mandated Parameters (AU family)

The following AU parameters have constraint values in the FedRAMP Rev 5 Low profile XML
(`.tmp/fedramp-low-profile.xml`) and are therefore **baseline-mandated** (origin `inherited`):

| Param ID | Mandated Value |
|---|---|
| `au-01_odp.05` | at least every 3 years (policy review frequency) |
| `au-01_odp.07` | at least annually (procedures review frequency) |
| `au-01_odp.08` | significant changes (update trigger) |
| `au-02_odp.01` | successful and unsuccessful account logon events, account management events, object access, policy change, privilege functions, process tracking, and system events. For Web applications: all administrator activity, authentication checks, authorization checks, data deletions, data access, data changes, and permission changes |
| `au-02_odp.04` | annually and whenever there is a change in the threat environment |
| `au-05_odp.03` | overwrite oldest record |
| `au-06_odp.01` | at least weekly |
| `au-08_odp` | one second granularity of time measurement |
| `au-11_odp` | a time period in compliance with M-21-31 (FedRAMP adds: at least 90 days online, off-line per NARA) |
| `au-12_odp.01` | all information system and network components where audit capability is deployed/available |

All other AU parameters (those NOT in the above table) are organization-defined
and will use homelab cadence values with origin `organization`.

---

## AU-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** This SSP and its ADR chain (`docs/adr/`) serve as the audit and accountability policy documentation for the Managed SOC Service (MSS).
- **Supporting mechanisms:** `CLAUDE.md` project reference (operating conventions), `runbooks/monthly-conmon.md` (monthly ConMon rhythm), ADR 0008 §3 (implementation status rubric, set-params policy), ADR 0007 (Plan 2 completion -- pipeline authority).
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (project-wide conventions, AU family context, service inventory)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0008-plan-3-pre-execution-realignment.md` (pre-execution decisions covering policy commitments)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0007-plan-2-complete.md` (done criteria, ConMon pipeline authority)
  - `/c/Projects/homelab-fedramp-low/runbooks/monthly-conmon.md` (procedures for recurring ConMon cycle)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0001-preflight-and-eula.md` (pre-flight policy review)
- **Set-params (proposed values):**
  - `au-1_prm_1` / `au-01_odp.01` and `au-01_odp.02` (personnel): `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `au-01_odp.03` (policy level): `["system-level"]`, origin `organization`
  - `au-01_odp.04` (official): `"Brian Chaplow, system owner"`, origin `organization`
  - `au-01_odp.05` (policy review frequency): `"at least every 3 years"`, origin `inherited` (baseline-mandated)
  - `au-01_odp.06` (policy update events): `"significant changes"`, origin `inherited` (baseline-mandated -- maps to au-01_odp.08)
  - `au-01_odp.07` (procedures review frequency): `"at least annually"`, origin `inherited` (baseline-mandated)
  - `au-01_odp.08` (procedures update events): `"significant changes"`, origin `inherited` (baseline-mandated)
- **Authoring notes:** Status is `partial` because the AU policy lives within the SSP itself and the ADR chain rather than as a standalone policy document -- appropriate for a single-operator system. The gap (no standalone policy document) should be named explicitly in the implementation prose. Designate Brian Chaplow as the responsible official under AU-1(b). Reference `runbooks/monthly-conmon.md` as the procedures artifact.

---

## AU-2 Event Logging

- **Status:** implemented
- **Primary mechanism:** Wazuh SIEM on brisket (15 agents, 214 detection rules) ingests endpoint security events, OPNsense firewall syslog, and Suricata IDS alerts into `wazuh-alerts-4.x-*` indices on the Wazuh Indexer (OpenSearch) at `brisket:9200`.
- **Supporting mechanisms:** Zeek on smokehouse eth4 AND haccp span0 (protocol metadata -- conn, dns, http, ssl, ssh, files, x509, notice, JA3/JA4/community-id); Suricata on smokehouse eth4 (47,487+ signature rules + 10 HOMELAB custom rules); ELK 8.17 on haccp (`logs-zeek.haccp-default-*` data stream via Logstash zeek-enrichment pipeline); Arkime full-PCAP on haccp span0; Shuffle WF2 (watch digest cron 0600/1800 EST).
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (brisket service inventory: Wazuh Manager ports, 15 agents, 214 rules; haccp: ELK + Arkime; smokehouse: Suricata + Zeek on eth4)
  - `/c/Projects/reference/host-details.md` lines 29-43 (`wazuh-alerts-4.x-*` index table, pipeline description, smokehouse Suricata/Zeek config)
  - `/c/Projects/reference/host-details.md` lines 213-233 (haccp Zeek 8.1.1 on span0, Logstash zeek-enrich pipeline, `logs-zeek.haccp-default-*` data stream)
  - `/c/Projects/reference/phase14/zeek/local.zeek` (haccp Zeek config: JSON output, JA3/JA4/community-id, local networks, protocol detection scripts)
  - `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` (5-stage enrichment pipeline: de-dot → OpenCTI TI → novel-entity → tier routing → Ollama, output to `logs-zeek.haccp-default-*`)
  - `/c/Projects/reference/phase14/filebeat/filebeat.yml` (Filebeat ships Zeek JSON from haccp → Logstash:5044)
  - `/c/Projects/HomeLab-SOC-v2/configs/suricata/suricata.yaml` (Suricata config: captures on eth4 SPAN, ET Open 47,487+ rules)
  - `/c/Projects/HomeLab-SOC-v2/configs/suricata/local.rules` (custom HOMELAB rules SID 9000001-9000021: SQLi, XSS, SQLmap, command injection, directory traversal)
  - `/c/Projects/brisket-setup/monitoring/build-soc-alerts-triage.py` line 499 (`wazuh-alerts-*` as dashboard data source)
  - `/c/Projects/brisket-setup/monitoring/generate-attack-layer.py` lines 249-254 (both `wazuh-alerts-*` and `logs-*` ELK queried for ATT&CK coverage)
- **Set-params (proposed values):**
  - `au-02_odp.01` (event types): `"successful and unsuccessful account logon events, account management events, object access, policy change, privilege functions, process tracking, and system events; plus network protocol metadata (conn, dns, http, ssl, ssh, files), IDS signature alerts, full-PCAP, and threat-intel-enriched tier events"`, origin `inherited` (baseline-mandated core + organization extension)
  - `au-2_prm_2` / `au-02_odp.02` and `au-02_odp.03` (logged event subset): `"all FedRAMP-mandated event types listed in AU-02_ODP[01] are logged continuously across all in-boundary agents"`, origin `organization`
  - `au-02_odp.04` (review frequency): `"annually and whenever there is a change in the threat environment"`, origin `inherited` (baseline-mandated)
- **Authoring notes:** AU-2 is the "hero control" for the SSP in-doc walkthrough (whole-project design §4.5, §15). Lead with Wazuh's 15-agent coverage and index pattern; second paragraph covers Zeek + Suricata + ELK dual-stack; cite `generate-attack-layer.py` as evidence that both stacks are coordinated for MITRE ATT&CK coverage. The FedRAMP-mandated `au-02_odp.01` event list is a baseline value -- inherit it verbatim plus the homelab extension.

---

## AU-3 Content of Audit Records

- **Status:** implemented
- **Primary mechanism:** Wazuh alert records in `wazuh-alerts-4.x-*` carry: rule description (event type), timestamp, agent hostname/IP (where), source IP/destination IP (source of event), rule level/action (outcome), and agent name/ID plus source user where available (identity fields) -- satisfying all six AU-3 content elements.
- **Supporting mechanisms:** Zeek logs in `logs-zeek.haccp-default-*` include `ts` (timestamp), `id_orig_h`/`id_resp_h` (source/destination), log type (`_path`), community-id for cross-correlation, JA3/JA4 fingerprints, and Ollama LLM classification (`llm.verdict`); Arkime PCAP captures packet-level source/destination/payload for forensic completeness.
- **Evidence paths:**
  - `/c/Projects/reference/host-details.md` lines 29-35 (Wazuh index table: `wazuh-alerts-4.x-*` content description)
  - `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` (Stage 0 de-dot producing `id_orig_h`, `id_resp_h`; Stage 4 Ollama verdict fields)
  - `/c/Projects/reference/phase14/zeek/local.zeek` (JSON output, community-id plugin -- enables cross-record correlation)
  - `/c/Projects/reference/phase14/es/haccp-entities-seen-mapping.json` (novel-entity index schema -- includes `first_seen`, `last_seen`, `entity_type`, `entity_value` fields)
- **Set-params (proposed values):**
  - (No set-params for AU-3 -- the control has no ODPs in the scaffold)
- **Authoring notes:** AU-3 has no parameters in the `x-trestle-set-params` YAML (the scaffold is param-free for this control). Implementation prose should walk through one Wazuh alert record field by field against the six AU-3 elements (a–f), then note that Zeek records carry the same elements at the network layer with community-id for cross-correlation to Arkime PCAP.

---

## AU-4 Audit Log Storage Capacity

- **Status:** implemented
- **Primary mechanism:** Wazuh Indexer (OpenSearch) on brisket uses the primary NVMe drive for `wazuh-alerts-*` index storage; Prometheus monitors disk utilization with a Grafana alert firing at 90% usage.
- **Supporting mechanisms:** ELK Elasticsearch on haccp uses a dedicated 2TB WD SN720 boot/root NVMe for `logs-zeek.haccp-default-*`; Arkime PCAP stored on a dedicated Samsung 990 EVO Plus 2TB NVMe at `/opt/arkime/raw` with `freeSpaceG=100` auto-delete policy; PCAP archived daily to smokehouse 17TB NFS (`~bchaplow/pcap-archive/haccp/`) with 90-day purge; Prometheus `--storage.tsdb.retention.time=90d` for metrics retention.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (haccp hardware: WD SN720 2TB boot + Samsung 990 EVO Plus 2TB PCAP, ~1.8TB usable; smokehouse 17TB NFS)
  - `/c/Projects/reference/host-details.md` lines 178-210 (haccp drive layout, Arkime `freeSpaceG=100`, PCAP at `/opt/arkime/raw`)
  - `/c/Projects/reference/phase14/pcap-archive-readme.md` (rsync archival to smokehouse, 90-day purge policy: `find ~bchaplow/pcap-archive/haccp/ -mtime +90 -delete`)
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` lines 1-8 (alert rules including "Disk Critical -- Usage Above 90%")
  - `/c/Projects/brisket-setup/monitoring/docker-compose.yml` lines 13-14 (`--storage.tsdb.retention.time=90d` Prometheus flag)
- **Set-params (proposed values):**
  - `au-04_odp` (retention requirements): `"Wazuh-alerts: hot storage on brisket NVMe, capacity monitored by Grafana alert at 90% disk usage; Zeek/ELK logs: haccp 2TB dedicated NVMe; PCAP: haccp 2TB NVMe with freeSpaceG=100 auto-purge + 90-day smokehouse archive; Prometheus metrics: 90-day TSDB retention"`, origin `organization`
- **Authoring notes:** The Grafana disk alert is the operational guard against silent capacity exhaustion -- cite `build-grafana-alerts.py` as evidence of proactive capacity monitoring. Note that AU-11's FedRAMP 90-day online requirement is met for PCAP by the smokehouse archive policy; Wazuh and ELK indices are retained for the life of the index (no automatic rollover configured -- this is a gap to name).

---

## AU-5 Response to Audit Logging Process Failures

- **Status:** partial
- **Primary mechanism:** Grafana Unified Alerting on brisket routes "Service Down" (HTTP probe failure), "Disk Critical" (>90% usage), and "Host Unreachable" (ICMP probe failure) alerts to Discord `#infrastructure-alerts` via the `discord-infrastructure` webhook -- providing human notification within 15 minutes of detection.
- **Supporting mechanisms:** GPU Thermal Critical alert (Grafana uid=dfihoiidr7k00c) routes to `#infrastructure-alerts` and can interrupt Ollama/Logstash enrichment if brisket GPU overheats; Shuffle WF2 watch digest (cron 0600/1800) reports on Wazuh alert volume gaps implicitly; ADR 0005 documents PBS backup failures going 5 days undetected due to absence of a targeted PBS failure alert.
- **Evidence paths:**
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` (4 alert rules: Service Down, Disk Critical, Host Unreachable, GPU Thermal Critical -- routes to `discord-infrastructure`)
  - `/c/Projects/CLAUDE.md` (Phase 14 thermal hardening notes: GPU alert uid=dfihoiidr7k00c, #infrastructure-alerts webhook `$discord_webhook_infra`)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (5-day gap went undetected -- explicit evidence of the gap this control is meant to close; Plan 1 Task 20 follow-up for PBS alert)
- **Set-params (proposed values):**
  - `au-05_odp.01` (personnel to alert): `"Brian Chaplow (system owner, sole operator) via Discord #infrastructure-alerts"`, origin `organization`
  - `au-05_odp.02` (time period): `"within 15 minutes (Grafana alert evaluation window + Discord delivery)"`, origin `organization`
  - `au-05_odp.03` (additional actions): `"overwrite oldest record"`, origin `inherited` (baseline-mandated)
- **Authoring notes:** Status is `partial` because audit logging process failures (disk full, Wazuh indexer down, Filebeat/Logstash pipeline failure) are not specifically alerted on -- the current alerts cover disk capacity and host reachability but not Wazuh indexer health or Logstash pipeline errors. ADR 0005 is the concrete evidence of this gap; cite it explicitly. The second prose paragraph should name the gap: no dedicated alerting on indexer unavailability or Logstash pipeline errors -- these are monitoring gaps planned in the ConMon roadmap (Plan 2 Task 12's PBS alert TODO).

---

## AU-6 Audit Record Review, Analysis, and Reporting

- **Status:** implemented
- **Primary mechanism:** Shuffle WF2 (watch digest, cron 0600/1800 EST) queries `wazuh-alerts-4.x-*` for the preceding 12 hours and delivers a MITRE ATT&CK-correlated alert summary to Discord `#soc-alerts` -- providing twice-daily audit record review at operator-set frequency exceeding the FedRAMP-mandated weekly minimum.
- **Supporting mechanisms:** Shuffle WF10 (nightly briefing, cron 0530 EST) ingests Phase 14 Zeek enrichment results from `logs-zeek.haccp-default-*` and delivers an Ollama-generated threat briefing to Discord `#morning-briefing`; Wazuh Dashboard (brisket:5601) and Kibana (haccp:5601) provide on-demand review and search; generate-attack-layer.py produces ATT&CK Navigator layer from both stacks for cross-stack MITRE coverage reporting; ADR 0005 documents that audit record review caught a PBS backup failure (5-day gap discovered via log analysis during Plan 1 Task 12).
- **Evidence paths:**
  - `/c/Projects/reference/shuffle-wf2-watch-turnover.json` (WF2 baseline: queries `wazuh-alerts-4.x-*`, Ollama assessment, Discord delivery)
  - `/c/Projects/reference/phase14/shuffle/wf10-baseline-20260408.json` (WF10 nightly briefing baseline: queries both Wazuh and ELK stacks)
  - `/c/Projects/CLAUDE.md` (Shuffle Backend: WF2 cron 0600/1800, WF10 cron 0530 EST; `$discord_webhook_briefing` variable)
  - `/c/Projects/brisket-setup/monitoring/generate-attack-layer.py` lines 249-255 (cross-stack MITRE reporting)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (audit-based detection: log review during Plan 1 Task 12 discovered 5-day PBS backup failure -- a concrete AU-6 auditable example)
  - `/c/Projects/brisket-setup/monitoring/build-soc-alerts-triage.py` line 499 (Wazuh Dashboard data source configured against `wazuh-alerts-*`)
- **Set-params (proposed values):**
  - `au-06_odp.01` (review frequency): `"at least weekly"`, origin `inherited` (baseline-mandated -- actual practice is twice-daily via WF2 and daily via WF10, which exceeds the FedRAMP floor)
  - `au-06_odp.02` (inappropriate/unusual activity): `"MITRE ATT&CK technique detections, rule.level >= 8 alerts, novel entity detections (tier2_novel), threat-intel matches (tier1_ti_match), authentication failures exceeding 5 attempts, and scan/reconnaissance signatures from Suricata"`, origin `organization`
  - `au-06_odp.03` (reporting personnel): `"Brian Chaplow (system owner, sole operator) via Discord #soc-alerts and #morning-briefing"`, origin `organization`
- **Authoring notes:** Lead with WF2's twice-daily automated review (which satisfies "at least weekly" with room to spare). Second paragraph: use ADR 0005 as the concrete "what this looks like in practice" -- audit record review during Plan 1 caught a 5-day PBS backup failure that had gone unnoticed by all other means. This is the SSP's strongest real-world AU-6 evidence. Note the FedRAMP additional requirement: "coordination between service provider and consumer shall be documented" -- for the single-tenant homelab, this reduces to the operator being both provider and consumer.

---

## AU-8 Time Stamps

- **Status:** implemented
- **Primary mechanism:** All in-boundary Linux hosts (brisket, haccp, smokehouse, dojo, regscale) run `systemd-timesyncd` synchronized to pool.ntp.org (Ubuntu 24.04 default), providing sub-second clock accuracy; Wazuh alerts carry ISO 8601 UTC timestamps with millisecond granularity in the `timestamp` field.
- **Supporting mechanisms:** Zeek logs on both smokehouse and haccp include `ts` field in Unix epoch with microsecond precision; ELK Elasticsearch stores all `@timestamp` fields as UTC epoch milliseconds; Arkime PCAP timestamps captured at kernel packet-capture precision (microsecond); OPNsense firewall synchronizes via NTP to pool.ntp.org; Phase 14 community-id enrichment relies on NTP-consistent timestamps for cross-source correlation.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (all in-boundary hosts listed: brisket Ubuntu 24.04, haccp Ubuntu 24.04, dojo/regscale Ubuntu 24.04.4 LTS)
  - `/c/Projects/reference/phase14/plan-corrections-20260409.md` line 203 (NTP protocol logging confirmed active: "NTP (time sync)" identified as a covered Zeek protocol)
  - `/c/Projects/reference/phase14/zeek/community-id-propagate.zeek` line 199-204 (NTP log hook defined -- Zeek capturing NTP protocol events, confirming NTP traffic is monitored)
  - `/c/Projects/reference/phase14/zeek/local.zeek` line 6 (`LogAscii::use_json = T` -- JSON output with full timestamp fidelity)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0002-deployment-complete.md` (dojo + regscale: Ubuntu 24.04.4 LTS, kernel 6.8.0-107-generic -- systemd-timesyncd active by default on this kernel)
- **Set-params (proposed values):**
  - `au-08_odp` (granularity): `"one second granularity of time measurement"`, origin `inherited` (baseline-mandated -- actual implementation provides millisecond granularity on Wazuh, microsecond on Zeek/Arkime, which exceeds the floor)
- **Authoring notes:** Ubuntu 24.04's `systemd-timesyncd` is active by default on all in-boundary hosts -- no explicit config file to cite, but the OS version is verifiable from ADR 0002 and CLAUDE.md. Note that the FedRAMP baseline mandates 1-second granularity; the actual implementation (ms on Wazuh, µs on Zeek/Arkime) exceeds this. Use UTC as the reference for all timestamps. The Zeek community-id propagation to NTP logs (community-id-propagate.zeek lines 199-204) is a useful technical detail showing awareness of time-protocol monitoring.

---

## AU-9 Protection of Audit Information

- **Status:** partial
- **Primary mechanism:** Wazuh Indexer (OpenSearch) on brisket requires TLS (`HTTPS:9200`) and basic authentication (`admin` account with password from `.env`); Wazuh Manager Docker stack enforces role-based access control through the Wazuh Dashboard; ELK Elasticsearch on haccp requires TLS (`HTTPS:9200`) with `elastic` user authentication.
- **Supporting mechanisms:** Both OpenSearch (brisket) and Elasticsearch (haccp) run in Docker networks with no host-port exposure beyond the documented service ports; Wazuh alert indices are write-only from the Wazuh Manager container -- agents cannot directly write to or delete from indices; PCAP files on haccp `/opt/arkime/raw` are owned by `nobody:daemon` (Arkime drops privileges after start per `dropUser=nobody`/`dropGroup=daemon`); `$discord_webhook_infra` alert fires on host unreachability, alerting to tampering attempts that take a monitored host offline.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (Wazuh Indexer port 9200 HTTPS, `admin` credentials in `.env`; ELK Elasticsearch port 9200 HTTPS, `elastic` credentials in `.env`)
  - `/c/Projects/reference/host-details.md` lines 195-206 (Arkime `dropUser=nobody`/`dropGroup=daemon`, PCAP at `/opt/arkime/raw` owned by `nobody:daemon`)
  - `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` (alert on host unreachability -- indirect protection: tampering that kills monitored hosts triggers an alert)
  - `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` lines 287-299 (Logstash output to Elasticsearch with TLS and credential authentication)
- **Set-params (proposed values):**
  - `au-09_odp` (personnel to alert on unauthorized access): `"Brian Chaplow (system owner, sole operator) via Discord #infrastructure-alerts (Grafana alert on host unreachability)"`, origin `organization`
- **Authoring notes:** Status is `partial` because audit information protection relies on OS-level access controls and Docker network isolation rather than formal write-once/WORM storage or cryptographic integrity verification of audit records. There is no dedicated file-integrity monitoring on the Wazuh index datastore itself (though Wazuh FIM can monitor host filesystem paths -- wiring it to watch the Docker volume mount points would close this gap). Name both the mechanism and the gap explicitly. The `.env` credential management (not committed to git per CLAUDE.md convention) is the primary secret-protection measure.

---

## AU-11 Audit Record Retention

- **Status:** partial
- **Primary mechanism:** Wazuh alerts (`wazuh-alerts-4.x-*`) are retained on brisket's OpenSearch indexer for the life of the index with no automatic rollover or deletion policy configured; Arkime PCAP on haccp is archived daily to smokehouse 17TB NFS and purged from the smokehouse archive after 90 days.
- **Supporting mechanisms:** ELK `logs-zeek.haccp-default-*` data stream retained on haccp 2TB NVMe until disk capacity triggers auto-deletion via Elasticsearch ILM (policy not yet explicitly configured -- gap); Prometheus metrics retained 90 days (`--storage.tsdb.retention.time=90d`); PBS backups on smokehouse 17TB NFS retain VM snapshots (daily critical + weekly jobs).
- **Evidence paths:**
  - `/c/Projects/reference/phase14/pcap-archive-readme.md` (PCAP archival: daily rsync at 0300 from haccp `/opt/arkime/raw` → smokehouse `~bchaplow/pcap-archive/haccp/`; 90-day purge via `find ... -mtime +90 -delete`)
  - `/c/Projects/reference/host-details.md` line 195 (Arkime `freeSpaceG=100` local auto-delete policy, 2TB NVMe)
  - `/c/Projects/brisket-setup/monitoring/docker-compose.yml` lines 13-14 (Prometheus `--storage.tsdb.retention.time=90d`)
  - `/c/Projects/CLAUDE.md` (PBS on smoker LXC 300 -- NFS→smokehouse 17TB, daily/weekly backup jobs; ADR 0005 PBS gap context)
  - `/c/Projects/homelab-fedramp-low/docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (PBS backup gap discovery -- auditable example of retention monitoring failure; fix with automount hardening)
- **Set-params (proposed values):**
  - `au-11_odp` (retention period): `"a time period in compliance with M-21-31 -- at least 90 days online; PCAP archived to smokehouse 17TB NAS for 90-day off-line retention; Wazuh-alerts retained for the duration of the index (no explicit rollover cap); no formal NARA-mapped off-line archive policy for endpoint event logs"`, origin `inherited` (baseline-mandated constraint) with organization-specific values
- **Authoring notes:** FedRAMP AU-11 requires 90 days online and off-line per NARA (as extended by M-21-31). PCAP meets the 90-day online requirement via local 2TB NVMe and smokehouse archive. However, Wazuh alert indices have no explicit ILM policy -- they retain until disk is full. This is technically permissive (never deletes, so always >= 90 days) but is not a policy-backed statement. Name this gap: no formal ILM lifecycle policy for `wazuh-alerts-*` or `logs-zeek.haccp-default-*` -- records are retained by default (disk not full) but not by documented policy. This is the honest partial.

---

## AU-12 Audit Record Generation

- **Status:** implemented
- **Primary mechanism:** Wazuh Manager on brisket generates audit records for all 15 in-boundary agents (FIM, process monitoring, log analysis, SCA, vulnerability detection) and ships them to `wazuh-alerts-4.x-*` on the Wazuh Indexer; Logstash on haccp generates enriched audit records from Zeek JSON logs into `logs-zeek.haccp-default-*` via the 5-stage zeek-enrichment pipeline.
- **Supporting mechanisms:** Suricata on smokehouse generates IDS alert records (eve.json) shipped via Wazuh agent to `wazuh-alerts-*`; Zeek on smokehouse generates protocol metadata records (conn, dns, http, ssl, ssh, files, notice) shipped via Fluent Bit to `zeek-*` indices on brisket; Zeek on haccp span0 generates JA3/JA4/community-id enriched protocol records; Arkime on haccp generates PCAP index records in its own database; Wazuh Dashboard (`brisket:5601`) allows authorized operator to select event types via rule groups, agents, and SCA policies (AU-12b compliance).
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (brisket: Wazuh Manager 1514/1515/514UDP/55000, 15 agents, 214 detection rules, Wazuh Indexer 9200; haccp: ES 8.17 + Kibana + Fleet + Logstash, 4 Fleet agents, 214 detection rules, `logs-zeek.haccp-default-*`)
  - `/c/Projects/reference/host-details.md` lines 29-43 (all `zeek-*` and `wazuh-alerts-*` index patterns, data pipeline description)
  - `/c/Projects/reference/host-details.md` lines 68-128 (smokehouse active containers: `suricata-live`, `zeek`, `fluent-bit-zeek`, `wazuh-agent`, `elastic-agent`)
  - `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` (Logstash 5-stage pipeline generating `logs-zeek.haccp-default-*` records with TI enrichment, LLM classification)
  - `/c/Projects/reference/phase14/filebeat/filebeat.yml` (Filebeat Zeek input → Logstash:5044)
  - `/c/Projects/brisket-setup/monitoring/generate-attack-layer.py` lines 249-254 (audit record generation verified by querying both stacks for MITRE technique coverage)
  - `/c/Projects/homelab-fedramp-low/oscal/component-definition.json` (7 in-boundary components listed, all with audit capability mapped)
- **Set-params (proposed values):**
  - `au-12_odp.01` (system components): `"all information system and network components where audit capability is deployed/available"`, origin `inherited` (baseline-mandated) -- in homelab: brisket (Wazuh Manager + Indexer + Shuffle + Velociraptor + OpenCTI + ml-scorer), haccp (ELK + Arkime + Zeek + Logstash + Filebeat), smokehouse (Suricata + Zeek + Fluent Bit + Wazuh agent), OPNsense (syslog → Wazuh), MokerLink (no direct log shipping), dojo (Wazuh agent 016), regscale (Wazuh agent 017)
  - `au-12_odp.02` (personnel with selection authority): `"Brian Chaplow (system owner, sole operator) via Wazuh Dashboard (brisket:5601), Wazuh Manager rule configuration, and Logstash pipeline configuration (haccp)"`, origin `organization`
- **Authoring notes:** AU-12 closes the loop on AU-2 (capability) and AU-3 (content) -- the generation step. Lead with the dual-stack architecture (Wazuh on brisket for endpoint/IDS/firewall events; ELK/Logstash on haccp for enriched Zeek records). Cite `component-definition.json` as the OSCAL-native evidence that all components are enumerated. Note that MokerLink (the L3 switch) does not ship logs directly -- it is a monitoring gap; syslog from OPNsense substitutes for boundary traffic events.
