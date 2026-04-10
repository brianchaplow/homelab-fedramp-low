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
  sc-08.01_odp:
    alt-identifier: sc-8.1_prm_1
    profile-values:
      - prevent unauthorized disclosure of information and detect changes to information
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sc-08.01
---

# sc-8.1 - \[System and Communications Protection\] Cryptographic Protection

## Control Statement

Implement cryptographic mechanisms to [Selection (one or more): prevent unauthorized disclosure of information; detect changes to information] during transmission.

## Control Assessment Objective

cryptographic mechanisms are implemented to [Selection (one or more): prevent unauthorized disclosure of information; detect changes to information] during transmission.

## Control guidance

Encryption protects information from unauthorized disclosure and modification during transmission. Cryptographic mechanisms that protect the confidentiality and integrity of information during transmission include TLS and IPSec. Cryptographic mechanisms used to protect information integrity include cryptographic hash functions that have applications in digital signatures, checksums, and message authentication codes.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Cryptographic mechanisms protect transmitted information across all in-boundary core service paths. TLS (via OpenSSL) secures Wazuh Manager API (brisket:55000, HTTPS), Wazuh Indexer/OpenSearch (brisket:9200, HTTPS), ELK Elasticsearch (haccp:9200, HTTPS), and Fleet server (haccp:8220, HTTPS) -- providing both confidentiality (ECDHE key exchange + AES-GCM bulk encryption) and integrity (HMAC or AEAD authentication tags) per the TLS record protocol. Wazuh agent-to-manager telemetry (brisket:1514) uses TLS with enrollment-key authentication. PCAP archival sync from haccp to smokehouse uses SSH (AES-based session encryption via OpenSSH). Tailscale remote administration uses WireGuard's ChaCha20-Poly1305 authenticated encryption, which provides both unauthorized-disclosure prevention and change detection for all management traffic crossing the administrative boundary.

Gap: DefectDojo (10.10.30.27:8080), RegScale CE (10.10.30.28:80), and Kibana (haccp:5601) do not implement cryptographic protection of transmitted information -- these paths use plain HTTP. This gap is documented in ADRs 0003 and 0004 as a POA&M item; the upgrade path to TLS for these services is captured in `runbooks/cert-trust.md`. All three are VLAN-scoped with no external exposure and handle synthetic lab data only. Status matches SC-8 at partial -- cryptographic mechanisms protect core Wazuh and ELK transmission paths; the GRC tools and Kibana are unprotected.

#### Implementation Status: partial

______________________________________________________________________
