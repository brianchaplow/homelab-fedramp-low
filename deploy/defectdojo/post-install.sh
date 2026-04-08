#!/usr/bin/env bash
#
# Create DefectDojo products, engagements, and SLA profile for MSS.
# Idempotent: safe to re-run.
#
# Required env (from /c/Projects/.env on PITBOSS):
#   DEFECTDOJO_URL       (e.g. http://10.10.30.27:8080)
#   DEFECTDOJO_API_KEY
#
set -e
: "${DEFECTDOJO_URL:?DEFECTDOJO_URL must be set in /c/Projects/.env}"
: "${DEFECTDOJO_API_KEY:?DEFECTDOJO_API_KEY must be set in /c/Projects/.env}"

AUTH="Authorization: Token $DEFECTDOJO_API_KEY"
API="$DEFECTDOJO_URL/api/v2"

curl_dd() {
  # --fail-with-body -> curl exits non-zero on >= 400 but still prints body
  # set -e (above) then aborts the script with the body visible.
  curl -s --fail-with-body -H "$AUTH" -H "Content-Type: application/json" "$@"
}

# --- Product Type: Managed SOC Service ---
PT_ID=$(curl_dd "$API/product_types/?name=Managed%20SOC%20Service" | jq -r '.results[0].id // empty')
if [ -z "$PT_ID" ]; then
  PT_ID=$(curl_dd -X POST "$API/product_types/" -d '{"name":"Managed SOC Service","critical_product":true,"key_product":true}' | jq -r .id)
  echo "Created Product Type 'Managed SOC Service' (id=$PT_ID)"
else
  echo "Product Type 'Managed SOC Service' already exists (id=$PT_ID)"
fi

# --- SLA Configuration (FedRAMP Low: 30/90/180/365) ---
# NOTE: ?name= on /sla_configurations/ does NOT actually filter (returns all
# rows). We must client-side filter the full list with jq exact-match.
SLA_ID=$(curl_dd "$API/sla_configurations/" | jq -r '.results[] | select(.name=="FedRAMP Low ConMon") | .id' | head -1)
if [ -z "$SLA_ID" ]; then
  SLA_ID=$(curl_dd -X POST "$API/sla_configurations/" -d '{
    "name": "FedRAMP Low ConMon",
    "description": "FedRAMP Low ConMon remediation timelines per FedRAMP ConMon Strategy Guide",
    "critical": 30,
    "high": 90,
    "medium": 180,
    "low": 365
  }' | jq -r .id)
  echo "Created SLA Configuration 'FedRAMP Low ConMon' (id=$SLA_ID)"
else
  echo "SLA Configuration 'FedRAMP Low ConMon' already exists (id=$SLA_ID)"
fi

# --- Products ---
# Idempotent + reconciling: creates missing products, and re-attaches the
# correct SLA / product type to existing products if they drifted.
create_product() {
  local name="$1"
  local desc="$2"
  local existing existing_sla existing_pt
  # /products/?name= filter works exactly on this endpoint, but be defensive
  # by client-side exact-matching on .name as well.
  local row
  row=$(curl_dd "$API/products/?name=$(printf '%s' "$name" | jq -sRr @uri)" \
    | jq -c --arg n "$name" '.results[] | select(.name==$n)' | head -1)
  if [ -z "$row" ]; then
    local id
    id=$(curl_dd -X POST "$API/products/" -d "{
      \"name\": \"$name\",
      \"description\": \"$desc\",
      \"prod_type\": $PT_ID,
      \"sla_configuration\": $SLA_ID
    }" | jq -r .id)
    echo "Created Product '$name' (id=$id)"
  else
    existing=$(jq -r '.id' <<<"$row")
    existing_sla=$(jq -r '.sla_configuration' <<<"$row")
    existing_pt=$(jq -r '.prod_type' <<<"$row")
    if [ "$existing_sla" != "$SLA_ID" ] || [ "$existing_pt" != "$PT_ID" ]; then
      curl_dd -X PATCH "$API/products/$existing/" -d "{
        \"prod_type\": $PT_ID,
        \"sla_configuration\": $SLA_ID
      }" > /dev/null
      echo "Reattached Product '$name' (id=$existing) -> prod_type=$PT_ID sla=$SLA_ID"
    else
      echo "Product '$name' already exists and is correctly attached (id=$existing)"
    fi
  fi
}

create_product "MSS Core - brisket" "Wazuh SIEM, Shuffle SOAR, Velociraptor DFIR, OpenCTI, ml-scorer, Prometheus+Grafana"
create_product "MSS Log Analytics - haccp" "ELK 8.17, Arkime, Fleet Server"
create_product "MSS Network Sensors - smokehouse" "Suricata, Zeek, Wazuh agent"
create_product "MSS Boundary Protection - OPNsense" "Inter-VLAN firewall, boundary enforcement"
create_product "MSS GRC Tooling - dojo + regscale" "DefectDojo and RegScale CE hosts themselves"

echo "DefectDojo seed data loaded successfully."
