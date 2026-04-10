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
  au-09_odp:
    alt-identifier: au-9_prm_1
    profile-values:
      - Brian Chaplow (system owner, sole operator) via Discord #infrastructure-alerts (Grafana alert on host unreachability)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: au-09
---

# au-9 - \[Audit and Accountability\] Protection of Audit Information

## Control Statement

- \[a.\] Protect audit information and audit logging tools from unauthorized access, modification, and deletion; and

- \[b.\] Alert [personnel or roles] upon detection of unauthorized access, modification, or deletion of audit information.

## Control Assessment Objective

- \[AU-09a.\] audit information and audit logging tools are protected from unauthorized access, modification, and deletion;

- \[AU-09b.\] [personnel or roles] are alerted upon detection of unauthorized access, modification, or deletion of audit information.

## Control guidance

Audit information includes all information needed to successfully audit system activity, such as audit records, audit log settings, audit reports, and personally identifiable information. Audit logging tools are those programs and devices used to conduct system audit and logging activities. Protection of audit information focuses on technical protection and limits the ability to access and execute audit logging tools to authorized individuals. Physical protection of audit information is addressed by both media protection controls and physical and environmental protection controls.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Audit information protection relies on three complementary controls. First, transport security: Wazuh Indexer (OpenSearch) at brisket:9200 requires TLS and HTTP basic authentication (`admin` account, password stored only in `.env` which is gitignored per CLAUDE.md conventions and never committed to version control); ELK Elasticsearch at haccp:9200 requires TLS and `elastic` user authentication. Logstash output in `zeek-enrichment.conf` (lines 287-299) authenticates to Elasticsearch with TLS and credentials before writing any enriched records. Second, network isolation: both OpenSearch (brisket) and Elasticsearch (haccp) run in Docker networks with no host-port exposure beyond the documented service ports; Wazuh alert indices are write-only from the Wazuh Manager container -- enrolled agents cannot directly write to, read from, or delete index data. Third, host-level access controls: UFW enforces default-deny ingress on all in-boundary Linux hosts, requiring explicit port-level allows that are documented in ADR 0002 and CLAUDE.md. PCAP files on haccp at `/opt/arkime/raw` are owned by `nobody:daemon` (Arkime drops privileges after start via `dropUser=nobody`/`dropGroup=daemon`), preventing any user-context process from writing or deleting PCAP directly.

The gap in this control is the absence of write-once or WORM storage for audit records and the absence of cryptographic integrity verification (e.g., hash chaining) applied to index content. Wazuh FIM could be configured to monitor the Docker volume mount points on brisket and haccp to detect unauthorized modification or deletion of index files on disk -- this is not currently wired. Until file-integrity monitoring is applied to the audit index data paths and a WORM or integrity-verification mechanism is in place, this control is assessed as partial.

#### Implementation Status: partial

______________________________________________________________________
