# Customer Responsibility Matrix, demonstration stub

This is a **demonstration** of how a Customer Responsibility Matrix (CRM, also called the Control Implementation Summary in some FedRAMP templates) would look if the notional Managed SOC Service (MSS) were an actual SaaS offering on top of an authorized FedRAMP High IaaS provider. **It is not a CRM for the homelab itself**, which is single-operator on-prem and has no tenants to split responsibilities with.

The intent of this stub is to show that the operator understands how a CRM fits in a real FedRAMP SaaS or PaaS package, can read FedRAMP Rev 5 templates, and can author a CRM in the same idiom an actual CSP would. Ten sample controls are included, drawn from the families where the CRM split is most informative (PE, MA, SC, AC, IA, AU).

A real Low baseline CRM has a row for every one of the 156 controls. This stub has 10 rows so a reader can see the pattern without reading a 30-page document.

## Hypothetical deployment context

For this demonstration, assume the following deployment shape:

- **Service model:** SaaS (the MSS is a fully managed offering)
- **Deployment model:** Public Cloud
- **Underlying IaaS:** AWS GovCloud (FedRAMP High authorized)
- **Inheritance source:** AWS FedRAMP High SSP and Customer Responsibility Matrix as published on the FedRAMP Marketplace (notional reference; AWS publishes the actual CRM to authorized customers under NDA)
- **Customer profile:** a federal agency consuming the MSS as a managed monitoring service for the agency's own systems

## Sample CRM rows

| Control | CSP (MSS) implements | Customer implements | Inherited from AWS GovCloud (IaaS) | Notes |
|---|---|---|---|---|
| **PE-2 Physical Access Authorization** | None | None | All | Physical access to AWS data centers is fully inherited at the IaaS layer. |
| **PE-3 Physical Access Control** | None | None | All | Same. AWS handles biometric access, badge readers, escort logs, visitor logging, and physical penetration testing. |
| **MA-2 Controlled Maintenance** | Maintenance on the MSS application stack: container image updates, MSS-specific OS package updates per the in-boundary host policy, scheduled maintenance windows announced to customers | None | Underlying host OS, hypervisor, and physical hardware maintenance | Customer has no maintenance role. CSP owns all logical maintenance on the MSS stack. IaaS owns all physical maintenance. |
| **SC-7 Boundary Protection** | MSS application-layer ingress (TLS termination, WAF rules, application authentication, IP allow-listing for tenant-specific endpoints) | Customer-side network egress controls when shipping logs and telemetry to the MSS | AWS VPC, NACLs, security groups at the IaaS layer | Three-way split. The MSS application perimeter and the IaaS network perimeter are different boundaries. |
| **SC-8 Transmission Confidentiality and Integrity** | TLS 1.3 between MSS components, signed log forwarding from MSS-managed agents, MSS-side mutual TLS for federated trust | Customer-side TLS configuration when forwarding logs from customer endpoints to the MSS ingest endpoint | AWS-managed VPC encryption between Availability Zones, AWS Transit Gateway TLS | |
| **SC-13 Cryptographic Protection** | Use of FIPS-validated TLS libraries (specific CMVP certificate numbers cited), KMS-backed key generation for tenant data, FIPS-validated container OS images (Ubuntu Pro FIPS or RHEL FIPS-validated) | Customer must use FIPS-validated TLS client when forwarding logs | AWS KMS HSM (FIPS 140-2 Level 3 validated) for IaaS-layer key material | A real package would cite specific NIST CMVP certificate numbers in the rightmost column. The homelab does not implement this; documented under SC-13 in the live SSP. |
| **AC-2 Account Management** | MSS application accounts (analyst, operator, admin roles), MFA enforcement on the MSS federation endpoint, account lifecycle automation for terminated tenant users | Customer-side IdP integration, customer admin account lifecycle in the customer's own IdP, customer responsibility for terminating customer-side users | AWS IAM at the IaaS control plane (CSP-internal IAM only, not customer-facing) | Customer chooses their IdP; CSP federates against it. |
| **AC-3 Access Enforcement** | Application-layer RBAC (role-based access control) within the MSS, API authorization on every request, tenant-scope enforcement preventing cross-tenant data access | Customer-side access policy on the customer's IdP determining who in the customer org can log into MSS at all | AWS IAM policies on the underlying compute (CSP-internal only) | |
| **IA-2 User Identification and Authentication** | SAML-federated SSO into MSS, support for OIDC, MFA enforcement at the federation endpoint, session timeout policy | Customer-side IdP (Okta, Azure AD, Login.gov, agency-specific SSO) and the customer's choice of MFA factor | AWS IAM for IaaS-layer admins (CSP-internal only) | Customer chooses MFA implementation; CSP enforces MFA presence at the federation endpoint regardless of customer choice. |
| **AU-2 Event Logging** | MSS application audit logs (analyst actions, configuration changes, tenant-data access events) emitted in a customer-readable format and shipped to a customer-controlled S3 bucket or equivalent | Customer-side ingestion, retention, and analysis of MSS-emitted logs; customer-side review of MSS-emitted security-relevant events per agency policy | AWS CloudTrail at the IaaS control plane (CSP-internal only, not exposed to customer) | The customer is responsible for *acting* on the security-relevant logs the MSS emits. The MSS produces; the customer consumes. |

## Reading the columns

- **CSP implements:** the MSS engineering team designs, builds, operates, and assesses this control. The customer has no role; the IaaS has no role beyond providing the substrate.
- **Customer implements:** the customer agency must do this themselves. The MSS package documents what the customer needs to do but does not do it for them. Customer responsibilities are summarized in the SSP customer responsibilities section (typically Section 4) and inform the customer's own RMF / ATO documentation for their consumption of the MSS.
- **Inherited from authorized IaaS:** the IaaS provider (here, AWS GovCloud) implemented and assessed this control as part of its own FedRAMP High authorization. The CSP inherits the implementation and the assessment. The 3PAO assessing the CSP does not re-assess inherited controls; they review the inheritance flag and the IaaS-side authorization status.

A real FedRAMP CRM also distinguishes between **inherited** and **shared** controls (controls where the CSP and IaaS each implement part of the control). For brevity, this stub uses three columns; the FedRAMP Rev 5 template uses additional flags (Implemented / Partially Implemented / Planned / N/A; Service Provider Corporate / Service Provider System Specific / Service Provider Hybrid / Configured by Customer / Provided by Customer / Shared / Inherited).

## What this stub is not

- It is not a complete 156-control CRM. A real Low baseline CRM has a row for every control in the baseline.
- It is not the CRM for the homelab. The homelab has no customers and no IaaS underneath it.
- It does not cite AWS-actual control inheritance language. AWS publishes its own CRM templates with specific control inheritance flags under NDA to authorized customers; this stub is illustrative.
- It is not a 3PAO-assessed artifact. No assessor has reviewed it.
- The inheritance flags shown here are illustrative, not definitive. A real CRM would cite the AWS GovCloud SSP version, the AWS-published inheritance flag for each control, and the date of the AWS authorization being inherited from.

## What it is

A demonstration that the operator can read, write, and reason about CRM splits, control inheritance from an authorized IaaS, and the three-way responsibility model that defines a real FedRAMP SaaS package. The mechanics here transfer 1:1 to writing the CRM for an actual cloud service if the operator were authoring one for a real CSP.

## See also

- [SC-13 Cryptographic Protection](../trestle-workspace/mss-ssp/sc/sc-13.md), the live SSP control documenting the homelab's actual (non-FIPS) crypto posture
- [Scope and framework mapping](../README.md#scope-and-framework-mapping), the README section that puts this CRM stub in context
- [What this project does not claim](../README.md#what-this-project-does-not-claim), the full disclaimer
- [OR-0001 Shared-tenancy DR](../deviation-requests/OR-0001-shared-tenancy.md), which documents a different kind of compliance gap (the on-prem shared-compute case) discovered during SSP authoring against the real homelab
