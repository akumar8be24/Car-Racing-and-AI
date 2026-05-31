"""Deterministic strategy scoring used for auditability and fallback."""

from __future__ import annotations

from datetime import UTC, datetime

from veritaspen_quantum.models import (
    OptimizationResult,
    RaceState,
    ScoreBreakdown,
    StrategyCandidate,
    StrategyRanking,
)


class ClassicalStrategyOptimizer:
    """Ranks strategy candidates with an explainable weighted objective."""

    backend_name = "classical-weighted-objective"

    def score(self, candidate: StrategyCandidate) -> ScoreBreakdown:
        return ScoreBreakdown(
            position_cost=max(candidate.expected_finish_position - 1, 0) * 8.0,
            time_cost=candidate.race_time_delta_seconds * 1.15,
            traffic_cost=max(candidate.traffic_loss_seconds, 0) * 0.9,
            tyre_risk_cost=min(max(candidate.tyre_risk, 0), 1) * 12.0,
            safety_car_credit=max(candidate.safety_car_upside_seconds, 0) * 0.75,
            confidence_credit=min(max(candidate.confidence, 0), 1) * 4.0,
        )

    def optimize(self, race_state: RaceState) -> OptimizationResult:
        if not race_state.candidates:
            return OptimizationResult.empty(race_state, self.backend_name, "No strategy candidates supplied.")

        ranked = sorted(
            ((candidate, self.score(candidate)) for candidate in race_state.candidates),
            key=lambda item: item[1].total_cost,
        )

        rankings = [
            StrategyRanking(
                rank=index,
                candidate=candidate,
                score=score,
                optimizer_backend=self.backend_name,
                rationale=self._rationale(candidate, score),
            )
            for index, (candidate, score) in enumerate(ranked, start=1)
        ]

        return OptimizationResult(
            race_id=race_state.race_id,
            driver=race_state.driver,
            generated_at=datetime.now(UTC),
            backend=self.backend_name,
            rankings=rankings,
            audit={
                "status": "ok",
                "candidate_count": len(race_state.candidates),
                "objective": "minimize finishing position, time loss, traffic, and tyre risk while crediting safety-car upside and confidence",
            },
        )

    def _rationale(self, candidate: StrategyCandidate, score: ScoreBreakdown) -> str:
        return (
            f"{candidate.strategy_id} cost={score.total_cost:.2f}; "
            f"position P{candidate.expected_finish_position}, "
            f"time delta {candidate.race_time_delta_seconds:+.1f}s, "
            f"traffic {candidate.traffic_loss_seconds:.1f}s, "
            f"tyre risk {candidate.tyre_risk:.2f}, "
            f"confidence {candidate.confidence:.2f}."
        )

