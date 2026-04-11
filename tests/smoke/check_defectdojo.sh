#!/usr/bin/env bash
# Smoke check for DefectDojo availability.
#
# The canonical endpoint is HTTP on port 8080 in DefectDojo 2.57.0
# (bundled nginx has no TLS cert wired in -- see docs/adr/0004).
#
# We check two signals:
#   1. /api/v2/user_profile/    -- must return 403 (service up, auth required)
#   2. /login                    -- must return 200 (login page renders)
#
# Either signal alone could be faked by a generic 403-returning proxy,
# so both are required for a PASS.

set -e

DD_URL="${DEFECTDOJO_URL:-http://10.10.30.27:8080}"

api_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 "$DD_URL/api/v2/user_profile/")
login_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 "$DD_URL/login")

if [ "$api_code" = "403" ] && [ "$login_code" = "200" ]; then
  echo "DefectDojo OK at $DD_URL (api=403 login=200)"
  exit 0
else
  echo "DefectDojo FAIL at $DD_URL (api=$api_code login=$login_code, expected api=403 login=200)"
  exit 1
fi
