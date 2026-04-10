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
  pe-06_odp.01:
    alt-identifier: pe-6_prm_1
    profile-values:
      - not-applicable -- no formal physical access log system; Wazuh agent health reviewed daily via WF2 watch digest
    profile-param-value-origin: organization
  pe-06_odp.02:
    alt-identifier: pe-6_prm_2
    profile-values:
      - unexpected host unavailability, Wazuh agent disconnect, or Grafana thermal/infrastructure alert
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: pe-06
---

# pe-6 - \[Physical and Environmental Protection\] Monitoring Physical Access

## Control Statement

- \[a.\] Monitor physical access to the facility where the system resides to detect and respond to physical security incidents;

- \[b.\] Review physical access logs [frequency] and upon occurrence of [events] ; and

- \[c.\] Coordinate results of reviews and investigations with the organizational incident response capability.

## Control Assessment Objective

- \[PE-06a.\] physical access to the facility where the system resides is monitored to detect and respond to physical security incidents;

- \[PE-06b.\]

  - \[PE-06b.[01]\] physical access logs are reviewed [frequency];
  - \[PE-06b.[02]\] physical access logs are reviewed upon occurrence of [events];

- \[PE-06c.\]

  - \[PE-06c.[01]\] results of reviews are coordinated with organizational incident response capabilities;
  - \[PE-06c.[02]\] results of investigations are coordinated with organizational incident response capabilities.

## Control guidance

Physical access monitoring includes publicly accessible areas within organizational facilities. Examples of physical access monitoring include the employment of guards, video surveillance equipment (i.e., cameras), and sensor devices. Reviewing physical access logs can help identify suspicious activity, anomalous events, or potential threats. The reviews can be supported by audit logging controls, such as [AU-2](#au-2) , if the access logs are part of an automated system. Organizational incident response capabilities include investigations of physical security incidents and responses to the incidents. Incidents include security violations or suspicious physical access activities. Suspicious physical access activities include accesses outside of normal work hours, repeated accesses to areas not normally accessed, accesses for unusual lengths of time, and out-of-sequence accesses.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Physical access monitoring relies on the Wazuh SIEM and Grafana environmental alerting as the primary detection mechanisms for physical security events. The Grafana alert "GPU Thermal Critical -- Brisket Above 90C" (uid=dfihoiidr7k00c, `brisket-setup/monitoring/build-grafana-alerts.py`) evaluates the `nvidia_smi_temperature_gpu{job="brisket-nvidia"}` metric on a 2-minute window and routes critical alerts to the `#infrastructure-alerts` Discord channel via the `discord-infrastructure` policy. This alert proved operational during the Phase 14 thermal hardening incident (2026-04-08): the brisket RTX A1000 reached 87C under unbounded Ollama load, triggering detection and remediation (power-capped to 40W, temperature reduced to 63C). Wazuh monitors all 15 in-boundary agents continuously; unexpected agent disconnects or service disruptions serve as indirect indicators of physical access events (power loss, accidental cable pull, or equipment tampering). The WF2 watch digest (cron 0600/1800) reviews agent health and outstanding alerts twice daily. Any detected physical security incident is routed to the homeowner/operator for response, who coordinates consequences through the Wazuh/Shuffle/TheHive incident response pipeline for digital impacts.

This implementation is partial because no dedicated physical access monitoring system is deployed -- no video surveillance cameras, badge readers, or motion sensors exist in the facility. Physical access "log review" is organic: the sole occupant of the equipment room is the homeowner, so anomalous access events would be directly observed rather than reviewed from a log. The Grafana thermal alert and Wazuh agent monitoring provide meaningful physical-access-consequence visibility (equipment tampering or power disruption would manifest as service anomalies) but do not substitute for enterprise-grade physical monitoring controls. This gap is an intentional residential-context scoping decision documented in the whole-project design §PE honest-gaps row.

#### Implementation Status: partial

______________________________________________________________________
