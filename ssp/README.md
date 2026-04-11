# System Security Plan (SSP)

This directory contains the SSP for the notional **Managed SOC Service
(MSS)** -- the system boundary that wraps the homelab SOC
infrastructure and is being authored against NIST SP 800-53 Rev 5
controls selected by the FedRAMP Low baseline profile.

## Status

- **Scaffold** -- generated 2026-04-09 during Plan 2 Task 4
- **Tier-1 authoring** -- pending (Plan 3)
- **Tier-2 authoring** -- pending (Plan 3)
- **OSCAL assembly** -- pending (Plan 3 done-criteria)

Until Plan 3 lands, every control markdown file under `controls/` is
a Trestle-generated scaffold containing the control statement text
from the NIST catalog plus `<REPLACE_ME>` placeholders for the FedRAMP
organizationally-defined parameters (ODPs). The scaffold is
schema-complete -- it's ready for authoring -- but the implementation
prose is empty.

## Structure

```
ssp/
├── README.md                    ← this file
├── controls/                    ← 156 control markdown files, mirrored
│                                  from trestle-workspace/mss-ssp/, one
│                                  per control in the FedRAMP Low baseline
│   ├── ac/                        organized by control family
│   │   ├── ac-1.md                ac-1 through ac-22 (11 controls selected
│   │   ├── ac-2.md                by FedRAMP Low)
│   │   └── ...
│   ├── at/                        5 controls
│   ├── au/                        10 controls
│   ├── ca/                        10 controls
│   ├── cm/                        9 controls
│   ├── cp/                        6 controls
│   ├── ia/                        16 controls (largest family)
│   ├── ir/                        7 controls
│   ├── ma/                        4 controls
│   ├── mp/                        4 controls
│   ├── pe/                        10 controls
│   ├── pl/                        7 controls
│   ├── ps/                        9 controls
│   ├── ra/                        8 controls
│   ├── sa/                        9 controls
│   ├── sc/                        14 controls
│   ├── si/                        6 controls
│   └── sr/                        11 controls
└── appendices/                  ← pending (acronym list, references,
                                    control summary table, rules-of-
                                    behavior -- Plan 3)
```

Total: **156 control markdown files** across **18 families**.

## Authoring tiers

Plan 3 will author the 156 controls across two tiers:

- **Tier 1 -- full implementation statements** (~40 controls). The
  controls where the homelab implementation has real evidence worth
  documenting: audit logging (AU family), configuration management
  (CM), identification and authentication (IA), system and
  communications protection (SC), vulnerability scanning and flaw
  remediation (RA-5, SI-2), incident response (IR). These are the
  controls a 3PAO would actually inspect, and they're the ones the
  portfolio writeup (Plan 4) will feature.
- **Tier 2 -- stub implementations** (~116 controls). The remaining
  controls get brief "see policy" statements with NA-rationale where
  applicable. The goal isn't to fake a production SSP; it's to
  demonstrate that the author understands the scoping decisions a real
  FedRAMP Low system would need to make, and that the SSP structure
  is OSCAL-assemble-ready end-to-end.

The tier assignment for each control is tracked in
`docs/control-family-matrix.md` (to be created during Plan 3) with
the rationale for why a given control is Tier 1 or Tier 2.

## OSCAL representation

The markdown files under `controls/` are the **human-editable source**.
Trestle's `ssp-assemble` command compiles them into
`oscal/ssp.json` at the end of Plan 3, which becomes the
machine-readable, schema-validated representation. The OSCAL JSON is
what downstream tooling consumes:

- RegScale CE imports it via the OSCAL import API (Plan 2 Task 16)
- FedRAMP RFC-0024 alignment (September 2026 OSCAL mandate) expects
  artifacts in this shape
- The Plan 4 portfolio writeup references it as the evidence that the
  full FedRAMP ConMon story is OSCAL-native end-to-end

## Editing conventions

When Plan 3 starts authoring:

- **Edit files under `trestle-workspace/mss-ssp/`, not here.** Trestle
  manages the workspace copy; this `ssp/controls/` directory is a
  mirror maintained for public-repo visibility. The mirror is
  re-synced during commits.
- Preserve the `x-trestle-*` frontmatter blocks -- they are instructions
  to `ssp-assemble` and removing them will break the OSCAL assembly.
- Set ODP parameter values in the `x-trestle-set-params` block by
  replacing `<REPLACE_ME>` with the FedRAMP-required value (or the
  homelab's declared value where FedRAMP leaves it to the ODP).
- Write implementation prose in the `## Implementation [a.]`,
  `## Implementation [b.]`, etc. sections that Trestle generates per
  control statement part.

See `docs/adr/0006-plan-2-environment-and-api-realignment.md` §
"Deviation 11" for the bootstrapping story that produced this
scaffold (GSA removed the canonical FedRAMP profile JSON URL;
profile was recovered from the compliance-trestle-fedramp plugin's
pinned XML snapshot).
