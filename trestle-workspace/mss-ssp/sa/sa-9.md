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
  sa-09_odp.01:
    alt-identifier: sa-9_prm_1
    profile-values:
      - "Tailscale: node certificate authentication plus WireGuard encryption in transit; PBS NFS: systemd automount with mount-timeout and idle-timeout hardening per ADR 0005; GCP VM: Wazuh agent enrollment with TLS, SSH key auth only"
    profile-param-value-origin: organization
  sa-09_odp.02:
    alt-identifier: sa-9_prm_2
    profile-values:
      - "daily PBS backup tripwire (manual check per runbooks/monthly-conmon.md Daily PBS backup tripwire section); Wazuh agent keepalive monitoring for GCP VM agent 009; Tailscale admin console for node expiry -- monthly review during ConMon cycle"
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: sa-09
---

# sa-9 - \[System and Services Acquisition\] External System Services

## Control Statement

- \[a.\] Require that providers of external system services comply with organizational security and privacy requirements and employ the following controls: [controls];

- \[b.\] Define and document organizational oversight and user roles and responsibilities with regard to external system services; and

- \[c.\] Employ the following processes, methods, and techniques to monitor control compliance by external service providers on an ongoing basis: [processes, methods, and techniques].

## Control Assessment Objective

- \[SA-09a.\]

  - \[SA-09a.[01]\] providers of external system services comply with organizational security requirements;
  - \[SA-09a.[02]\] providers of external system services comply with organizational privacy requirements;
  - \[SA-09a.[03]\] providers of external system services employ [controls];

- \[SA-09b.\]

  - \[SA-09b.[01]\] organizational oversight with regard to external system services are defined and documented;
  - \[SA-09b.[02]\] user roles and responsibilities with regard to external system services are defined and documented;

- \[SA-09c.\] [processes, methods, and techniques] are employed to monitor control compliance by external service providers on an ongoing basis.

## Control guidance

External system services are provided by an external provider, and the organization has no direct control over the implementation of the required controls or the assessment of control effectiveness. Organizations establish relationships with external service providers in a variety of ways, including through business partnerships, contracts, interagency agreements, lines of business arrangements, licensing agreements, joint ventures, and supply chain exchanges. The responsibility for managing risks from the use of external system services remains with authorizing officials. For services external to organizations, a chain of trust requires that organizations establish and retain a certain level of confidence that each provider in the consumer-provider relationship provides adequate protection for the services rendered. The extent and nature of this chain of trust vary based on relationships between organizations and the external providers. Organizations document the basis for the trust relationships so that the relationships can be monitored. External system services documentation includes government, service providers, end user security roles and responsibilities, and service-level agreements. Service-level agreements define the expectations of performance for implemented controls, describe measurable outcomes, and identify remedies and response requirements for identified instances of noncompliance.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS consumes three external system services, each documented and monitored. (1) Tailscale provides encrypted mesh VPN for remote administrative access from PITBOSS to all in-boundary hosts (brisket TS: 100.124.139.56, haccp TS: 100.74.16.82, smokehouse TS: 100.110.112.98); Tailscale nodes authenticate via device certificates and WireGuard encryption in transit. (2) PBS NFS -- Proxmox Backup Server LXC 300 (smoker, 10.10.30.24) mounts a NFS export from smokehouse (10.10.20.10, 17 TB) as the backup data store; this external dependency for CP-9 backup services is documented in ADR 0005, which also records the 5-day backup gap caused by a mount failure during the 2026-04-07 rack consolidation reboot and the automount hardening fix (`x-systemd.automount,x-systemd.idle-timeout=600,x-systemd.mount-timeout=30`). (3) GCP VM (Wazuh agent 009) -- an externally hosted VM ships logs to the brisket Wazuh Manager; it is explicitly out-of-boundary but the MSS monitoring depends on it for telemetry. Oversight roles: Brian Chaplow (system owner, sole operator) holds all external service oversight responsibility. Compliance monitoring runs on the monthly ConMon cycle via `runbooks/monthly-conmon.md` (PBS backup tripwire, Wazuh agent keepalive check, Tailscale node expiry review).

This control is partial because no formal service-level agreements exist with any external provider (Tailscale is free tier, PBS NFS is self-hosted, GCP VM is personal) and compliance monitoring is informal -- manual tripwire rather than automated alerting for Tailscale or GCP disconnects. ADR 0005 is the definitive external service governance record: it documents a real external-service failure caught, analyzed, and remediated. Cross-reference CP-9 (backup service -- PBS external dependency) and CA-3 (internal connections including the PBS NFS link).

#### Implementation Status: partial

______________________________________________________________________
