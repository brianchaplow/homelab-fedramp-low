#!/bin/bash
# Weekly ConMon apt sweep for in-boundary Ubuntu hosts.
#
# Picks up Canonical noble-security + noble-updates patches as they ship
# so the FedRAMP Low POA&M residual decays organically between manual
# ConMon cycles. Does NOT touch held packages (docker-ce, containerd.io,
# docker-ce-cli) -- those are handled out-of-band on a slower cadence.
#
# Deployed to: /usr/local/sbin/conmon-apt-sweep.sh on brisket, haccp,
# dojo VM, regscale VM (the four in-boundary Ubuntu hosts).
# Triggered by: /etc/cron.d/conmon-apt-sweep -- Sunday 04:00 host-local.
# Logs to:      /var/log/conmon-apt-sweep.log (logrotate handles size).
#
# Wrapper-script pattern (not inline cron chain) per
# memory/feedback_cron_chain_log_swallow.md -- a chain like
# "cd && source && cmd >> log" silently swallows output when any
# preceding step fails. Doing the redirect on the wrapper invocation
# inside cron captures every line including unexpected stderr.

set -u

LOG=/var/log/conmon-apt-sweep.log
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HOST=$(hostname)

{
  echo
  echo "=== $TS conmon-apt-sweep BEGIN on $HOST ==="

  echo "--- apt-get update ---"
  apt-get update -qq

  echo "--- upgradable BEFORE ---"
  apt list --upgradable 2>/dev/null | tail -n +2 || true

  echo "--- apt-get upgrade ---"
  DEBIAN_FRONTEND=noninteractive apt-get -y \
    -o Dpkg::Options::=--force-confold \
    -o Dpkg::Options::=--force-confdef \
    upgrade

  echo "--- upgradable AFTER ---"
  apt list --upgradable 2>/dev/null | tail -n +2 || true

  echo "--- restart wazuh-agent ---"
  systemctl restart wazuh-agent || echo "WARN: wazuh-agent restart failed"

  echo "=== $TS conmon-apt-sweep END on $HOST ==="
} >> "$LOG" 2>&1
