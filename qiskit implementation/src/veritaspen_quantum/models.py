"""Domain models shared by API and optimization code."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class StrategyCandidate:
    strategy_id: str
    pit_laps: list[int]
    tyre_plan: list[str]
    expected_finish_position: int
    race_time_delta_seconds: float
    traffic_loss_seconds: float
    tyre_risk: float
    safety_car_upside_seconds: float
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RaceState:
    race_id: str
    driver: str
    lap: int
    weather: str
    candidates: list[StrategyCandidate]
    telemetry_snapshot_id: str | None = None


@dataclass(frozen=True)
class ScoreBreakdown:
    position_cost: float
    time_cost: float
    traffic_cost: float
    tyre_risk_cost: float
    safety_car_credit: float
    confidence_credit: float

    @property
    def total_cost(self) -> float:
        return (
            self.position_cost
            + self.time_cost
            + self.traffic_cost
            + self.tyre_risk_cost
            - self.safety_car_credit
            - self.confidence_credit
        )


@dataclass(frozen=True)
class StrategyRanking:
    rank: int
    candidate: StrategyCandidate
    score: ScoreBreakdown
    optimizer_backend: str
    rationale: str


@dataclass(frozen=True)
class OptimizationResult:
    race_id: str
    driver: str
    generated_at: datetime
    backend: str
    rankings: list[StrategyRanking]
    audit: dict[str, Any]

    @classmethod
    def empty(cls, race_state: RaceState, backend: str, reason: str) -> "OptimizationResult":
        return cls(
            race_id=race_state.race_id,
            driver=race_state.driver,
            generated_at=datetime.now(UTC),
            backend=backend,
            rankings=[],
            audit={"status": "empty", "reason": reason},
        )

