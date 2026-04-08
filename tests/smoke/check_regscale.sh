#!/usr/bin/env bash
# Smoke check for RegScale CE availability + auth.
#
# Three signals are checked:
#   1. /                     -> 200 (SPA shell renders)
#   2. POST /api/authentication/login with admin creds -> 200 + JWT
#   3. GET /api/SeedingStatus with that JWT -> 200 (proves the JWT round-trips
#      through the auth middleware to a protected endpoint; SeedingStatus is
#      a no-param GET that returns 200 for any authenticated caller)
#
# Required env (source from /c/Projects/.env on PITBOSS):
#   REGSCALE_URL       (e.g. http://10.10.30.28)
#   REGSCALE_USERNAME  (admin)
#   REGSCALE_PASSWORD

set -e
: "${REGSCALE_URL:?REGSCALE_URL must be set}"
: "${REGSCALE_USERNAME:?REGSCALE_USERNAME must be set}"
: "${REGSCALE_PASSWORD:?REGSCALE_PASSWORD must be set}"

root_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 "$REGSCALE_URL/")
if [ "$root_code" != "200" ]; then
  echo "RegScale FAIL at $REGSCALE_URL/ (root=$root_code, expected 200)"
  exit 1
fi

login_resp=$(curl -s -X POST "$REGSCALE_URL/api/authentication/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"${REGSCALE_USERNAME}\",\"password\":\"${REGSCALE_PASSWORD}\"}")
token=$(echo "$login_resp" | jq -r '.auth_token // empty')
if [ -z "$token" ]; then
  echo "RegScale FAIL at $REGSCALE_URL/api/authentication/login (no auth_token in response)"
  echo "  body: $login_resp"
  exit 1
fi

probe_code=$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $token" \
  "$REGSCALE_URL/api/SeedingStatus")
if [ "$probe_code" != "200" ]; then
  echo "RegScale FAIL at $REGSCALE_URL/api/SeedingStatus (got $probe_code with valid JWT)"
  exit 1
fi

echo "RegScale OK at $REGSCALE_URL (root=200 login=200 seedingstatus=200, JWT round-trips)"
