# OSCAL Profile Source

## File

`FedRAMP_rev5_LOW-baseline-profile.json` — the FedRAMP Rev 5 Low
baseline profile, selecting 156 controls from
[`../catalog/NIST_SP-800-53_rev5_catalog.json`](../catalog/NIST_SP-800-53_rev5_catalog.json).

## Identity

| Field           | Value                                       |
|-----------------|---------------------------------------------|
| UUID            | `512149a6-7f04-4c01-bb1b-78eafd6a950d`      |
| Title           | FedRAMP Rev 5 Low Baseline                  |
| Version         | `5.1.1+fedramp-20240111-0`                  |
| Published       | 2023-08-31                                  |
| Last modified   | 2024-01-11                                  |
| OSCAL version   | 1.1.1                                       |
| Controls        | 156 (parents + enhancements)                |

## Provenance

The profile JSON in this directory is **bootstrapped from the upstream
FedRAMP Rev 5 Low baseline XML** using a one-shot converter during Plan
2 Task 3 execution on 2026-04-09. The derivation story:

1. Plan 2 Task 3 Step 1 (as written) expected to download the profile
   JSON from `https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LOW-baseline_profile.json`.

2. That URL returns HTTP 404 as of 2026-04-09. The entire
   `GSA/fedramp-automation` repository has been removed or renamed — no
   alternate branch or path under `GSA/` hosts the content, and the
   FedRAMP GitHub organization (`FedRAMP/`) does not have an
   `fedramp-automation` peer either. FedRAMP content has reorganized
   around the `FedRAMP/docs` and `FedRAMP/docs-alpha` repos which host
   the FRMR documentation, not OSCAL baselines.

3. The upstream OSCAL Rev 5 Low baseline content survives in the
   [`oscal-compass/compliance-trestle-fedramp`](https://github.com/oscal-compass/compliance-trestle-fedramp)
   plugin repository. That repo originally consumed the GSA content as
   a submodule pinned to a commit before the delete, and a later
   commit (2024-02-08) vendored the pinned snapshot into its own tree
   at `trestle_fedramp/resources/fedramp-source/content/baselines/rev5/`.
   Only XML versions are present in that snapshot.

4. Trestle's `trestle import` subcommand in 4.0.1 only supports JSON
   and YAML input (`Unsupported file extension .xml`). Writing a full
   OSCAL XML-to-JSON converter by hand is out of scope for a bootstrap
   task; NIST's official XSLT-based converter is also out of scope.

5. A focused extractor was therefore run against the XML
   (`.tmp/fedramp-low-profile.xml`, downloaded from
   `raw.githubusercontent.com/oscal-compass/compliance-trestle-fedramp/main/trestle_fedramp/resources/fedramp-source/content/baselines/rev5/xml/FedRAMP_rev5_LOW-baseline_profile.xml`)
   to pull the 156 `<with-id>` control references and the identity
   fields (UUID, title, version, published, last-modified, OSCAL
   version). Those were assembled into a minimal OSCAL Profile JSON
   that imports from the local NIST catalog via
   `trestle://catalogs/nist-800-53-rev5/catalog.json`.

6. The generated profile was validated with `trestle validate` (VALID)
   and resolved against the imported catalog with
   `trestle author profile-resolve -n fedramp-rev5-low -o fedramp-rev5-low-resolved`.
   The resolved catalog has **exactly 156 controls** when counted
   recursively (parents + control enhancements), matching the upstream
   XML's `<with-id>` count precisely — zero missing, zero extra.

## What was NOT carried across from the XML source

The upstream XML includes metadata blocks that are semantically
interesting for a production 3PAO submission but do not affect control
coverage, SSP scaffolding, or profile resolution:

- Party definitions (FedRAMP PMO, FedRAMP JAB) with contact addresses
- Role definitions (prepared-by, fedramp-pmo, fedramp-jab) and
  responsible-party bindings
- Modify blocks (`<set-parameter>`, `<alter>`) that adjust control
  parameters and add FedRAMP-specific prose to some controls
- Back-matter resources (the FedRAMP logo, reference documents)

For the homelab portfolio these are not needed. The notional Managed
SOC Service SSP doesn't claim PMO authorship, and the parameter
modifications apply to a tiny subset of controls and can be added
selectively during Plan 3 (SSP Authoring) if a given control's
authoring requires the FedRAMP-specific prose.

If a future phase requires full fidelity — for instance, if a
reviewer wants to see the `<alter>` blocks exposed in the SSP — the
path forward is:

1. Install a Python XSLT engine (e.g., `saxonche`)
2. Download the official OSCAL XML→JSON converter XSLT from
   `usnistgov/OSCAL`
3. Transform the upstream XML to JSON
4. Re-import via `trestle import` and swap the catalog href from
   whatever the upstream points at to the local catalog via
   `trestle href`

This approach would preserve every metadata block but adds a
build-time dependency and a dead-letter on the original upstream
catalog href. For a minimal-viable portfolio bootstrap the focused
extractor is cleaner.

## Canonical vs public copy

- **Canonical (Trestle-managed)**:
  `trestle-workspace/profiles/fedramp-rev5-low/profile.json` — this is
  the copy Trestle operates on for `profile-resolve`, `ssp-generate`,
  `ssp-assemble`, etc. It must stay in the Trestle workspace layout or
  commands fail.
- **Public mirror**: this directory —
  `oscal/profile/FedRAMP_rev5_LOW-baseline-profile.json` — exists so
  that a reader browsing the repo's top-level `oscal/` directory sees
  the profile without needing to understand Trestle layout. Both
  copies are byte-identical.

## References

- Compliance Trestle FedRAMP plugin: https://github.com/oscal-compass/compliance-trestle-fedramp
- Upstream XML (accessed 2026-04-09): https://raw.githubusercontent.com/oscal-compass/compliance-trestle-fedramp/main/trestle_fedramp/resources/fedramp-source/content/baselines/rev5/xml/FedRAMP_rev5_LOW-baseline_profile.xml
- ADR covering this bootstrap story: `docs/adr/0006-plan-2-environment-and-api-realignment.md` §"Deviation 11"
