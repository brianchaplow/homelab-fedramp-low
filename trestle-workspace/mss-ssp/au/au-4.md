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
  au-04_odp:
    alt-identifier: au-4_prm_1
    profile-values:
      - Wazuh-alerts on brisket NVMe (capacity monitored by Grafana alert at 90% disk usage); Zeek/ELK logs on haccp 2TB dedicated NVMe; PCAP on haccp 2TB NVMe with freeSpaceG=100 auto-purge plus 90-day smokehouse archive; Prometheus metrics 90-day TSDB retention
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: au-04
---

# au-4 - \[Audit and Accountability\] Audit Log Storage Capacity

## Control Statement

Allocate audit log storage capacity to accommodate [audit log retention requirements].

## Control Assessment Objective

audit log storage capacity is allocated to accommodate [audit log retention requirements].

## Control guidance

Organizations consider the types of audit logging to be performed and the audit log processing requirements when allocating audit log storage capacity. Allocating sufficient audit log storage capacity reduces the likelihood of such capacity being exceeded and resulting in the potential loss or reduction of audit logging capability.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Audit log storage is allocated across three purpose-sized tiers. On brisket, the Wazuh Indexer (OpenSearch) stores `wazuh-alerts-4.x-*` on the host NVMe -- the Grafana Unified Alerting rule "Disk Critical -- Usage Above 90%" (`build-grafana-alerts.py`) evaluates every 5 minutes and routes a Discord notification to `#infrastructure-alerts` before the brisket data volume reaches saturation. On haccp, ELK Elasticsearch stores `logs-zeek.haccp-default-*` on a dedicated 2TB WD SN720 NVMe (boot/root) that is separate from the PCAP drive, preventing Zeek log growth from starving PCAP capacity. Arkime PCAP is stored on a dedicated Samsung 990 EVO Plus 2TB NVMe at `/opt/arkime/raw` (~1.8TB usable); Arkime's `freeSpaceG=100` configuration triggers automatic oldest-PCAP deletion before the volume reaches full, preventing capture interruption due to disk exhaustion.

Overflow protection for PCAP is handled by the nightly rsync cron (0300) that archives completed pcap files from haccp `/opt/arkime/raw` to smokehouse's 17TB NFS volume (`~bchaplow/pcap-archive/haccp/`), after which a `find ... -mtime +90 -delete` sweep enforces the 90-day off-line retention window required by AU-11 and M-21-31. Prometheus metrics are retained for 90 days via `--storage.tsdb.retention.time=90d`. The current gap in this tier is the absence of an explicit Elasticsearch ILM lifecycle policy governing rollover of `wazuh-alerts-*` and `logs-zeek.haccp-default-*` indices -- both are retained by default (disk not full) but retention is not enforced by a documented policy object. This gap is tracked in the ConMon roadmap.

#### Implementation Status: implemented

______________________________________________________________________
