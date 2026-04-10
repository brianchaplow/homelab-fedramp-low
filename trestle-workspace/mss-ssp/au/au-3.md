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
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: au-03
---

# au-3 - \[Audit and Accountability\] Content of Audit Records

## Control Statement

Ensure that audit records contain information that establishes the following:

- \[a.\] What type of event occurred;

- \[b.\] When the event occurred;

- \[c.\] Where the event occurred;

- \[d.\] Source of the event;

- \[e.\] Outcome of the event; and

- \[f.\] Identity of any individuals, subjects, or objects/entities associated with the event.

## Control Assessment Objective

- \[AU-03a.\] audit records contain information that establishes what type of event occurred;

- \[AU-03b.\] audit records contain information that establishes when the event occurred;

- \[AU-03c.\] audit records contain information that establishes where the event occurred;

- \[AU-03d.\] audit records contain information that establishes the source of the event;

- \[AU-03e.\] audit records contain information that establishes the outcome of the event;

- \[AU-03f.\] audit records contain information that establishes the identity of any individuals, subjects, or objects/entities associated with the event.

## Control guidance

Audit record content that may be necessary to support the auditing function includes event descriptions (item a), time stamps (item b), source and destination addresses (item c), user or process identifiers (items d and f), success or fail indications (item e), and filenames involved (items a, c, e, and f) . Event outcomes include indicators of event success or failure and event-specific results, such as the system security and privacy posture after the event occurred. Organizations consider how audit records can reveal information about individuals that may give rise to privacy risks and how best to mitigate such risks. For example, there is the potential to reveal personally identifiable information in the audit trail, especially if the trail records inputs or is based on patterns or time of usage.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Wazuh alert records in `wazuh-alerts-4.x-*` satisfy all six AU-3 content elements. (a) Event type: the `rule.description` field identifies what occurred (e.g., "Multiple authentication failures," "File integrity monitoring -- file modified"). (b) Timestamp: `@timestamp` in ISO 8601 UTC with millisecond precision. (c) Where: `agent.name` and `agent.ip` identify the host where the event was generated; `manager.name` identifies the Wazuh node. (d) Source: `data.srcip`, `data.win.eventdata.ipAddress`, or equivalent source-address fields capture the originating entity; for FIM events, the path field identifies the object. (e) Outcome: `rule.level` (0-15 severity scale) and `rule.groups` encode success/failure; for authentication events, `data.win.system.keywords` carries Success/Failure explicitly. (f) Identity: `data.win.eventdata.targetUserName`, `data.srcuser`, or `agent.name` identify the subject or object associated with the event -- covering both human accounts and process identities.

At the network layer, Zeek records in `logs-zeek.haccp-default-*` carry the same six elements: `_path` (event type), `ts` (Unix epoch microseconds, UTC), `id_orig_h`/`id_resp_h` (source/destination addresses satisfying where and source), connection state field (outcome -- S0, SF, REJ, RSTO), and community-id enabling correlation back to the originating Wazuh alert or Arkime PCAP session for identity resolution. The Logstash zeek-enrichment pipeline appends `llm.verdict` (Ollama classification) and OpenCTI TI match fields, enriching the base content without replacing the required six elements. Arkime PCAP provides packet-level source/destination/payload as a forensic backstop for any event where field-level identity resolution is incomplete.

#### Implementation Status: implemented

______________________________________________________________________
