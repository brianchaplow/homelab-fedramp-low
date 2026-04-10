---
x-trestle-add-props: []
  # Add or modify control properties here
  # Properties may be at the control or part level
  # Add control level properties like this:
  #   - name: ac1_new_prop
  #     value: new property value
  #
  # Add properties to a statement part like this, where "b." is the label of the target statement part
  #   - name: ac1_new_prop
  #     value: new property value
  #     smt-part: b.
  #
x-trestle-set-params:
  # You may set values for parameters in the assembled SSP by adding
  #
  # ssp-values:
  #   - value 1
  #   - value 2
  #
  # below a section of values:
  # The values list refers to the values in the resolved profile catalog, and the ssp-values represent new values
  # to be placed in SetParameters of the SSP.
  #
  ra-05.02_odp.01:
    alt-identifier: ra-5.2_prm_1
    profile-values:
      - prior to a new scan; when new vulnerabilities are identified and reported
    profile-param-value-origin: organization
  ra-05.02_odp.02:
    alt-identifier: ra-5.2_prm_2
    profile-values:
      - monthly (ConMon pipeline run) and continuously (Wazuh NVD feed refresh)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ra-05.02
---

# ra-5.2 - \[Risk Assessment\] Update Vulnerabilities to Be Scanned

## Control Statement

Update the system vulnerabilities to be scanned [Selection (one or more): [frequency] ; prior to a new scan; when new vulnerabilities are identified and reported].

## Control Assessment Objective

the system vulnerabilities to be scanned are updated [Selection (one or more): [frequency] ; prior to a new scan; when new vulnerabilities are identified and reported].

## Control guidance

Due to the complexity of modern software, systems, and other factors, new vulnerabilities are discovered on a regular basis. It is important that newly discovered vulnerabilities are added to the list of vulnerabilities to be scanned to ensure that the organization can take steps to mitigate those vulnerabilities in a timely manner.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Wazuh's vulnerability detector automatically updates its NVD feed and vendor-specific advisories as part of the Wazuh manager's built-in feed management. When the manager identifies a new CVE relevant to an in-boundary package version, it creates a new document in `wazuh-states-vulnerabilities-*` on the next agent check-in -- no operator action required. The `VULN_INDEX_PATTERN = "wazuh-states-vulnerabilities-*"` wildcard in `pipelines/common/wazuh_indexer.py` ensures the monthly pipeline pull captures any new vulnerability documents across future index shards automatically. OpenCTI v7 on brisket augments this by syncing fresh IOCs from 6 connectors to Wazuh CDB lists every 6 hours (cron `0 */6 * * *`), continuously extending the scanner's IOC-based detection coverage without manual update. The DefectDojo engagement auto-create logic (`_engagement_name()` returns `ConMon YYYY-MM`) ensures each monthly pipeline run opens a fresh engagement rather than silently accumulating into a stale one, so new NVD entries discovered since the prior run are captured as new findings with correct detection dates. Together, the Wazuh built-in NVD refresh and the OpenCTI IOC sync implement RA-5.2 continuously and automatically for both host-based vulnerability enumeration and network-based IOC detection.

#### Implementation Status: implemented

______________________________________________________________________
