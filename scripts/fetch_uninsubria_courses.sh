#!/usr/bin/env bash
set -euo pipefail

# You can override these via environment variables if needed.
API_URL="${API_URL:-https://elearning.uninsubria.it/lib/ajax/service.php?sesskey=NcErR8AioT&info=core_course_get_enrolled_courses_by_timeline_classification}"
COOKIE_HEADER="${COOKIE_HEADER:-_shibsession_656c6561726e696e672e756e696e7375627269612e697468747470733a2f2f73702d656c6561726e696e672d756e696e7375627269612d70726f642e63696e6563612e69742f73686962626f6c657468=_c60e10d3e594c4bae5c9efedbe81d37d; MoodleSessioninsubriaprod=r4thbvfikpakfcpq2rl893ajd8}"
if [[ -z "${PAYLOAD:-}" ]]; then
  PAYLOAD='[{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":0,"classification":"all","sort":"fullname"}}]'
fi
ORIGIN_HEADER="${ORIGIN_HEADER:-https://elearning.uninsubria.it}"
REFERER_HEADER="${REFERER_HEADER:-https://elearning.uninsubria.it/my/}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${OUT_DIR:-$ROOT_DIR/data}"
mkdir -p "$OUT_DIR"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="${OUT_FILE:-$OUT_DIR/uninsubria_courses_${STAMP}.json}"
LAST_FILE="$OUT_DIR/uninsubria_courses_latest.json"

TMP_FILE="$(mktemp)"
HTTP_CODE="$(
  curl -sS \
    -X POST "$API_URL" \
    -H "Cookie: $COOKIE_HEADER" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Origin: $ORIGIN_HEADER" \
    -H "Referer: $REFERER_HEADER" \
    --data "$PAYLOAD" \
    -o "$TMP_FILE" \
    -w "%{http_code}"
)"

mv "$TMP_FILE" "$OUT_FILE"
cp "$OUT_FILE" "$LAST_FILE"

echo "timestamp: $(date -Iseconds)"
echo "http_code: $HTTP_CODE"
echo "saved_to: $OUT_FILE"
echo "latest: $LAST_FILE"
echo "response:"
cat "$OUT_FILE"
echo
