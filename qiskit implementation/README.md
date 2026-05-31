# VeritasPen Quantum Intelligence Layer

This folder contains a production-ready scaffold for the VeritasPen Quantum Strategy Research Layer. It exposes a FastAPI service and a reusable Python package for quantum-inspired Formula 1 race strategy optimization.

The deterministic strategy scorer remains the default execution path. Qiskit support is optional and isolated behind an adapter so production systems keep working even when quantum dependencies or IBM Quantum credentials are unavailable.

## Features

- Quantum Strategy Sandbox for comparing alternate pit and stint plans.
- Replay analysis primitives for historical what-if strategy studies.
- Hybrid classical-quantum architecture with auditable ranking output.
- Optional Qiskit adapter with deterministic fallback behavior.
- Explainable strategy scoring suitable for downstream IBM Granite summaries.
- FastAPI endpoints for health checks, sandbox optimization, and replay analysis.

## Project Layout

```text
src/veritaspen_quantum/
  api.py                       FastAPI application and HTTP schemas
  config.py                    Runtime settings
  models.py                    Core strategy/replay dataclasses
  service.py                   Use-case orchestration
  optimization/
    classical.py               Deterministic objective scoring
    qiskit_adapter.py          Optional Qiskit-backed optimizer adapter
tests/
  test_optimizer.py            Core behavior tests
examples/
  sandbox_request.json         Example API payload
```

## Local Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn veritaspen_quantum.api:app --reload
```

Open `http://127.0.0.1:8000/docs`.

To enable the optional Qiskit stack:

```bash
pip install -e ".[quantum,dev]"
```

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/v1/quantum/sandbox/optimize ^
  -H "Content-Type: application/json" ^
  --data @examples/sandbox_request.json
```

## Production Notes

- Keep deterministic scoring enabled for auditability and failover.
- Treat Qiskit results as research augmentation until validated against race replays.
- Persist every input, score component, selected backend, and optimizer version in the audit store.
- Use IBM Quantum Runtime credentials only through environment-managed secrets.

