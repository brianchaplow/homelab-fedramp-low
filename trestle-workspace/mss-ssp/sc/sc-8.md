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
  sc-08_odp:
    alt-identifier: sc-8_prm_1
    profile-values:
      - confidentiality and integrity
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sc-08
---

# sc-8 - \[System and Communications Protection\] Transmission Confidentiality and Integrity

## Control Statement

Protect the [Selection (one or more): confidentiality; integrity] of transmitted information.

## Control Assessment Objective

the [Selection (one or more): confidentiality; integrity] of transmitted information is/are protected.

## Control guidance

Protecting the confidentiality and integrity of transmitted information applies to internal and external networks as well as any system components that can transmit information, including servers, notebook computers, desktop computers, mobile devices, printers, copiers, scanners, facsimile machines, and radios. Unprotected communication paths are exposed to the possibility of interception and modification. Protecting the confidentiality and integrity of information can be accomplished by physical or logical means. Physical protection can be achieved by using protected distribution systems. A protected distribution system is a wireline or fiber-optics telecommunications system that includes terminals and adequate electromagnetic, acoustical, electrical, and physical controls to permit its use for the unencrypted transmission of classified information. Logical protection can be achieved by employing encryption techniques.

Organizations that rely on commercial providers who offer transmission services as commodity services rather than as fully dedicated services may find it difficult to obtain the necessary assurances regarding the implementation of needed controls for transmission confidentiality and integrity. In such situations, organizations determine what types of confidentiality or integrity services are available in standard, commercial telecommunications service packages. If it is not feasible to obtain the necessary controls and assurances of control effectiveness through appropriate contracting vehicles, organizations can implement appropriate compensating controls.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Transmission confidentiality and integrity is enforced for all core MSS service-to-service paths using TLS. Wazuh Manager API (brisket:55000) and Wazuh Indexer/OpenSearch (brisket:9200) are HTTPS with self-signed certificates per `runbooks/cert-trust.md`. ELK Elasticsearch on haccp (10.10.30.25:9200) is HTTPS. Wazuh agent-to-manager telemetry on brisket:1514 uses TLS with enrollment-key authentication; agent enrollment on brisket:1515 is TLS-protected. Fluent Bit shipping Zeek logs from smokehouse to brisket:9200 transits over HTTPS. PCAP archival from haccp to smokehouse uses SSH/rsync (encrypted channel). Fleet agent communications to haccp:8220 use HTTPS. Tailscale encrypted mesh (WireGuard-based) protects all administrative remote access paths -- PITBOSS to brisket, sear, smokehouse, and haccp -- providing both confidentiality and integrity for management plane traffic.

Gap: DefectDojo on dojo (10.10.30.27:8080) and RegScale CE on regscale (10.10.30.28:80) are HTTP-only per ADRs 0003 and 0004 respectively. Kibana on haccp (:5601) is also HTTP. These services handle synthetic lab data only, are scoped to VLAN 30 with no external exposure, and are subject to a POA&M item documented in ADR 0003 §Consequences. The upgrade path to HTTPS for these services is documented in `runbooks/cert-trust.md`. Status is partial -- the Wazuh and ELK core paths protect transmission confidentiality and integrity; the two GRC tools and Kibana do not.

#### Implementation Status: partial

______________________________________________________________________
