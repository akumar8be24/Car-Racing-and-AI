"""Runtime configuration for the quantum strategy layer."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class QuantumSettings:
    environment: str = "local"
    backend: str = "classical"
    max_candidates: int = 64
    ibm_quantum_instance: str | None = None

    @classmethod
    def from_env(cls) -> "QuantumSettings":
        max_candidates = int(os.getenv("QUANTUM_MAX_CANDIDATES", "64"))
        return cls(
            environment=os.getenv("VERITASPEN_ENV", "local"),
            backend=os.getenv("QUANTUM_BACKEND", "classical"),
            max_candidates=max_candidates,
            ibm_quantum_instance=os.getenv("IBM_QUANTUM_INSTANCE") or None,
        )

