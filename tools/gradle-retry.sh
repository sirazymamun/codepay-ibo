#!/usr/bin/env bash
set -euo pipefail
log=$(mktemp)
trap 'rm -f "$log"' EXIT
for attempt in 1 2 3 4 5; do
  if ./gradlew "$@" 2>&1 | tee "$log"; then exit 0; else status=${PIPESTATUS[0]}; fi
  if [[ "$status" == 0 ]]; then exit 1; fi
  if [[ "$attempt" == 5 ]] || ! grep -Eiq 'status code 429|HTTP[^[:alnum:]]*429|Too Many Requests' "$log"; then exit "$status"; fi
  delay=$((60 * (2 ** (attempt - 1))))
  echo "Maven rate limit: retry $((attempt+1))/5 in ${delay}s"
  sleep "$delay"
done
