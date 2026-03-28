#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/data"
mkdir -p "$LOG_DIR"

python3 "$ROOT_DIR/scripts/sync_uninsubria_notebooklm.py" "$@" >> "$LOG_DIR/uninsubria_notebooklm_sync.log" 2>&1
