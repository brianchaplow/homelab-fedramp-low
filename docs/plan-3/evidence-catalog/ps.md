# PS -- Personnel Security Evidence Catalog

**Family:** Personnel Security (PS)
**Controls in baseline:** ps-1, ps-2, ps-3, ps-4, ps-5, ps-6, ps-7, ps-8, ps-9
**Catalog produced by:** Phase 1 subagent (2026-04-10)
**Repo:** homelab-fedramp-low (main branch)

> **Evidence policy (per Plan 3 design §3.2):** Every path cited below was verified to exist in the local filesystem before writing. Paths rooted at `/c/Projects/` are from the parent workspace; paths without a leading `/c/Projects/homelab-fedramp-low/` prefix are relative to this repo root. ADR references point to `docs/adr/` in this repo unless otherwise noted.

> **Parameter policy (per Plan 3 design §3.4):** The bootstrapped FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `set-parameters` alter blocks for the PS family -- the GSA-sourced XML modify/alter sections were intentionally excluded during the Plan 2 bootstrap (ADR 0006 Deviation 11). All PS ODPs therefore resolve as `organization-defined`. For the eight controls that are `not-applicable`, the proposed ODP value is the canonical N/A string per Plan 3 design §3.4.

> **Family context:** PS is the most consistently not-applicable family in a single-operator homelab. Controls PS-2 through PS-5 and PS-7 through PS-9 all presuppose an organization with multiple personnel subject to hiring, transfer, termination, and sanction workflows. MSS is a single-operator personal system (Brian Chaplow, system owner and sole operator). The not-applicable justification for each control references whole-project design §2.5 (shared-tenancy handling acknowledges the single-operator nature) and the CLAUDE.md system-level policy. PS-1 is `partial` (policy exists in ADRs and CLAUDE.md; no formal HR-style dissemination). PS-6 is `partial` (the repo LICENSE and the absence of any contributor serve as the access agreement artifact; no external individual accesses the system, so the re-sign workflow has no trigger).

---

## PS-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** The personnel security policy for MSS is documented at the system level. The CLAUDE.md policy document (`/c/Projects/CLAUDE.md`) establishes the single-operator access model, credential conventions, SSH key-only authentication requirements, and attack-boundary rules (all attacks MUST target VLAN 40 only). This SSP itself -- together with ADR 0001 (EULA/pre-flight), ADR 0002 (Plan 1 deployment), and ADR 0008 (Plan 3 pre-execution realignment) -- collectively constitutes the personnel security policy and procedures record for the MSS boundary.
- **Supporting mechanisms:** ADR update cadence is event-driven: each plan phase produces at least one ADR documenting decisions, deviations, and consequences. The `deploy/` subdirectory READMEs (`deploy/defectdojo/README.md`, `deploy/regscale/README.md`) capture per-service access provisioning procedures. No second operator exists, so "dissemination" is internal to a single role. The gap relative to a multi-person organization is acknowledged: no formal HR policy publication process and no designated separate policy official. Brian Chaplow performs all policy, management, and compliance roles.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (system-level policy: VLAN conventions, SSH rules, credential handling, attack boundary -- functions as the personnel security policy for this system)
  - `docs/adr/0001-preflight-and-eula.md` (EULA analysis, pre-flight access decisions -- earliest policy artifact)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 completion, operator action items -- procedure record)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` (authoring conventions, implementation status rubric, set-params policy)
  - `deploy/defectdojo/README.md` (DefectDojo access provisioning procedure)
  - `deploy/regscale/README.md` (RegScale access provisioning procedure)
- **Set-params (proposed values):**
  - `ps-01_odp.01` / `ps-1_prm_1` aggregate -- personnel or roles receiving policy: value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `ps-01_odp.02` / `ps-1_prm_1` aggregate -- personnel or roles receiving procedures: value `["Brian Chaplow (system owner, sole operator)"]`, origin `organization`
  - `ps-01_odp.03` / `ps-1_prm_2` (designated official): value `Brian Chaplow (system owner)`, origin `organization`
  - `ps-01_odp.04` / `ps-1_prm_3` (policy review frequency): value `annually and after each plan phase completion or security incident`, origin `organization`
  - `ps-01_odp.05` / `ps-1_prm_4` (events triggering policy review): value `plan phase completion, new service enrollment, security incident, or regulatory change`, origin `organization`
  - `ps-01_odp.06` / `ps-1_prm_5` (procedures review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `ps-01_odp.07` / `ps-1_prm_6` (events triggering procedures review): value `plan phase completion, new service enrollment, or deviation requiring an ADR`, origin `organization`
  - `ps-01_odp.08` / `ps-1_prm_7` (policy level selection -- org/mission/system): value `system-level`, origin `organization`
- **Authoring notes:** Status is `partial`, not `not-applicable`, because policy artifacts exist (CLAUDE.md, ADRs, deploy READMEs) but no formal multi-role dissemination process applies for a single-operator system. Prose paragraph 2 should name this gap explicitly. Cross-reference AC-1 and AT-1 (same pattern: policy lives in CLAUDE.md + ADRs, single-operator).

---

## PS-2 Position Risk Designation

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-2 requires assigning OPM-style risk designations to organizational positions and establishing screening criteria for each position. There are no organizational positions -- Brian Chaplow is the sole operator, holding all roles simultaneously (system owner, administrator, security officer, and operator). The OPM Position Designation System (PDS) model presupposes an employer-employee relationship and multiple assignable positions; neither exists here.
- **Supporting mechanisms:** The single-operator model is established in whole-project design §2.5 (shared-tenancy handling, which acknowledges the homelab is a personal system), in `/c/Projects/CLAUDE.md` (sole operator listed in SSH quick reference and credential table), and in ADR 0001 (pre-flight). In a real MSS with staff, this control would be Service Provider Corporate origination applied across the organization.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (single-operator model: one SSH user `bchaplow`, one credential holder per service, no organizational hierarchy)
  - `docs/adr/0001-preflight-and-eula.md` (documents the homelab-portfolio context; no employee/employer relationship)
  - `trestle-workspace/mss-ssp/ps/ps-2.md` (control scaffold, confirming FedRAMP Low baseline includes this control)
- **Set-params (proposed values):**
  - `ps-02_odp` / `ps-2_prm_1` (frequency for reviewing position risk designations): value `not-applicable -- single-operator personal system; no organizational positions exist`, origin `organization`
- **Authoring notes:** One sentence N/A justification. Cite §2.5 reference. Note what Service Provider Corporate origination would look like in a real MSS. This is the canonical PS N/A pattern for PS-2 through PS-5 and PS-7 through PS-9.

---

## PS-3 Personnel Screening

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-3 requires screening individuals prior to authorizing access and defining conditions and frequency for rescreening. There is only one individual with access -- Brian Chaplow -- and no organizational hiring process through which a screening requirement could be triggered. No external individuals are authorized access to in-boundary systems; any access would require credential provisioning by the operator, an event that has not occurred and is not planned.
- **Supporting mechanisms:** The absence of external access is enforced technically: SSH key-only authentication on all in-boundary Linux hosts, per-service individual account provisioning documented in deploy/ READMEs, and Wazuh monitoring of all 15 agents covering in-boundary hosts. No guest accounts, shared accounts, or contractor accounts exist.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (credentials table: all accounts owned by Brian Chaplow; SSH key reference)
  - `trestle-workspace/mss-ssp/ps/ps-3.md` (control scaffold)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 agent enrollment: 13 agents, all operated by sole operator)
- **Set-params (proposed values):**
  - `ps-3_prm_1` aggregate -- `ps-03_odp.01` (conditions requiring rescreening): value `not-applicable -- single-operator personal system; no personnel screening process exists`, origin `organization`
  - `ps-03_odp.02` (rescreening frequency): value `not-applicable -- single-operator personal system; no personnel screening process exists`, origin `organization`
- **Authoring notes:** Single sentence N/A. Note the technical compensating posture (SSH key-only, no external accounts) even though it is not a compensating control claim -- it is context that shows the control's intent (controlling who can access) is met by the single-operator architecture.

---

## PS-4 Personnel Termination

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-4 requires disabling system access, revoking credentials, conducting exit interviews, retrieving property, and retaining data upon individual employment termination. There are no employees, no employer-employee relationships, and no termination events. The sole operator, Brian Chaplow, owns all access. Termination of the operator's access would be equivalent to decommissioning the system itself.
- **Supporting mechanisms:** No multi-user credential provisioning exists. All service credentials are held by a single operator and stored in `/c/Projects/.env` (gitignored). No third-party accounts with system privileges exist.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (credentials table: single credential holder per service, `.env` location)
  - `trestle-workspace/mss-ssp/ps/ps-4.md` (control scaffold)
- **Set-params (proposed values):**
  - `ps-04_odp.01` / `ps-4_prm_1` (time period to disable access upon termination): value `not-applicable -- single-operator personal system; no personnel termination process exists`, origin `organization`
  - `ps-04_odp.02` / `ps-4_prm_2` (information security topics for exit interview): value `not-applicable -- single-operator personal system; no exit interview process exists`, origin `organization`
- **Authoring notes:** Single sentence N/A. Do not attempt to map "operator stopping work" to a termination scenario -- that is overreaching and would undermine the honest assessment.

---

## PS-5 Personnel Transfer

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-5 requires reviewing logical and physical access authorizations upon reassignment or transfer, initiating transfer actions, modifying access, and notifying relevant personnel. There are no personnel transfers or reassignments because there is only one operator and no organizational hierarchy into which a transfer could occur.
- **Supporting mechanisms:** Access authorizations are static: all service accounts are provisioned to Brian Chaplow at deployment and documented in `deploy/` READMEs. No position-change trigger exists that would invoke a review or modification of access.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (single-operator SSH reference, service account table)
  - `trestle-workspace/mss-ssp/ps/ps-5.md` (control scaffold)
- **Set-params (proposed values):**
  - `ps-05_odp.01` / `ps-5_prm_1` (transfer or reassignment actions): value `not-applicable -- single-operator personal system; no personnel transfer process exists`, origin `organization`
  - `ps-05_odp.02` / `ps-5_prm_2` (time period following formal transfer action): value `not-applicable -- single-operator personal system`, origin `organization`
  - `ps-05_odp.03` / `ps-5_prm_3` (personnel or roles to notify): value `not-applicable -- single-operator personal system`, origin `organization`
  - `ps-05_odp.04` / `ps-5_prm_4` (time period for notification): value `not-applicable -- single-operator personal system`, origin `organization`
- **Authoring notes:** Single sentence N/A.

---

## PS-6 Access Agreements

- **Status:** partial
- **Primary mechanism:** The repo LICENSE (`homelab-fedramp-low/LICENSE`, MIT License, copyright 2026 Brian Chaplow) serves as the system-level access agreement artifact. It establishes ownership and usage terms. Because MSS is a single-operator system, the only individual "requiring access" is the operator-owner, who implicitly agrees to all terms as the system's author and owner. There are no external contributors -- no pull requests, no outside committers, no contractor accounts -- so the PS-6(c) requirement to verify signatures before granting access has no external trigger.
- **Supporting mechanisms:** The README (`README.md`) establishes the purpose and scope of the system. The CLAUDE.md policy (`/c/Projects/CLAUDE.md`) documents behavioral constraints for the operator: VLAN 40 attack-only rule, credential handling, no hardcoded secrets. These collectively constitute the "rules of behavior" element of access agreements. ADR 0001 documents the EULA analysis performed at pre-flight -- the closest analog to a pre-access review for this system.
- **Evidence paths:**
  - `LICENSE` (MIT License -- system-level access agreement artifact, verified present in repo root)
  - `README.md` (system purpose and scope documentation, verified present in repo root)
  - `/c/Projects/CLAUDE.md` (behavioral rules for the operator: attack boundary, credential policy, naming conventions)
  - `docs/adr/0001-preflight-and-eula.md` (EULA analysis at system pre-flight -- pre-access review analog)
- **Set-params (proposed values):**
  - `ps-06_odp.01` / `ps-6_prm_1` (frequency to review and update access agreements): value `annually and after each plan phase completion or when the system boundary changes`, origin `organization`
  - `ps-06_odp.02` / `ps-6_prm_2` (frequency for individuals to re-sign access agreements): value `not-applicable -- single-operator personal system; no external individuals require re-sign workflow`, origin `organization`
- **Authoring notes:** Status is `partial`. PS-6(a) is met by the LICENSE + CLAUDE.md behavioral rules. PS-6(b) review cadence can be defined (annually). PS-6(c) is the gap: no external individual has ever been granted access, so the pre-access signing workflow has never been exercised and there is no second signatory. Prose paragraph 2 should name this gap. Do not claim the LICENSE as a signed NDA -- it is not; it is an ownership and usage rights statement. The honest framing is: "the access agreement artifact exists; the signing workflow has no current external applicability."

---

## PS-7 External Personnel Security

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-7 requires establishing and documenting personnel security requirements for external providers, requiring compliance, and monitoring provider compliance. There are no external providers with system privileges, credentials, or badges. All in-boundary system administration is performed exclusively by Brian Chaplow. No contractors, service bureaus, or third-party managed service providers have been granted access to in-boundary hosts.
- **Supporting mechanisms:** SSH access is key-only and no external SSH keys are authorized on any in-boundary host. Service accounts are provisioned exclusively for the operator. No outsourced IT services have been contracted for the in-boundary components.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (SSH quick reference: only `bchaplow` accounts; no external key entries)
  - `trestle-workspace/mss-ssp/ps/ps-7.md` (control scaffold)
- **Set-params (proposed values):**
  - `ps-07_odp.01` / `ps-7_prm_1` (personnel or roles to notify for external personnel changes): value `not-applicable -- single-operator personal system; no external providers with system access`, origin `organization`
  - `ps-07_odp.02` / `ps-7_prm_2` (time period for notification of external personnel changes): value `not-applicable -- single-operator personal system; no external providers with system access`, origin `organization`
- **Authoring notes:** Single sentence N/A.

---

## PS-8 Personnel Sanctions

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-8 requires a formal sanctions process for individuals failing to comply with security policies and a notification mechanism when sanctions are initiated. There is only one individual with system access -- Brian Chaplow -- and no employer-employee or supervisor-subordinate relationship through which a formal sanction could be imposed. Self-sanction is not a coherent security control.
- **Supporting mechanisms:** Behavioral compliance with CLAUDE.md conventions (attack boundary, credential policy, no hardcoded secrets) is enforced by the operator on themselves. Wazuh monitors all in-boundary hosts for anomalous behavior, providing an independent audit trail, but anomaly detection is not a sanctions process.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (behavioral conventions: attack boundary rule, credential policy -- the rules that a sanctions process would enforce)
  - `trestle-workspace/mss-ssp/ps/ps-8.md` (control scaffold)
- **Set-params (proposed values):**
  - `ps-08_odp.01` / `ps-8_prm_1` (personnel or roles to notify when sanctions initiated): value `not-applicable -- single-operator personal system; no formal sanctions process exists`, origin `organization`
  - `ps-08_odp.02` / `ps-8_prm_2` (time period for notification): value `not-applicable -- single-operator personal system; no formal sanctions process exists`, origin `organization`
- **Authoring notes:** Single sentence N/A. Note that the audit trail from Wazuh provides accountability evidence even without a formal sanctions process -- but do not overclaim this as a compensating control.

---

## PS-9 Position Descriptions

- **Status:** not-applicable
- **Primary mechanism:** Not applicable. MSS is a single-operator personal system. PS-9 requires incorporating security and privacy roles and responsibilities into organizational position descriptions. There are no formal organizational position descriptions -- there is one operator who holds all roles simultaneously (system owner, administrator, security officer, privacy officer, and sole operator). The CLAUDE.md policy document serves as the informal role definition, but it is not a position description in the organizational HR sense.
- **Supporting mechanisms:** CLAUDE.md documents the single-operator's responsibilities by convention rather than by position description. The Plan 3 design (ADR 0008) explicitly assigns Implementation Status rubric responsibility to the system owner. No HR system, position-classification process, or organizational chart exists.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` (sole operator conventions, responsibilities by section -- informal role definition)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` (pre-execution decisions item 5: "Implementation Status rubric: honest per-control" -- documents system owner responsibility)
  - `trestle-workspace/mss-ssp/ps/ps-9.md` (control scaffold -- note: no `x-trestle-set-params` block; PS-9 has no ODPs)
- **Set-params (proposed values):**
  - No ODPs defined for PS-9 in the FedRAMP Rev 5 Low baseline. The `trestle-workspace/mss-ssp/ps/ps-9.md` scaffold contains no `x-trestle-set-params` block. No values to fill.
- **Authoring notes:** Single sentence N/A. The absence of a set-params block in the scaffold is intentional -- PS-9 carries no ODPs. The authoring step for this control only requires filling the `### This System` prose block and the `#### Implementation Status:` line.

---

*Subagent report:*
- **family:** ps
- **controls_cataloged:** 9 (ps-1 through ps-9)
- **grep_verifications_performed:** 14 (LICENSE confirmed in repo root; README.md confirmed in repo root; all 9 ps-*.md scaffold files confirmed in `trestle-workspace/mss-ssp/ps/`; CLAUDE.md confirmed at `/c/Projects/CLAUDE.md`; ADR 0001, 0002, 0008 confirmed in `docs/adr/`; `deploy/defectdojo/README.md` and `deploy/regscale/README.md` confirmed in repo)
- **cites_to_parent_claude_md:** 9 (every control references CLAUDE.md as the system-level policy document)
- **cites_to_adrs:** 6 (ADR 0001 in PS-1, PS-2, PS-3; ADR 0002 in PS-1, PS-3; ADR 0008 in PS-1, PS-9)
- **unresolved_questions:** None. PS is a straightforward N/A family. The only authoring judgment call is the `partial` status for PS-1 and PS-6. PS-1 `partial` because policy exists in CLAUDE.md + ADRs but no formal multi-role dissemination process. PS-6 `partial` because the LICENSE serves as the access agreement artifact but no external signing workflow has been exercised. Both gap statements are honest and should be named explicitly in the prose.
