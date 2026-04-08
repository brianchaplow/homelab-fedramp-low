#!/usr/bin/env bash
#
# RegScale Community Edition install wrapper.
# Run on the regscale VM (Ubuntu 24.04, Docker installed).
#
# Uses the MIT-licensed standalone Python installer from
# github.com/RegScale/community, which pulls the public regscale/regscale
# Docker image and serves plain HTTP on port 80 (NOT 81 — see ADR 0003).
#
# Post-install requires manual admin password reset via SQL — RegScale CE
# does NOT print or document a default admin password (see ADR 0003).
#
set -e

echo "[1/5] Verifying Docker is installed..."
docker version > /dev/null

echo "[2/5] Installing Python 3.11 (deadsnakes PPA)..."
if ! command -v python3.11 >/dev/null; then
  sudo DEBIAN_FRONTEND=noninteractive add-apt-repository -y ppa:deadsnakes/ppa
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3.11 python3.11-venv
fi

echo "[3/5] Fetching standalone_regscale.py from MIT community repo..."
mkdir -p ~/regscale
cd ~/regscale
curl -fsSL -o standalone_regscale.py \
  https://raw.githubusercontent.com/RegScale/community/main/standalone/standalone_regscale.py

python3.11 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip > /dev/null

echo "[4/5] Running installer (8-10 minutes; will say it errored — that is fine)..."
# The installer wraps docker compose. On a 6 GB VM the SQL Server migration
# wave can race the EF Core lock release and the Python installer prints a
# fatal-looking exception, BUT atlas's restart_policy=always then retries
# the migration and it succeeds on the second pass. Hence `|| true`.
python standalone_regscale.py start 2>&1 | tee /tmp/regscale-install.log || true

echo "[5/5] Waiting for atlas container to finish migrations + post-startup seeding..."
for i in $(seq 1 60); do
  if curl -sf http://127.0.0.1:80/ -o /dev/null; then
    echo "  RegScale is up at http://127.0.0.1:80/"
    break
  fi
  echo "  ($i/60) waiting..."
  sleep 5
done

echo
echo "Install complete."
echo
echo "ADMIN PASSWORD RESET REQUIRED — see deploy/regscale/reset-admin-password.sh"
echo "(RegScale CE does not ship a known default admin password.)"
