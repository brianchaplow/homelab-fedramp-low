#!/usr/bin/env bash
#
# Reset the RegScale CE admin password to a known value.
#
# Why this exists:
#   RegScale CE seeds an admin user (Email=admin@admin.com, UserName=admin)
#   with EmailConfirmed=0 and a hashed password that is NOT documented in
#   the public installer or repo. There is no first-run wizard, no password
#   printed to stdout, and no env var to override it. The only practical way
#   to log in to a fresh CE instance is to overwrite the PasswordHash in the
#   AspNetUsers table directly. See docs/adr/0003-regscale-install-deviation.md.
#
# This script:
#   1. Generates an ASP.NET Identity v3 PBKDF2-HMAC-SHA512 hash for $NEWPASS
#      (matches the format DefaultPasswordHasher uses: byte 0x01 marker,
#       PRF=2, iter=100000, salt=16 bytes, subkey=32 bytes).
#   2. UPDATEs AspNetUsers in the SQL Server container with the new hash,
#      sets EmailConfirmed=1, clears LockoutEnd, resets AccessFailedCount.
#   3. Verifies login via /api/authentication/login.
#
# Required env (set in shell or source from /c/Projects/.env on PITBOSS):
#   REGSCALE_DB_SA_PASSWORD  - SQL sa password (in atlas.env on the VM)
#   REGSCALE_PASSWORD        - the new admin password to set (12+ chars,
#                              must include upper, lower, digit, symbol per
#                              tenant policy)
#
set -e
: "${REGSCALE_DB_SA_PASSWORD:?must be set (see ~/regscale/atlas.env on the VM)}"
: "${REGSCALE_PASSWORD:?must be set to the desired new admin password}"

NEWHASH=$(python3 - <<PY
import hashlib, os, base64, struct
password = b"""${REGSCALE_PASSWORD}"""
prf = 2          # HMACSHA512
iterations = 100000
salt = os.urandom(16)
subkey = hashlib.pbkdf2_hmac("sha512", password, salt, iterations, 32)
header = struct.pack(">BIII", 1, prf, iterations, 16)
print(base64.b64encode(header + salt + subkey).decode())
PY
)
echo "Generated hash (truncated): ${NEWHASH:0:20}..."

cd ~/regscale
docker compose exec -T atlas-db /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P "${REGSCALE_DB_SA_PASSWORD}" -C -d ATLAS -I -Q \
  "UPDATE AspNetUsers
     SET PasswordHash = '${NEWHASH}',
         EmailConfirmed = 1,
         AccessFailedCount = 0,
         LockoutEnd = NULL,
         LastPasswordChange = SYSUTCDATETIME()
   WHERE UserName = 'admin';
   SELECT @@ROWCOUNT AS rows_updated"

echo
echo "Verifying login..."
code=$(curl -s -o /tmp/regscale-login.json -w '%{http_code}' \
  -X POST http://127.0.0.1:80/api/authentication/login \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"admin\",\"password\":\"${REGSCALE_PASSWORD}\"}")
if [ "$code" = "200" ]; then
  echo "  PASS: login returns 200, JWT issued"
else
  echo "  FAIL: login returned $code"
  cat /tmp/regscale-login.json
  exit 1
fi
