#!/usr/bin/env bash
set -euo pipefail

systemctl --user restart duck-gtex.service
systemctl --user status duck-gtex.service --no-pager
