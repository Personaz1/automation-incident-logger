# automation-incident-logger

[![CI](https://img.shields.io/github/actions/workflow/status/Personaz1/automation-incident-logger/tests.yml?branch=master)](https://github.com/Personaz1/automation-incident-logger/actions)
[![Release](https://img.shields.io/github/v/release/Personaz1/automation-incident-logger)](https://github.com/Personaz1/automation-incident-logger/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## Summary

Incident lifecycle and reporting scaffold for AI/automation reliability workflows.

## Features

- Installable CLI: `ailogger`
- Incident lifecycle (`create`, `close`, `reopen`, `list`)
- Weekly markdown summary generation
- Automated tests + CI
- End-to-end demo artifacts

## Install

```bash
pip install -e .
```

## Test

```bash
pytest -q
```

## Demo

```bash
bash demo/run_demo.sh
```

## AI Evaluation Signals

- Structured incident records and deterministic summary output
- CLI lifecycle coverage and testability
- Reproducible demo outputs

## Project status

See [PROJECT_STATUS.md](./PROJECT_STATUS.md).

## Roadmap

See [ROADMAP.md](./ROADMAP.md).

## Contributing

See [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md).

## License

MIT
