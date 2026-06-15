#!/usr/bin/env bash
set -euo pipefail

systemctl --user status duck-gtex.service --no-pager
