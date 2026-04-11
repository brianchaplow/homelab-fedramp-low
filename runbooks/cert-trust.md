# Runbook: TLS posture for DefectDojo and RegScale

## Current state (2026-04-08)

Both services run **plain HTTP on the lab subnets**. This is a deliberate
control trade-off documented in ADRs 0003 and 0004:

| Service | URL | Port | Rationale |
|---|---|---|---|
| DefectDojo | `http://10.10.30.27:8080/` | 8080 | DefectDojo 2.57.0 bundled nginx has no TLS cert wired in. Compose maps 8443 but the container does not listen on it. |
| RegScale CE | `http://10.10.30.28/` | 80 | Bundled compose binds 0.0.0.0:80 → atlas:8080. No TLS termination in the container. |

There are no self-signed certificates to trust. If a command-line or
Python client sees a TLS error talking to these services, it means the
caller is pointing at the wrong scheme -- correct to `http://`.

## Why this is acceptable in the homelab

- Reachable only from VLAN 10/20/30 (trusted subnets) via UFW egress rules
  on the service VMs
- Synthetic FedRAMP-Low scope data only (no real PHI / PII / financial --
  see ADR 0001 for the RegScale EULA analysis)
- No external exposure -- no OPNsense port forwards to these VMs, no
  Tailscale exit nodes routing public traffic through them
- Portfolio writeup (Plan 4) explicitly calls this out as "in a real
  FedRAMP-Low deployment, front with a TLS-terminating reverse proxy"

## If you later add a reverse proxy (production-adjacent posture)

The recommended pattern for this homelab is:

1. Stand up **Caddy** or **Traefik** on brisket as a reverse proxy
   (brisket already runs the SOC platform and has Grafana at :3000 as
   a comparable TLS-terminated service)
2. Register local DNS names in OPNsense Unbound:
   - `dojo.local` → 10.10.30.27
   - `regscale.local` → 10.10.30.28
3. Use step-ca or Caddy's internal CA to issue certs for `*.local`
4. Update `deploy/defectdojo/README.md` and `deploy/regscale/README.md`
   to point at the TLS URLs once the proxy is in place
5. **Update the Plan 1 done-criteria** (ADR 0002) to require HTTPS instead
   of HTTP at that point
6. Scrub `/c/Projects/.env` `DEFECTDOJO_URL` / `REGSCALE_URL` to the new
   https URLs
7. Rerun `./pipelines.sh smoke` to confirm the pipelines still work via
   the proxy -- this is a good regression check

## In Python requests (current HTTP-only reality)

```python
import requests, os
from dotenv import load_dotenv
load_dotenv("/c/Projects/.env")

url = os.environ["DEFECTDOJO_URL"]        # http://10.10.30.27:8080
key = os.environ["DEFECTDOJO_API_KEY"]
r = requests.get(
    f"{url}/api/v2/user_profile/",
    headers={"Authorization": f"Token {key}"},
)
r.raise_for_status()
print(r.json())
```

No `verify=False` is needed because there is no TLS. When the reverse
proxy lands, switch to `verify=True` (the default) against the trusted
`*.local` cert chain.

## In browsers (PITBOSS Firefox / Chrome / Edge)

Just visit the HTTP URL. Chromium-family browsers will show a "Not
secure" badge -- expected for the lab. Do **not** click "Proceed to
site" for an HTTPS error on these services; that means the URL is wrong.

## Portfolio writeup note

Plan 4's writeup treats this HTTP-only state as the "as-built" posture
and the TLS-fronted state as the "if we were actually FedRAMP authorized"
posture. The delta is a single paragraph in the SSP §SC-8 explaining
why the homelab trades TLS for clarity-of-scope, and a line item in
the POA&M that would close out only when a production deployment is
contemplated.
