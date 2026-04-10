# Deviation Request OR-0001 -- Shared-Tenancy Compute on brisket

## DR metadata

- **DR ID:** OR-0001
- **Category:** Operational Requirement
- **Submitted:** 2026-04-10
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Finding summary

The brisket host (10.10.20.30) -- designated as the MSS Core component
in the authorization boundary -- is also the runtime host for two
non-MSS workloads:

1. **AlgoTrader** -- autonomous day-trading bot (LSTM + XGBoost +
   FinBERT + Claude/Ollama). Currently paused as of 2026-04-01.
2. **Capitol Signals API** -- Congressional Trade Correlation Engine
   (Phases 1-7 live, port 5010).

Per FedRAMP guidance on logical separation between authorization
boundaries, production GRC/SOC compute should not co-tenant with
non-GRC workloads on the same physical hardware unless logical
isolation is documented and assessed.

## Why this exists

brisket is the homelab's most capable single host (Intel Ultra 9 285,
64 GB RAM, RTX A1000). In a homelab pilot deployment, dedicating
this hardware exclusively to MSS would leave the non-MSS workloads
homeless and force a hardware purchase that's not feasible for the
pilot phase.

This gap was **discovered during SSP authoring** (Plan 3) when
documenting SC-32 (Information System Partitioning) and AC-4
(Information Flow Enforcement). The SSP authoring process surfaced
the gap; this DR documents the acceptance decision.

## Compensating controls

The shared-tenancy risk is mitigated by:

1. **cgroup isolation** -- each tenant workload runs in a Docker
   container with explicit memory and CPU limits (`mem_limit`,
   `cpus`), preventing one workload from starving the others.

2. **Network namespace isolation** -- Docker bridge networks separate
   the MSS workload network from the AlgoTrader/Capitol Signals
   networks. Inter-container communication is restricted to documented
   ingress paths only (no cross-stack bridging).

3. **Least-privilege service accounts** -- each tenant runs as a
   non-root user with minimal Linux capabilities. Docker security
   options drop all capabilities except those explicitly required.

4. **File system isolation** -- each tenant workload writes to its own
   directory tree under `/opt/<tenant>/`; cross-tenant filesystem
   access requires explicit bind mounts (none configured).

5. **Wazuh agent monitors all activity** on brisket (agent 015)
   including non-MSS tenant workloads, providing AU-2 audit visibility
   across the shared host.

6. **Backup separation** -- MSS and tenant workloads have separate PBS
   backup jobs allowing independent restore.

7. **GPU power cap** -- the shared RTX A1000 is power-capped to 40W
   via `nvidia-power-cap.service` (persistent across reboot),
   preventing tenant GPU workloads from thermal-throttling MSS
   services. See parent project CLAUDE.md Phase 14 thermal hardening.

## Risk acceptance rationale

For the pilot phase, the shared-tenancy risk is **accepted** because:

- The mitigations above provide effective logical isolation
- The pilot is a single-tenant single-operator environment with no
  external customer data
- The operational benefit (not forcing a hardware purchase) is
  significant for a demonstration-grade deployment
- A scale-out plan (dedicated hardware for MSS) is documented as a
  future activity

## Proposed disposition

Accept the shared-tenancy risk under this Operational Requirement DR.
Document the compensating controls in SSP SC-32 (Information System
Partitioning) and AC-4 (Information Flow Enforcement).

## Reviewer approval (notional)

- **Approved by:** AO (notional)
- **Approval date:** 2026-04-10
- **Expiration:** 2026-10-10 (6-month review cadence -- shorter than
  default to force re-assessment as the homelab evolves)

## Future state

When dedicated hardware becomes available, migrate AlgoTrader and
Capitol Signals to a separate host, removing the shared-tenancy
situation. At that point this DR can be closed.

## Notes

This is the **most valuable** DR in this package from a learning
perspective. It demonstrates that the SSP authoring process surfaced a
real, defensible compliance gap in the homelab -- and that the operator
chose to document and accept it rather than fabricate a clean state.
This is the honest "found a gap in my own environment" moment that
hiring managers respond to in interviews.

The 6-month expiration (rather than the default 12-month) reflects the
fact that shared tenancy is a temporary pilot constraint, not a
permanent architectural decision. A real CSP would schedule the
hardware procurement to close this DR before expiration.
