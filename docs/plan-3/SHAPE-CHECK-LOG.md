# Plan 3 Gate 2 Shape-Check Log

**Date:** 2026-04-09
**Purpose:** Record the Trestle 4.0.1 behavior observed when assembling real authored prose against a partial scaffold, retiring Plan 3 Risk #1 from homelab-fedramp-low ADR 0007.

## CM-2 (base control)

**Scaffold shape observed:**
- x-trestle-set-params: 2 ODPs (cm-02_odp.01, cm-02_odp.02)
- prose marker: `<!-- Add implementation prose for the main This System component for control: cm-2 -->`
- Implementation Status default: planned

**Authoring outcome:**
- ssp-assemble: PASS
- Round-trip via JSON parse: PASS
- REPLACE_ME count in assembled cm-2 entry: 0
- statements observed: none (prose is in by-components, not statements)
- by-component observed: desc_len=1423, starts: "The Managed SOC Service maintains its baseline configuration as git-tracked code across four public and private reposito..."
- set_parameters observed: none surfaced in implemented-requirements (x-trestle-set-params is metadata only; set-params do not appear as set-parameters in the assembled ir entry)

**Trestle 4.0.1 quirks observed:**
- Prose appears in `by-components[].description`, not in `statements[].description` or `description` directly on the ir entry. The ir entry has keys: `uuid`, `control-id`, `by-components` only.
- `x-trestle-set-params` ODP values (profile-values + profile-param-value-origin) do NOT surface as `set-parameters` entries inside the assembled implemented-requirement. They are YAML frontmatter consumed by Trestle for profile-level resolution only. Set-params are not present in the control-implementation top-level set-parameters array either. This means ODPs filled in x-trestle-set-params are captured in the markdown source but do not produce set-parameters in the output SSP JSON for this profile configuration.

## IA-5(1) (enhancement control)

**Scaffold shape observed:**
- x-trestle-set-params: 2 ODPs (ia-05.01_odp.01 with alt-identifier ia-5.1_prm_1, ia-05.01_odp.02 with alt-identifier ia-5.1_prm_2)
- prose marker: `<!-- Add implementation prose for the main This System component for control: ia-5.1 -->`
- Implementation Status default: planned
- Frontmatter differences from base controls: none -- enhancement ia-5.1 has identical frontmatter structure to base control cm-2. Both have x-trestle-add-props, x-trestle-set-params, and x-trestle-global. The sort-id differs (ia-05.01 vs cm-02) and the profile-values param IDs differ, but the YAML structure is identical.

**Authoring outcome:**
- ssp-assemble: PASS
- Round-trip via JSON parse: PASS
- REPLACE_ME count in assembled ia-5.1 entry: 0
- statements observed: none (same pattern as CM-2; prose is in by-components)
- by-component observed: desc_len=1233, starts: "The Managed SOC Service enforces password-based authentication strength through multiple layers, though the system favor..."
- set_parameters observed: none (same quirk as CM-2 -- x-trestle-set-params not surfaced as set-parameters in assembled JSON)

**Trestle 4.0.1 quirks observed:**
- Enhancement controls (ia-5.1) have identical scaffold shape to base controls. No structural difference between base and enhancement authoring files.
- Same by-components prose pattern: assembled ir has keys `uuid`, `control-id`, `by-components` only.

## Conclusions

- Risk #1 (Trestle 4.0.1 behavior on real prose): retired -- ssp-assemble accepts real authored prose without errors; prose round-trips cleanly; REPLACE_ME count is 0 for both controls.
- Bulk authoring can proceed: yes
- Authoring template adjustments required before bulk work: none for prose authoring. Note for verification scripts: do not look for prose in `statements[]` or `description` at the ir level -- always look in `by-components[].description`. Note for set-params tracking: x-trestle-set-params ODP values are not echoed into SSP JSON set-parameters for this FedRAMP Rev 5 Low profile configuration; verification of ODP values must read the source markdown, not the assembled JSON.
