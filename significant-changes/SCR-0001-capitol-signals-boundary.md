# Significant Change Request SCR-0001 -- Add Capitol Signals API to Authorization Boundary

## SCR metadata

- **SCR ID:** SCR-0001
- **Submitted:** 2026-05-10
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low
- **Change category:** Significant (new service in boundary)
- **Status:** Pending AO approval (notional)

## Proposed change

Add the **Capitol Signals API** (currently running on brisket:5010 as
an out-of-boundary tenant workload) as a second in-scope service under
the MSS authorization boundary.

## Why this is a significant change

Per FedRAMP guidance, a change is "significant" if it:

- Adds a new component to the authorization boundary
- Adds a new external connection
- Changes the system's data classification
- Materially changes the risk posture

This change adds a new in-scope service component (the Capitol Signals
API endpoint and its Postgres database), which qualifies as a
Significant Change requiring AO approval before implementation.

It also interacts with the open DR OR-0001 (shared-tenancy compute on
brisket) -- that DR's risk acceptance is predicated on Capitol Signals
being *out of boundary*. Bringing Capitol Signals in-boundary resolves
part of OR-0001 for that workload but raises separate SC-32 / AC-4
questions about the remaining out-of-boundary tenants.

## Risk analysis

| Risk area | Current state | Post-change state | Net |
|---|---|---|---:|
| Components in IIW | 7 (5 agents + 2 non-agent) | 8 (+1 Capitol Signals service) | +1 |
| External connections | Customer telemetry, Tailscale, PBS | Same + Congressional trade data ingest from House/Senate API | +1 |
| Data classification | All Low | Capitol Signals data is **public** but the service availability becomes more important | Unchanged |
| Required new controls | Existing 156 | Extends 5 controls: AC-3, SC-7, SC-13, AU-2, CM-8 | 5 extended |
| POA&M impact | 25,416 (May cycle) | Add Capitol Signals package scan results to next cycle | +unknown |
| DR interactions | OR-0001 covers shared tenancy | OR-0001 still covers AlgoTrader; Capitol Signals removed from that DR | partial close |

## Controls requiring extension

- **AC-3** Access Enforcement -- add Capitol Signals API authentication mechanism
  (API key header, no session-based auth; document token rotation policy)
- **SC-7** Boundary Protection -- document the new external API ingress
  (House/Senate trade data feed) and egress to congressional data sources
- **SC-13** Cryptographic Protection -- verify Capitol Signals uses approved
  TLS for outbound API calls to data sources (confirm cipher suites)
- **AU-2** Event Logging -- add Capitol Signals application logs to the
  Wazuh agent shipping configuration on brisket (agent 015); route to
  Wazuh Manager with `capitol-signals` tag for search
- **CM-8** Component Inventory -- update `inventory/overlay.yaml` to
  mark `capitol-signals` as `boundary: in` with function `trade-correlation`

## Migration plan

1. Update `inventory/overlay.yaml` to mark `capitol-signals` as
   `boundary: in`, with metadata describing the service (function,
   ports, data classification)
2. Run `./pipelines.sh inventory && ./pipelines.sh render-iiw` to
   regenerate the IIW with the new component row
3. Author Capitol-Signals-specific implementation prose updates in
   `trestle-workspace/mss-ssp/ac/ac-3.md`, `sc/sc-7.md`, `sc/sc-13.md`,
   `au/au-2.md`, `cm/cm-8.md`
4. Re-assemble SSP via `./pipelines.sh ssp-assemble`
5. Add a Capitol Signals DefectDojo product (product id=6) and a
   Wazuh agent filter so `./pipelines.sh conmon` captures Capitol
   Signals findings in the next cycle
6. Document the boundary change in SSP section 9 ("System Environment")
7. Update OR-0001 to reflect that Capitol Signals is no longer covered
   under the shared-tenancy DR (AlgoTrader remains covered)

## Proposed disposition

**Pending AO approval.** Implementation deferred until next
authorization cycle.

For the homelab pilot, this SCR exists as a **demonstration artifact**
showing understanding that the boundary is not static -- real CSPs
process Significant Change Requests on an ongoing basis, and the
decision to expand or contract the boundary must be documented
*before* implementation, not after.

## Reviewer approval (notional)

- **Submitted by:** MSS Operator
- **Approved by:** AO (notional)
- **Approval date:** Pending
- **Implementation start:** Next authorization cycle

## Alternatives considered

1. **Keep Capitol Signals out of boundary (status quo).** Cost: OR-0001
   continues to cover the shared-tenancy risk indefinitely. Benefit:
   no migration work, no additional control authoring.

2. **Move Capitol Signals to a separate host.** Cost: hardware
   procurement + deployment time + new Wazuh agent + new PBS backup
   target. Benefit: cleanly separates the workload from the MSS boundary
   without requiring a boundary expansion.

3. **Expand the boundary to include Capitol Signals (this SCR).**
   Cost: 5 controls extended, new IIW row, new DefectDojo product.
   Benefit: legitimizes the shared-tenancy situation by making Capitol
   Signals a documented in-scope service; a future auditor sees a
   single consistent picture rather than an always-renewing DR.

## Notes

This SCR is intentionally documented but **not implemented** in this
pilot. Real CSPs distinguish between "submitted" SCRs and "approved
and implemented" ones; tracking the documentation pattern is the
learning artifact here.

The decision on which alternative to pursue would, in a real program,
involve the AO, system owner, and security officer. Documenting all
three options in the SCR (rather than presenting only the preferred
alternative) reflects the deliberation pattern a real approval process
would use.
