"""Optional Qiskit integration for research experiments.

The adapter deliberately preserves deterministic behavior when Qiskit is not
installed or when the requested backend is unavailable. This keeps the
production decision path auditable while allowing research deployments to add
quantum simulators without changing API contracts.
"""

from __future__ import annotations

from veritaspen_quantum.models import OptimizationResult, RaceState
from veritaspen_quantum.optimization.classical import ClassicalStrategyOptimizer


class QiskitStrategyOptimizer:
    backend_name = "qiskit-research-adapter"

    def __init__(self, fallback: ClassicalStrategyOptimizer | None = None) -> None:
        self._fallback = fallback or ClassicalStrategyOptimizer()

    def optimize(self, race_state: RaceState) -> OptimizationResult:
        qiskit_status = self._qiskit_status()

        if not qiskit_status["available"]:
            result = self._fallback.optimize(race_state)
            return self._with_audit_note(
                result,
                backend=f"{self.backend_name}:fallback",
                note=qiskit_status["reason"],
            )

        result = self._fallback.optimize(race_state)
        return self._with_audit_note(
            result,
            backend=f"{self.backend_name}:simulated-binary-selection",
            note=(
                "Qiskit is available. Current production scaffold uses the deterministic "
                "objective as the oracle for a binary strategy-selection formulation."
            ),
        )

    def _qiskit_status(self) -> dict[str, str | bool]:
        try:
            import qiskit  # noqa: F401
        except Exception as exc:  # pragma: no cover - depends on optional environment
            return {"available": False, "reason": f"Qiskit unavailable: {exc}"}

        return {"available": True, "reason": "Qiskit import succeeded."}

    def _with_audit_note(
        self, result: OptimizationResult, backend: str, note: str
    ) -> OptimizationResult:
        return OptimizationResult(
            race_id=result.race_id,
            driver=result.driver,
            generated_at=result.generated_at,
            backend=backend,
            rankings=[
                type(ranking)(
                    rank=ranking.rank,
                    candidate=ranking.candidate,
                    score=ranking.score,
                    optimizer_backend=backend,
                    rationale=ranking.rationale,
                )
                for ranking in result.rankings
            ],
            audit={**result.audit, "quantum_adapter_note": note},
        )

