# Automation Incident Logger

A practical incident logging toolkit for AI automations and agent workflows.

## Why
Automation failures are common, but teams rarely track root causes consistently.

## What this project provides
- Structured incident templates
- Retry/runbook notes
- Postmortem checklist
- Severity + impact tagging

## Planned MVP
- Markdown/JSON incident schema
- CLI to create/search incidents
- Weekly incident summary generator
- Postmortem template pack

## Use cases
- solo operators managing many automations
- small teams needing incident discipline
- AI workflows with unstable external APIs

## Status
Scaffold released. Open for contributors.



## Working scaffold CLI
```bash
python3 src/ailog.py create --title "Webhook timeout" --severity high --summary "Provider timed out"
python3 src/ailog.py list
python3 src/ailog.py summary
```


## Filters, status changes, and markdown weekly summary
```bash
python3 src/ailog.py list --severity high --status open
python3 src/ailog.py close --id inc-123
python3 src/ailog.py reopen --id inc-123
python3 src/ailog.py summary --out weekly-summary.md
```


## Install
```bash
pip install -e .
ailogger summary --out weekly-summary.md
```

## Tests
```bash
python3 -m pytest -q
```


## End-to-end demo
```bash
bash demo/run_demo.sh
```
See generated artifacts in `demo/`.
