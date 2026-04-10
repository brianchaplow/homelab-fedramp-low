# Deviation Request FP-0001 -- Ubuntu ESM CVE Tracker Lag

## DR metadata

- **DR ID:** FP-0001
- **Category:** False Positive
- **Submitted:** 2026-04-10
- **System:** Managed SOC Service (MSS)
- **Baseline:** FedRAMP Low

## Linked POA&M item(s)

This DR covers a class of findings rather than a single item: any CVE
that the Wazuh vulnerability detector flags as "vulnerable" on an Ubuntu
24.04 host where `apt list --installed` shows the patched version is
already installed.

Representative examples from the current POA&M:

- CVE-2024-7883 in libclang1-18 (uuid: 61ef953f... -- Low)
- Openssl Heap Overflow (uuid: 7fd5a114... -- High)

Both exhibit the pattern where Canonical's Ubuntu Security Notice (USN)
confirms the patch exists in the noble-security apt repository, but the
upstream NVD database has not yet updated to reflect the fix.

## Finding summary

The Wazuh vulnerability detection module compares the installed version
of a package against the upstream CVE database (NVD). If NVD has not
yet been updated to reflect that the Ubuntu ESM patch addresses the
CVE in the patched version, Wazuh continues to report the package as
vulnerable.

This creates a window of false positives between Ubuntu's patch
release and NVD's data update -- typically 1-2 weeks.

## Justification

Evidence that the package is patched on the affected host:

```bash
$ apt-get changelog <package> | head -20
# Shows the ESM patch entry referencing the CVE
$ dpkg -l <package> | grep ^ii
# Shows the installed version contains the patched release
```

The Ubuntu Security Notice (USN) referenced in the apt changelog
explicitly states the CVE is mitigated.

For the MSS in-boundary hosts (brisket, haccp, dojo, regscale -- all
Ubuntu 24.04 LTS), `unattended-upgrades` is enabled and applies
noble-security updates automatically (per SI-2 Flaw Remediation).
The gap between Canonical's patch and NVD's acknowledgment is a
data-source synchronization issue, not a remediation failure.

## Compensating controls

- **SI-2** Flaw Remediation (unattended-upgrades applies ESM patches automatically)
- **CA-7** Continuous Monitoring (next Wazuh re-scan after NVD updates will close the finding)

## Proposed disposition

Mark these findings as **False Positive** with reference to:

1. The local apt changelog confirming the patch
2. The vendor (Canonical) USN identifier
3. Expected NVD update timeline (typically 7-14 days)

The findings will auto-resolve in the next ConMon cycle once NVD
updates. No manual remediation work is required.

## Reviewer approval (notional)

- **Approved by:** AO (notional)
- **Approval date:** 2026-04-10
- **Expiration:** Per-finding (resolves on next NVD update)

## Notes

This DR pattern is extremely common for Ubuntu ESM users. Real CSPs
running Ubuntu encounter this every month. Documenting it well saves
significant POA&M-tracker noise and prevents the SLA clock from
running on findings that are already remediated at the host level.

The class-based approach (covering all findings matching this pattern,
not just a single CVE) is the practical way to handle this in
production -- submitting a per-CVE FP-DR for each instance of NVD lag
would generate more paperwork than the lag itself.
