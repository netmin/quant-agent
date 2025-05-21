# Quant Agent Platform

***Multi‑agent AI sandbox for generating and back‑testing trading strategies***

![CI](https://img.shields.io/github/actions/workflow/status/your‑org/quant‑agent‑platform/ci.yml?branch=main)
![License](https://img.shields.io/github/license/your‑org/quant‑agent‑platform)

> **Status – Sprint 0 (bootstrapping)**

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture Snapshot](#architecture-snapshot)
4. [Quick Start](#quick-start)
5. [Directory Layout](#directory-layout)
6. [Configuration](#configuration)
7. [Development Workflow](#development-workflow)
8. [Code Style & Tooling](#code-style--tooling)
9. [Contributing Guide](#contributing-guide)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)

---

## Overview

Quant Agent Platform (QAP) is an open‑source project that aims to evolve from a personal research sandbox into a SaaS platform for automated **idea generation, back‑testing, and evaluation** of algorithmic trading strategies.

*Current MVP goal*: collect market data & news, run simple strategies inside a resource‑limited sandbox, and output performance reports — all from a single `docker compose up`.

## Features

| Sprint | Focus                                          | Delivered artefacts                      |
| ------ | ---------------------------------------------- | ---------------------------------------- |
| **0**  | Dev environment bootstrap                      | Docker Compose stack, CI, sandbox limits |
| 1      | ETL for Binance prices & news                  | Parquet datasets, incremental loader     |
| 2      | Multi‑agent workflow (Planner, DataCurator, …) | AutoGen logs, test hypotheses            |
| ⋯      | ⋯                                              | ⋯                                        |

## Architecture Snapshot

```
┌──────────────┐        Parquet      ┌──────────────┐
│  Binance API │──►┐  + DuckDB  ┌──►│  Python app  │◄─┐
└──────────────┘  │             │   └──────────────┘  │ REST/gRPC
                  │             │                     │
┌──────────────┐  │   price DB  │   ┌──────────────┐  │  vector search
│ News sources │──┤             ├──►│   Qdrant DB  │◄─┘
└──────────────┘  └──────────────┘   └──────────────┘
```

*Embedded DuckDB* handles analytical SQL over Parquet; *Qdrant* stores news embeddings for sentiment signals.

## Quick Start

### Prerequisites

* Docker 24+ and Docker Compose plugin.
* Linux/macOS/WSL2 (x86‑64).

```bash
# 1. Clone the repo
$ git clone https://github.com/your‑org/quant‑agent‑platform.git
$ cd quant‑agent‑platform

# 2. Fill environment variables
$ cp .env.example .env && $EDITOR .env

# 3. Build & run
$ docker compose -f docker/docker-compose.dev.yml up --build
```

After start‑up:

* `app` container opens a Python REPL (`docker compose exec app python`) where `duckdb.connect()` works.
* Qdrant is reachable at `http://localhost:6333`.

## Directory Layout

```
app/            # application source code
configs/        # config.yml + Pydantic schema
scripts/        # utility scripts (ETL, tests)
notebooks/      # research notebooks (ignored in CI)
 docker/
     Dockerfile
     docker-compose.dev.yml
 tests/
 data/          # mounted volume, excluded from Git
```

## Configuration

`configs/config.yml` (validated by `config.schema.yaml`):

```yaml
sandbox:
  cpu_limit: 1          # cores
  memory_limit_mb: 2048
  disk_limit_mb: 50
  network: false
metrics:
  sharpe_min: 1.5
  sortino_min: 2.0
  calmar_min: 0.5
  psr_min: 0.55
```

Adjust limits to fit your hardware.

## Development Workflow

1. **Fork → branch → PR** model. Create a feature branch from `main`.
2. Activate pre‑commit hooks: `pre-commit install`. They run Black, isort, flake8, detect‑secrets.
3. Run tests: `pytest`.
4. Build & run containers locally (`docker compose …`).
5. Push and open a Pull Request; CI must be green.
6. At least one review approval is required before merge.

## Code Style & Tooling

| Tool                     | Purpose                                    |
| ------------------------ | ------------------------------------------ |
| **Black**                | code formatter                             |
| **isort**                | import ordering                            |
| **flake8**               | static analysis                            |
| **pytest**               | testing                                    |
| **pre‑commit**           | unified git hooks                          |
| **Conventional Commits** | commit message style (`feat: …`, `fix: …`) |

> *No OOP is enforced; prefer functional style. Keep code clear and readable (Kent Beck “Tidy First?”).* 

## Contributing Guide

We welcome pull requests! To contribute:

1. **Open an issue** to discuss your idea if it is non‑trivial.
2. Follow the [Development Workflow](#development-workflow).
3. Keep PRs focused and under 300 lines where possible.
4. Add or update tests for any new functionality.
5. Docs matter — update README or docstrings as needed.
6. By submitting code you agree to license it under the MIT License.

For large changes (architecture, dependencies) please open a **design discussion** issue first.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

* [DuckDB](https://duckdb.org/)
* [Qdrant](https://qdrant.tech/)
* [Polars](https://www.pola.rs/)

---

*Happy hacking!*

