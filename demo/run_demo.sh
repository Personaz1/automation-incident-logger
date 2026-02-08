#!/usr/bin/env bash
set -euo pipefail

rm -f data/incidents.jsonl
python3 -m ailogger.cli create --title "Webhook timeout" --severity high --summary "Provider timed out"
python3 -m ailogger.cli create --title "Parser warning" --severity low --summary "Non-blocking parse issue"

FIRST_ID=$(python3 - <<'PY'
import json, pathlib
p=pathlib.Path('data/incidents.jsonl')
print(json.loads(p.read_text().splitlines()[0])['id'])
PY
)

python3 -m ailogger.cli close --id "$FIRST_ID"
python3 -m ailogger.cli list > demo/list.txt
python3 -m ailogger.cli summary --out demo/weekly-summary.md

echo "Demo artifacts generated in demo/"
