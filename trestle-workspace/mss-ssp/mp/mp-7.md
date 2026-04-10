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
  mp-07_odp.01:
    alt-identifier: mp-7_prm_2
    profile-values:
      - all removable portable storage devices (USB flash drives, external hard drives, optical discs, SD cards, magnetic tapes)
    profile-param-value-origin: organization
  mp-07_odp.02:
    alt-identifier: mp-7_prm_1
    profile-values:
      - prohibit
    profile-param-value-origin: organization
  mp-07_odp.03:
    alt-identifier: mp-7_prm_3
    profile-values:
      - all in-boundary bare-metal hosts: brisket (10.10.20.30), haccp (10.10.30.25), smokehouse (10.10.20.10); Proxmox VMs dojo (10.10.30.27) and regscale (10.10.30.28)
    profile-param-value-origin: organization
  mp-07_odp.04:
    alt-identifier: mp-7_prm_4
    profile-values:
      - operator policy (sole operator, no external personnel); physical access control (home lab rack, Virginia); explicit documentation of all USB devices attached to in-boundary hosts in CLAUDE.md
    profile-param-value-origin: organization
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: mp-07
---

# mp-7 - \[Media Protection\] Media Use

## Control Statement

- \[a.\] [Selection: restrict; prohibit] the use of [types of system media] on [systems or system components] using [controls] ; and

- \[b.\] Prohibit the use of portable storage devices in organizational systems when such devices have no identifiable owner.

## Control Assessment Objective

- \[MP-07a.\] the use of [types of system media] is [Selection: restrict; prohibit] on [systems or system components] using [controls];

- \[MP-07b.\] the use of portable storage devices in organizational systems is prohibited when such devices have no identifiable owner.

## Control guidance

System media includes both digital and non-digital media. Digital media includes diskettes, magnetic tapes, flash drives, compact discs, digital versatile discs, and removable hard disk drives. Non-digital media includes paper and microfilm. Media use protections also apply to mobile devices with information storage capabilities. In contrast to [MP-2](#mp-2) , which restricts user access to media, MP-7 restricts the use of certain types of media on systems, for example, restricting or prohibiting the use of flash drives or external hard disk drives. Organizations use technical and nontechnical controls to restrict the use of system media. Organizations may restrict the use of portable storage devices, for example, by using physical cages on workstations to prohibit access to certain external ports or disabling or removing the ability to insert, read, or write to such devices. Organizations may also limit the use of portable storage devices to only approved devices, including devices provided by the organization, devices provided by other approved organizations, and devices that are not personally owned. Finally, organizations may restrict the use of portable storage devices based on the type of device, such as by prohibiting the use of writeable, portable storage devices and implementing this restriction by disabling or removing the capability to write to such devices. Requiring identifiable owners for storage devices reduces the risk of using such devices by allowing organizations to assign responsibility for addressing known vulnerabilities in the devices.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The MSS enforces an absolute prohibition on removable storage device use at all in-boundary hosts. No USB flash drives, external hard drives, optical discs, or other portable storage devices participate in any in-boundary data flow or administrative workflow. The only USB device attached to any in-boundary host is the span0 adapter on haccp (Realtek RTL8156B, MAC `6c:1f:f7:5f:6a:88`) -- a network interface used exclusively for SPAN traffic capture carrying no storage function. All administrative data flows use SSH over Tailscale, NFS, or Logstash/Filebeat pipelines. The prohibition is enforced through operator policy (sole operator, no external personnel authorized) and physical access control (home lab rack, Virginia). Because every USB device attached to in-boundary hardware is explicitly documented in CLAUDE.md with owner identity and function, the MP-7b identifiable-owner requirement is fully satisfied.

#### Implementation Status: implemented

______________________________________________________________________
