# Deviation Requests

FedRAMP Continuous Monitoring includes a documented process for handling
findings that cannot or will not be remediated in their original form.
There are exactly **three categories** of deviation request defined by
the FedRAMP ConMon Deviation Request Guide:

| Category | When to use | This package |
|---|---|---|
| **Risk Adjustment (RA)** | Finding's risk rating is wrong for your environment due to compensating controls | RA-0001 (Grafana exposure) |
| **False Positive (FP)** | Finding isn't actually present (scanner error, signature lag, patched but not yet reflected upstream) | FP-0001 (Ubuntu ESM lag) |
| **Operational Requirement (OR)** | Finding is real and accepted because remediating breaks required functionality | OR-0001 (shared tenancy) |

## DRs in this package

### RA-0001 -- Grafana Exposure Risk Adjustment

A Grafana CVE rated High by NVD is downgraded to Low because the
service is only reachable from the operator workstation behind a
firewall and a switch ACL. Demonstrates **risk re-rating with
compensating controls**.

### FP-0001 -- Ubuntu ESM CVE Tracker Lag

A class of false-positive findings caused by NVD lagging behind Ubuntu
ESM patch releases. Demonstrates **vendor-vs-scanner mismatch
handling**.

### OR-0001 -- Shared-Tenancy Compute on brisket

The MSS Core host also runs AlgoTrader and Capitol Signals tenant
workloads. Demonstrates **operationally-required risk acceptance with
documented compensating controls**.

## Why all three

Coverage of all three DR categories in a single package demonstrates
fluency with the FedRAMP DR vocabulary. Real CSPs handle dozens of DRs
per cycle; this package shows the operator can write any of the three
types.

## Format

Each DR is markdown for readability and version control. If a FedRAMP
DR template xlsx were available, an xlsx version would be generated
alongside. The markdown is the canonical form for this portfolio --
it's more useful for a public-facing repo than a binary spreadsheet,
and it diffs cleanly across ConMon cycles.

## DR lifecycle

DRs follow a lifecycle:

1. **Submitted** -- operator documents the finding, justification, and compensating controls
2. **Reviewed** -- AO (or delegate) evaluates the technical justification
3. **Approved/Denied** -- AO signs off (or requests remediation)
4. **Active** -- DR is in effect; finding tracks against adjusted SLA or is excluded from SLA
5. **Expired/Closed** -- DR reaches its expiration date and must be renewed or the underlying finding is resolved

In this homelab pilot, steps 2-3 are notional (no real AO). The
documentation pattern is real and matches what a CSP would submit.
