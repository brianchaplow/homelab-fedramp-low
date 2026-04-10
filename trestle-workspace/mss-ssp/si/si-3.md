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
  si-03_odp.01:
    alt-identifier: si-3_prm_1
    profile-values:
      - signature-based and non-signature-based
    profile-param-value-origin: organization
  si-03_odp.02:
    alt-identifier: si-3_prm_2
    profile-values:
      - daily -- Suricata continuous network monitoring plus Wazuh SCA weekly scan; Wazuh agents perform real-time file monitoring via FIM
    profile-param-value-origin: organization
  si-03_odp.03:
    alt-identifier: si-3_prm_3
    profile-values:
      - network entry and exit points (Suricata on smokehouse eth4 SPAN, Zeek on haccp span0) and endpoint (Wazuh FIM on 15 agents)
    profile-param-value-origin: organization
  si-03_odp.04:
    alt-identifier: si-3_prm_4
    profile-values:
      - block malicious code at the OPNsense firewall via Wazuh CDB-fed ACL rules; send alert to Brian Chaplow via Discord #soc-alerts webhook (Shuffle WF1)
    profile-param-value-origin: organization
  si-03_odp.05:
    alt-identifier: si-3_prm_5
    profile-values:
      - Brian Chaplow (system owner, sole operator) via Discord #soc-alerts
    profile-param-value-origin: organization
  si-03_odp.06:
    alt-identifier: si-3_prm_6
    profile-values:
      - Wazuh deduplication in Shuffle WF1 v2 suppresses repeated low-confidence alerts; OPNsense ACL blocks are reviewed manually when a Discord alert fires
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: si-03
---

# si-3 - \[System and Information Integrity\] Malicious Code Protection

## Control Statement

- \[a.\] Implement [Selection (one or more): signature-based; non-signature-based] malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code;

- \[b.\] Automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management policy and procedures;

- \[c.\] Configure malicious code protection mechanisms to:

  - \[1.\] Perform periodic scans of the system [frequency] and real-time scans of files from external sources at [Selection (one or more): endpoint; network entry and exit points] as the files are downloaded, opened, or executed in accordance with organizational policy; and
  - \[2.\] [Selection (one or more): block malicious code; quarantine malicious code; take [action]] ; and send alert to [personnel or roles] in response to malicious code detection; and

- \[d.\] Address the receipt of false positives during malicious code detection and eradication and the resulting potential impact on the availability of the system.

## Control Assessment Objective

- \[SI-03a.\]

  - \[SI-03a.[01]\] [Selection (one or more): signature-based; non-signature-based] malicious code protection mechanisms are implemented at system entry and exit points to detect malicious code;
  - \[SI-03a.[02]\] [Selection (one or more): signature-based; non-signature-based] malicious code protection mechanisms are implemented at system entry and exit points to eradicate malicious code;

- \[SI-03b.\] malicious code protection mechanisms are updated automatically as new releases are available in accordance with organizational configuration management policy and procedures;

- \[SI-03c.\]

  - \[SI-03c.01\]

    - \[SI-03c.01[01]\] malicious code protection mechanisms are configured to perform periodic scans of the system [frequency];
    - \[SI-03c.01[02]\] malicious code protection mechanisms are configured to perform real-time scans of files from external sources at [Selection (one or more): endpoint; network entry and exit points] as the files are downloaded, opened, or executed in accordance with organizational policy;

  - \[SI-03c.02\]

    - \[SI-03c.02[01]\] malicious code protection mechanisms are configured to [Selection (one or more): block malicious code; quarantine malicious code; take [action]] in response to malicious code detection;
    - \[SI-03c.02[02]\] malicious code protection mechanisms are configured to send alerts to [personnel or roles] in response to malicious code detection;

- \[SI-03d.\] the receipt of false positives during malicious code detection and eradication and the resulting potential impact on the availability of the system are addressed.

## Control guidance

System entry and exit points include firewalls, remote access servers, workstations, electronic mail servers, web servers, proxy servers, notebook computers, and mobile devices. Malicious code includes viruses, worms, Trojan horses, and spyware. Malicious code can also be encoded in various formats contained within compressed or hidden files or hidden in files using techniques such as steganography. Malicious code can be inserted into systems in a variety of ways, including by electronic mail, the world-wide web, and portable storage devices. Malicious code insertions occur through the exploitation of system vulnerabilities. A variety of technologies and methods exist to limit or eliminate the effects of malicious code.

Malicious code protection mechanisms include both signature- and nonsignature-based technologies. Nonsignature-based detection mechanisms include artificial intelligence techniques that use heuristics to detect, analyze, and describe the characteristics or behavior of malicious code and to provide controls against such code for which signatures do not yet exist or for which existing signatures may not be effective. Malicious code for which active signatures do not yet exist or may be ineffective includes polymorphic malicious code (i.e., code that changes signatures when it replicates). Nonsignature-based mechanisms also include reputation-based technologies. In addition to the above technologies, pervasive configuration management, comprehensive software integrity controls, and anti-exploitation software may be effective in preventing the execution of unauthorized code. Malicious code may be present in commercial off-the-shelf software as well as custom-built software and could include logic bombs, backdoors, and other types of attacks that could affect organizational mission and business functions.

In situations where malicious code cannot be detected by detection methods or technologies, organizations rely on other types of controls, including secure coding practices, configuration management and control, trusted procurement processes, and monitoring practices to ensure that software does not perform functions other than the functions intended. Organizations may determine that, in response to the detection of malicious code, different actions may be warranted. For example, organizations can define actions in response to malicious code detection during periodic scans, the detection of malicious downloads, or the detection of maliciousness when attempting to open or execute files.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Malicious code protection is implemented at network entry and exit points using both signature-based and non-signature-based mechanisms. Suricata on smokehouse (10.10.20.10, eth4 SPAN) provides continuous signature-based detection, with rule sets maintained under `HomeLab-SOC-v2/configs/suricata/` and updated via `suricata-update`. Wazuh on brisket ingests Suricata `eve.json` alerts via the Wazuh agent on smokehouse, correlating malicious traffic signatures against the `wazuh-alerts-*` index. Zeek on haccp span0 (`reference/phase14/zeek/local.zeek`) and smokehouse eth4 provides complementary non-signature protocol-behavior detection -- JA3/JA4 TLS fingerprinting and anomalous connection pattern analysis that catches threats for which signatures do not yet exist. OpenCTI v7 on brisket aggregates IOC feeds from 6 connectors; the sync cron (`0 */6 * * *`) pushes current malicious indicators to Wazuh CDB lists, creating an IOC-driven detection layer updated every 6 hours. On detection, Shuffle WF1 routes high-confidence alerts to OPNsense and Cloudflare for blocking and sends an immediate Discord #soc-alerts notification to Brian Chaplow. Wazuh FIM provides endpoint real-time file monitoring on all 15 agents, detecting unauthorized file modifications as a non-signature behavioral signal.

The XGBoost ML scorer on brisket (`brisket:5002`, PR-AUC 0.9998) applies behavioral anomaly scoring as a non-signature layer on top of rule-based detection. False positives are addressed through Wazuh deduplication logic in Shuffle WF1 v2, which suppresses repeated low-confidence alerts before they reach the operator. The primary gap for this control is the absence of an endpoint antivirus agent on Linux SOC infrastructure hosts (brisket, haccp, smokehouse) -- malicious code protection on those hosts is network-only (Suricata, Zeek, Wazuh IDS rules) with no host-based AV scanning. OPNsense at the VLAN boundary provides the outer network entry-point blocking layer.

#### Implementation Status: partial

______________________________________________________________________
