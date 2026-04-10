# Gate 3 Evidence-Path Spot-Check Audit

**Auditor:** Claude Code (independent reviewer, no catalog authorship)
**Date:** 2026-04-09
**Scope:** 18 FedRAMP Low evidence catalog files in `docs/plan-3/evidence-catalog/`
**Method:** Per-family path verification — min(10, control_count) paths sampled across controls; each path checked via `ls` or `Read` on the local filesystem; live index names (ELK/OpenSearch data streams) skipped
**Protocol:** Paths with `/c/Projects/homelab-fedramp-low/` prefix OR no prefix (repo-relative) checked against repo root; paths with `/c/Projects/` prefix checked against parent workspace

---

## AC — Access Control (11 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| AC-1 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |
| AC-2 | `inventory/overlay.yaml` | VERIFIED |
| AC-2 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| AC-3 | `/c/Projects/reference/network.md` | VERIFIED |
| AC-3 | `docs/adr/0008-zeek-community-id-tier1-rollout.md` | VERIFIED |
| AC-4 | `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` | VERIFIED |
| AC-7 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| AC-17 | `runbooks/cert-trust.md` | VERIFIED |
| AC-17 | `deploy/proxmox/dojo-vm-config.yaml` | VERIFIED |
| AC-19 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## AT — Awareness and Training (5 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| AT-1 | `trestle-workspace/mss-ssp/at/at-1.md` | VERIFIED |
| AT-2 | `runbooks/monthly-conmon.md` | VERIFIED |
| AT-3 | `/c/Projects/brisket-setup/monitoring/build-threat-intel-soc.py` | VERIFIED |
| AT-3 | `/c/Projects/reference/phase14/zeek/local.zeek` | VERIFIED |
| AT-4 | `docs/adr/0002-deployment-complete.md` | VERIFIED |

**Family result:** 5/5 VERIFIED, 0 MISSING

---

## AU — Audit and Accountability (10 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| AU-2 | `/c/Projects/reference/host-details.md` | VERIFIED |
| AU-3 | `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` | VERIFIED |
| AU-3 | `/c/Projects/reference/phase14/filebeat/filebeat.yml` | VERIFIED |
| AU-3 | `/c/Projects/reference/phase14/zeek/community-id-propagate.zeek` | VERIFIED |
| AU-4 | `/c/Projects/reference/phase14/es/haccp-entities-seen-mapping.json` | VERIFIED |
| AU-6 | `/c/Projects/reference/shuffle-wf2-watch-turnover.json` | VERIFIED |
| AU-6 | `/c/Projects/reference/phase14/shuffle/wf10-baseline-20260408.json` | VERIFIED |
| AU-8 | `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` | VERIFIED |
| AU-9 | `/c/Projects/brisket-setup/monitoring/docker-compose.yml` | VERIFIED |
| AU-12 | `oscal/component-definition.json` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## CA — Assessment, Authorization, and Monitoring (10 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| CA-1 | `trestle-workspace/profiles/fedramp-rev5-low/profile.json` | VERIFIED |
| CA-2 | `pipelines/build/oscal_poam.py` | VERIFIED |
| CA-3 | `oscal/ssp.json` | VERIFIED |
| CA-5 | `poam/POAM-2026-04.xlsx` | VERIFIED |
| CA-6 | `trestle-workspace/catalogs/nist-800-53-rev5/catalog.json` | VERIFIED |
| CA-7 | `runbooks/monthly-conmon.md` | VERIFIED |
| CA-7 | `inventory/IIW-2026-04.xlsx` | VERIFIED |
| CA-8 | `deploy/defectdojo/post-install.sh` | VERIFIED |
| CA-9 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |
| CA-9 | `docs/adr/0002-deployment-complete.md` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## CM — Configuration Management (9 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| CM-1 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |
| CM-2 | `/c/Projects/homelab-soc-portfolio/wazuh/configs/ossec.conf` | VERIFIED |
| CM-2 | `/c/Projects/brisket-setup/monitoring/prometheus.yml` | VERIFIED |
| CM-3 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| CM-6 | `/c/Projects/reference/phase14/zeek/networks.cfg` | VERIFIED |
| CM-6 | `/c/Projects/reference/phase14/zeek/node.cfg` | VERIFIED |
| CM-7 | `inventory/overlay.yaml` | VERIFIED |
| CM-8 | `inventory/IIW-2026-04.xlsx` | VERIFIED |
| CM-8 | `pipelines/ingest/inventory.py` | VERIFIED |
| CM-10 | `deploy/proxmox/dojo-vm-config.yaml` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## CP — Contingency Planning (6 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| CP-1 | `runbooks/monthly-conmon.md` | VERIFIED |
| CP-2 | `deploy/proxmox/README.md` | VERIFIED |
| CP-4 | `tests/smoke/check_defectdojo.sh` | VERIFIED |
| CP-4 | `tests/smoke/check_regscale.sh` | VERIFIED |
| CP-9 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| CP-10 | `runbooks/restore-from-pbs.md` | VERIFIED |

**Family result:** 6/6 VERIFIED, 0 MISSING

---

## IA — Identification and Authentication (16 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| IA-1 | `trestle-workspace/mss-ssp/ia/ia-1.md` | VERIFIED |
| IA-2 | `trestle-workspace/mss-ssp/ia/ia-2.md` | VERIFIED |
| IA-2.12 | `trestle-workspace/mss-ssp/ia/ia-2.12.md` | VERIFIED |
| IA-3 | `docs/adr/0003-regscale-install-deviation.md` | VERIFIED |
| IA-4 | `inventory/overlay.yaml` | VERIFIED |
| IA-5 | `deploy/regscale/install.sh` | VERIFIED |
| IA-5.1 | `trestle-workspace/mss-ssp/ia/ia-5.1.md` | VERIFIED |
| IA-6 | `runbooks/cert-trust.md` | VERIFIED |
| IA-7 | `docs/adr/0006-plan-2-environment-and-api-realignment.md` | VERIFIED |
| IA-8 | `pipelines/common/wazuh.py` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## IR — Incident Response (7 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| IR-1 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| IR-2 | `runbooks/monthly-conmon.md` | VERIFIED |
| IR-4 | `oscal/component-definition.json` | VERIFIED |
| IR-5 | `poam/POAM-2026-04.xlsx` | VERIFIED |
| IR-6 | `oscal/ssp.json` | VERIFIED |
| IR-8 | `runbooks/restore-from-pbs.md` | VERIFIED |
| IR-8 | `docs/adr/0002-deployment-complete.md` | VERIFIED |

**Family result:** 7/7 VERIFIED, 0 MISSING

---

## MA — Maintenance (4 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| MA-1 | `/c/Projects/CLAUDE.md` | VERIFIED |
| MA-1 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| MA-2 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| MA-2 | `runbooks/monthly-conmon.md` | VERIFIED |

**Family result:** 4/4 VERIFIED, 0 MISSING

---

## MP — Media Protection (4 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| MP-1 | `/c/Projects/CLAUDE.md` | VERIFIED |
| MP-1 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| MP-1 | `runbooks/monthly-conmon.md` | VERIFIED |
| MP-2 | `inventory/overlay.yaml` | VERIFIED |
| MP-6 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| MP-7 | `runbooks/restore-from-pbs.md` | VERIFIED |

**Family result:** 6/6 VERIFIED, 0 MISSING

---

## PE — Physical and Environmental Protection (10 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| PE-1 | `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` | VERIFIED |
| PE-1 | `/c/Projects/docs/superpowers/specs/2026-03-11-rack-build-design.md` | VERIFIED |
| PE-2 | `inventory/overlay.yaml` | VERIFIED |
| PE-3 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |
| PE-6 | `/c/Projects/brisket-setup/monitoring/build-grafana-alerts.py` | VERIFIED |
| PE-8 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| PE-12 | `docs/adr/0003-regscale-install-deviation.md` | VERIFIED |
| PE-13 | `docs/adr/0004-defectdojo-install-deviation.md` | VERIFIED |
| PE-14 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| PE-17 | `inventory/IIW-2026-04.xlsx` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## PL — Planning (7 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| PL-1 | `trestle-workspace/profiles/fedramp-rev5-low/profile.json` | VERIFIED |
| PL-2 | `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` | VERIFIED |
| PL-2 | `oscal/ssp.json` | VERIFIED |
| PL-4 | `deploy/defectdojo/README.md` | VERIFIED |
| PL-4 | `deploy/regscale/README.md` | VERIFIED |
| PL-8 | `trestle-workspace/catalogs/fedramp-rev5-low-resolved/catalog.json` | VERIFIED |
| PL-8 | `runbooks/cert-trust.md` | VERIFIED |

**Family result:** 7/7 VERIFIED, 0 MISSING

---

## PS — Personnel Security (9 controls, mostly N/A)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| PS-1 | `README.md` | VERIFIED |
| PS-2 | `LICENSE` | VERIFIED |
| PS-3 | `deploy/defectdojo/README.md` | VERIFIED |
| PS-4 | `deploy/regscale/README.md` | VERIFIED |
| PS-5 | `trestle-workspace/mss-ssp/ps/ps-5.md` | VERIFIED |

**Family result:** 5/5 VERIFIED, 0 MISSING

---

## RA — Risk Assessment (8 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| RA-1 | `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` | **MISSING** — cited without `/c/Projects/` prefix; file exists only at `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` (parent workspace), not as a repo-relative path |
| RA-2 | `pipelines/ingest/inventory.py` | VERIFIED |
| RA-3 | `poam/POAM-2026-04.xlsx` | VERIFIED |
| RA-5 | `docs/adr/0007-wazuh-agent-vuln-scan-deviation.md` | VERIFIED |
| RA-5 | `pipelines/ingest/defectdojo.py` | VERIFIED |
| RA-5 | `tests/test_wazuh_vulns_ingest.py` | VERIFIED |
| RA-7 | `inventory/overlay.yaml` | VERIFIED |
| RA-9 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |

**Family result:** 7/8 VERIFIED, 1 MISSING

---

## SA — System and Services Acquisition (multiple controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| SA-1 | `deploy/defectdojo/README.md` | VERIFIED |
| SA-1 | `deploy/regscale/README.md` | VERIFIED |
| SA-3 | `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` | **MISSING** — cited without `/c/Projects/` prefix; file exists only at `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md` (parent workspace), not as a repo-relative path |
| SA-4 | `docs/adr/0003-regscale-install-deviation.md` | VERIFIED |
| SA-4 | `docs/adr/0004-defectdojo-install-deviation.md` | VERIFIED |
| SA-5 | `runbooks/restore-from-pbs.md` | VERIFIED |
| SA-8 | `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` | **MISSING** — cited without `/c/Projects/` prefix; file exists only at `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` (parent workspace), not as a repo-relative path |
| SA-9 | `inventory/overlay.yaml` | VERIFIED |
| SA-11 | `pipelines/build/oscal_component.py` | VERIFIED |
| SA-22 | `docs/adr/0006-plan-2-environment-and-api-realignment.md` | VERIFIED |

**Family result:** 8/10 VERIFIED, 2 MISSING

---

## SC — System and Communications Protection (14 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| SC-1 | `/c/Projects/reference/network.md` | VERIFIED |
| SC-5 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| SC-7 | `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` | VERIFIED |
| SC-8 | `runbooks/cert-trust.md` | VERIFIED |
| SC-12 | `docs/adr/0003-regscale-install-deviation.md` | VERIFIED |
| SC-13 | `docs/adr/0004-defectdojo-install-deviation.md` | VERIFIED |
| SC-20 | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` | VERIFIED |
| SC-28 | `docs/adr/0008-zeek-community-id-tier1-rollout.md` | VERIFIED |
| SC-39 | `inventory/overlay.yaml` | VERIFIED |
| SC-39 | `oscal/ssp.json` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## SI — System and Information Integrity (6 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| SI-2 | `/c/Projects/HomeLab-SOC-v2/configs/suricata/suricata.yaml` | VERIFIED |
| SI-3 | `/c/Projects/reference/phase14/logstash/zeek-enrichment.conf` | VERIFIED |
| SI-3 | `/c/Projects/reference/phase14/zeek/local.zeek` | VERIFIED |
| SI-4 | `/c/Projects/reference/phase14/logstash/ruby/tier2_rate_limit.rb` | VERIFIED |
| SI-4 | `/c/Projects/reference/phase14/logstash/ruby/novel_entity.rb` | VERIFIED |
| SI-4 | `/c/Projects/brisket-setup/monitoring/provisioning/alerting/discord.yml` | VERIFIED |
| SI-5 | `/c/Projects/reference/phase14/shuffle/wf10-haccp-embed-20260409.json` | VERIFIED |
| SI-7 | `/c/Projects/reference/phase14/cron/archive-pcap.sh` | VERIFIED |
| SI-12 | `tests/test_wazuh_vulns_ingest.py` | VERIFIED |
| SI-12 | `poam/POAM-2026-04.xlsx` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## SR — Supply Chain Risk Management (11 controls)

| Control | Evidence Path | Status |
|---------|--------------|--------|
| SR-1 | `inventory/overlay.yaml` | VERIFIED |
| SR-2 | `/c/Projects/CLAUDE.md` | VERIFIED |
| SR-3 | `inventory/IIW-2026-04.xlsx` | VERIFIED |
| SR-5 | `deploy/defectdojo/README.md` | VERIFIED |
| SR-5 | `pyproject.toml` | VERIFIED |
| SR-6 | `pipelines/ingest/inventory.py` | VERIFIED |
| SR-8 | `docs/adr/0002-deployment-complete.md` | VERIFIED |
| SR-9 | `docs/adr/0001-initial-boundary-and-scope.md` | VERIFIED |
| SR-11 | `docs/adr/0004-defectdojo-install-deviation.md` | VERIFIED |
| SR-11 | `docs/adr/0003-regscale-install-deviation.md` | VERIFIED |

**Family result:** 10/10 VERIFIED, 0 MISSING

---

## Audit Summary

| Family | Controls | Paths Checked | Verified | Missing |
|--------|----------|--------------|----------|---------|
| AC | 11 | 10 | 10 | 0 |
| AT | 5 | 5 | 5 | 0 |
| AU | 10 | 10 | 10 | 0 |
| CA | 10 | 10 | 10 | 0 |
| CM | 9 | 10 | 10 | 0 |
| CP | 6 | 6 | 6 | 0 |
| IA | 16 | 10 | 10 | 0 |
| IR | 7 | 7 | 7 | 0 |
| MA | 4 | 4 | 4 | 0 |
| MP | 4 | 6 | 6 | 0 |
| PE | 10 | 10 | 10 | 0 |
| PL | 7 | 7 | 7 | 0 |
| PS | 9 | 5 | 5 | 0 |
| RA | 8 | 8 | 7 | **1** |
| SA | ~10 | 10 | 8 | **2** |
| SC | 14 | 10 | 10 | 0 |
| SI | 6 | 10 | 10 | 0 |
| SR | 11 | 10 | 10 | 0 |
| **TOTAL** | **161** | **148** | **145** | **3** |

**Overall pass rate:** 145/148 = **97.97%**

**Families requiring correction: `ra`, `sa`**

---

## Missing Paths — Correction Required

All 3 missing paths share the same root cause: the `docs/superpowers/specs/` directory exists only in the **parent workspace** (`/c/Projects/docs/superpowers/specs/`), not inside the `homelab-fedramp-low` repo itself. The catalogs cite these paths without the required `/c/Projects/` prefix.

### RA-1
- **Cited as:** `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`
- **Correct absolute path:** `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`
- **Action:** Update `docs/plan-3/evidence-catalog/ra.md` RA-1 evidence path to use the full `/c/Projects/` prefix

### SA-3
- **Cited as:** `docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`
- **Correct absolute path:** `/c/Projects/docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`
- **Action:** Update `docs/plan-3/evidence-catalog/sa.md` SA-3 evidence path to use the full `/c/Projects/` prefix

### SA-8
- **Cited as:** `docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`
- **Correct absolute path:** `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`
- **Action:** Update `docs/plan-3/evidence-catalog/sa.md` SA-8 evidence path to use the full `/c/Projects/` prefix

---

## Notes

- **Live index names skipped** (not file paths): `logs-zeek.haccp-default-*`, `wazuh-alerts-*`, `zeek-*`, `haccp-entities-seen`, `honeypot-*`, `apache-parsed-v2` — these are ELK/OpenSearch data stream identifiers, not filesystem paths
- **Claude memory file** (`/c/Users/bchap/.claude/projects/C--Projects/memory/rack_build_2026-04-07.md`) cited in the MA catalog was verified as present but is not a repo artifact — it is the operator's persistent memory file. The path resolves correctly.
- **SA catalog self-disclosure:** The SA catalog's own "unresolved questions" section already flagged the SA-3 path inconsistency. Gate 3 independently confirms and records it.
- **No catalog-authorship bias:** All verification performed independently via `ls` / `Read` checks with no reference to the catalog's own assessments.
