#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/data"
mkdir -p "$LOG_DIR"

python3 "$ROOT_DIR/scripts/sync_uninsubria_notebooklm.py" "$@" >> "$LOG_DIR/uninsubria_notebooklm_sync.log" 2>&1

# Auto-publish generated study materials to GitHub (can be disabled with AUTO_GIT_PUSH=0)
if [[ "${AUTO_GIT_PUSH:-1}" == "1" ]]; then
  (
    cd "$ROOT_DIR"
    git add materiali_studio_notebooklm/courses scripts/sync_uninsubria_notebooklm.py || true
    if ! git diff --cached --quiet; then
      git commit -m "Auto-update generated study materials ($(date '+%Y-%m-%d %H:%M:%S'))" >> "$LOG_DIR/uninsubria_notebooklm_sync.log" 2>&1 || true
      git push origin main >> "$LOG_DIR/uninsubria_notebooklm_sync.log" 2>&1 || true
    fi
  )
fi
