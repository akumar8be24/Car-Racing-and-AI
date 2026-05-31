"""Application service for sandbox and replay optimization workflows."""

from __future__ import annotations

from veritaspen_quantum.config import QuantumSettings
from veritaspen_quantum.models import OptimizationResult, RaceState
from veritaspen_quantum.optimization.classical import ClassicalStrategyOptimizer
from veritaspen_quantum.optimization.qiskit_adapter import QiskitStrategyOptimizer


class QuantumStrategyService:
    def __init__(self, settings: QuantumSettings | None = None) -> None:
        self.settings = settings or QuantumSettings.from_env()
        self._classical = ClassicalStrategyOptimizer()
        self._qiskit = QiskitStrategyOptimizer(fallback=self._classical)

    def optimize_sandbox(self, race_state: RaceState) -> OptimizationResult:
        bounded_state = self._limit_candidates(race_state)
        if self.settings.backend.lower() in {"qiskit", "quantum", "aer"}:
            return self._qiskit.optimize(bounded_state)
        return self._classical.optimize(bounded_state)

    def analyze_replay(self, race_state: RaceState, scenario_label: str) -> OptimizationResult:
        result = self.optimize_sandbox(race_state)
        return OptimizationResult(
            race_id=result.race_id,
            driver=result.driver,
            generated_at=result.generated_at,
            backend=result.backend,
            rankings=result.rankings,
            audit={**result.audit, "scenario_label": scenario_label, "workflow": "replay-analysis"},
        )

    def _limit_candidates(self, race_state: RaceState) -> RaceState:
        if len(race_state.candidates) <= self.settings.max_candidates:
            return race_state

        return RaceState(
            race_id=race_state.race_id,
            driver=race_state.driver,
            lap=race_state.lap,
            weather=race_state.weather,
            telemetry_snapshot_id=race_state.telemetry_snapshot_id,
            candidates=race_state.candidates[: self.settings.max_candidates],
        )

