# PL — Planning Evidence Catalog

**Family:** Planning (PL)
**Controls in baseline:** pl-1, pl-2, pl-4, pl-4.1, pl-8, pl-10, pl-11
**Catalog produced by:** Phase 1 subagent (2026-04-09)
**Repo:** homelab-fedramp-low (main branch)

> **Evidence policy (per Plan 3 design §3.2):** Every path cited below was verified to exist in the local filesystem before writing. Paths rooted at `/c/Projects/` are from the parent workspace; paths without a leading `/c/Projects/homelab-fedramp-low/` prefix are relative to this repo root. ADR references point to `docs/adr/` in this repo unless otherwise noted.

> **Parameter policy (per Plan 3 design §3.4):** The bootstrapped FedRAMP Rev 5 Low profile (`trestle-workspace/profiles/fedramp-rev5-low/profile.json`) contains no `set-parameters` alter blocks — the GSA-sourced XML modify/alter sections were intentionally excluded during the Plan 2 bootstrap (ADR 0006 Deviation 11). All PL ODPs therefore resolve as `organization-defined`. Proposed values use real homelab cadences; `inherited` origin is not applicable for this family.

> **PL family context:** Planning controls are self-referential in this portfolio. The SSP being assembled at `oscal/ssp.json` (from `trestle-workspace/mss-ssp/`) IS the security plan (PL-2). The ADR chain ADR 0001–0008 collectively forms the policy-and-procedures record (PL-1). The whole-project design spec §2 (authorization boundary) and §5 (data pipeline, §3 IIW generator) document the security and privacy architecture (PL-8). The FedRAMP Rev 5 Low profile at `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (156 controls, ADR 0006 Deviation 11) is the selected baseline (PL-10) tailored from the NIST SP 800-53 Rev 5 catalog (PL-11). No runbooks/rules-of-behavior file currently exists for PL-4/PL-4(1) — those controls are `partial`.

---

## PL-1 Policy and Procedures

- **Status:** partial
- **Primary mechanism:** The ADR chain (ADRs 0001–0008) collectively functions as the planning policy and procedures record for the Managed SOC Service. ADR 0001 establishes pre-flight checks and EULA acceptance (earliest policy artifact). ADR 0008 §Pre-execution decisions items 1–8 encodes the authoritative authoring conventions, implementation-status rubric, set-params fill policy, and branch strategy — the nearest equivalent to planning procedures for this single-operator system. The 2026-04-09 Plan 3 design spec (`docs/superpowers/specs/2026-04-09-homelab-fedramp-low-plan-3-ssp-authoring-design.md`, in the parent workspace at `/c/Projects/`) provides purpose, scope, roles, and compliance alignment for the Plan 3 SSP authoring effort.
- **Supporting mechanisms:** `runbooks/monthly-conmon.md` (stub — planning procedures for the monthly ConMon cycle). `/c/Projects/CLAUDE.md` (system owner identified as Brian Chaplow; canonical VLAN/host reference, SSH conventions, credential handling — system-level policy enforced by convention). Parent workspace conventions memo: `feedback_no_coauthor.md` and `feedback_env_scrub.md` document operating procedures applied consistently across all projects.
- **Evidence paths:**
  - `docs/adr/0001-preflight-and-eula.md` (EULA analysis, pre-flight decisions — earliest planning policy artifact, establishes EULA compliance posture)
  - `docs/adr/0002-deployment-complete.md` (Plan 1 completion, done-criteria verification — serves as the Plan 1 procedures record)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` (11 deviations + Branch Strategy — the Plan 2 procedures record; Deviation 11 documents FedRAMP profile bootstrap)
  - `docs/adr/0007-plan-2-complete.md` (Plan 2 done-criteria verification — procedures record with commit-level traceability)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Pre-execution decisions (authoring order, implementation status rubric, set-params policy, no-alternative rule — closest artifact to formal planning procedures)
  - `runbooks/monthly-conmon.md` (ConMon cycle planning procedures, currently stub pending Plan 3 completion)
  - `/c/Projects/CLAUDE.md` (system-level conventions and owner identification)
- **Set-params (proposed values):**
  - `pl-01_odp.01` / `pl-1_prm_1` aggregates `pl-01_odp.01` + `pl-01_odp.02` (personnel or roles to receive policy): value `Brian Chaplow (system owner, sole operator)`, origin `organization`
  - `pl-01_odp.02` (personnel or roles to receive procedures): value `Brian Chaplow (system owner, sole operator)`, origin `organization`
  - `pl-01_odp.03` / `pl-1_prm_2` (policy review frequency): value `annually and after each plan phase completion (at ADR filing)`, origin `organization`
  - `pl-01_odp.04` / `pl-1_prm_3` (events triggering policy review): value `plan phase completion, significant infrastructure change, security incident, or external regulatory change`, origin `organization`
  - `pl-01_odp.05` / `pl-1_prm_4` (procedures review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `pl-01_odp.06` / `pl-1_prm_5` (events triggering procedures review): value `plan phase completion, deviation requiring an ADR, or new service enrollment`, origin `organization`
  - `pl-01_odp.07` / `pl-1_prm_6` (designation official — policy): value `Brian Chaplow (system owner)`, origin `organization`
  - `pl-01_odp.08` / `pl-1_prm_7` (designation official — procedures): value `Brian Chaplow (system owner)`, origin `organization`
- **Authoring notes:** PL-1 is `partial` — not `not-applicable` — because planning policy artifacts exist (ADR chain, CLAUDE.md, runbooks) but no single standalone "PL Policy" document has been published and formally disseminated. For a single-operator system this is the honest answer: the ADRs ARE the policy record, but there is no dissemination ritual beyond git commits to a public repo. Prose paragraph 2 should name this gap explicitly. Cross-reference PL-2 (this SSP is the security plan) and AC-1 (same pattern: policy lives in ADRs + CLAUDE.md). Note that the `pl-1_prm_1` ODP uses an `aggregates` key in the scaffold — fill both `pl-01_odp.01` and `pl-01_odp.02` to satisfy it.

---

## PL-2 System Security and Privacy Plans

- **Status:** partial
- **Primary mechanism:** The system security plan for the Managed SOC Service is being assembled at `oscal/ssp.json` via `./pipelines.sh ssp-assemble` (Trestle 4.0.1 `ssp-assemble` wrapper at `pipelines/build/oscal_ssp.py`). The markdown authoring surface is `trestle-workspace/mss-ssp/` (156 control files across 18 families). The SSP is linked to the FedRAMP Rev 5 Low profile at `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (import-profile href in the assembled JSON). Authorization boundary, system components, operational context, mission, roles, information types, security categorization, threats, operational environment, and external dependencies are documented in the whole-project design spec §2 (`docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1–§2.6) in the parent workspace.
- **Supporting mechanisms:** `oscal/component-definition.json` (7 in-boundary components: brisket, haccp, smokehouse, dojo, regscale, opnsense, mokerlink — produced by Plan 2 Task 8). `inventory/overlay.yaml` (static metadata for non-agent assets). `inventory/IIW-2026-04.xlsx` (Integrated Inventory Workbook, April 2026, 7 rows). `oscal/poam.json` (gitignored) / `poam/POAM-2026-04.xlsx` (Plan of Action and Milestones, April 2026, 8,473 items). ADR 0006 Deviation 11 documents baseline selection rationale (156 controls, FedRAMP Rev 5 Low, FIPS 199 Low categorization).
- **Evidence paths:**
  - `oscal/ssp.json` (assembled SSP — the primary deliverable artifact; Plan 2 Task 15 produced the scaffold; Plan 3 fills control prose)
  - `trestle-workspace/mss-ssp/` (markdown authoring surface, 156 control files — verified directory exists)
  - `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (linked profile, 156 controls, UUID 512149a6)
  - `oscal/component-definition.json` (7 in-boundary components per Plan 2 Task 8)
  - `inventory/IIW-2026-04.xlsx` (IIW April 2026, 7 rows per Plan 2 Task 9)
  - `poam/POAM-2026-04.xlsx` (POA&M April 2026, 8,473 items per Plan 2 Task 13)
  - `docs/adr/0007-plan-2-complete.md` §Final artifact inventory (authoritative artifact inventory with sizes and item counts)
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Supersession deltas (documents SSP authoring shape, 868 REPLACE_ME placeholders, Trestle 4.0.1 behavior)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1–§2.6 (authorization boundary, in-boundary components, out-of-boundary assets, external connections, shared-tenancy handling, leveraged authorization)
- **Set-params (proposed values):**
  - `pl-02_odp.01` / `pl-2_prm_1` (individuals or groups for security-/privacy-related activity coordination): value `Brian Chaplow (system owner, sole operator — self-coordination)`, origin `organization`
  - `pl-02_odp.02` / `pl-2_prm_2` (personnel or roles to receive SSP copies): value `Brian Chaplow (system owner); public GitHub repo (github.com/brianchaplow/homelab-fedramp-low) for portfolio reviewers`, origin `organization`
  - `pl-02_odp.03` / `pl-2_prm_3` (SSP review frequency): value `annually and after each plan phase completion`, origin `organization`
- **Authoring notes:** PL-2 is `partial` because the SSP is assembled but control prose authoring is incomplete as of Plan 3 start (all 156 controls carry placeholder prose pending Plan 3 fill). Privacy risk assessment (PL-02a.08) is `not-applicable` for this system — MSS processes only operational telemetry (alert metadata, network flows, vulnerability scan data), no PII/PHI/CUI. Authorizing official (PL-02a.15) is Brian Chaplow as system owner — no separate AO role in a single-operator homelab. Note that `oscal/poam.json` is gitignored per Plan 2 design; the xlsx artifact is the shippable deliverable. Cross-reference PL-10 (baseline selection) and PL-11 (baseline tailoring) which document the FedRAMP Rev 5 Low profile selection rationale.

---

## PL-4 Rules of Behavior

- **Status:** partial
- **Primary mechanism:** No standalone Rules of Behavior (RoB) document exists in this repo. The closest artifacts are: `/c/Projects/CLAUDE.md` §Conventions (attack-VLAN-40-only rule, no-hardcoded-credentials convention, canonical host/tool names, git commit conventions) which functions as a system-level behavioral ruleset enforced by convention for the sole operator. ADR 0001 §RegScale CE EULA review (Brian Chaplow read, understood, and agreed to RegScale CE license terms before system access — documented acknowledgment for external software used in this system). `runbooks/cert-trust.md` (documents the TLS posture decisions operators must follow when interacting with self-signed certificates).
- **Supporting mechanisms:** `runbooks/cert-trust.md` (TLS access procedure — behavioral rule for in-boundary service access). `deploy/regscale/README.md` §Password policy (length 12, complexity requirement — behavioral rule for account credential management). `deploy/defectdojo/README.md` (behavioral rule: no hardcoded passwords, `.env` storage required). No formal RoB dissemination or acknowledgment signature process exists beyond git commit history.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` §Conventions (canonical behavioral rules: attack VLAN 40 only, no hardcoded credentials, no "Chappy McNasty" in commits, tool canonical names — verified in CLAUDE.md)
  - `docs/adr/0001-preflight-and-eula.md` §RegScale CE EULA review (documented acknowledgment of license terms before access — satisfies PL-4b spirit for external software)
  - `runbooks/cert-trust.md` (TLS posture behavioral rules for in-boundary service access)
  - `deploy/regscale/README.md` (password policy behavioral rule — length 12, upper/lower/digit/symbol)
  - `deploy/defectdojo/README.md` (no-hardcoded-passwords behavioral rule, `.env` storage)
- **Set-params (proposed values):**
  - `pl-04_odp.01` / `pl-4_prm_1` (rules of behavior review frequency): value `annually and after each plan phase completion`, origin `organization`
  - `pl-04_odp.02` / `pl-4_prm_2` (events triggering rules review): value `plan phase completion, new service enrollment, or security incident`, origin `organization`
  - `pl-04_odp.03` / `pl-4_prm_3` (re-acknowledgment selection — frequency or upon revision): value `when the rules are revised or updated (at each plan phase completion that modifies behavioral conventions)`, origin `organization`
- **Authoring notes:** PL-4 is `partial` because behavioral rules exist (CLAUDE.md conventions, ADR 0001 EULA acknowledgment, runbooks) but no single consolidated RoB document has been drafted, and no formal acknowledgment process (electronic signature, checkbox, etc.) exists beyond the EULA acknowledgment in ADR 0001. For a single-operator system the conventions are effectively self-signed. Prose paragraph 2 should name the gap: no formal standalone RoB document, no acknowledgment mechanism beyond EULA and git conventions. Cross-reference PL-4(1) (social media restrictions — same RoB document gap) and AC-8 (system use notification — related behavioral rules at login).

---

## PL-4(1) Social Media and External Site/Application Usage Restrictions

- **Status:** partial
- **Primary mechanism:** No standalone Rules of Behavior document exists that explicitly enumerates social media and external site restrictions. The partial coverage comes from: `/c/Projects/CLAUDE.md` §Credentials and §Conventions (passwords in `.env` gitignored — enforces the restriction on using organizational credentials on external sites; "NEVER hardcode credentials" is the organizational identifier-protection rule). ADR 0001 §RegScale CE EULA review §Material clauses (§2(ix) "No publishing circumvention info" — external-site posting restriction accepted as a term of use).
- **Supporting mechanisms:** `deploy/regscale/README.md` (password requirements; no organizational email credentials used for RegScale account creation — admin/password from reset script, not organizational identity provider). `deploy/defectdojo/README.md` (same pattern: no organizational email linked). No formal social media policy for this single-operator system. No organizational identifiers (e.g., `.gov` email addresses) are in use — the system owner uses personal accounts where accounts exist.
- **Evidence paths:**
  - `/c/Projects/CLAUDE.md` §Credentials (`.env` gitignored — organizational secrets not posted to external sites)
  - `/c/Projects/CLAUDE.md` §Conventions ("NEVER hardcode credentials" — implements the organizational identifier protection restriction)
  - `docs/adr/0001-preflight-and-eula.md` §RegScale CE EULA review (§2(ix) no circumvention publishing — external posting restriction acknowledged)
  - `deploy/regscale/README.md` (admin account not linked to organizational email)
  - `deploy/defectdojo/README.md` (admin account not linked to organizational email)
- **Set-params (proposed values):**
  - none — PL-4(1) has no ODPs in the FedRAMP Rev 5 Low baseline scaffold (enhancement has no set-params block in `trestle-workspace/mss-ssp/pl/pl-4.1.md`)
- **Authoring notes:** PL-4(1) is `partial` for the same reason as PL-4: restrictions exist in practice (no organizational identifiers on external sites, no secrets posted publicly) but no RoB document formally enumerates the three restriction categories ((a) social media use, (b) posting organizational info on public websites, (c) organizational identifiers on external accounts). Prose should note that the public GitHub repo (github.com/brianchaplow/homelab-fedramp-low) explicitly excludes all secrets via `.gitignore` — the `.env` pattern is the mechanism satisfying restriction (c). This is a Tier 2 depth control — 1 short paragraph (40–80 words) citing the CLAUDE.md credential convention and the gitignore pattern is sufficient.

---

## PL-8 Security and Privacy Architectures

- **Status:** partial
- **Primary mechanism:** The security architecture for the Managed SOC Service is documented in the whole-project design spec §2 (authorization boundary, in-boundary components, external connection points, shared-tenancy handling) and §3 (IIW generator architecture) at `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md`. The authorization boundary defines 14 in-boundary components (3 bare-metal hosts + 2 GRC VMs + 1 firewall + 1 managed switch + ~7 internal services) with explicit CIA rationale: FIPS 199 Low categorization (C: Low, I: Low, A: Low), no PII/PHI/CUI, advisory telemetry not authoritative record. The boundary diagram is specified at `docs/diagrams/boundary.mmd` and `docs/diagrams/rendered/boundary.png` per the design spec §2.7, though those files do not yet exist in the repo (the spec calls for them as a Plan 3 deliverable). External dependencies are documented in design spec §2.4 (Wazuh agent TLS enrollment, Tailscale mesh, admin SSH path, PBS NFS backup).
- **Supporting mechanisms:** `oscal/component-definition.json` (OSCAL-native component enumeration of 7 in-boundary assets — the machine-readable architecture artifact). ADR 0006 Deviation 11 + `oscal/profile/SOURCE.md` (profile derivation story — the architecture decision for baseline selection and how the profile integrates with the NIST catalog). `docs/plan-3/SHAPE-CHECK-LOG.md` (Trestle 4.0.1 assembly architecture — documents how the SSP assembler integrates with the architecture). Phase 14 pipeline architecture in parent `/c/Projects/CLAUDE.md` (Zeek on haccp span0, Logstash enrichment, ELK data pipeline — the data-flow architecture for the SOC service).
- **Evidence paths:**
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1 (service definition, CIA categorization, FedRAMP baseline rationale), §2.2 (in-boundary components table), §2.3 (out-of-boundary assets), §2.4 (external connection points), §2.5 (shared-tenancy handling), §2.6 (leveraged authorization sidebar)
  - `oscal/component-definition.json` (OSCAL component-definition, 7 in-boundary components — the machine-readable architecture artifact)
  - `oscal/profile/SOURCE.md` (FedRAMP Rev 5 Low profile derivation, 156 controls, UUID 512149a6 — architecture decision record for the control baseline)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` §Deviation 11 (profile bootstrap rationale, GSA repo deletion, compliance-trestle-fedramp sourcing)
  - `docs/adr/0007-plan-2-complete.md` §Final artifact inventory (5 OSCAL artifacts, sizes, item counts — architecture artifact inventory)
  - `/c/Projects/CLAUDE.md` Phase 14 section (Zeek → Filebeat → Logstash → ELK pipeline; Wazuh 4.14.4 SIEM architecture; OpenCTI v7 threat intel; Shuffle SOAR WF1–WF11; brisket services table — the data-flow architecture)
- **Set-params (proposed values):**
  - `pl-08_odp` / `pl-8_prm_1` (architecture review frequency): value `annually and after each infrastructure phase completion (rack build, major migration, or new service enrollment)`, origin `organization`
- **Authoring notes:** PL-8 is `partial` because the architecture is documented in the design spec and CLAUDE.md but the boundary diagram (`docs/diagrams/boundary.mmd`, `docs/diagrams/rendered/boundary.png`) called for in design spec §2.7 does not yet exist in the repo. The `oscal/component-definition.json` is the machine-readable architecture artifact and satisfies OSCAL-layer architecture documentation. Prose paragraph 2 should cite the design spec §2 sections explicitly and note the boundary diagram as a pending artifact. Privacy architecture: MSS processes no PII/PHI — privacy architecture is not-applicable as stated in design spec §1.5 ("No PII/CUI processing scenarios"). Cross-reference PL-2 (SSP contains the architecture overview), SA-17 (not in Low baseline — N/A), and CA-3 (external system connections documented in design spec §2.4).

---

## PL-10 Baseline Selection

- **Status:** implemented
- **Primary mechanism:** The FedRAMP Rev 5 Low baseline (156 controls) is selected and documented at `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (UUID 512149a6-7f04-4c01-bb1b-78eafd6a950d, version 5.1.1+fedramp-20240111-0). The rationale for Low selection is stated in the whole-project design spec §2.1: FIPS 199 Low categorization (C: Low, I: Low, A: Low) because MSS processes only operational telemetry (alert metadata, network flows, vulnerability scan data) — no PII, PHI, CUI, or financial data; 99% monthly availability target; advisory output not safety-critical. The selected baseline is implemented as an OSCAL profile that imports the NIST SP 800-53 Rev 5 catalog (`trestle-workspace/catalogs/nist-800-53-rev5/catalog.json`, 10.7 MB) via `trestle://catalogs/nist-800-53-rev5/catalog.json`.
- **Supporting mechanisms:** `trestle-workspace/catalogs/fedramp-rev5-low-resolved/catalog.json` (resolved catalog — exactly 156 controls verified by `trestle author profile-resolve` per ADR 0007 Plan 2 done criteria). `oscal/ssp.json` `import-profile` href points to the profile, linking the SSP to the selected baseline. ADR 0006 Deviation 11 documents the derivation story for the profile (GSA repo deletion, compliance-trestle-fedramp plugin sourcing, XML→JSON bootstrap, 156 `<with-id>` references preserved).
- **Evidence paths:**
  - `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (selected baseline profile, UUID 512149a6, 156 controls — verified file exists)
  - `trestle-workspace/catalogs/nist-800-53-rev5/catalog.json` (NIST SP 800-53 Rev 5.2.0 source catalog, 10.7 MB — verified file exists)
  - `trestle-workspace/catalogs/fedramp-rev5-low-resolved/catalog.json` (resolved profile catalog, 156 controls — verified file exists)
  - `oscal/profile/SOURCE.md` (derivation narrative: GSA repo deletion, compliance-trestle-fedramp sourcing, 156 control count validation — verified file exists)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` §Deviation 11 (profile bootstrap rationale, validation evidence: `trestle validate` VALID, 156 controls)
  - `docs/adr/0007-plan-2-complete.md` §Done criteria (FedRAMP Rev 5 Low profile entry: bootstrapped from plugin XML, 156 `<with-id>` references preserved, VALID)
  - `/c/Projects/docs/superpowers/specs/2026-04-07-homelab-fedramp-low-design.md` §2.1 (FIPS 199 Low categorization rationale: no PII/PHI/CUI, advisory telemetry, 99% availability target)
- **Set-params (proposed values):**
  - none — PL-10 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold (control has no `x-trestle-set-params` block in `trestle-workspace/mss-ssp/pl/pl-10.md`)
- **Authoring notes:** PL-10 is `implemented` — the baseline selection is complete, documented, and encoded in machine-readable OSCAL artifacts. This is one of the cleanest `implemented` controls in the PL family. Prose should be concise: (1) name the selected baseline (FedRAMP Rev 5 Low, 156 controls, profile UUID), (2) state the FIPS 199 rationale in 1–2 sentences, (3) cite the OSCAL profile file and the ADR 0006 Deviation 11 derivation story. Cross-reference PL-11 (tailoring applied to the selected baseline) and PL-2 (SSP built against this baseline).

---

## PL-11 Baseline Tailoring

- **Status:** implemented
- **Primary mechanism:** The FedRAMP Rev 5 Low baseline was tailored from the NIST SP 800-53 Rev 5 catalog by applying the 156-control `<with-id>` inclusion filter documented in the profile at `trestle-workspace/profiles/fedramp-rev5-low/profile.json`. The tailoring decisions are: (1) inclusion filter — only 156 specific control IDs from the NIST catalog are included per the FedRAMP Low selection; (2) merge/combine method `keep` with `as-is: true` — no further structural alteration beyond the inclusion filter; (3) no additional organization-specific overlays applied beyond the FedRAMP Low selection itself. The resolved catalog at `trestle-workspace/catalogs/fedramp-rev5-low-resolved/catalog.json` is the post-tailoring artifact (exactly 156 controls, verified zero missing / zero extra per ADR 0007).
- **Supporting mechanisms:** ADR 0006 Deviation 11 (derivation story: what the original FedRAMP XML `<alter>` / `<set-parameter>` blocks contained that were intentionally excluded from the bootstrapped profile, and why — parties, role definitions, modify blocks, back-matter resources were omitted as they don't affect control coverage). `oscal/profile/SOURCE.md` (omission documentation — what is absent from the profile and why, with future re-fetch path). The 868 `<REPLACE_ME>` parameter placeholders in `trestle-workspace/mss-ssp/` represent the organization-defined parameter tailoring surface that Plan 3 fills with homelab-specific values.
- **Evidence paths:**
  - `trestle-workspace/profiles/fedramp-rev5-low/profile.json` (tailored profile: 156 `with-ids`, `merge.combine.method: keep`, `as-is: true` — the OSCAL tailoring record; verified file exists)
  - `trestle-workspace/catalogs/fedramp-rev5-low-resolved/catalog.json` (post-tailoring resolved catalog, 156 controls, passes `trestle validate` — the output of applying the tailoring actions; verified file exists)
  - `oscal/profile/SOURCE.md` (documents intentional omissions from the GSA XML: parties, roles, modify/alter blocks, back-matter — the tailoring scope narrative)
  - `docs/adr/0006-plan-2-environment-and-api-realignment.md` §Deviation 11 (full tailoring derivation story: upstream XML structure, what was extracted, what was excluded, validation evidence — zero missing, zero extra controls)
  - `docs/adr/0007-plan-2-complete.md` §Done criteria ("FedRAMP Rev 5 Low profile bootstrapped … 156 `<with-id>` references preserved, VALID")
  - `docs/adr/0008-plan-3-pre-execution-realignment.md` §Pre-execution decision 6 (set-params fill policy: the per-control ODP tailoring completing the final layer of tailoring)
- **Set-params (proposed values):**
  - none — PL-11 has no ODPs in the FedRAMP Rev 5 Low baseline scaffold (control has no `x-trestle-set-params` block in `trestle-workspace/mss-ssp/pl/pl-11.md`)
- **Authoring notes:** PL-11 is `implemented` — tailoring actions are applied and documented. The two-layer tailoring story is: Layer 1 = the FedRAMP PMO's tailoring of NIST SP 800-53 Rev 5 to produce the 156-control Low baseline (captured in the profile); Layer 2 = the organization's tailoring of ODP values (captured in the markdown `x-trestle-set-params` blocks, filled during Plan 3). Prose should be concise: (1) name the tailoring mechanism (OSCAL profile, 156 `<with-id>` filter), (2) cite the ADR 0006 Deviation 11 derivation story, (3) note the ODP-fill layer as the remaining tailoring action. The intentional omissions from the GSA XML (parties, modify blocks) should be mentioned with the ADR 0006 derivation story reference. Cross-reference PL-10 (baseline selection that precedes tailoring) and PL-2 (SSP reflects tailored baseline).

---

## Summary Report

```json
{
  "family": "pl",
  "controls_cataloged": 7,
  "grep_verifications_performed": 22,
  "cites_to_parent_claude_md": 4,
  "cites_to_adrs": 14,
  "unresolved_questions": [
    "docs/diagrams/boundary.mmd and docs/diagrams/rendered/boundary.png do not yet exist — cited in design spec §2.7 as planned; PL-8 notes this as a partial-status driver",
    "runbooks/monthly-conmon.md exists but is a stub (Plan 2 complete; Plan 3 prose will note stub status) — PL-1 and PL-4 cite it accurately as stub",
    "No standalone Rules of Behavior document exists — PL-4 and PL-4(1) are partial for this reason; no further action needed for catalog (SSP prose will state the gap explicitly)",
    "oscal/poam.json is gitignored — PL-2 cites the xlsx artifact instead; this is correct per Plan 2 design"
  ]
}
```
