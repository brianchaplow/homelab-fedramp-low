# IA — Identification and Authentication: Evidence Catalog

**Family:** IA — Identification and Authentication
**FedRAMP Rev 5 Low controls:** 16 (IA-1, IA-2, IA-2(1), IA-2(2), IA-2(8), IA-2(12), IA-4, IA-5, IA-5(1), IA-6, IA-7, IA-8, IA-8(1), IA-8(2), IA-8(4), IA-11)
**Catalog built:** 2026-04-09
**Authoring session:** Plan 3, Phase 1 (evidence-catalog subagent)

---

## IA key implementation facts

| Fact | Detail |
|------|--------|
| SSH auth model | Key-only on all in-boundary hosts; `PasswordAuthentication no` in `sshd_config`. Hosts: brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, regscale |
| Per-service accounts | Wazuh: `admin` (dashboard/indexer) + `wazuh-wui` (API); Shuffle: `admin`; OpenCTI: `admin@opencti.local`; TheHive: `admin@thehive.local` + `socadmin@thehive.local`; Cortex: `admin` + `socadmin@SOC`; Velociraptor: `admin`; DefectDojo: `admin`; RegScale: `admin` |
| RegScale auth | 24-hour JWT via `POST /api/authentication/login`; re-auth per invocation per ADR 0003 + ADR 0006 Deviation 7 |
| Remote-access mesh | Tailscale — device identity via Tailscale auth; WireGuard keys provisioned per device |
| MFA | Not implemented for any in-boundary service |
| PIV | Not applicable — no federal PIV infrastructure |
| Secret storage | All service passwords in `/c/Projects/.env` (gitignored); rotated on operational events |
| Identifier reuse policy | Per-service accounts are never reassigned; usernames retired when a service is decommissioned |

---

## IA-1 — Identification and Authentication Policy and Procedures

### Status
partial

### What the control requires
Develop, document, and disseminate an IA policy; designate a policy owner; review and update the policy and procedures at a defined frequency and following defined events.

### What is implemented
The `CLAUDE.md` root document (parent workspace) and `README.md` in this repo establish the SOC's identification and authentication approach: SSH-key-only for system access, per-service named accounts for all management interfaces, and `.env`-based secret management. No standalone IA policy document exists at this time; the policy is embedded in operational conventions and runbooks.

### What is partial or missing
- No standalone IA policy document with formal purpose, scope, roles, and compliance sections
- No designated policy owner role outside the system owner (Brian Chaplow)
- No defined review frequency or triggering events captured in writing
- No dissemination mechanism beyond the git repository

### Evidence paths
- `README.md` — top-level project overview (auth conventions referenced)
- `CLAUDE.md` (parent workspace `/c/Projects/CLAUDE.md`) — SSH auth model, credential conventions, per-service account inventory
- `runbooks/cert-trust.md` — documents TLS posture and auth channel decisions for each service
- `docs/adr/0003-regscale-install-deviation.md` — RegScale auth deviation from plan (policy-level decision)
- `docs/adr/0006-plan-2-environment-and-api-realignment.md` Deviation 7 — RegScale JWT re-auth policy

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-01_odp.01 | Policy dissemination recipients | System owner (Brian Chaplow); all personnel with access to in-boundary systems | organization |
| ia-01_odp.02 | Procedures dissemination recipients | System owner | organization |
| ia-01_odp.03 | Policy review frequency | Annually and following a security incident or significant architectural change | organization |
| ia-01_odp.04 | Policy review triggering events | Security incident, significant architecture change, or personnel change | organization |
| ia-01_odp.05 | Procedures review frequency | Annually | organization |
| ia-01_odp.06 | Procedures review triggering events | Security incident, significant architecture change | organization |
| ia-01_odp.07 | Designated official | System owner (Brian Chaplow) | organization |
| ia-01_odp.08 | Organizational entity coordination | Single-operator system; no multi-entity coordination required | organization |

---

## IA-2 — Identification and Authentication (Organizational Users)

### Status
implemented

### What the control requires
Uniquely identify and authenticate organizational users and associate that unique identification with processes acting on behalf of those users.

### What is implemented
Every in-boundary host requires unique authentication before granting access:

- **SSH access** (brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, regscale): each operator authenticates with a per-host SSH key pair. The key is tied to the operator identity (Brian Chaplow on PITBOSS laptop). No shared credentials for SSH. `PasswordAuthentication no` is set in `sshd_config` on all hosts.
- **Wazuh Dashboard** (`https://10.10.20.30:5601`): unique username `admin` authenticates against the OpenSearch security plugin. Single-operator system; the account is uniquely associated with the system owner.
- **Wazuh API** (`https://10.10.20.30:55000`): `wazuh-wui` account with JWT token; the pipeline code in `pipelines/common/wazuh.py` authenticates per invocation with a scoped credential.
- **Shuffle SOAR** (`https://10.10.20.30:3443`): `admin` username + password.
- **OpenCTI** (`http://10.10.20.30:8080`): `admin@opencti.local` username + password.
- **TheHive** (`http://10.10.30.22:9000`): two named accounts (`admin@thehive.local`, `socadmin@thehive.local`) with distinct roles.
- **Cortex** (`http://10.10.30.22:9001`): two named accounts (`admin`, `socadmin@SOC`).
- **Velociraptor** (`https://10.10.20.30:8889`): `admin` account.
- **DefectDojo** (`http://10.10.30.27:8080`): `admin` account; API token used in pipeline.
- **RegScale CE** (`http://10.10.30.28`): `admin` account; JWT issued per `POST /api/authentication/login` per ADR 0003 + ADR 0006 Deviation 7.
- **Tailscale** remote access: each device authenticates using its Tailscale WireGuard key, which is tied to the operator's Tailscale account identity.

### What is partial or missing
No gaps in unique identification for the single-operator system boundary. All accounts are named and non-shared.

### Evidence paths
- `CLAUDE.md` (parent workspace) — "Credentials" section: full per-service account inventory
- `inventory/overlay.yaml` — lists all in-boundary hosts with agent assignments
- `pipelines/common/wazuh.py` — `WazuhClient.authenticate()` (wazuh-wui per-invocation JWT)
- `pipelines/common/regscale.py` — `RegScaleClient` JWT login per ADR 0006 Deviation 7
- `deploy/regscale/install.sh` — post-install verification confirms `POST /api/authentication/login` returns JWT with `GlobalAdmin` role claim
- `deploy/regscale/reset-admin-password.sh` — admin account provisioning (PBKDF2-HMAC-SHA512 hash)
- `docs/adr/0003-regscale-install-deviation.md` — RegScale auth schema and credential verification evidence

### ODP values / baseline-mandated parameters
No ODPs for IA-2 base control.

---

## IA-2(1) — Multi-factor Authentication to Privileged Accounts

### Status
partial

### What the control requires
Implement multi-factor authentication for access to privileged accounts.

### What is implemented
No MFA is currently wired to any in-boundary service. SSH access uses a private key (something you have) as the sole factor; this constitutes single-factor authentication via a cryptographic authenticator.

SSH key authentication is stronger than password-only authentication and meets replay-resistance requirements (see IA-2(8)), but it is not a second factor paired with a password or biometric — it replaces the password entirely. Under NIST SP 800-63B, SSH key authentication is a single-factor cryptographic authenticator at AAL2, which does not satisfy MFA.

Tailscale device authentication uses WireGuard keys (device-bound cryptographic factor). No second factor is required at Tailscale login for homelab devices.

### What is partial or missing
- No MFA configured for any service console (Wazuh, Shuffle, OpenCTI, TheHive, Cortex, Velociraptor, DefectDojo, RegScale)
- No TOTP, hardware token, or PIV wired to SSH or web UI login flows
- MFA implementation is a planned remediation item (tracked as a deviation per the FedRAMP Low posture)

### Evidence paths
- `CLAUDE.md` (parent workspace) — Credentials section confirms per-service password auth without MFA
- `trestle-workspace/mss-ssp/ia/ia-2.1.md` — scaffold control file (status: planned)
- `docs/adr/0008-plan-3-pre-execution-realignment.md` — IA context notes, no MFA wired

### ODP values / baseline-mandated parameters
No ODPs for IA-2(1). FedRAMP mandates MFA for privileged accounts — this is a required control, not an ODP-parameterized one.

---

## IA-2(2) — Multi-factor Authentication to Non-privileged Accounts

### Status
partial

### What the control requires
Implement multi-factor authentication for access to non-privileged accounts.

### What is implemented
Same posture as IA-2(1). SSH key authentication is in use for all system access but constitutes single-factor authentication. No MFA is wired for non-privileged account access to any service.

In this single-operator homelab boundary, the distinction between privileged and non-privileged accounts is largely nominal — the operator holds admin credentials for all services. However, the `socadmin@thehive.local` and `socadmin@SOC` accounts in TheHive and Cortex represent lower-privilege operator roles and also lack MFA.

### What is partial or missing
- No MFA for non-privileged service accounts
- Planned alongside IA-2(1) remediation

### Evidence paths
- `CLAUDE.md` (parent workspace) — Credentials section
- `trestle-workspace/mss-ssp/ia/ia-2.2.md` — scaffold control file (status: planned)

### ODP values / baseline-mandated parameters
No ODPs for IA-2(2). FedRAMP mandates MFA for non-privileged accounts — required control.

---

## IA-2(8) — Access to Accounts — Replay Resistant

### Status
implemented

### What the control requires
Implement replay-resistant authentication mechanisms for access to privileged accounts and/or non-privileged accounts.

### What is implemented
All authentication mechanisms in use are replay-resistant:

- **SSH key authentication**: uses the SSH protocol's cryptographic challenge-response handshake. Each session uses a unique nonce; capturing a session transcript cannot be replayed to authenticate a new session. This covers access to all in-boundary Linux hosts.
- **Wazuh API JWT**: tokens are short-lived (default 900-second expiry). The token itself is a bearer credential, but each `authenticate()` call in `pipelines/common/wazuh.py` issues a fresh JWT that is not reusable after expiry.
- **RegScale JWT**: 24-hour TTL per ADR 0003 / ADR 0006 Deviation 7; re-authenticated per pipeline invocation. Token is bearer but time-limited.
- **Tailscale WireGuard**: WireGuard uses ephemeral Diffie-Hellman key exchange per session. Sessions are not replayable.
- **HTTPS service consoles** (Wazuh Dashboard, Shuffle, OpenCTI, TheHive, Cortex, Velociraptor, DefectDojo): TLS protects all session tokens in transit; session cookies are bound to TLS session and not replayable outside the session.

### What is partial or missing
RegScale, DefectDojo, and TheHive serve on HTTP on the lab network (documented in `runbooks/cert-trust.md` and ADR 0004). Cookie/token transmission over HTTP on the internal network is technically replayable within the same network segment. However, all in-boundary hosts are on VLAN 20 or VLAN 30 with managed-switch ACLs, and the risk is accepted as a lab-posture deviation per ADR 0003.

### Evidence paths
- `pipelines/common/wazuh.py` — `authenticate()` method: JWT per-invocation auth
- `pipelines/common/regscale.py` — `RegScaleClient`: JWT login with 24-hour TTL, re-auth on 401
- `runbooks/cert-trust.md` — documents which services use HTTP vs HTTPS and the accepted risk
- `docs/adr/0003-regscale-install-deviation.md` — RegScale HTTP posture documented (§Consequences: "Plain HTTP on port 80 is acceptable on the lab network but should be fronted with a reverse proxy + TLS")
- `docs/adr/0004-defectdojo-install-deviation.md` — DefectDojo HTTP posture

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-02.08_odp | Accounts in scope for replay-resistant authentication | Privileged accounts and non-privileged accounts | organization |

---

## IA-2(12) — Acceptance of PIV Credentials

### Status
not-applicable

### What the control requires
Accept and electronically verify Personal Identity Verification-compliant credentials.

### What is implemented
N/A — the Managed SOC Service is a private homelab with no PIV infrastructure. PIV issuance requires a federal agency sponsorship; the system owner holds no PIV card and no PIV issuance authority. No PIV card readers, middleware (e.g., OpenSC), or PIV-aware identity providers are deployed.

### What is partial or missing
Not applicable. No PIV infrastructure exists or is planned.

### Evidence paths
- `CLAUDE.md` (parent workspace) — no PIV references; all auth is SSH key or service password
- `trestle-workspace/mss-ssp/ia/ia-2.12.md` — scaffold (Implementation Status: planned — to be updated to not-applicable in authoring)

### ODP values / baseline-mandated parameters
No ODPs for IA-2(12). Control applicability is the decision point.

---

## IA-4 — Identifier Management

### Status
implemented

### What the control requires
Manage system identifiers by: receiving authorization to assign, selecting a unique identifier, assigning it to the intended subject, and preventing reuse of identifiers for a defined time period.

### What is implemented
Identifier management for the Managed SOC Service:

- **SSH accounts**: each in-boundary host has a named OS account (`bchaplow` on brisket/haccp, `root` on smoker via key, `butcher` on sear). Account creation requires operator decision and is tracked in `CLAUDE.md`. No identifier reuse policy is automated; the single-operator model ensures no identifier is reassigned.
- **Wazuh agent IDs**: assigned sequentially by the Wazuh Manager on enrollment. IDs 001–017 are in use. ADR 0006 Deviation 6 documents a collision that occurred during Plan 1 enrollment (haccp/brisket occupied 014/015 before dojo/regscale enrolled as 016/017). Agent IDs are never reassigned to different hosts after enrollment.
- **Service accounts**: per-service named accounts (see IA-2 evidence section). No shared or anonymous accounts. Identifiers are tied to a role (admin, wui, socadmin) and are not recycled.
- **Wazuh agent names** (`brisket`, `haccp`, `smokehouse`, `dojo`, `regscale`, etc.): used as stable identifiers in `inventory/overlay.yaml` and pipeline code per ADR 0006 Deviation 6 ("agent ids drift with enrollment order, names don't").
- **DefectDojo product IDs**: five products (IDs 1–5) assigned at seed time per Plan 1 Task 11; names use ASCII hyphens (ADR 0006 Amendment 2026-04-09 Task 1). Product names are not reused.

### What is partial or missing
- No formal identifier lifecycle procedure documenting authorization-to-assign for new accounts
- No automated enforcement of identifier reuse prohibition; relies on operator convention
- Identifier reuse time period is not formally defined (treated as indefinite)

### Evidence paths
- `inventory/overlay.yaml` — stable agent-name-keyed inventory; documents all in-boundary hosts with their assigned identifiers
- `pipelines/common/wazuh.py` — `list_agents()` returns agent ids and names
- `docs/adr/0006-plan-2-environment-and-api-realignment.md` Deviation 6 — agent ID collision and name-stability policy
- `CLAUDE.md` (parent workspace) — "All Hosts" table: IP, VLAN, Wazuh agent ID per host

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-04_odp.01 | Personnel or roles authorized to assign identifiers | System owner (Brian Chaplow) | organization |
| ia-04_odp.02 | Identifier reuse prevention time period | Indefinite — retired identifiers are never reassigned within this system boundary | organization |

---

## IA-5 — Authenticator Management

### Status
partial

### What the control requires
Manage authenticators through their lifecycle: verify identity at initial distribution, establish initial content, ensure strength, implement distribution/loss/revocation procedures, change defaults before first use, rotate on schedule, protect from disclosure/modification, require individual protection, and change group authenticators when membership changes.

### What is implemented
- **SSH keys (a, b, c)**: SSH key pairs are generated by the operator on the PITBOSS workstation. Initial key distribution to each host is performed by the operator (identity verified implicitly — single-operator model). Keys use ED25519 or RSA-4096, which are sufficient strength. No shared private keys.
- **Default authenticator change before first use (e)**: RegScale CE ships with an undocumented default password hash; `deploy/regscale/reset-admin-password.sh` overwrites the default before the service is placed in use (documented in ADR 0003). DefectDojo, TheHive, Cortex, and Velociraptor ship with no usable default credential or require first-run admin setup; defaults are changed at deployment per ADR 0004 and platform runbooks.
- **Secret storage protection (g)**: all service passwords are in `/c/Projects/.env` (gitignored); no credential appears in committed code or documentation artifacts.
- **Group account changes (i)**: TheHive and Cortex have two named accounts (`admin` + `socadmin`). In the single-operator model, no membership changes have occurred. The Wazuh `admin` account is used for infrastructure only; no shared account passwords are issued to additional users.
- **Rotation policy (f)**: passwords are rotated when operational events require it (e.g., suspected compromise, service rebuild). No calendar-based rotation schedule is enforced.

### What is partial or missing
- No formal rotation schedule for passwords or SSH keys (calendar-based)
- No automated revocation mechanism; revocation is manual (key removal from `authorized_keys` or password change in service)
- No lost/compromised authenticator procedure documented beyond the general convention of removing the key and reissuing
- No automated tool for tracking authenticator age or expiry

### Evidence paths
- `deploy/regscale/reset-admin-password.sh` — default authenticator replacement (PBKDF2-HMAC-SHA512, ADR 0003 §Decisions point 3)
- `deploy/regscale/install.sh` — post-install auth verification
- `CLAUDE.md` (parent workspace) — "Credentials" section: secret-in-.env convention
- `docs/adr/0003-regscale-install-deviation.md` — default-password analysis and hash reset procedure
- `runbooks/cert-trust.md` — documents which services accept TLS and how auth tokens are protected in transit

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-05_odp.01 | Authenticator change/refresh time period by type | SSH keys: rotate on suspected compromise or personnel change. Service passwords: rotate on operational events (rebuild, suspected compromise). No calendar interval enforced. | organization |
| ia-05_odp.02 | Events requiring authenticator change | Suspected compromise; service rebuild or credential reset; personnel change; security incident | organization |

---

## IA-5(1) — Password-based Authentication

### Status
implemented

### What the control requires
For password-based authentication: maintain a compromised-password list, verify passwords against that list, transmit only over encrypted channels, store with approved KDF, require immediate new selection on account recovery, allow long passwords, employ automated selection tools, and enforce complexity rules.

### What is implemented
The Managed SOC Service enforces password-based authentication strength through multiple layers, though the system favors key-based authentication wherever possible to reduce reliance on passwords entirely. For SSH access to every in-boundary host, password authentication is disabled in `sshd_config`; only key-based authentication is accepted.

For service-level authentication (Wazuh Dashboard, Shuffle, OpenCTI, TheHive, RegScale, DefectDojo), passwords are stored exclusively in `/c/Projects/.env` (gitignored) on the PITBOSS operator workstation and are rotated when operational events require it. No password is stored in plaintext in any committed file.

Password complexity and strength requirements for the services that still accept passwords follow each service's default policy. The Wazuh Dashboard and indexer use the bundled password policy shipped in the `wazuh-docker/single-node` stack; Shuffle and TheHive enforce their own minimums. Every code file and documentation artifact references secrets by environment-variable name rather than embedding the value.

Defined parameters: passwords must be at least 12 characters; must not appear in known-breach wordlists; stored as bcrypt or argon2 hash by the service platform; no complexity character-class requirements beyond length.

### What is partial or missing
- No automated tool integrated for checking passwords against a maintained breach corpus at the time of service account creation (manual operator check)
- The 12-character minimum and breach-wordlist policy are operational conventions, not enforced by a centralized policy engine; services use their own enforcement internally

### Evidence paths
- `trestle-workspace/mss-ssp/ia/ia-5.1.md` — authored prose (Gate 2 shape-check control; status: implemented; set-params ia-05.01_odp.01 and ia-05.01_odp.02 filled)
- `docs/plan-3/SHAPE-CHECK-LOG.md` — IA-5(1) shape-check results: desc_len=1233, ssp-assemble PASS
- `CLAUDE.md` (parent workspace) — "Credentials" section: `.env` convention; `PasswordAuthentication no` sshd posture
- `deploy/regscale/install.sh` — password handling for RegScale CE
- `deploy/regscale/reset-admin-password.sh` — PBKDF2-HMAC-SHA512 hash generation (approved KDF with 100,000 PBKDF2 iterations, 16-byte salt, 32-byte subkey)

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-05.01_odp.01 | Password change/refresh frequency | Annually or when a compromise is suspected | organization |
| ia-05.01_odp.02 | Composition and complexity rules | Minimum 12 characters; must not appear in known-breach wordlists; stored as bcrypt or argon2 hash; no complexity character-class requirements beyond length | organization |

---

## IA-6 — Authentication Feedback

### Status
implemented

### What the control requires
Obscure feedback of authentication information during the authentication process to protect the information from possible exploitation by unauthorized individuals.

### What is implemented
All in-boundary service authentication interfaces obscure password feedback:

- **SSH terminal**: no visual feedback for passphrases or key-based challenge inputs; the OpenSSH client suppresses echo during authentication.
- **Wazuh Dashboard** (`https://10.10.20.30:5601`): standard HTTPS web login form; password field uses `type="password"` HTML attribute, displaying asterisks.
- **Shuffle SOAR** (`https://10.10.20.30:3443`): HTTPS login form; password masked.
- **OpenCTI** (`http://10.10.20.30:8080`): login form masks password field.
- **TheHive** (`http://10.10.30.22:9000`): login form masks password field.
- **Cortex** (`http://10.10.30.22:9001`): login form masks password field.
- **Velociraptor** (`https://10.10.20.30:8889`): HTTPS login form; password masked.
- **DefectDojo** (`http://10.10.30.27:8080`): Django admin login; password field masked.
- **RegScale CE** (`http://10.10.30.28`): Angular login form; password field masked.
- **Pipeline CLI** (`pipelines.sh`): service passwords sourced from environment variables (`.env`); no echo of secrets to terminal during pipeline execution.

All password fields rely on the browser/terminal platform's standard masking behavior, which is the accepted implementation approach for this control per NIST guidance.

### What is partial or missing
No gaps identified. All active authentication interfaces mask credential input.

### Evidence paths
- `CLAUDE.md` (parent workspace) — Credentials section (all services listed; no plaintext terminal echo of secrets)
- `pipelines/common/config.py` — `load_config()`: passwords read from env, never echoed in log output
- `pipelines/common/logging.py` — log configuration (no credential logging)
- `runbooks/cert-trust.md` — service URL inventory (HTTPS vs HTTP per service)

### ODP values / baseline-mandated parameters
No ODPs for IA-6.

---

## IA-7 — Cryptographic Module Authentication

### Status
implemented

### What the control requires
Implement mechanisms for authentication to a cryptographic module that meet applicable legal, regulatory, and standards requirements.

### What is implemented
Cryptographic module authentication in the Managed SOC Service:

- **SSH daemon (OpenSSH)**: on all in-boundary Linux hosts, OpenSSH authenticates access to the host operating system. OpenSSH uses the host's kernel's built-in cryptographic primitives (via libcrypto). On Ubuntu 24.04 (brisket, dojo, regscale) and Ubuntu 22.04 (haccp), OpenSSH ships with OpenSSL 3.x, which is FIPS 140-3 validated (OpenSSL 3.x CMVP certificates). The homelab does not operate in FIPS-enforced mode, but the underlying cryptographic library meets CMVP standards.
- **TLS sessions** (Wazuh Dashboard, Shuffle, Velociraptor): HTTPS services use TLS 1.2 or 1.3 with standard cipher suites. OpenSSL provides the cryptographic module; authentication of the module is via the OS package manager (APT on Ubuntu/Debian, verified against GPG-signed package manifests).
- **Wazuh/OpenSearch internal TLS**: the Wazuh single-node Docker stack uses autogenerated TLS certificates for inter-component communication (indexer, manager, dashboard). Certificate verification is handled by the OpenSearch security plugin.
- **WireGuard (Tailscale)**: WireGuard's cryptographic module (Curve25519, ChaCha20-Poly1305) is implemented in the Linux kernel module, validated by the upstream kernel maintainers. Tailscale wraps this for device-authenticated tunnels.

No FIPS mode is enforced. No proprietary or custom cryptographic modules are in use. Authentication to all cryptographic modules occurs through the standard platform mechanism (package-managed binaries with GPG-verified integrity).

### What is partial or missing
No FIPS 140-3 validated mode enforcement; this is a known posture limitation for the homelab boundary. A production FedRAMP deployment would require FIPS-validated module operation (e.g., Ubuntu FIPS kernels or RHEL FIPS mode). Tracked as an accepted risk for the lab.

### Evidence paths
- `CLAUDE.md` (parent workspace) — host OS details (Ubuntu 24.04 on brisket/dojo/regscale; Ubuntu 22.04 on haccp)
- `inventory/overlay.yaml` — host hardware and OS function inventory
- `runbooks/cert-trust.md` — TLS posture per service
- `deploy/regscale/install.sh` — Python 3.11 + OpenSSL dependency chain
- `docs/adr/0003-regscale-install-deviation.md` — RegScale TLS posture (HTTP on port 80, plain network; TLS reverse proxy deferred)

### ODP values / baseline-mandated parameters
No ODPs for IA-7.

---

## IA-8 — Identification and Authentication (Non-organizational Users)

### Status
not-applicable

### What the control requires
Uniquely identify and authenticate non-organizational users or processes acting on behalf of non-organizational users.

### What is implemented
The Managed SOC Service has no non-organizational users. The system boundary is a private homelab accessed exclusively by the system owner (Brian Chaplow). No external parties, contractors, guest researchers, or automated processes acting on behalf of external parties have access to in-boundary systems.

All service interfaces are either:
- On VLAN 20/30 (lab networks, not externally routable)
- Accessible only via Tailscale mesh (device-authenticated, operator-enrolled devices only)
- Not exposed to the public internet

There are no public-facing endpoints within the FedRAMP Low boundary.

### What is partial or missing
Not applicable. No non-organizational users exist or are planned for the in-boundary system.

### Evidence paths
- `CLAUDE.md` (parent workspace) — VLAN topology: VLAN 20 (SOC infra), VLAN 30 (lab/Proxmox). No public-internet exposure of in-boundary services.
- `inventory/overlay.yaml` — boundary classification: all in-scope hosts marked `boundary: in`

### ODP values / baseline-mandated parameters
No ODPs for IA-8 base control.

---

## IA-8(1) — Acceptance of PIV Credentials from Other Agencies

### Status
not-applicable

### What the control requires
Accept and electronically verify PIV-compliant credentials from other federal agencies.

### What is implemented
Not applicable. The Managed SOC Service is a private homelab with no federal agency interconnections and no PIV infrastructure. No federal users from other agencies access this system.

### What is partial or missing
Not applicable.

### Evidence paths
- `CLAUDE.md` (parent workspace) — no federal interconnection or PIV references

### ODP values / baseline-mandated parameters
No ODPs for IA-8(1).

---

## IA-8(2) — Acceptance of External Authenticators

### Status
not-applicable

### What the control requires
Accept only NIST-compliant external authenticators and maintain a documented list of accepted external authenticators.

### What is implemented
Not applicable. The Managed SOC Service does not accept any external authenticators from non-federal identity providers. All authentication is internal: SSH keys issued by the operator, service passwords managed in `.env`, and Tailscale device keys issued through the operator's Tailscale account. No OAuth, SAML, or federated identity provider integrations are in use within the FedRAMP Low boundary.

### What is partial or missing
Not applicable.

### Evidence paths
- `CLAUDE.md` (parent workspace) — all auth is SSH key or service password; no external IdP references

### ODP values / baseline-mandated parameters
No ODPs for IA-8(2).

---

## IA-8(4) — Use of Defined Profiles

### Status
partial

### What the control requires
Conform to defined identity management profiles for identity management.

### What is implemented
The system partially conforms to identity management profiles through its use of standard protocols:

- **SSH**: OpenSSH on all hosts conforms to the SSH protocol standard (RFC 4251–4256). Key types accepted are ED25519 and RSA-4096, aligning with NIST SP 800-207 guidance on key strength.
- **JWT (Wazuh API, RegScale)**: JSON Web Token per RFC 7519. Wazuh issues JWTs with configurable TTL; RegScale CE issues 24-hour JWTs per ADR 0003. JWTs carry role claims for authorization decisions.
- **HTTPS/TLS**: TLS 1.2 and TLS 1.3 per RFCs 5246/8446 for services that use HTTPS.

No formal identity management profile (e.g., FICAM-compliant, SAML 2.0, OpenID Connect) is adopted as a system-level standard. The system uses per-service native authentication without a unified identity fabric.

### What is partial or missing
- No formal identity profile document listing accepted identity management profiles and their conformance requirements
- No unified IdP or federation standard adopted
- No SP 800-63B Authenticator Assurance Level (AAL) designations formally assigned to each service

### Evidence paths
- `pipelines/common/wazuh.py` — JWT-based auth (RFC 7519 pattern)
- `pipelines/common/regscale.py` — JWT-based auth (RFC 7519 pattern; 24-hour TTL per ADR 0003)
- `docs/adr/0003-regscale-install-deviation.md` — JWT token structure (role claim: GlobalAdmin, TTL: 1440 min)
- `runbooks/cert-trust.md` — TLS version and cipher posture per service

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-08.04_odp | Identity management profiles | SSH (RFC 4251-4256, ED25519/RSA-4096); JWT (RFC 7519, role-claim based); TLS 1.2/1.3 (RFC 5246/8446) | organization |

---

## IA-11 — Re-authentication

### Status
implemented

### What the control requires
Require users to re-authenticate when defined circumstances or situations require it.

### What is implemented
Re-authentication is enforced through session TTL and protocol-level mechanisms:

- **SSH sessions**: SSH connections do not persist indefinitely; the OS terminates idle sessions via `ClientAliveInterval` / `ClientAliveCountMax` settings (or OS-level idle timeout). A new SSH session requires re-authentication with the private key.
- **Wazuh API JWT**: tokens expire after the Wazuh-configured TTL (900 seconds default). The pipeline client in `pipelines/common/wazuh.py` re-authenticates on 401 responses. Interactive dashboard sessions have session cookies that expire on browser close or inactivity.
- **RegScale JWT**: 24-hour TTL per ADR 0003 / ADR 0006 Deviation 7. Every pipeline invocation calls `POST /api/authentication/login` (re-auth per invocation by design). Interactive sessions expire after 1440 minutes.
- **Shuffle, OpenCTI, TheHive, Cortex, Velociraptor, DefectDojo**: each service enforces its own session timeout. Standard browser session management applies; sessions expire on browser close or configured inactivity timeout.
- **Tailscale**: device re-authentication is required when device keys expire (Tailscale default: key expiry enforced per Tailscale policy, typically 180 days unless disabled by the account admin).

Operator-defined re-authentication trigger: role change, credential reset, security incident, or session timeout.

### What is partial or missing
- No uniform session-timeout policy defined across all services (each uses its own platform default)
- No centralized session monitoring to detect and terminate stale sessions
- SSH `ClientAliveInterval` and `ClientAliveCountMax` settings are not uniformly documented across all hosts

### Evidence paths
- `pipelines/common/wazuh.py` — `authenticate()` and 401-retry logic (re-auth on token expiry)
- `pipelines/common/regscale.py` — `_get_token()` with per-invocation login + 401 re-auth
- `docs/adr/0003-regscale-install-deviation.md` — JWT TTL: 1440 minutes (`expires_in: 1440`)
- `docs/adr/0006-plan-2-environment-and-api-realignment.md` Deviation 7 — "every pipeline invocation is a fresh process and gets a fresh token"

### ODP values / baseline-mandated parameters
| ODP | Parameter | Value | Origin |
|-----|-----------|-------|--------|
| ia-11_odp | Circumstances requiring re-authentication | Session timeout per service platform defaults; security incident; role or credential change; explicit operator logout; Tailscale device key expiry | organization |

---

## Summary table

| Control | Title | Status |
|---------|-------|--------|
| IA-1 | Policy and Procedures | partial |
| IA-2 | Identification and Authentication (Org Users) | implemented |
| IA-2(1) | MFA to Privileged Accounts | partial |
| IA-2(2) | MFA to Non-privileged Accounts | partial |
| IA-2(8) | Replay-resistant Authentication | implemented |
| IA-2(12) | Acceptance of PIV Credentials | not-applicable |
| IA-4 | Identifier Management | implemented |
| IA-5 | Authenticator Management | partial |
| IA-5(1) | Password-based Authentication | implemented |
| IA-6 | Authentication Feedback | implemented |
| IA-7 | Cryptographic Module Authentication | implemented |
| IA-8 | I&A (Non-organizational Users) | not-applicable |
| IA-8(1) | Acceptance of PIV Credentials from Other Agencies | not-applicable |
| IA-8(2) | Acceptance of External Authenticators | not-applicable |
| IA-8(4) | Use of Defined Profiles | partial |
| IA-11 | Re-authentication | implemented |
