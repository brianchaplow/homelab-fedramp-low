# CP — Contingency Planning: Evidence Catalog

**Family:** CP — Contingency Planning
**Controls in FedRAMP Rev 5 Low baseline:** cp-1, cp-2, cp-3, cp-4, cp-9, cp-10
**Catalog date:** 2026-04-09
**Author:** Plan 3 Phase 1 subagent

---

## How to read this catalog

Each control has six standard headings:

1. **Control summary** — what the control requires
2. **Implementation status** — `implemented`, `partial`, or `planned`
3. **What is implemented** — specific mechanisms in production
4. **Gaps / open items** — honest gaps driving the status rating
5. **Evidence paths** — verified file paths in this repo; all paths confirmed to exist as of catalog date
6. **ODP values** — organization-defined parameter values; baseline-mandated values noted where FedRAMP fixes them

---

## CP-1 — Contingency Planning Policy and Procedures

### Control summary

Develop, document, and disseminate a contingency planning policy addressing purpose, scope, roles, responsibilities, management commitment, coordination, and compliance. Designate an official to manage policy and procedures. Review and update policy on a defined frequency and after defined events.

### Implementation status

`planned`

### What is implemented

No dedicated contingency planning policy document exists in the repository. The closest artifacts are:

- ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`) documents the decision to implement automated NFS automount hardening after a backup failure was discovered, demonstrating reactive contingency decision-making.
- `runbooks/restore-from-pbs.md` establishes informal recovery procedures for the two in-boundary GRC VMs (dojo, regscale).
- `runbooks/monthly-conmon.md` establishes a daily manual PBS backup tripwire as an interim monitoring procedure.
- The system owner (Brian Chaplow) is the de facto sole contingency role; no documented role assignment exists.

### Gaps / open items

- No formal CP policy document authored (purpose, scope, roles, responsibilities, management commitment, compliance references).
- No designated official entry beyond implicit system-owner role.
- No defined review frequency or triggering events committed to in a policy artifact.
- CP policy and procedures are the SSP Plan 3 authoring deliverable for this control; prose will reference ADR 0005 and the restore runbook as the procedure corpus.

### Evidence paths

- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` — reactive CP decision record (NFS automount hardening)
- `runbooks/restore-from-pbs.md` — informal recovery procedures (dojo, regscale)
- `runbooks/monthly-conmon.md` — interim backup monitoring tripwire (§"Daily PBS backup tripwire")

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Personnel or roles (policy dissemination) | cp-01_odp.01 | System Owner (Brian Chaplow) | organization |
| Personnel or roles (procedure dissemination) | cp-01_odp.02 | System Owner (Brian Chaplow) | organization |
| Official (policy manager) | cp-01_odp.03 | System Owner (Brian Chaplow) | organization |
| Policy review frequency | cp-01_odp.04 | annually | organization |
| Events triggering policy review | cp-01_odp.05 | significant system change, security incident, or external audit finding | organization |
| Procedure review frequency | cp-01_odp.06 | annually | organization |
| Events triggering procedure review | cp-01_odp.07 | significant system change, security incident, or external audit finding | organization |
| Selection (policy level) | cp-01_odp.08 | system-level | organization |

---

## CP-2 — Contingency Plan

### Control summary

Develop a contingency plan for the system that identifies essential mission and business functions, recovery objectives, restoration priorities, metrics, contingency roles and responsibilities, procedures for maintaining essential functions during a disruption, full system restoration approach, and information-sharing approach. The plan must be reviewed, approved, distributed, coordinated with incident handling, and updated after changes or lessons learned.

### Implementation status

`partial`

### What is implemented

The following partial elements are in place:

- **Recovery procedures documented:** `runbooks/restore-from-pbs.md` provides step-by-step restore commands for dojo (VMID 201 on pitcrew) and regscale (VMID 301 on smoker) from PBS LXC 300 snapshots. Procedure covers snapshot verification, VM stop, pre-restore config preservation, `qmrestore` invocation, startup, and smoke check validation.
- **Backup chain documented:** `deploy/proxmox/README.md` documents the PBS backup job schedule (pitcrew job at 02:00, smoker job at 02:30), storage target (`pbs-smokehouse` → `10.10.20.10:/pbs-datastore`), and the NFS automount hardening from ADR 0005.
- **Incident-to-recovery linkage:** ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`) documents a real contingency event (5-day backup gap 2026-04-03 to 2026-04-07) including root cause, corrective action, and consequences — the structural equivalent of a lessons-learned section.
- **Essential system components identified (implicitly):** The critical backup job covers DC01 (VMID 100), WS01 (VMID 101), TheHive (VMID 200), dojo (VMID 201), and regscale (VMID 301), implying these are the essential components.
- **FedRAMP DR Form template available:** `templates/FedRAMP-DR-Form.xlsx` downloaded 2026-04-08 from fedramp.gov (Rev 5).

### Gaps / open items

- No formal contingency plan document authored (CP-2.a.1 through CP-2.a.7 require a single document covering all elements).
- No defined RTO (Recovery Time Objective) or RPO (Recovery Point Objective) values committed to in writing. RPO is implicitly ≤24 hours (nightly backup), RTO is undocumented.
- No explicit restoration priority ordering across the five covered VMs.
- No contingency contact list or assigned individuals with contact information.
- No documented coordination procedure linking CP to incident response (IR-4 / IR-8).
- Restore drill not yet executed — `runbooks/restore-from-pbs.md` §"First-time restore drill" calls for a drill within 7 days of Plan 1 completion (Plan 1 completed 2026-04-08); an ADR documenting drill results is still owed.
- The weekly PBS job (Sunday 03:00 on smoker) covers the target-VM group but is not formally documented as a contingency asset.
- Contingency plan is not stored in a location protected from unauthorized modification (currently ad-hoc in runbooks).

### Evidence paths

- `runbooks/restore-from-pbs.md` — step-by-step restore procedure for dojo and regscale (the primary partial CP-2 artifact)
- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` — lessons-learned record from the April 2026 backup gap
- `deploy/proxmox/README.md` — PBS backup job schedules, storage target, MAC pinning, and re-creation runbook
- `runbooks/monthly-conmon.md` — §"Daily PBS backup tripwire" and §"Backup verification (monthly)" (operational monitoring aligned with CP)
- `templates/FedRAMP-DR-Form.xlsx` — FedRAMP Rev 5 Disaster Recovery form template (not yet filled)
- `docs/adr/0002-deployment-complete.md` — §"Infrastructure state (end of Plan 1)" establishes the system component inventory

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Personnel or roles (plan review) | cp-02_odp.01 | System Owner (Brian Chaplow) | organization |
| Personnel or roles (plan approval) | cp-02_odp.02 | System Owner (Brian Chaplow) | organization |
| Key contingency personnel (plan distribution) | cp-02_odp.03 | System Owner (Brian Chaplow) | organization |
| Organizational elements (plan distribution) | cp-02_odp.04 | N/A — single-operator homelab; no organizational elements | organization |
| Plan review frequency | cp-02_odp.05 | annually | organization |
| Key contingency personnel (change notification) | cp-02_odp.06 | System Owner (Brian Chaplow) | organization |
| Organizational elements (change notification) | cp-02_odp.07 | N/A — single-operator homelab | organization |

---

## CP-3 — Contingency Training

### Control summary

Provide contingency training to system users consistent with assigned roles and responsibilities: within a defined time period of assuming a contingency role, when required by system changes, and on a defined frequency thereafter. Review and update training content on a defined frequency and after defined events.

### Implementation status

`planned`

### What is implemented

No formal contingency training program, curriculum, or training records exist. The restore runbook (`runbooks/restore-from-pbs.md`) and the PBS monitoring tripwire in `runbooks/monthly-conmon.md` serve as implicit self-paced reference material for the sole operator, but they do not constitute training in the CP-3 sense (no delivery, no acknowledgment, no record).

The system is a single-operator homelab. The system owner both designs the contingency procedures and executes them, collapsing the typical trainer/trainee distinction.

### Gaps / open items

- No contingency training curriculum or records.
- No defined time period for initial training on assumption of a contingency role.
- No defined training refresh frequency.
- No triggering events defined for training content updates.
- The single-operator nature of the system means CP-3 is largely satisfied through direct familiarity with the procedures; however, no documentation captures this as a deliberate training activity.

### Evidence paths

- `runbooks/restore-from-pbs.md` — implicitly serves as operator reference material; not formal training
- `runbooks/monthly-conmon.md` — §"Daily PBS backup tripwire" describes monitoring procedure the operator is expected to know

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Time period for initial training | cp-03_odp.01 | within 30 days of assuming contingency responsibility | organization |
| Frequency thereafter | cp-03_odp.02 | annually | organization |
| Training content review frequency | cp-03_odp.03 | annually | organization |
| Events triggering training content review | cp-03_odp.04 | system change affecting backup or recovery procedures, contingency activation, or audit finding | organization |

---

## CP-4 — Contingency Plan Testing

### Control summary

Test the contingency plan on a defined frequency using defined tests to determine effectiveness and readiness. Review test results and initiate corrective actions if needed.

### Implementation status

`planned`

### What is implemented

No contingency plan test has been formally conducted. The restore procedure was authoritatively tested once in an operational context: ADR 0005 (`docs/adr/0005-pbs-backup-gap-and-automount-fix.md`) documents that `vzdump` was run against dojo (VMID 201) on 2026-04-08 as a verification step after the NFS remount fix, producing a confirmed snapshot at `vm/201/2026-04-08T17:26:22Z`. However this was an operational verification, not a scheduled contingency plan test against defined success criteria.

`runbooks/restore-from-pbs.md` §"First-time restore drill" specifies that a restore drill should be performed within 7 days of Plan 1 completion (2026-04-08), with results documented in a new ADR (`docs/adr/NNNN-restore-drill.md`). That drill has not yet been executed.

### Gaps / open items

- No formal CP test has been conducted against documented test criteria.
- No test results record exists (the ADR 0005 operational verification does not qualify as a CP test).
- No defined test frequency established.
- Restore drill owed within 7 days of 2026-04-08 (i.e., by 2026-04-15) per `runbooks/restore-from-pbs.md`.
- No corrective action tracking process defined beyond ad-hoc ADR creation.

### Evidence paths

- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` — §"Verification" section: operational vzdump verification run on 2026-04-08 (nearest analog to a partial CP test)
- `runbooks/restore-from-pbs.md` — §"First-time restore drill": drill specification and expected ADR output
- `docs/adr/0002-deployment-complete.md` — §"Operator action items deferred to Plan 2 or beyond" item 3: restore drill called out as a Plan 1 follow-on action

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Test frequency | cp-04_odp.01 | annually | organization |
| Tests used | cp-04_odp.02 | tabletop walkthrough and restore drill (qmrestore from PBS snapshot to alternate VMID, verified by smoke check) | organization |
| Review of test results by personnel | cp-04_odp.03 | System Owner (Brian Chaplow) | organization |

---

## CP-9 — System Backup

### Control summary

Conduct backups of user-level information, system-level information, and system documentation (including security- and privacy-related documentation) on defined frequencies for defined system components. Protect the confidentiality, integrity, and availability of backup information.

### Implementation status

`partial`

### What is implemented

The backup infrastructure is implemented and operational:

**Backup jobs:**
- **Pitcrew daily job** (`1da17d50-2183-4592-946b-47e956174e0a`): daily at 02:00, storage `pbs-smokehouse`, covers VMs 100 (DC01), 101 (WS01), 200 (TheHive), 201 (dojo). Verified by ADR 0002: first dojo snapshot `vm/201/2026-04-08T17:26:22Z` confirmed.
- **Smoker daily job** (`851dfd63-cbf4-464a-b394-0cc985de3810`): daily at 02:30, storage `pbs-smokehouse`, covers VM 301 (regscale). Verified by ADR 0002: `vm/301/2026-04-08T21:08:15Z` confirmed.
- **Smoker weekly job**: Sundays at 03:00, covers target VMs (VLAN 40). Offset from daily window avoids PBS datastore contention.

**PBS storage chain:**
- PBS LXC 300 on smoker (10.10.30.21), NFS-backed to smokehouse (`10.10.20.10:/pbs-datastore`, 17TB available).
- NFS mount hardened with `x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30` per ADR 0005 to eliminate boot-race failure class.
- Backup format: Proxmox vzdump snapshot (crash-consistent qemu image chunks in PBS chunk-store format).

**Gap verification and gap closure:**
- ADR 0005 documents the 5-day backup gap (2026-04-03 to 2026-04-07) caused by a silent NFS mount failure during the 2026-04-07 rack consolidation reboot.
- ADR 0002 §"Plan 2 start" confirms the gap was closed by the 02:00 run on 2026-04-09: VM 100 at 02:00, VM 101 at 02:03, VM 201 at 02:08, VM 301 at 02:30, VM 200 caught by weekly job at 06:45.

**Availability of backup information:**
- Snapshots are stored on smokehouse (QNAP TVS-871, 17TB NFS export). The PBS LXC provides the chunk-store index; raw data is on the NFS volume.
- Daily tripwire in `runbooks/monthly-conmon.md` §"Daily PBS backup tripwire" provides interim human-operated availability verification.

**System documentation backups:**
- Git repository (`github.com/brianchaplow/homelab-fedramp-low`) on `origin/main` provides version-controlled backup of all in-repo documentation, OSCAL artifacts, and runbooks. As of the Plan 2 completion tag (`plan-2-complete`), all artifacts are committed and pushed.

### Gaps / open items

- **Confidentiality:** PBS backup data is transmitted over the LAN NFS mount without TLS encryption (NFS v4.1 in-flight, unencrypted). SC-8 is a known gap treated as a portfolio trade-off per ADR 0002 §"Operator action items" item 4 and `runbooks/cert-trust.md`. CP-9.d.01 (confidentiality protection) is therefore a gap.
- **Integrity verification:** PBS uses chunk-based deduplication with SHA-256 hashes for chunk integrity. No additional cryptographic signing of backup archives is in place (no GPG signatures, no HMAC over full archives). CP-9.d.02 (integrity protection) is partially met (chunk hashes) but not fully.
- **Backup alerting:** No automated Wazuh/Discord alert is wired for PBS backup job failure. The 5-day gap (ADR 0005) went undetected because `mail-to-root` on the PBS LXC is the only notification target, which nobody reads. A Wazuh custom rule + Shuffle fanout is documented as a follow-up TODO in `runbooks/monthly-conmon.md` §"Follow-up TODO — proper PBS alert wiring". Interim manual tripwire is active.
- **Backup of brisket (SOC platform) and haccp (ELK):** Neither brisket (VLAN 20, SOC platform) nor haccp (VLAN 30, ELK + Arkime) has a VM-level PBS backup job. These are bare-metal hosts, not VMs, so vzdump cannot be used directly. PCAP archival from haccp to smokehouse via nightly SSH/rsync cron (0300) is documented in CLAUDE.md but is not a full system backup.
- **Backup frequency for system documentation:** Git push cadence is ad-hoc (per-commit); no dedicated documentation backup schedule exists beyond git.

### Evidence paths

- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` — root cause, fix, and verification of the backup chain (fstab hardening, mount verification, vzdump confirmation)
- `docs/adr/0002-deployment-complete.md` — §"Deployment Done Criteria" row "Both VMs show successful PBS backup" and §"Plan 2 start" gap-closure confirmation
- `deploy/proxmox/README.md` — §"Resource reservations": PBS job UUIDs, schedules, storage target, offset rationale
- `runbooks/restore-from-pbs.md` — snapshot verification commands and restore procedure (availability evidence)
- `runbooks/monthly-conmon.md` — §"Daily PBS backup tripwire" (interim availability monitoring), §"Backup verification (monthly)", §"Follow-up TODO — proper PBS alert wiring"
- `runbooks/cert-trust.md` — documents NFS/TLS gap and upgrade path (confidentiality gap context)

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| System components for user-level backup | cp-09_odp.01 | dojo (VMID 201 on pitcrew), regscale (VMID 301 on smoker), DC01 (VMID 100 on pitcrew), WS01 (VMID 101 on pitcrew), TheHive (VMID 200 on pitcrew) | organization |
| Frequency for user-level backup | cp-09_odp.02 | daily (02:00 pitcrew job; 02:30 smoker job) | organization |
| Frequency for system-level backup | cp-09_odp.03 | daily (same PBS jobs; vzdump captures full VM image including OS, middleware, and application layers) | organization |
| Frequency for documentation backup | cp-09_odp.04 | per-commit push to origin/main (ad-hoc); Git history serves as the versioned documentation backup | organization |

---

## CP-10 — System Recovery and Reconstitution

### Control summary

Provide for the recovery and reconstitution of the system to a known state within a defined time period consistent with recovery time and recovery point objectives after a disruption, compromise, or failure.

### Implementation status

`partial`

### What is implemented

The technical capability to recover both in-boundary GRC VMs from PBS snapshots to a known state is implemented and documented:

**Recovery capability:**
- `runbooks/restore-from-pbs.md` provides the complete procedure to recover dojo (VMID 201) and regscale (VMID 301) from PBS snapshots using `qmrestore`. The procedure covers: snapshot listing, VM stop, pre-restore config preservation, `qmrestore` invocation with `--force` (in-place disk rewrite without destroying VM entry to preserve MAC address), VM start, and smoke check verification.
- Restore smoke checks (`./pipelines.sh smoke-dojo`, `./pipelines.sh smoke-regscale`) provide automated verification that the restored system reaches a healthy known state.
- MAC address pinning (dojo `BC:24:11:DE:F0:01`, regscale `BC:24:11:DE:F0:02`) documented in `deploy/proxmox/README.md` ensures cloud-init state survives restore without NIC identity churn.

**Recovery Point Objective (RPO — implicit):**
- Nightly backup jobs (02:00 pitcrew, 02:30 smoker) imply an RPO of ≤24 hours for all covered VMs. In practice the gap between the most recent snapshot and a failure event is at most the time since the last successful backup window.

**Known state definition:**
- For dojo: known state = DefectDojo 2.57.0 containers (nginx, uwsgi, celeryworker, celerybeat, postgres, valkey) all `Up`, smoke check `PASS`. Defined by `deploy/defectdojo/README.md` and the smoke check script `tests/smoke/check_defectdojo.sh`.
- For regscale: known state = atlas + atlas-db containers both `Up`, smoke check `PASS`. Defined by `deploy/regscale/README.md` and `tests/smoke/check_regscale.sh`.

**Reconstitution tooling:**
- `deploy/regscale/reset-admin-password.sh` addresses a specific reconstitution step (admin password re-seeding) needed after a restore if the image predates a password rotation.
- `deploy/defectdojo/post-install.sh` (idempotent seed script) can be re-run post-restore to reconcile DefectDojo SLA configurations and product definitions.

### Gaps / open items

- **No formally defined RTO:** Recovery Time Objective is not committed to in any policy artifact. The `qmrestore` procedure is expected to complete in under 15 minutes based on the 11m11s validated run for dojo (ADR 0005 §"Verification"), but no SLA is formally stated.
- **No formally defined RPO in writing:** The ≤24-hour RPO implied by nightly backups is not documented as an organizational commitment.
- **Restore drill not yet executed:** `runbooks/restore-from-pbs.md` §"First-time restore drill" specifies a drill within 7 days of Plan 1 completion. The drill has not been conducted; therefore recovery readiness is documented but not empirically validated end-to-end.
- **brisket and haccp recovery not documented:** Neither the brisket SOC platform nor the haccp ELK host has a recovery procedure. Both are bare-metal hosts without PBS VM-level backups. Recovery from hardware failure would require reinstallation from CLAUDE.md runbooks, which is informally documented but not formally a CP-10 artifact.
- **Deactivation of interim capabilities:** No documented deactivation procedure for interim capabilities (e.g., manual PBS tripwire) upon full reconstitution.
- **No reauthorization procedure:** No ATO or reauthorization process is defined for this homelab system; however this is appropriate for a FedRAMP Low portfolio lab that has not submitted for authorization.

### Evidence paths

- `runbooks/restore-from-pbs.md` — complete restore procedure for dojo and regscale (primary CP-10 artifact)
- `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` — §"Verification": 11m11s dojo restore run validating recovery speed and snapshot completeness
- `deploy/proxmox/README.md` — §"Resource reservations" (backup schedules supporting RPO), §"Rollback" (VM destroy / recreate path), MAC pinning guidance
- `deploy/regscale/reset-admin-password.sh` — reconstitution step for RegScale admin credential
- `deploy/defectdojo/post-install.sh` — idempotent reconstitution step for DefectDojo SLA + product seeding
- `tests/smoke/check_defectdojo.sh` — known-state verification for dojo post-restore
- `tests/smoke/check_regscale.sh` — known-state verification for regscale post-restore
- `docs/adr/0002-deployment-complete.md` — §"Operator action items deferred to Plan 2 or beyond" item 3: restore drill noted as owed

### ODP values

| ODP | Identifier | Value | Origin |
|-----|-----------|-------|--------|
| Time period for recovery and reconstitution (RTO) | cp-10_odp.01 | 4 hours from detection of disruption to restored known state for GRC VMs (dojo, regscale); informally supported by 11m11s qmrestore runtime observed in ADR 0005 | organization |
| Time period (RPO reference) | cp-10_odp.02 | 24 hours (implied by nightly backup cadence; no data loss exceeding the prior nightly backup window) | organization |

---

## Summary table

| Control | Title | Status | Primary evidence |
|---------|-------|--------|-----------------|
| CP-1 | Policy and Procedures | planned | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md`, `runbooks/restore-from-pbs.md` |
| CP-2 | Contingency Plan | partial | `runbooks/restore-from-pbs.md`, `docs/adr/0005-pbs-backup-gap-and-automount-fix.md`, `deploy/proxmox/README.md` |
| CP-3 | Contingency Training | planned | `runbooks/restore-from-pbs.md` (informal reference only) |
| CP-4 | Contingency Plan Testing | planned | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md` (operational verification, not a formal test) |
| CP-9 | System Backup | partial | `docs/adr/0005-pbs-backup-gap-and-automount-fix.md`, `docs/adr/0002-deployment-complete.md`, `deploy/proxmox/README.md`, `runbooks/restore-from-pbs.md`, `runbooks/monthly-conmon.md` |
| CP-10 | System Recovery and Reconstitution | partial | `runbooks/restore-from-pbs.md`, `docs/adr/0005-pbs-backup-gap-and-automount-fix.md`, `deploy/proxmox/README.md`, smoke check scripts |

### Key cross-cutting gaps (for SSP prose authoring)

1. **No formal CP plan document** — CP-2 is the highest-priority authoring target; it will draw on the runbook and ADR corpus.
2. **Restore drill outstanding** — due by 2026-04-15; result ADR will close the CP-4 and CP-10 readiness gaps.
3. **NFS backup transport unencrypted** — SC-8 gap that touches CP-9 confidentiality; documented as portfolio trade-off.
4. **PBS backup alerting absent** — the ADR 0005 gap story is the strongest evidence for CP-9 partial rating; Wazuh/Discord alert is the pending fix (`runbooks/monthly-conmon.md` §"Follow-up TODO").
5. **brisket and haccp have no VM-level backup** — bare-metal hosts; CP-9 scope is bounded to the five PBS-covered VMs for SSP authoring purposes.
