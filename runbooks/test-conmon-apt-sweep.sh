#!/usr/bin/env bash
# Isolated regression harness for conmon-apt-sweep.sh.
# Every host, package, disk, runtime, and HTTP command is replaced by a stub.

set -Eeuo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
SUT="$SCRIPT_DIR/conmon-apt-sweep.sh"
TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/test-conmon-apt-sweep.XXXXXX")
FAKE_BIN="$TEST_ROOT/bin"
RUNNER="$TEST_ROOT/run-sweep"
TOTAL=0
PASSED=0

cleanup() {
  rm -rf -- "$TEST_ROOT"
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_file_contains() {
  local file=$1
  local pattern=$2
  grep -Eq -- "$pattern" "$file" || \
    fail "$file does not contain pattern: $pattern"
}

assert_file_not_contains() {
  local file=$1
  local pattern=$2
  if grep -Eq -- "$pattern" "$file"; then
    fail "$file unexpectedly contains pattern: $pattern"
  fi
}

mkdir -p "$FAKE_BIN"
cat >"$FAKE_BIN/dispatcher" <<'STUB'
#!/usr/bin/env bash
set -u

command_name=$(basename -- "$0")
printf '%s|%s\n' "$command_name" "$*" >>"$FAKE_CALLS"

case "$command_name" in
  hostname)
    printf '%s\n' "$FAKE_HOST"
    ;;

  df)
    if [[ "$FAKE_SCENARIO" == low-disk ]]; then
      available=1024
    else
      available=10485760
    fi
    printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\n'
    printf '/dev/fake 20971520 10485760 %s 50%% /\n' "$available"
    ;;

  apt-mark)
    packages=(
      docker-ce
      docker-ce-cli
      docker-ce-rootless-extras
      containerd.io
      docker-buildx-plugin
      docker-compose-plugin
    )
    for package in "${packages[@]}"; do
      if [[ "$FAKE_SCENARIO" == missing-hold && "$package" == docker-compose-plugin ]]; then
        continue
      fi
      printf '%s\n' "$package"
    done
    ;;

  dpkg-query)
    package=${!#}
    version=1.0
    if [[ "$FAKE_SCENARIO" == runtime-version-changed && -f "$FAKE_STATE/upgraded" && "$package" == docker-ce ]]; then
      version=2.0
    fi
    printf '%s' "$version"
    ;;

  systemctl)
    action=${1:-}
    unit=${!#}
    case "$action" in
      is-active)
        if [[ "$FAKE_SCENARIO" == haccp-arkime-fails && "$unit" == arkimeviewer ]]; then
          exit 3
        fi
        exit 0
        ;;
      show)
        pid=100
        if [[ "$FAKE_SCENARIO" == runtime-restart && -f "$FAKE_STATE/upgraded" && "$unit" == docker ]]; then
          pid=200
        fi
        printf '%s\n' "$pid"
        ;;
      *) exit 64 ;;
    esac
    ;;

  docker)
    action=${1:-}
    case "$action" in
      info)
        if [[ "$*" == *DockerRootDir* ]]; then
          printf '/\n'
        else
          printf '27.5.1\n'
        fi
        ;;
      inspect)
        container=${!#}
        if [[ "$FAKE_SCENARIO" == haccp-container-fails && "$container" == elk-logstash-1 ]]; then
          printf 'exited none\n'
        else
          printf 'running healthy\n'
        fi
        ;;
      exec)
        [[ "$FAKE_SCENARIO" != haccp-es-red ]]
        ;;
      *) exit 64 ;;
    esac
    ;;

  curl)
    url=${!#}
    if [[ "$url" == *9090/api/v1/query ]]; then
      if [[ "$FAKE_SCENARIO" == brisket-probe-fails ]]; then
        printf '{"status":"success","data":{"result":[{"metric":{"instance":"failed"}}]}}\n'
      else
        printf '{"status":"success","data":{"result":[]}}\n'
      fi
      exit 0
    fi

    case "$url" in
      *:55000*) code=401 ;;
      *:8889*) code=307 ;;
      *:5601*) code=302 ;;
      *:3000*) code=302 ;;
      *) code=200 ;;
    esac
    if [[ "$FAKE_SCENARIO" == brisket-endpoint-fails && "$url" == *:5002/health ]]; then
      code=503
    fi
    if [[ "$FAKE_SCENARIO" == post-health-fails && -f "$FAKE_STATE/upgraded" && "$url" == *:5002/health ]]; then
      code=503
    fi
    printf '%s' "$code"
    ;;

  apt-get)
    operation=""
    simulated=0
    for argument in "$@"; do
      case "$argument" in
        update|check|upgrade) operation=$argument ;;
        -s|--simulate|--dry-run) simulated=1 ;;
      esac
    done

    case "$operation" in
      update)
        [[ "$FAKE_SCENARIO" != update-fails ]] || exit 42
        printf 'apt metadata refreshed\n'
        ;;
      check)
        [[ "$FAKE_SCENARIO" != check-fails ]] || exit 43
        printf 'package graph is consistent\n'
        ;;
      upgrade)
        if ((simulated == 1)); then
          if [[ "$FAKE_SCENARIO" == runtime-plan ]]; then
            printf 'Inst docker-ce [1.0] (2.0 fake [amd64])\n'
            printf 'Conf docker-ce (2.0 fake [amd64])\n'
          elif [[ "$FAKE_SCENARIO" == removal-plan ]]; then
            printf 'Remv obsolete-package [1.0]\n'
          else
            printf 'Inst bash [5.2] (5.3 fake [amd64])\n'
            printf 'Conf bash (5.3 fake [amd64])\n'
          fi
        else
          [[ "$FAKE_SCENARIO" != upgrade-fails ]] || exit 44
          : >"$FAKE_STATE/upgraded"
          printf 'stubbed package upgrade complete\n'
        fi
        ;;
      *) exit 64 ;;
    esac
    ;;

  *)
    printf 'unhandled stub command: %s\n' "$command_name" >&2
    exit 64
    ;;
esac
STUB
chmod +x "$FAKE_BIN/dispatcher"

for command_name in apt-get apt-mark curl df docker dpkg-query hostname systemctl; do
  ln -s dispatcher "$FAKE_BIN/$command_name"
done

cat >"$RUNNER" <<'RUNNER_SCRIPT'
#!/usr/bin/env bash
set -Eeuo pipefail

TEST_CONMON_LOG=${CONMON_LOG:?}
TEST_CONMON_LOCK=${CONMON_LOCK:?}
TEST_CONMON_HEARTBEAT=${CONMON_HEARTBEAT:?}
source "${CONMON_SUT:?}"

configure_runtime() {
  PATH=${CONMON_TEST_PATH:?}
  CONMON_LOG=$TEST_CONMON_LOG
  CONMON_LOCK=$TEST_CONMON_LOCK
  CONMON_HEARTBEAT=$TEST_CONMON_HEARTBEAT
  MIN_FREE_KB=${CONMON_MIN_FREE_KB:-5242880}
  APT_PREFLIGHT_TIMEOUT=${CONMON_APT_PREFLIGHT_TIMEOUT:-10s}
  export PATH
  export LC_ALL=C
}

require_root() {
  :
}

main "$@"
RUNNER_SCRIPT
chmod +x "$RUNNER"

run_sweep() {
  local case_dir=$1
  local host=$2
  local scenario=$3
  shift 3

  env \
    CONMON_SUT="$SUT" \
    CONMON_TEST_PATH="$FAKE_BIN:/usr/bin:/bin" \
    CONMON_LOG="$case_dir/sweep.log" \
    CONMON_LOCK="$case_dir/sweep.lock" \
    CONMON_HEARTBEAT="$case_dir/state/last-clean-completion" \
    CONMON_MIN_FREE_KB=5242880 \
    CONMON_APT_PREFLIGHT_TIMEOUT=10s \
    FAKE_CALLS="$case_dir/calls.log" \
    FAKE_HOST="$host" \
    FAKE_SCENARIO="$scenario" \
    FAKE_STATE="$case_dir/state" \
    bash "$RUNNER" "$@"
}

new_case() {
  local name=$1
  CASE_DIR="$TEST_ROOT/$name"
  mkdir -p "$CASE_DIR/state"
  : >"$CASE_DIR/calls.log"
  TOTAL=$((TOTAL + 1))
}

pass_case() {
  local name=$1
  PASSED=$((PASSED + 1))
  printf 'ok %02d - %s\n' "$PASSED" "$name"
}

expect_success() {
  local name=$1
  local host=$2

  new_case "$name"
  run_sweep "$CASE_DIR" "$host" success --expected-host "$host" || \
    fail "$name returned nonzero"
  [[ -f "$CASE_DIR/state/last-clean-completion" ]] || \
    fail "$name did not publish a heartbeat"
  assert_file_contains "$CASE_DIR/state/last-clean-completion" '^[0-9]+$'
  assert_file_contains "$CASE_DIR/sweep.log" 'host health gate PASS'
  assert_file_contains "$CASE_DIR/sweep.log" 'conmon-apt-sweep END'
  pass_case "$name"
}

expect_failure_without_heartbeat() {
  local name=$1
  local host=$2
  local scenario=$3
  shift 3
  local rc

  new_case "$name"
  set +e
  run_sweep "$CASE_DIR" "$host" "$scenario" --expected-host "$host" "$@"
  rc=$?
  set -e
  ((rc != 0)) || fail "$name unexpectedly succeeded"
  [[ ! -e "$CASE_DIR/state/last-clean-completion" ]] || \
    fail "$name published a false-green heartbeat"
  assert_file_contains "$CASE_DIR/sweep.log" 'conmon-apt-sweep FAILED'
  assert_file_not_contains "$CASE_DIR/sweep.log" 'conmon-apt-sweep END'
  pass_case "$name"
}

expect_success haccp-success haccp
assert_file_contains "$CASE_DIR/calls.log" 'docker\|exec elk-es01-1'
assert_file_contains "$CASE_DIR/calls.log" 'systemctl\|is-active --quiet arkimecapture'
assert_file_not_contains "$CASE_DIR/calls.log" ':5002/health'

expect_success brisket-success brisket
assert_file_contains "$CASE_DIR/calls.log" ':5002/health'
assert_file_contains "$CASE_DIR/calls.log" '9090/api/v1/query'
assert_file_not_contains "$CASE_DIR/calls.log" 'arkimecapture'

expect_failure_without_heartbeat missing-required-hold haccp missing-hold
assert_file_not_contains "$CASE_DIR/calls.log" 'apt-get\|.*update'

expect_failure_without_heartbeat protected-runtime-in-plan haccp runtime-plan
[[ ! -e "$CASE_DIR/state/upgraded" ]] || \
  fail 'protected-runtime-in-plan reached the live upgrade'

expect_failure_without_heartbeat removal-in-plan haccp removal-plan
expect_failure_without_heartbeat low-disk haccp low-disk
expect_failure_without_heartbeat apt-update-failure haccp update-fails
expect_failure_without_heartbeat apt-upgrade-failure haccp upgrade-fails
expect_failure_without_heartbeat runtime-version-change haccp runtime-version-changed
expect_failure_without_heartbeat runtime-daemon-restart haccp runtime-restart
expect_failure_without_heartbeat haccp-arkime-gate haccp haccp-arkime-fails
expect_failure_without_heartbeat haccp-container-gate haccp haccp-container-fails
expect_failure_without_heartbeat haccp-elasticsearch-gate haccp haccp-es-red
expect_failure_without_heartbeat brisket-endpoint-gate brisket brisket-endpoint-fails
expect_failure_without_heartbeat brisket-probe-gate brisket brisket-probe-fails
expect_failure_without_heartbeat post-upgrade-health-gate brisket post-health-fails

new_case stale-heartbeat-preserved
printf '12345\n' >"$CASE_DIR/state/last-clean-completion"
set +e
run_sweep "$CASE_DIR" haccp update-fails --expected-host haccp
rc=$?
set -e
((rc != 0)) || fail 'stale-heartbeat-preserved unexpectedly succeeded'
[[ $(<"$CASE_DIR/state/last-clean-completion") == 12345 ]] || \
  fail 'failed run overwrote the prior heartbeat'
pass_case stale-heartbeat-preserved

new_case preflight-no-heartbeat
run_sweep "$CASE_DIR" haccp success --expected-host haccp --preflight-only || \
  fail 'preflight-no-heartbeat returned nonzero'
[[ ! -e "$CASE_DIR/state/last-clean-completion" ]] || \
  fail 'preflight-only run published a heartbeat'
assert_file_contains "$CASE_DIR/sweep.log" 'PREFLIGHT PASS'
assert_file_not_contains "$CASE_DIR/calls.log" 'apt-get\|.*update'
[[ ! -e "$CASE_DIR/state/upgraded" ]] || fail 'preflight-only run upgraded packages'
pass_case preflight-no-heartbeat

new_case wrong-host-profile
set +e
run_sweep "$CASE_DIR" haccp success --expected-host brisket
rc=$?
set -e
((rc != 0)) || fail 'wrong-host-profile unexpectedly succeeded'
[[ ! -e "$CASE_DIR/state/last-clean-completion" ]] || \
  fail 'wrong-host-profile published a heartbeat'
assert_file_not_contains "$CASE_DIR/calls.log" 'apt-get\|'
pass_case wrong-host-profile

new_case unsupported-host
set +e
run_sweep "$CASE_DIR" dojo success
rc=$?
set -e
((rc != 0)) || fail 'unsupported-host unexpectedly succeeded'
[[ ! -e "$CASE_DIR/state/last-clean-completion" ]] || \
  fail 'unsupported-host published a heartbeat'
assert_file_not_contains "$CASE_DIR/calls.log" 'apt-get\|'
pass_case unsupported-host

new_case lock-contention
exec 8>"$CASE_DIR/sweep.lock"
flock -n 8 || fail 'test could not acquire contention lock'
set +e
run_sweep "$CASE_DIR" haccp success --expected-host haccp
rc=$?
set -e
exec 8>&-
((rc != 0)) || fail 'lock-contention unexpectedly succeeded'
[[ ! -e "$CASE_DIR/state/last-clean-completion" ]] || \
  fail 'lock-contention published a heartbeat'
assert_file_contains "$CASE_DIR/sweep.log" 'another sweep already holds'
assert_file_not_contains "$CASE_DIR/calls.log" 'apt-get\|'
pass_case lock-contention

printf '%s/%s conmon apt sweep regression cases passed\n' "$PASSED" "$TOTAL"
((PASSED == TOTAL)) || fail "only $PASSED of $TOTAL cases passed"
