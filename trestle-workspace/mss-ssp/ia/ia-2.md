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
  sort-id: ia-02
---

# ia-2 - \[Identification and Authentication\] Identification and Authentication (Organizational Users)

## Control Statement

Uniquely identify and authenticate organizational users and associate that unique identification with processes acting on behalf of those users.

## Control Assessment Objective

- \[IA-02[01]\] organizational users are uniquely identified and authenticated;

- \[IA-02[02]\] the unique identification of authenticated organizational users is associated with processes acting on behalf of those users.

## Control guidance

Organizations can satisfy the identification and authentication requirements by complying with the requirements in [HSPD 12](#f16e438e-7114-4144-bfe2-2dfcad8cb2d0) . Organizational users include employees or individuals who organizations consider to have an equivalent status to employees (e.g., contractors and guest researchers). Unique identification and authentication of users applies to all accesses other than those that are explicitly identified in [AC-14](#ac-14) and that occur through the authorized use of group authenticators without individual authentication. Since processes execute on behalf of groups and roles, organizations may require unique identification of individuals in group accounts or for detailed accountability of individual activity.

Organizations employ passwords, physical authenticators, or biometrics to authenticate user identities or, in the case of multi-factor authentication, some combination thereof. Access to organizational systems is defined as either local access or network access. Local access is any access to organizational systems by users or processes acting on behalf of users, where access is obtained through direct connections without the use of networks. Network access is access to organizational systems by users (or processes acting on behalf of users) where access is obtained through network connections (i.e., nonlocal accesses). Remote access is a type of network access that involves communication through external networks. Internal networks include local area networks and wide area networks.

The use of encrypted virtual private networks for network connections between organization-controlled endpoints and non-organization-controlled endpoints may be treated as internal networks with respect to protecting the confidentiality and integrity of information traversing the network. Identification and authentication requirements for non-organizational users are described in [IA-8](#ia-8).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Every in-boundary host and service in the Managed SOC Service requires unique identification and authentication before granting access. For SSH access to all Linux hosts -- brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, and regscale -- the operator (Brian Chaplow) authenticates using a per-host ED25519 or RSA-4096 key pair provisioned on the PITBOSS workstation. `PasswordAuthentication no` is set in `sshd_config` on every host, preventing credential-based access. No shared SSH credentials are used.

All management service interfaces enforce named account authentication. Wazuh Dashboard (`https://10.10.20.30:5601`) authenticates via the `admin` account against the OpenSearch security plugin. The Wazuh API (`https://10.10.20.30:55000`) uses the `wazuh-wui` account with a per-invocation JWT issued by the pipeline client in `pipelines/common/wazuh.py`. Shuffle SOAR (`https://10.10.20.30:3443`) and OpenCTI (`http://10.10.20.30:8080`) each use a named admin account. TheHive (`http://10.10.30.22:9000`) maintains two distinct named accounts -- `admin@thehive.local` and `socadmin@thehive.local` -- with separate roles. Cortex (`http://10.10.30.22:9001`) likewise uses `admin` and `socadmin@SOC`. Velociraptor (`https://10.10.20.30:8889`) and DefectDojo (`http://10.10.30.27:8080`) each use a dedicated `admin` account with API token-based pipeline access. RegScale CE (`http://10.10.30.28`) authenticates via `admin` with a 24-hour JWT issued per `POST /api/authentication/login` per ADR 0003 and ADR 0006 Deviation 7. Tailscale remote access authenticates each device by its WireGuard key, tied to the operator's Tailscale account identity. All accounts are uniquely identified and non-shared.

#### Implementation Status: implemented

______________________________________________________________________
