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
  mp-6_prm_1:
    aggregates:
      - mp-06_odp.01
      - mp-06_odp.02
      - mp-06_odp.03
    profile-param-value-origin: organization
  mp-6_prm_2:
    aggregates:
      - mp-06_odp.04
      - mp-06_odp.05
      - mp-06_odp.06
    profile-param-value-origin: organization
  mp-06_odp.01:
    profile-values:
      - permanently installed internal NVMe and SATA drives in all in-boundary bare-metal hosts (brisket, haccp, smokehouse); Proxmox VM disk images for dojo and regscale
    profile-param-value-origin: organization
  mp-06_odp.02:
    profile-values:
      - full-disk overwrite using shred or dd if=/dev/zero for functional drives; physical destruction for failed or damaged drives
    profile-param-value-origin: organization
  mp-06_odp.03:
    profile-values:
      - full-disk overwrite using shred or dd if=/dev/zero before any drive is repurposed for a different host or data classification
    profile-param-value-origin: organization
  mp-06_odp.04:
    profile-values:
      - commensurate with FedRAMP Low; full-disk overwrite satisfies NIST SP 800-88 Rev 1 Clear for ATA drives
    profile-param-value-origin: organization
  mp-06_odp.05:
    profile-values:
      - full-disk overwrite per NIST SP 800-88 Rev 1 Clear
    profile-param-value-origin: organization
  mp-06_odp.06:
    profile-values:
      - full-disk overwrite per NIST SP 800-88 Rev 1 Clear
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: mp-06
---

# mp-6 - \[Media Protection\] Media Sanitization

## Control Statement

- \[a.\] Sanitize [organization-defined system media] prior to disposal, release out of organizational control, or release for reuse using [organization-defined sanitization techniques and procedures] ; and

- \[b.\] Employ sanitization mechanisms with the strength and integrity commensurate with the security category or classification of the information.

## Control Assessment Objective

- \[MP-06a.\]

  - \[MP-06a.[01]\] [system media] is sanitized using [sanitization techniques and procedures] prior to disposal;
  - \[MP-06a.[02]\] [system media] is sanitized using [sanitization techniques and procedures] prior to release from organizational control;
  - \[MP-06a.[03]\] [system media] is sanitized using [sanitization techniques and procedures] prior to release for reuse;

- \[MP-06b.\] sanitization mechanisms with strength and integrity commensurate with the security category or classification of the information are employed.

## Control guidance

Media sanitization applies to all digital and non-digital system media subject to disposal or reuse, whether or not the media is considered removable. Examples include digital media in scanners, copiers, printers, notebook computers, workstations, network components, mobile devices, and non-digital media (e.g., paper and microfilm). The sanitization process removes information from system media such that the information cannot be retrieved or reconstructed. Sanitization techniques--including clearing, purging, cryptographic erase, de-identification of personally identifiable information, and destruction--prevent the disclosure of information to unauthorized individuals when such media is reused or released for disposal. Organizations determine the appropriate sanitization methods, recognizing that destruction is sometimes necessary when other methods cannot be applied to media requiring sanitization. Organizations use discretion on the employment of approved sanitization techniques and procedures for media that contains information deemed to be in the public domain or publicly releasable or information deemed to have no adverse impact on organizations or individuals if released for reuse or disposal. Sanitization of non-digital media includes destruction, removing a classified appendix from an otherwise unclassified document, or redacting selected sections or words from a document by obscuring the redacted sections or words in a manner equivalent in effectiveness to removing them from the document. NSA standards and policies control the sanitization process for media that contains classified information. NARA policies control the sanitization process for controlled unclassified information.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

All permanently installed drives in the MSS boundary are sanitized before disposal or reuse using full-disk overwrite (via `shred` or `dd if=/dev/zero`) for functional drives, or physical destruction for failed media, per NIST SP 800-88 Rev 1 Clear. The 2026-04-07 rack consolidation involved three drive swaps (haccp 2TB Samsung 990 EVO Plus PCAP drive, pitcrew +512GB, smoker +1TB) -- the most recent concrete event where this policy applied to replaced drives. PBS daily snapshots (smoker LXC 300 to smokehouse NFS) ensure data is preserved at the logical layer before any physical media swap. Proxmox VM disk images (dojo VMID 201, regscale VMID 301) are retired by deleting the disk image via the hypervisor, not by sanitizing physical media. Because the MSS uses no removable media, MP-6 applies exclusively to permanently installed drives at end of service life or during hardware replacement.

#### Implementation Status: implemented

______________________________________________________________________
