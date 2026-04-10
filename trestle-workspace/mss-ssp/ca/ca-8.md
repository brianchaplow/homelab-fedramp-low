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
  ca-08_odp.01:
    alt-identifier: ca-8_prm_1
    profile-values:
      - annually; ad hoc following significant system change
    profile-param-value-origin: organization
  ca-08_odp.02:
    alt-identifier: ca-8_prm_2
    profile-values:
      - VLAN 40 target segment (10.10.40.0/24): DVWA + Juice Shop (10.10.40.10), Metasploitable 3 Linux (10.10.40.20), Metasploitable 3 Win (10.10.40.21), WordPress (10.10.40.30), crAPI (10.10.40.31)
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ca-08
---

# ca-8 - \[Assessment, Authorization, and Monitoring\] Penetration Testing

## Control Statement

Conduct penetration testing [frequency] on [system(s) or system components].

## Control Assessment Objective

penetration testing is conducted [frequency] on [system(s) or system components].

## Control guidance

Penetration testing is a specialized type of assessment conducted on systems or individual system components to identify vulnerabilities that could be exploited by adversaries. Penetration testing goes beyond automated vulnerability scanning and is conducted by agents and teams with demonstrable skills and experience that include technical expertise in network, operating system, and/or application level security. Penetration testing can be used to validate vulnerabilities or determine the degree of penetration resistance of systems to adversaries within specified constraints. Such constraints include time, resources, and skills. Penetration testing attempts to duplicate the actions of adversaries and provides a more in-depth analysis of security- and privacy-related weaknesses or deficiencies. Penetration testing is especially important when organizations are transitioning from older technologies to newer technologies (e.g., transitioning from IPv4 to IPv6 network protocols).

Organizations can use the results of vulnerability analyses to support penetration testing activities. Penetration testing can be conducted internally or externally on the hardware, software, or firmware components of a system and can exercise both physical and technical controls. A standard method for penetration testing includes a pretest analysis based on full knowledge of the system, pretest identification of potential vulnerabilities based on the pretest analysis, and testing designed to determine the exploitability of vulnerabilities. All parties agree to the rules of engagement before commencing penetration testing scenarios. Organizations correlate the rules of engagement for the penetration tests with the tools, techniques, and procedures that are anticipated to be employed by adversaries. Penetration testing may result in the exposure of information that is protected by laws or regulations, to individuals conducting the testing. Rules of engagement, contracts, or other appropriate mechanisms can be used to communicate expectations for how to protect this information. Risk assessments guide the decisions on the level of independence required for the personnel conducting penetration testing.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS homelab has a dedicated penetration testing capability targeting the VLAN 40 isolated segment (10.10.40.0/24). All attacks are constrained to VLAN 40 per `CLAUDE.md` §"Conventions"; the `./run_attack.sh` wrapper provides ground-truth logging for each session.

The attack platform is sear (10.10.20.20, Kali Linux, 32GB RAM, GTX 1650 Ti), the dedicated red-team box. The Kali toolset was updated per the fleet patch of 2026-03-31. SSH access is `butcher@10.10.20.20` (Tailscale: `butcher@100.86.67.91`). Caldera v5.3.0 (smoker:8888, 10.10.30.21) serves as the adversary emulation platform with 4 Sandcat agents enrolled. Red team (Caldera `red` account) and Blue team (Caldera `blue` account) are configured; Shuffle WF3 integrates Caldera via `$caldera_url` and `$caldera_api_key` workflow variables.

Target systems are the full VLAN 40 segment: DVWA + Juice Shop (10.10.40.10, web application), Metasploitable 3 Linux (10.10.40.20, multi-service), Metasploitable 3 Win (10.10.40.21, multi-service), WordPress (10.10.40.30, WPScan target), crAPI (10.10.40.31, REST API), vsftpd (10.10.40.32, FTP), SMTP relay (10.10.40.42), and SNMPd (10.10.40.43). MokerLink L3 switch ACL (10.10.10.2) and OPNsense firewall (10.10.10.1) enforce VLAN 40 isolation -- sear (VLAN 20) cannot route to VLAN 40 except through the explicit attack path, preventing lateral movement to production infrastructure.

Wazuh detection validation was completed in Phase 7 (documented in `CLAUDE.md` §v3 Migration Status): Caldera red-team exercises validated Wazuh detection rules across the target set. This detection-validation feedback loop is the primary output of each penetration test cycle.

CA-8 is partially implemented: the penetration testing capability is fully operational and detection validation has been performed. The named gap is that no formal penetration test report artifact currently exists in the repo -- `./run_attack.sh` session logs exist on sear but are not committed. A formal pen-test report artifact is a Plan 4 writeup item.

#### Implementation Status: partial

______________________________________________________________________
