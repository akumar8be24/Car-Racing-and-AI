from veritaspen_quantum.config import QuantumSettings
from veritaspen_quantum.models import RaceState, StrategyCandidate
from veritaspen_quantum.service import QuantumStrategyService


def candidate(
    strategy_id: str,
    expected_position: int,
    time_delta: float,
    traffic: float,
    tyre_risk: float,
    confidence: float,
) -> StrategyCandidate:
    return StrategyCandidate(
        strategy_id=strategy_id,
        pit_laps=[30],
        tyre_plan=["medium", "hard"],
        expected_finish_position=expected_position,
        race_time_delta_seconds=time_delta,
        traffic_loss_seconds=traffic,
        tyre_risk=tyre_risk,
        safety_car_upside_seconds=0.0,
        confidence=confidence,
    )


def test_optimizer_ranks_lowest_cost_first():
    service = QuantumStrategyService(QuantumSettings(backend="classical"))
    race_state = RaceState(
        race_id="test-gp",
        driver="VER",
        lap=25,
        weather="dry",
        candidates=[
            candidate("risky-two-stop", 2, 2.0, 3.0, 0.6, 0.5),
            candidate("balanced-one-stop", 1, 0.2, 1.0, 0.1, 0.9),
        ],
    )

    result = service.optimize_sandbox(race_state)

    assert result.rankings[0].candidate.strategy_id == "balanced-one-stop"
    assert result.rankings[0].rank == 1
    assert result.audit["status"] == "ok"


def test_service_limits_candidate_count():
    service = QuantumStrategyService(QuantumSettings(backend="classical", max_candidates=1))
    race_state = RaceState(
        race_id="test-gp",
        driver="LEC",
        lap=12,
        weather="wet",
        candidates=[
            candidate("kept", 1, 0.0, 1.0, 0.1, 0.9),
            candidate("trimmed", 1, -10.0, 0.0, 0.0, 1.0),
        ],
    )

    result = service.optimize_sandbox(race_state)

    assert [ranking.candidate.strategy_id for ranking in result.rankings] == ["kept"]


def test_replay_analysis_adds_audit_context():
    service = QuantumStrategyService(QuantumSettings(backend="classical"))
    race_state = RaceState(
        race_id="2023-monaco-gp",
        driver="VER",
        lap=28,
        weather="dry",
        candidates=[candidate("pit-five-laps-earlier", 1, -1.0, 2.0, 0.2, 0.7)],
    )

    result = service.analyze_replay(race_state, "Verstappen pits five laps earlier")

    assert result.audit["workflow"] == "replay-analysis"
    assert result.audit["scenario_label"] == "Verstappen pits five laps earlier"

