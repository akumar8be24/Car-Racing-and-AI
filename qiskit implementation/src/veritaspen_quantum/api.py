"""HTTP API for the VeritasPen quantum strategy layer."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from veritaspen_quantum.config import QuantumSettings
from veritaspen_quantum.models import RaceState, StrategyCandidate
from veritaspen_quantum.service import QuantumStrategyService

app = FastAPI(
    title="VeritasPen Quantum Intelligence Layer",
    version="0.1.0",
    description="Quantum-inspired race strategy optimization service.",
)


class StrategyCandidatePayload(BaseModel):
    strategy_id: str
    pit_laps: list[int] = Field(default_factory=list)
    tyre_plan: list[str] = Field(default_factory=list)
    expected_finish_position: int = Field(ge=1)
    race_time_delta_seconds: float
    traffic_loss_seconds: float = Field(ge=0)
    tyre_risk: float = Field(ge=0, le=1)
    safety_car_upside_seconds: float = Field(ge=0)
    confidence: float = Field(ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_domain(self) -> StrategyCandidate:
        return StrategyCandidate(**self.model_dump())


class SandboxRequest(BaseModel):
    race_id: str
    driver: str
    lap: int = Field(ge=1)
    weather: str
    telemetry_snapshot_id: str | None = None
    candidates: list[StrategyCandidatePayload]

    def to_domain(self) -> RaceState:
        return RaceState(
            race_id=self.race_id,
            driver=self.driver,
            lap=self.lap,
            weather=self.weather,
            telemetry_snapshot_id=self.telemetry_snapshot_id,
            candidates=[candidate.to_domain() for candidate in self.candidates],
        )


class ReplayRequest(SandboxRequest):
    scenario_label: str = "historical-what-if"


@app.get("/health")
def health() -> dict[str, str]:
    settings = QuantumSettings.from_env()
    return {"status": "ok", "environment": settings.environment, "backend": settings.backend}


@app.post("/v1/quantum/sandbox/optimize")
def optimize_sandbox(payload: SandboxRequest) -> dict[str, Any]:
    service = QuantumStrategyService()
    return _serialize_result(service.optimize_sandbox(payload.to_domain()))


@app.post("/v1/quantum/replay/analyze")
def analyze_replay(payload: ReplayRequest) -> dict[str, Any]:
    service = QuantumStrategyService()
    result = service.analyze_replay(payload.to_domain(), payload.scenario_label)
    return _serialize_result(result)


def _serialize_result(result) -> dict[str, Any]:
    return {
        "race_id": result.race_id,
        "driver": result.driver,
        "generated_at": result.generated_at.isoformat(),
        "backend": result.backend,
        "rankings": [
            {
                "rank": ranking.rank,
                "strategy_id": ranking.candidate.strategy_id,
                "pit_laps": ranking.candidate.pit_laps,
                "tyre_plan": ranking.candidate.tyre_plan,
                "total_cost": round(ranking.score.total_cost, 4),
                "score": {
                    "position_cost": ranking.score.position_cost,
                    "time_cost": ranking.score.time_cost,
                    "traffic_cost": ranking.score.traffic_cost,
                    "tyre_risk_cost": ranking.score.tyre_risk_cost,
                    "safety_car_credit": ranking.score.safety_car_credit,
                    "confidence_credit": ranking.score.confidence_credit,
                },
                "rationale": ranking.rationale,
            }
            for ranking in result.rankings
        ],
        "audit": result.audit,
    }

