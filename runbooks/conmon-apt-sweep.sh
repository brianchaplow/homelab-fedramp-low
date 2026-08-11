#!/usr/bin/env bash
# Weekly PATCH-01 ConMon apt sweep for the brisket and haccp core nodes.
#
# The sweep deliberately does not restart Docker, containerd, Wazuh, or any
# application service. Container-runtime packages must already be held, the
# simulated transaction must leave them untouched, and their versions and
# daemon PIDs must remain unchanged across the real apt transaction.

set -Eeuo pipefail
umask 027

readonly -a PROTECTED_PACKAGES=(
  docker-ce
  docker-ce-cli
  docker-ce-rootless-extras
  containerd.io
  docker-buildx-plugin
  docker-compose-plugin
)

EXPECTED_HOST=""
PREFLIGHT_ONLY=0
TEMP_DIR=""
CONMON_LOG=""
CONMON_LOCK=""
CONMON_HEARTBEAT=""
MIN_FREE_KB=""
APT_PREFLIGHT_TIMEOUT=""

usage() {
  cat <<'EOF'
Usage: conmon-apt-sweep.sh [--expected-host brisket|haccp] [--preflight-only]

  --expected-host   Refuse to run when the installed cron is on the wrong host.
  --preflight-only  Run read-only host, disk, hold, and apt simulation checks.
                    Do not upgrade packages or publish a success heartbeat.
EOF
}

configure_runtime() {
  # Fixed production paths prevent a cron environment from redirecting
  # privileged writes or substituting package-management commands.
  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  CONMON_LOG=/var/log/conmon-apt-sweep.log
  CONMON_LOCK=/run/lock/conmon-apt-sweep.lock
  CONMON_HEARTBEAT=/var/lib/conmon-apt-sweep/last-clean-completion
  MIN_FREE_KB=5242880
  APT_PREFLIGHT_TIMEOUT=20m
  export PATH
  export LC_ALL=C
}

parse_args() {
  EXPECTED_HOST=""
  PREFLIGHT_ONLY=0

  while (($#)); do
    case "$1" in
      --expected-host)
        (($# >= 2)) || { usage >&2; exit 64; }
        EXPECTED_HOST=$2
        shift 2
        ;;
      --preflight-only)
        PREFLIGHT_ONLY=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        printf 'ERROR: unknown argument: %s\n' "$1" >&2
        usage >&2
        exit 64
        ;;
    esac
  done

  case "$EXPECTED_HOST" in
    ""|brisket|haccp) ;;
    *)
      printf 'ERROR: unsupported expected host: %s\n' "$EXPECTED_HOST" >&2
      exit 64
      ;;
  esac
}

require_root() {
  if ((EUID != 0)); then
    printf 'ERROR: conmon-apt-sweep must run as root\n' >&2
    exit 77
  fi
}

cleanup() {
  if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
    rm -rf -- "$TEMP_DIR"
  fi
}

utc_now() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

fatal() {
  local message=$1
  local code=${2:-1}
  printf '=== %s conmon-apt-sweep FAILED on %s: %s ===\n' \
    "$(utc_now)" "${HOST_SHORT:-unknown}" "$message"
  exit "$code"
}

on_error() {
  local code=$1
  local line=$2
  trap - ERR
  fatal "unexpected command failure at line $line (rc=$code)" "$code"
}

require_commands() {
  local command_name
  for command_name in apt-get apt-mark awk chmod curl df docker dpkg-query \
    flock grep hostname mktemp mkdir mv rm systemctl timeout tr; do
    command -v "$command_name" >/dev/null 2>&1 || \
      fatal "required command is unavailable: $command_name" 69
  done
}

check_free_space() {
  local path=$1
  local available_kb

  if ! available_kb=$(df -Pk -- "$path" | awk 'NR == 2 { print $4 }'); then
    fatal "could not read free space for $path"
  fi
  [[ "$available_kb" =~ ^[0-9]+$ ]] || \
    fatal "invalid free-space result for $path: $available_kb"
  ((available_kb >= MIN_FREE_KB)) || \
    fatal "insufficient free space on $path: ${available_kb}KB available, ${MIN_FREE_KB}KB required"
  printf 'disk preflight: %s has %sKB available (minimum %sKB)\n' \
    "$path" "$available_kb" "$MIN_FREE_KB"
}

assert_runtime_holds() {
  local holds
  local package
  local -a missing=()

  if ! holds=$(apt-mark showhold); then
    fatal "apt-mark showhold failed"
  fi
  for package in "${PROTECTED_PACKAGES[@]}"; do
    if ! grep -Fqx -- "$package" <<<"$holds"; then
      missing+=("$package")
    fi
  done
  ((${#missing[@]} == 0)) || \
    fatal "required container-runtime holds are missing: ${missing[*]}"
  printf 'hold assertion: all %s protected container-runtime packages are held\n' \
    "${#PROTECTED_PACKAGES[@]}"
}

snapshot_runtime_versions() {
  local package
  local version

  for package in "${PROTECTED_PACKAGES[@]}"; do
    if ! version=$(dpkg-query -W -f='${Version}' "$package"); then
      printf 'protected package is not installed: %s\n' "$package" >&2
      return 1
    fi
    printf '%s=%s\n' "$package" "$version"
  done
}

snapshot_runtime_pids() {
  local unit
  local pid

  for unit in docker containerd; do
    if ! systemctl is-active --quiet "$unit"; then
      printf 'runtime unit is not active: %s\n' "$unit" >&2
      return 1
    fi
    if ! pid=$(systemctl show --property=MainPID --value "$unit"); then
      printf 'could not read runtime PID: %s\n' "$unit" >&2
      return 1
    fi
    if [[ ! "$pid" =~ ^[1-9][0-9]*$ ]]; then
      printf 'runtime unit has an invalid PID: %s=%s\n' "$unit" "$pid" >&2
      return 1
    fi
    printf '%s=%s\n' "$unit" "$pid"
  done
}

assert_container_running() {
  local container=$1
  local state
  local health

  if ! read -r state health < <(
    docker inspect --format \
      '{{.State.Status}} {{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' \
      "$container"
  ); then
    fatal "could not inspect required container: $container"
  fi
  [[ "$state" == running ]] || \
    fatal "required container is not running: $container (state=$state)"
  case "$health" in
    none|healthy) ;;
    *) fatal "required container is not healthy: $container (health=$health)" ;;
  esac
  printf 'container health: %s state=%s health=%s\n' "$container" "$state" "$health"
}

assert_unit_active() {
  local unit=$1
  systemctl is-active --quiet "$unit" || \
    fatal "required systemd unit is not active: $unit"
  printf 'systemd health: %s active\n' "$unit"
}

check_http() {
  local name=$1
  local url=$2
  local allowed_codes=$3
  local code

  if ! code=$(curl --silent --show-error --insecure \
    --connect-timeout 5 --max-time 15 --output /dev/null \
    --write-out '%{http_code}' "$url"); then
    fatal "$name endpoint request failed: $url"
  fi
  case ",$allowed_codes," in
    *",$code,"*) ;;
    *) fatal "$name endpoint returned HTTP $code, expected one of: $allowed_codes" ;;
  esac
  printf 'endpoint health: %s HTTP %s\n' "$name" "$code"
}

check_haccp() {
  local container

  for container in elk-es01-1 elk-kibana-1 elk-logstash-1 elk-fleet-server-1; do
    assert_container_running "$container"
  done
  assert_unit_active arkimecapture
  assert_unit_active arkimeviewer
  assert_unit_active wazuh-agent
  check_http haccp-kibana http://localhost:5601 200,302

  # Authenticate inside the Elasticsearch container. A short-lived 0600 netrc
  # file keeps the credential out of the host/container process lists and log.
  if ! docker exec elk-es01-1 sh -eu -c '
    auth_file=$(mktemp)
    trap '\''rm -f -- "$auth_file"'\'' EXIT
    chmod 0600 "$auth_file"
    printf "machine localhost\\nlogin elastic\\npassword %s\\n" \
      "${ELASTIC_PASSWORD:?}" >"$auth_file"
    response=$(curl --silent --show-error --fail \
      --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt \
      --netrc-file "$auth_file" \
      "https://localhost:9200/_cluster/health?filter_path=status")
    case "$response" in
      *\"status\":\"green\"*|*\"status\":\"yellow\"*) exit 0 ;;
      *) printf "unexpected Elasticsearch health: %s\\n" "$response" >&2; exit 1 ;;
    esac
  '; then
    fatal "Elasticsearch cluster health is unavailable or red"
  fi
  echo 'Elasticsearch cluster health: green/yellow'
}

check_brisket() {
  local probe_response

  assert_unit_active wazuh-agent
  check_http wazuh-dashboard https://localhost:5601 200,302
  check_http wazuh-api https://localhost:55000 401
  check_http shuffle http://localhost:3443 200,301,302
  check_http opencti http://localhost:8080 200,301,302
  check_http velociraptor https://localhost:8889 307
  check_http grafana http://localhost:3000 200,302
  check_http ml-scorer http://localhost:5002/health 200

  if ! probe_response=$(curl --silent --show-error --fail \
    --connect-timeout 5 --max-time 15 --get \
    --data-urlencode 'query=probe_success==0' \
    http://localhost:9090/api/v1/query); then
    fatal "Prometheus end-to-end probe query failed"
  fi
  if ! grep -Eq '"status"[[:space:]]*:[[:space:]]*"success"' \
    <<<"$probe_response" || \
    ! grep -Eq '"result"[[:space:]]*:[[:space:]]*\[[[:space:]]*\]' \
      <<<"$probe_response"; then
    fatal "one or more brisket Prometheus blackbox probes are failing"
  fi
  echo 'Prometheus blackbox health: no failing probes'
}

run_host_gate() {
  local phase=$1

  printf '%s host health gate BEGIN\n' "$phase"
  docker info --format '{{.ServerVersion}}' >/dev/null || \
    fatal "Docker daemon is unavailable during the $phase gate"
  case "$HOST_SHORT" in
    haccp) check_haccp ;;
    brisket) check_brisket ;;
    *) fatal "unsupported PATCH-01 host: $HOST_SHORT" ;;
  esac
  printf '%s host health gate PASS\n' "$phase"
}

assert_safe_simulation() {
  local plan_file=$1
  local package

  if awk '$1 == "Remv" { found = 1 } END { exit(found ? 0 : 1) }' "$plan_file"; then
    fatal "apt simulation contains package removals"
  fi

  for package in "${PROTECTED_PACKAGES[@]}"; do
    if awk -v protected="$package" '
      $1 == "Inst" || $1 == "Remv" || $1 == "Conf" {
        candidate = $2
        sub(/:.*/, "", candidate)
        if (candidate == protected) found = 1
      }
      END { exit(found ? 0 : 1) }
    ' "$plan_file"; then
      fatal "apt simulation would change protected package: $package"
    fi
  done
  printf 'package simulation assertion: no removals or protected runtime changes\n'
}

run_package_preflight() {
  local plan_file=$1
  local rc

  echo '--- apt-get check ---'
  if timeout "$APT_PREFLIGHT_TIMEOUT" apt-get check; then
    :
  else
    rc=$?
    fatal "apt-get check failed (rc=$rc)" "$rc"
  fi

  echo '--- apt-get simulated upgrade ---'
  if timeout "$APT_PREFLIGHT_TIMEOUT" apt-get -s -y --no-remove \
    -o APT::Get::allow-change-held-packages=false \
    -o Dpkg::Options::=--force-confold \
    -o Dpkg::Options::=--force-confdef \
    -o Dpkg::Use-Pty=0 \
    upgrade >"$plan_file" 2>&1; then
    :
  else
    rc=$?
    cat "$plan_file"
    fatal "apt simulated upgrade failed (rc=$rc)" "$rc"
  fi
  cat "$plan_file"
  assert_safe_simulation "$plan_file"
}

publish_heartbeat() {
  local heartbeat_dir
  local heartbeat_tmp
  local heartbeat_epoch

  heartbeat_dir=$(dirname -- "$CONMON_HEARTBEAT")
  mkdir -p -- "$heartbeat_dir"
  chmod 0750 -- "$heartbeat_dir"
  heartbeat_tmp=$(mktemp "${CONMON_HEARTBEAT}.tmp.XXXXXX")
  heartbeat_epoch=$(date -u +%s)
  printf '%s\n' "$heartbeat_epoch" >"$heartbeat_tmp"
  chmod 0640 -- "$heartbeat_tmp"
  mv -f -- "$heartbeat_tmp" "$CONMON_HEARTBEAT"
  printf 'clean-completion heartbeat: %s epoch=%s\n' \
    "$CONMON_HEARTBEAT" "$heartbeat_epoch"
}

main() {
  local start_ts
  local docker_root
  local plan_file
  local runtime_versions_before
  local runtime_versions_after
  local runtime_pids_before
  local runtime_pids_after

  configure_runtime
  parse_args "$@"
  require_root

  mkdir -p -- "$(dirname -- "$CONMON_LOG")" "$(dirname -- "$CONMON_LOCK")"
  touch "$CONMON_LOG"
  chmod 0640 "$CONMON_LOG"
  exec >>"$CONMON_LOG" 2>&1
  trap cleanup EXIT
  trap 'on_error "$?" "$LINENO"' ERR

  require_commands
  HOST_SHORT=$(hostname -s | tr '[:upper:]' '[:lower:]')
  readonly HOST_SHORT
  [[ "$HOST_SHORT" == brisket || "$HOST_SHORT" == haccp ]] || \
    fatal "unsupported PATCH-01 host: $HOST_SHORT" 65
  if [[ -n "$EXPECTED_HOST" && "$HOST_SHORT" != "$EXPECTED_HOST" ]]; then
    fatal "cron profile expects $EXPECTED_HOST but this host is $HOST_SHORT" 65
  fi

  exec 9>"$CONMON_LOCK"
  flock -n 9 || fatal "another sweep already holds $CONMON_LOCK" 75

  TEMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/conmon-apt-sweep.XXXXXX")
  plan_file="$TEMP_DIR/apt-simulation.txt"
  start_ts=$(utc_now)
  printf '\n=== %s conmon-apt-sweep BEGIN on %s ===\n' "$start_ts" "$HOST_SHORT"

  check_free_space /
  if ! docker_root=$(docker info --format '{{.DockerRootDir}}'); then
    fatal "could not determine Docker data root"
  fi
  [[ -n "$docker_root" ]] || fatal "Docker returned an empty data root"
  if [[ "$docker_root" != / ]]; then
    check_free_space "$docker_root"
  fi

  assert_runtime_holds
  if ! runtime_versions_before=$(snapshot_runtime_versions); then
    fatal "could not snapshot protected runtime package versions"
  fi
  if ! runtime_pids_before=$(snapshot_runtime_pids); then
    fatal "could not snapshot Docker/containerd daemon PIDs"
  fi
  printf '%s\n' 'runtime package baseline:' "$runtime_versions_before"
  printf '%s\n' 'runtime daemon PID baseline:' "$runtime_pids_before"
  run_host_gate PRE

  if ((PREFLIGHT_ONLY == 0)); then
    echo '--- apt-get update ---'
    if timeout "$APT_PREFLIGHT_TIMEOUT" apt-get update -qq; then
      :
    else
      fatal "apt-get update failed" "$?"
    fi
  fi
  run_package_preflight "$plan_file"

  if ((PREFLIGHT_ONLY == 1)); then
    printf '=== %s conmon-apt-sweep PREFLIGHT PASS on %s (no heartbeat published) ===\n' \
      "$(utc_now)" "$HOST_SHORT"
    exit 0
  fi

  echo '--- apt-get upgrade (container runtime held; service restart automation disabled) ---'
  DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=l \
    apt-get -y --no-remove \
      -o APT::Get::allow-change-held-packages=false \
      -o Dpkg::Options::=--force-confold \
      -o Dpkg::Options::=--force-confdef \
      -o Dpkg::Use-Pty=0 \
      upgrade

  assert_runtime_holds
  if ! runtime_versions_after=$(snapshot_runtime_versions); then
    fatal "could not resnapshot protected runtime package versions"
  fi
  [[ "$runtime_versions_after" == "$runtime_versions_before" ]] || \
    fatal "a protected container-runtime package version changed"
  echo 'runtime package assertion: protected versions unchanged'

  if ! runtime_pids_after=$(snapshot_runtime_pids); then
    fatal "could not resnapshot Docker/containerd daemon PIDs"
  fi
  [[ "$runtime_pids_after" == "$runtime_pids_before" ]] || \
    fatal "Docker or containerd restarted during the patch transaction"
  echo 'runtime daemon assertion: Docker/containerd PIDs unchanged'

  run_host_gate POST

  # This is intentionally the final state mutation. Any earlier failure leaves
  # an existing heartbeat untouched and never creates a new success signal.
  publish_heartbeat
  printf '=== %s conmon-apt-sweep END on %s ===\n' "$(utc_now)" "$HOST_SHORT"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
  main "$@"
fi
