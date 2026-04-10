# Deviation Request RA-0001 -- Grafana Exposure Risk Adjustment

## DR metadata

- **DR ID:** RA-0001
- **Category:** Risk Adjustment
- **Submitted:** 2026-04-10
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Linked POA&M item

- **POA&M Item ID:** e19cafa0-bab (representative -- actual Grafana-specific CVEs receive the same treatment)
- **Original Severity:** High
- **Proposed Adjusted Severity:** Low
- **Affected component:** Grafana on brisket (10.10.20.30:3000)

## Finding summary

Wazuh vulnerability detection surfaces High-severity CVEs against packages
installed on brisket that serve the Grafana monitoring UI (port 3000).
DefectDojo applies the corresponding High SLA (90-day remediation window)
per the FedRAMP Low SLA profile.

This DR covers the class of Grafana-related CVEs where the scanner-assigned
severity does not reflect the actual exposure in our environment.

## Technical justification for adjustment

The Grafana service on brisket is **not internet-exposed**. Its actual
attack surface is restricted by two compensating controls:

1. **OPNsense inter-VLAN firewall** denies all inbound traffic to
   10.10.20.30:3000 from VLANs 30, 40, 50, and the WAN. Only VLAN 10
   (Management -- PITBOSS, 10.10.10.100) and VLAN 20 (SOC -- sear,
   10.10.20.20) can reach port 3000. See `reference/network.md`
   firewall rules table.

2. **MokerLink switch ACL** enforces intra-VLAN microsegmentation
   between sear and brisket on VLAN 20. Only the operator workstation
   (PITBOSS) and the sear analyst host can SSH or hit web ports on
   brisket. See `reference/network.md` MokerLink ACL section.

Effective exposure: **single operator workstation + single analyst host
on a private VLAN behind a firewall behind a NAT**.

The vulnerability requires authenticated access to Grafana to exploit;
all Grafana accounts use named operators with non-default credentials
(per IA-2). There is no anonymous read or write path.

## Risk re-rating

| Factor | NVD/Default | Adjusted |
|---|---|---|
| Attack vector | Network | Adjacent (private VLAN) |
| Attack complexity | Low | High |
| Privileges required | Low | High (auth required) |
| User interaction | None | None |
| Scope | Unchanged | Unchanged |
| Confidentiality impact | High | Low (limited data exposure) |
| Integrity impact | High | Low |
| Availability impact | High | Low |
| **Overall** | **High (CVSS 7.8)** | **Low (CVSS 3.1)** |

## Compensating controls cited

- **SC-7** Boundary Protection (OPNsense inter-VLAN firewall)
- **AC-3** Access Enforcement (MokerLink ACL microsegmentation)
- **IA-2** Identification and Authentication (named accounts only)
- **AU-2** Event Logging (Wazuh agent on brisket logs all auth events)

## Proposed disposition

Adjust this finding's severity from **High to Low** and re-apply the
FedRAMP Low SLA timeline (365 days instead of 90 days). The finding
remains open and will be remediated during the next Grafana update
cycle.

## Reviewer approval (notional)

- **Approved by:** AO (notional -- homelab pilot)
- **Approval date:** 2026-04-10
- **Expiration:** 2027-04-10 (annual review)

## Notes

This is a real RA-DR pattern that FedRAMP CSPs use frequently. The
specific scenario (compensating controls on a private interface)
represents the most common reason a high-CVSS vuln gets risk-adjusted
in real ConMon programs.

The network isolation described above is verified by:
- OPNsense firewall rule export (see `evidence/configs/`)
- MokerLink ACL configuration (see `reference/network.md`)
- Wazuh agent AU-2 logging on brisket (agent 015)
