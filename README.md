# HomeLab FedRAMP Low ConMon Program

> A working, evidence-backed FedRAMP Low continuous monitoring program for a
> notional "Managed SOC Service" offering, built on a functioning homelab SOC.
> OSCAL-native, aligned with FedRAMP RFC-0024's September 30, 2026 machine-readable
> authorization package mandate.

## Host reference

The homelab uses descriptive hostnames. This table maps them for readers encountering them for the first time.

**In boundary (the Managed SOC Service):**

| Hostname | IP | Role | What it runs |
|---|---|---|---|
| **brisket** | 10.10.20.30 | MSS Core | Wazuh SIEM (15 agents), Shuffle SOAR, Velociraptor DFIR, OpenCTI threat intel, ML scorer, Prometheus + Grafana |
| **haccp** | 10.10.30.25 | Log Analytics | ELK 8.17 (Elasticsearch + Kibana + Fleet), Arkime full-PCAP, Logstash enrichment pipeline, Zeek on SPAN port |
| **smokehouse** | 10.10.20.10 | Network Sensors | Suricata IDS, Zeek (eth4 SPAN), Fluent Bit log shipping. QNAP NAS appliance. |
| **dojo** | 10.10.30.27 | GRC Tooling | DefectDojo 2.57 (vulnerability management, FedRAMP Low SLA clocks) |
| **regscale** | 10.10.30.28 | GRC Tooling | RegScale Community Edition (OSCAL import, SSP and POA&M reporting UI) |
| OPNsense | 10.10.10.1 | Firewall | Inter-VLAN routing, boundary protection (SC-7) |
| MokerLink | 10.10.10.2 | Switch | L3 managed 10G switch, microsegmentation, SPAN mirror sessions |

**Out of boundary (consumes or interacts with the service, not part of it):**

| Asset | Why out of boundary |
|---|---|
| DC01, WS01, GCP VM | Customer endpoints: monitored by the service, not components of it |
| PITBOSS (10.10.10.100) | Operator workstation: admin access path, not a service component |
| AlgoTrader, Capitol Signals API | Co-tenant workloads on brisket: shared compute documented in OR-0001 |
| PBS LXC 300 | External backup target: inter-system data flow documented under CA-3 |

The boundary test is not hosting location. It is whether the asset *is* the monitoring service or *consumes* it. The GCP VM and DC01 are identical under that test, even though one runs in Google Cloud and the other runs in the rack.

## What this is

A working FedRAMP Low Continuous Monitoring program built on a live homelab
SOC. I'm a 26-year Navy veteran running a production homelab for SOC,
detection, and threat-intel work, and this project extends that infrastructure
into the GRC (governance, risk, and compliance) side of cybersecurity. I've
managed POA&Ms in the military and done deep prior research on NIST SP 800-53
Rev 5, but I hadn't actually worked FedRAMP-specific Continuous Monitoring
end-to-end. Reading the catalog and running the program are different things.
This repo is the working artifact of running the program.

The "system" is a notional **Managed SOC Service (MSS)** built on top of my real
homelab SOC infrastructure. Everything is generated from live data: no fabricated
POA&M items, no hand-edited xlsx, no theatrical 3PAO reports.

## Scope and framework mapping

The repo title says "FedRAMP Low" because the **artifacts** in it (OSCAL SSP, POA&M, IIW, Deviation Requests, Significant Change Request, monthly ConMon cycles) are modeled on the FedRAMP Low Rev 5 baseline and use the official FedRAMP Rev 5 xlsx templates. That framing is accurate for what the artifacts are. It would not be accurate to call this a FedRAMP authorization, and the project does not.

FedRAMP is statutorily limited to **cloud computing products and services offered to federal agencies** under the FedRAMP Authorization Act of 2022 (44 USC 3607) and OMB Memorandum M-24-15 (July 2024). The legal definition of "cloud" comes from NIST SP 800-145, which requires five essential characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service. A single-operator homelab fails all five. The framework that legally fits an on-prem mission system is **NIST RMF (SP 800-37 Rev 2)**, implemented for DoD via **DoDI 8510.01**. RMF and FedRAMP share the NIST 800-53 Rev 5 control catalog, the OSCAL data model, the POA&M concept, and the continuous monitoring cycle. The pipeline in this repo would generate the same artifacts for either.

| Artifact or mechanic | FedRAMP cloud package | RMF on-prem package (DoDI 8510.01) | DISA SRG cloud package |
|---|---|---|---|
| OSCAL SSP, POA&M, component-def | Required by RFC-0024 (deadline 2026-09-30 initial, 2027-09-30 final) | Valid format under DoD Cybersecurity Reciprocity Playbook (Jan 2024) | Required (FedRAMP-derived) |
| Monthly ConMon cycle | Required | Required | Required (with DoD overlays) |
| Three-category DR taxonomy (RA, FP, OR) | Standard FedRAMP language | Different DoD-specific terminology, same semantics | Standard |
| 156-control NIST 800-53 Rev 5 Low | Direct mapping | Same catalog (different baseline at IL2 and above) | IL2 ≈ FedRAMP Moderate; IL4 = Moderate + DoD overlays; IL5/IL6 = High + DoD overlays |
| Customer Responsibility Matrix (CRM, SSP Appendix J) | Required for SaaS / PaaS | Not applicable (no tenants) | Required for the CSP side, not for the DoD tenant side |
| 3PAO assessment | Required for FedRAMP authorization | Different for DoD (component AO, RMF assessor) | Required, FedRAMP-recognized 3PAO |
| Authorized IaaS reference + control inheritance | Required for SaaS / PaaS | Not applicable | Required (IaaS authorized at FedRAMP High for IL5 and above) |

The project's **operational mechanics** (POA&M state machine, DR adjudication, OSCAL build, monthly cycle, automated evidence) are directly relevant to all three target programs. The project's **scope-bound omissions** (cloud service model, deployment model, CRM, IaaS inheritance, FIPS-validated modules, 3PAO assessment, agency AO) are documented honestly throughout this README and called out individually in the "[What this project does not claim](#what-this-project-does-not-claim)" section near the bottom.

### Service model, deployment model, multi-tenancy

| Field | Value | Why |
|---|---|---|
| Cloud Service Model | N/A on-prem | Not a cloud service. If the notional MSS were a real SaaS, the model would be SaaS on top of an authorized IaaS layer (AWS GovCloud or Azure Government would be the typical choice). |
| Cloud Deployment Model | N/A on-prem | Single-operator homelab. Would be Public Cloud in a real MSS deployment, or possibly Community Cloud if scoped to a federal sector. |
| Multi-tenancy | Single-operator | The shared-tenancy gap documented in [OR-0001](deviation-requests/OR-0001-shared-tenancy.md) is between MSS workloads and unrelated operator workloads on the same hardware, not between distinct customer tenants. |
| Customer Responsibility Matrix | None in production form | A demonstrative stub for 10 sample controls (PE, MA, SC, AC, IA, AU families) showing how a real CRM would split CSP-implemented / customer-implemented / inherited-from-IaaS responsibilities is at [`docs/crm-example.md`](docs/crm-example.md). |

### DoD-specific framing for a DISA audience

For a reader coming from DISA rather than the FedRAMP PMO, the more direct framework mappings are:

- **DISA Cloud Computing SRG IL ladder** (IL2 / IL4 / IL5 / IL6) is layered on top of FedRAMP authorizations. IL4 = FedRAMP Moderate + DoD CUI overlays; IL5 / IL6 = FedRAMP High + DoD-specific controls. Building FedRAMP-shaped artifacts is upstream of DISA cloud authorization, not orthogonal to it.
- **DoDI 8510.01 (RMF for DoD IT)** is the framework that fits an on-prem demonstration like this one cleanly. Same control catalog, same authorization steps, OSCAL formats valid, no cloud-specific artifacts required.
- **cATO (Continuous ATO)** is the DoD strategic direction: dashboards, automated evidence, real-time indicators replacing paper packages. The pipeline in this repo (monthly OSCAL output, automated POA&M generation, idempotent DR application via [`runbooks/apply-deviation-requests.py`](runbooks/apply-deviation-requests.py), schema validation at every stage) is exactly the mechanics cATO requires.
- **DoD Cybersecurity Reciprocity Playbook (January 2024)** mandates components accept each other's authorizations without re-validation. Reciprocity-by-OSCAL is the future state RFC-0024 and FedRAMP 20x are enabling.

### FIPS cryptographic posture

The in-boundary Ubuntu hosts run **stock Ubuntu cryptography**, not FIPS-validated modules. This gap is documented inside the SSP under SC-13 ([`trestle-workspace/mss-ssp/sc/sc-13.md`](trestle-workspace/mss-ssp/sc/sc-13.md)): all algorithms in active use (AES, SHA-256, ECDHE, ChaCha20-Poly1305, Ed25519) are NIST-approved at the algorithm level, but the underlying OpenSSL and kernel cryptographic modules are not CMVP-validated. A real FedRAMP or DoD IL package would require Ubuntu Pro FIPS or an equivalent FIPS-enabled build with cited NIST CMVP certificate numbers; that hardening path is deferred as a future phase.

## What's real, what's notional

| Real | Notional |
|---|---|
| The homelab SOC infrastructure (brisket, haccp, smokehouse, dojo, regscale) | The "MSS" commercial offering |
| Live Wazuh / ELK / Suricata / Zeek / OpenCTI scans and findings | The CSP business relationship |
| The 3,760 Open POA&M items (post-remediation) and the 77.8% April-to-May reduction | The 3PAO assessment and AO approval |
| The OSCAL SSP / POA&M / IIW pipeline and its Trestle schema validation | The FedRAMP PMO submission workflow |
| The shared-tenancy compliance gap and OR-0001 DR (found during SSP authoring) | The annual authorization cycle |

## Quick tour (60 seconds)

| Artifact | Where | What |
|---|---|---|
| **SSP** (OSCAL) | [`oscal/ssp.json`](oscal/ssp.json) | 156-control assembled SSP, schema-valid |
| **SSP source** | [`trestle-workspace/mss-ssp/`](trestle-workspace/mss-ssp/) | One markdown file per control, organized by family |
| **POA&M** | [`poam/POAM-2026-04.xlsx`](poam/POAM-2026-04.xlsx) | FedRAMP Rev 5 template, populated from real findings |
| **April -> May diff** | [`conmon-submissions/`](conmon-submissions/) | Two consecutive ConMon cycles showing operational rhythm |
| **IIW** | [`inventory/IIW-2026-04.xlsx`](inventory/IIW-2026-04.xlsx) | FedRAMP Rev 5 template, live-sourced from Wazuh syscollector |
| **Deviation Requests** | [`deviation-requests/`](deviation-requests/) | All three FedRAMP DR categories (RA, FP, OR) |
| **SCR** | [`significant-changes/`](significant-changes/) | One Significant Change Request demonstrating boundary evolution |
| **OSCAL package** | [`oscal/`](oscal/) | Catalog, profile, component-def, SSP, POA&M: all schema-validated |
| **Pipelines** | [`pipelines/`](pipelines/) | Python code that regenerates everything from live homelab data |
| **ADR chain** | [`docs/adr/`](docs/adr/) | Execution decisions and deviations, 0001 to 0011 |
| **Main writeup** | [`writeups/01-building-fedramp-low-conmon-homelab.md`](writeups/01-building-fedramp-low-conmon-homelab.md) | Build narrative (~3,200 words) |
| **Paramify comparison** | [`writeups/02-paramify-vs-diy.md`](writeups/02-paramify-vs-diy.md) | Fair comparison post (~1,800 words) |

To regenerate the artifacts from current live state:

```bash
./pipelines.sh conmon
```

## Tooling inventory

| Tool | Status | Purpose |
|---|---|---|
| **DefectDojo 2.57** | Deployed on dojo VM (10.10.30.27) | Vulnerability management + FedRAMP Low SLA clock |
| **RegScale Community Edition** | Deployed on regscale VM (10.10.30.28) | GRC workflow + SSP / POA&M reporting UI |
| **Compliance Trestle 4.0.1** | Running on PITBOSS / Git Bash | OSCAL authoring + schema validation |
| **Wazuh Manager 4.14.5** | Existing homelab SIEM | Scan input for findings (5 in-boundary agents) |
| **OpenSearch** | Existing homelab (Wazuh Indexer) | Vulnerability state index for pipeline ingest |
| **Paramify** | Comparison post only (commercial SaaS, no self-host path) | See [writeup #2](writeups/02-paramify-vs-diy.md) |
| **ServiceNow GRC** | Not evaluated | Acknowledged for honesty |
| **Onspring** | Not evaluated | Acknowledged for honesty |

## How to read this repo

If you have **60 seconds**:

1. Scan the host reference table at the top to see what's in vs out of boundary.
2. Skim the "Quick tour" table above.
3. Open one POA&M xlsx, one DR markdown, one control markdown (try [`trestle-workspace/mss-ssp/si/si-4.md`](trestle-workspace/mss-ssp/si/si-4.md), the writeup hero control).

If you have **10 minutes**:

1. Read the [main writeup](writeups/01-building-fedramp-low-conmon-homelab.md).
2. Open [`deviation-requests/OR-0001-shared-tenancy.md`](deviation-requests/OR-0001-shared-tenancy.md) to see the compliance gap I found in my own environment.
3. Look at the April -> May diff in [`conmon-submissions/2026-05/README.md`](conmon-submissions/2026-05/README.md) to see the POA&M lifecycle in action.

If you're a **technical reviewer**:

1. Clone the repo, set up your `~/.env` per [`.env.example`](.env.example).
2. Run `./pipelines.sh install && ./pipelines.sh test` (136 tests pass).
3. Run `./pipelines.sh conmon` to regenerate the OSCAL output from live homelab data.
4. Walk the [ADR chain](docs/adr/) (0001 to 0011) to see every execution decision and deviation from the original plan.

## Writeups

- [Building a FedRAMP Low ConMon Program in a Homelab](writeups/01-building-fedramp-low-conmon-homelab.md) (main build narrative, ~12 min read)
- [Paramify vs. DIY: What a Few Hundred Lines of Python Replicates from a Commercial GRC Platform](writeups/02-paramify-vs-diy.md) (comparison post, ~7 min read)

Both posts are cross-posted on:

- [brianchaplow.com](https://brianchaplow.com)
- [bytesbourbonbbq.com](https://bytesbourbonbbq.com)

## Why this exists

Most homelab compliance portfolios are paper. Someone reads a few NIST publications,
writes a pretend SSP against a pretend system, and calls it a portfolio project. This
repo is the opposite. Every POA&M item came out of a live Wazuh vulnerability scan
against the real homelab. Every OSCAL artifact was generated by a Python pipeline
against a real DefectDojo instance. The shared-tenancy gap the project documents
(OR-0001) was found by authoring the SSP against my actual running environment,
not invented to demonstrate that I know what a DR looks like.

The other reason is timing. FedRAMP RFC-0024 mandates OSCAL as the required submission
format for all authorization packages by **September 30, 2026**. Every CSP with an
Excel-first compliance workflow is going to have to retrofit OSCAL generation between
now and then, and the retrofit is hard. This pipeline starts OSCAL-first and projects
downward, which puts it on the right side of the deadline from day one.

## Project execution pattern

The project was built across four sequential plans:

| Plan | Status | Summary |
|---|---|---|
| Plan 1 | Done (2026-04-08) | Infrastructure: DefectDojo + RegScale CE VMs, Wazuh agents 016/017, PBS backup integration |
| Plan 2 | Done (2026-04-09) | OSCAL pipelines: Trestle + Python + 130 tests, 5 OSCAL artifacts from live homelab data |
| Plan 3 | Done (2026-04-10) | SSP authoring: 156 controls across 18 families, zero REPLACE_ME, 6 new verify-family.py tests |
| Plan 4 | Done (2026-04-10) | ConMon cycles + DRs + SCR + writeups + portfolio polish |

Each plan's completion is captured in an ADR in [`docs/adr/`](docs/adr/). ADR 0010 is
the pre-execution realignment for Plan 4, documenting the scope decisions that shaped
the final output.

## Pipelines at a glance

**Five stages:** Wazuh Indexer vulnerability state plus Wazuh Manager REST API inventory feed into a Python ingest stage. Findings push to DefectDojo (SLA clocks, dedup, per-product engagements). OSCAL build via Compliance Trestle produces the canonical JSON artifacts (component-definition, 156-control SSP, POA&M). An xlsx render stage projects into official FedRAMP Rev 5 IIW and POA&M templates. RegScale CE receives the SSP and POA&M via OSCAL import.

**Core principle** (from the design spec Section 5.1): OSCAL is the source of truth;
xlsx and markdown are projections. Every artifact is generated, never hand-edited.
Re-running `./pipelines.sh conmon` regenerates the entire monthly cycle from the
current state of DefectDojo and the Wazuh Indexer.

## What this project does not claim

To pre-empt the obvious objections from a careful reviewer:

- **Not 3PAO assessed.** No FedRAMP-recognized Third-Party Assessment Organization has reviewed any of these artifacts. Self-assessment is explicitly not equivalent to a 3PAO assessment under FedRAMP.
- **No agency Authorizing Official approval.** No federal agency AO has signed off on the SSP, POA&M, or any other artifact. The "Approved by: AO (notional)" lines in the DR markdowns are notional and labeled as such.
- **Not on the FedRAMP Marketplace.** The notional MSS is not, and is not on a path to be, listed on the FedRAMP Marketplace. The Marketplace listing is the public artifact of an actual FedRAMP authorization, which this project does not have and does not claim.
- **No Customer Responsibility Matrix in the live SSP.** Real FedRAMP SaaS / PaaS packages require Appendix J (the CRM) detailing which controls the CSP implements versus the customer versus inherited from authorized IaaS. The single-operator homelab has no customer to split with. A demonstrative CRM stub for 10 sample controls lives at [`docs/crm-example.md`](docs/crm-example.md).
- **No FIPS module attestation.** Stock Ubuntu cryptography, no CMVP certificate numbers, no FIPS-validated build. Documented honestly under SC-13 and in the [Scope and framework mapping](#scope-and-framework-mapping) section above.
- **Not a cloud service.** FedRAMP is statutorily limited to cloud computing under 44 USC 3607 and OMB M-24-15. A homelab fails NIST SP 800-145's five essential cloud characteristics. The framework that legally fits a single-operator on-prem mission system is NIST RMF (DoDI 8510.01 for DoD).

These omissions are the boundary between "this project demonstrates FedRAMP-shaped ConMon mechanics on a real, operating environment" and "this project is a FedRAMP authorization." The repo is honest about where that boundary sits.

## About the author

**Brian Chaplow** -- 26-year Navy veteran and cybersecurity practitioner. Focus areas: SOC operations, detection engineering, threat intel, and the GRC layer of cybersecurity.

- [brianchaplow.com](https://brianchaplow.com)
- [github.com/brianchaplow](https://github.com/brianchaplow)
- LinkedIn: search for "Brian Chaplow"

## License

MIT. See [LICENSE](LICENSE).
