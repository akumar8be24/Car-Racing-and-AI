# Veritasppen

Veritasppen is an AI-assisted race strategy and telemetry platform for motorsport
teams, drivers, engineers, and fans. It combines historical Formula 1 session
replay, real-time WebSocket telemetry, explainable strategy scoring, IBM
Granite narration, post-race debrief analysis, and role-specific dashboards in
one application.

The repository is intentionally structured as a single deployable product:

- `backend/` contains the FastAPI API, strategy engine, AI integrations,
  persistence services, and the integrated historical replay utility.
- `frontend/` contains the React and TypeScript application.
- `scripts/` contains local and cloud deployment helpers.
- `replay-data-examples/` contains example replay payloads.
- `examples/driver-telemetry-trace/` contains a WebSocket telemetry subscriber.

## The Racing Problem

Race strategy decisions are made under time pressure. Teams must interpret tyre
degradation, pace loss, traffic gaps, weather, safety-car risk, and pit-window
timing while the race state is continuously changing. The raw data is valuable,
but it can be difficult to convert into a clear, auditable recommendation fast
enough to influence a decision.

Fans face a related problem: the decisive strategic story is often hidden
behind timing screens and commentary shorthand. A pit stop may look arbitrary
unless the viewer can see the evidence, alternatives, and confidence behind
the call.

Veritasppen addresses both needs:

- Engineers receive structured telemetry analysis, strategy scores, evidence,
  assumptions, and an auditable explanation.
- Strategists can compare scenarios and commit decisions to an audit log.
- Fans receive accessible race context and commentary-oriented views.
- Developers can replay historical sessions as realistic live feeds without
  waiting for a live race weekend.

## Technical Execution

### IBM AI Integration

Veritasppen uses IBM Granite through watsonx.ai as an explanation layer on top of a
deterministic strategy engine. The model is not asked to invent the numerical
strategy calculation. Instead, the backend computes the race recommendation
first and supplies Granite with structured context:

1. Telemetry is validated and normalized.
2. The heuristic strategy engine calculates pit urgency, safety-car
   probability, overtake risk, and a recommended pit window.
3. Optional Langflow orchestration enriches the context with external signals.
4. Granite generates a concise explanation with evidence, assumptions,
   confidence, and an alternative action.
5. The backend returns both the deterministic scores and the AI explanation.

This hybrid pattern is important for high-pressure decision support. It keeps
the recommendation traceable while using generative AI where it adds the most
value: communication, summarization, contextual reasoning, and accessibility.

Post-race analysis uses Docling-compatible document processing to extract
structured content from uploaded reports before generating a concise technical
debrief. This makes the same platform useful during a race and after the
chequered flag.

### Open-Source Technology

Veritasppen combines IBM services with open-source components:

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | React, TypeScript, Vite | Engineer, strategist, and fan interfaces |
| Backend | FastAPI, Pydantic, Uvicorn | Async APIs, validation, and streaming |
| Historical data | FastF1, pandas, NumPy | Session loading and telemetry processing |
| Replay | WebSockets | Historical session broadcast as a live-style feed |
| AI explanation | IBM Granite on watsonx.ai | Explainable race strategy narration |
| Workflow orchestration | Langflow, optional | Visual enrichment pipeline |
| Document processing | Docling | Post-race report extraction |
| Persistence | PostgreSQL, SQLAlchemy, Alembic | Audit logs and durable state |
| Cache | Redis | Strategy caching and session coordination |
| Authentication | Firebase, optional for local use | User identity and race-state sync |
| Deployment | Docker Compose, Nginx | Portable local and production deployment |

### Integrated Historical Replay

The historical replay utility is bundled in `backend/open_pit_wall/`. It can:

- Download recorded sessions through FastF1.
- Cache normalized replay files as JSON.
- Broadcast telemetry at 10 Hz.
- Replay leaderboard, weather, lap, and race-control events.
- Provide play, pause, seek, restart, loop, and speed controls.
- Publish full-field telemetry or driver-specific channels.

The API exposes replay discovery at:

```text
GET /api/v1/replay/sessions
```

Replay WebSocket clients can subscribe to:

| Channel | Description |
| --- | --- |
| `telemetry.drivers` | Full-field telemetry frames |
| `telemetry.drivers.{DRIVER_CODE}` | Telemetry for one driver |
| `leaderboard` | Derived race order and gaps |
| `telemetry.weather` | Weather snapshots |
| `telemetry.lap` | Current lap and replay elapsed time |
| `race_control` | Track status and race-control messages |

## Innovation

Veritasppen is not only a telemetry dashboard and not only an AI chat interface.
Its distinctive value is the connection between replayable race evidence,
deterministic strategy scoring, and explainable AI narration.

Key ideas:

- **Inspectable AI:** Every recommendation includes scores, reasons,
  assumptions, alternatives, and confidence decomposition.
- **Historical sessions as live simulations:** Teams and developers can test
  race workflows against recorded sessions through the same streaming model
  used for live-style operation.
- **Dual audience design:** Engineer views preserve technical detail while fan
  views translate the same race state into understandable context.
- **Auditable decisions:** Strategy calls can be persisted with execution
  checklists and telemetry snapshots.
- **Graceful degradation:** Redis, PostgreSQL, Langflow, and external AI
  services are integrated so the application can retain useful local behavior
  when optional infrastructure is unavailable.

## Challenge Fit

Veritasppen directly addresses a real racing challenge: turning dense telemetry
into a timely, explainable decision.

For teams, it reduces the cognitive load involved in evaluating pit windows,
tyre degradation, traffic risk, and changing race conditions. For drivers, it
improves the clarity of the reasoning that supports radio instructions. For
fans, it makes strategy easier to follow and turns hidden race dynamics into
an understandable narrative.

The historical replay engine also makes the project practical in a challenge
environment. A complete race weekend is not required to demonstrate the
solution. Recorded telemetry can be replayed as a realistic streaming feed,
allowing repeatable demos, testing, and strategy experiments.

## Implementation And Feasibility

The system is designed to grow beyond a prototype:

- FastAPI provides an async foundation for REST and WebSocket workloads.
- Redis supports cache-backed coordination and can be replaced by a managed
  service in production.
- PostgreSQL stores audit history and strategy commitments.
- Docker Compose provides a repeatable local environment.
- Nginx proxies browser API and WebSocket traffic through a single origin.
- The replay utility decouples product testing from live data availability.
- Environment templates contain configuration names only. Runtime values are
  supplied by each deployment owner.

The architecture can support future integrations such as live timing feeds,
weather providers, team-specific simulation models, managed observability,
and additional AI workflows without replacing the core application.

## Architecture

```mermaid
flowchart LR
    FastF1["FastF1 historical sessions"] --> Replay["Replay loader and broadcaster"]
    Replay --> WS["WebSocket telemetry channels"]
    Upload["CSV, JSON, and PDF uploads"] --> API["FastAPI backend"]
    WS --> API
    API --> Strategy["Deterministic strategy engine"]
    Strategy --> Langflow["Optional Langflow enrichment"]
    Langflow --> Granite["IBM Granite on watsonx.ai"]
    Strategy --> Granite
    Granite --> API
    API --> Redis["Redis cache"]
    API --> Postgres["PostgreSQL audit store"]
    API --> UI["React application"]
```

# Quantum Intelligence Layer (Qiskit)

VeritasPen integrates quantum-inspired optimization concepts and is architected
for future acceleration through IBM Quantum technologies using Qiskit.

Modern Formula 1 race strategy involves solving highly complex optimization
problems under strict time constraints. Engineers must continuously evaluate
thousands of possible race outcomes while balancing tyre degradation, pit-stop
timing, traffic, weather changes, safety-car probability, fuel usage, and
track position.

Many of these challenges resemble combinatorial optimization problems that
become increasingly difficult as the number of variables grows. Quantum
computing offers a promising approach for exploring these large decision spaces
more efficiently than traditional brute-force methods.

The deterministic strategy engine remains the primary decision-making
component of VeritasPen. Qiskit-based modules are designed to enhance strategy
exploration, scenario generation, and optimization while maintaining complete
auditability and explainability.

---

## Why Quantum Computing in Motorsport?

A Formula 1 race can be viewed as a real-time optimization problem where teams
must continuously answer questions such as:

- When is the optimal pit-stop window?
- Should the team attempt an undercut or overcut?
- How will traffic affect race pace?
- What is the probability of a Safety Car in the next stint?
- Which strategy provides the highest expected finishing position?
- How should weather uncertainty influence decisions?

As telemetry streams grow larger and simulations become more detailed, the
number of possible strategy combinations increases exponentially.

Quantum computing provides a pathway for:

- Faster optimization
- Larger scenario exploration
- Better uncertainty modelling
- More efficient resource allocation
- Enhanced simulation capabilities
- Future-ready race intelligence systems

---

# Current Quantum Integration

The platform includes a dedicated Quantum Strategy Research Layer powered by
Qiskit for experimentation, simulation, and optimization studies.

Historical race replays can be transformed into optimization problems and
evaluated using quantum-inspired algorithms and quantum simulators.

Current research areas include:

- Quantum-enhanced pit strategy optimization
- Traffic network analysis
- Safety-car probability modelling
- Multi-objective race strategy selection
- Quantum Monte Carlo acceleration
- Hybrid classical-quantum decision systems

---

# Implemented Quantum Features

## Quantum Strategy Sandbox

The Quantum Strategy Sandbox allows historical race sessions to be converted
into optimization problems for experimentation.

Inputs include:

- Driver telemetry
- Tyre degradation data
- Sector times
- Track position
- Weather information
- Historical pit-stop performance

These variables are transformed into optimization objectives that can be
evaluated using Qiskit simulators.

### Example Use Cases

- Compare one-stop vs two-stop strategies
- Evaluate alternate pit windows
- Analyze undercut opportunities
- Assess safety-car timing benefits

---

## Quantum Replay Analysis

Historical sessions replayed through FastF1 can be processed through quantum
optimization experiments.

This enables:

- Retrospective strategy evaluation
- Alternative race outcome exploration
- What-if simulations
- Driver-specific optimization studies

Example:

> "What would have happened if Verstappen pitted 5 laps earlier during the
> 2023 Monaco Grand Prix?"

The replay engine can generate alternate race states and evaluate strategy
quality using quantum-inspired optimization techniques.

---

## Hybrid Classical-Quantum Architecture

VeritasPen follows a hybrid architecture where quantum modules complement the
deterministic strategy engine rather than replacing it.

### Workflow

1. Telemetry is collected and normalized.
2. Classical strategy scoring is performed.
3. Optimization candidates are generated.
4. Qiskit evaluates candidate solutions.
5. Results are ranked and fused.
6. IBM Granite explains the recommendation.
7. Engineers receive an auditable recommendation.

This ensures every recommendation remains explainable and traceable.

---

# Potential Future Quantum Features

## Quantum Pit Window Optimization

### Problem

Determining the optimal pit-stop lap requires balancing:

- Tyre degradation
- Traffic congestion
- Undercut opportunities
- Safety-car probability
- Weather conditions

The search space grows rapidly throughout a race.

### Proposed Solution

Model pit-window selection as a combinatorial optimization problem and solve
using:

- QAOA (Quantum Approximate Optimization Algorithm)
- Quantum Annealing-inspired methods
- Variational Optimization approaches

### Benefits

- Faster exploration of pit scenarios
- Improved strategy ranking
- Better uncertainty handling

---

## Quantum Traffic Graph Optimization

### Problem

Traffic interactions involve dozens of interconnected variables.

Drivers may gain or lose several seconds depending on:

- DRS trains
- Dirty air
- Overtake probability
- Sector performance
- Relative tyre age

### Proposed Solution

Represent race traffic as a graph optimization problem.

Qiskit graph algorithms can help identify:

- Optimal release positions
- Clean-air opportunities
- Low-risk overtaking windows

### Benefits

- Better traffic forecasting
- Improved pit-stop timing decisions
- Reduced traffic penalties

---

## Quantum Safety Car Prediction

### Problem

Safety Cars significantly alter race outcomes.

Predicting their impact requires evaluating large numbers of race scenarios.

### Proposed Solution

Use quantum-enhanced probability estimation techniques to evaluate:

- Historical incident patterns
- Track-specific risks
- Weather effects
- Race-control events

### Benefits

- Better safety-car risk assessment
- More accurate strategy confidence scores

---

## Quantum Monte Carlo Simulation

### Problem

Race engineers often simulate thousands of possible race outcomes.

Classical Monte Carlo methods become computationally expensive as complexity
increases.

### Proposed Solution

Explore:

- Quantum Amplitude Estimation
- Quantum Monte Carlo acceleration
- Probabilistic scenario sampling

### Benefits

- Faster convergence
- Larger simulation spaces
- More accurate uncertainty estimation

---

## Quantum Strategy Portfolio Optimization

### Problem

Teams rarely evaluate a single strategy.

Instead, they maintain a portfolio of possible race plans.

Examples:

- One-stop strategy
- Two-stop strategy
- Aggressive undercut
- Defensive overcut
- Safety-car opportunistic strategy

### Proposed Solution

Use quantum optimization to rank strategy portfolios based on:

- Expected finishing position
- Risk score
- Confidence level
- Traffic impact
- Tyre wear projections

### Benefits

- Better decision quality
- Stronger contingency planning
- Improved race adaptability

---

## Quantum Machine Learning for Telemetry

### Proposed Research Area

Investigate Quantum Machine Learning (QML) techniques for:

- Tyre degradation prediction
- Driver performance modelling
- Lap-time forecasting
- Weather impact analysis
- Race-state classification

Potential technologies:

- Quantum Support Vector Machines
- Variational Quantum Classifiers
- Quantum Neural Networks

---

# IBM Quantum Ecosystem Support

VeritasPen is designed to support future integration with:

- Qiskit
- IBM Quantum Runtime
- QAOA
- Variational Quantum Eigensolver (VQE)
- Quantum Machine Learning frameworks
- Hybrid Classical-Quantum Pipelines
- IBM Quantum Simulators
- Future IBM Quantum Hardware

---

# Quantum Technology Stack

| Layer | Technology | Purpose |
|---------|------------|----------|
| Quantum SDK | Qiskit | Quantum application development |
| Optimization | QAOA | Strategy optimization |
| Simulation | Qiskit Aer | Quantum simulation |
| Runtime | IBM Quantum Runtime | Accelerated execution |
| ML Research | Qiskit Machine Learning | Telemetry prediction |
| Hybrid Processing | FastAPI + Qiskit | Classical-quantum orchestration |
| Explainability | IBM Granite | Human-readable strategy reasoning |

---

# Example Future Architecture

```mermaid
flowchart LR

    Telemetry["Race Telemetry"] --> Strategy["Deterministic Strategy Engine"]

    Strategy --> Classical["Classical Optimization"]

    Strategy --> Quantum["Qiskit Optimization Layer"]

    Quantum --> QAOA["QAOA"]
    Quantum --> Runtime["IBM Quantum Runtime"]
    Quantum --> Aer["Qiskit Aer Simulator"]

    Classical --> Fusion["Strategy Fusion Layer"]

    QAOA --> Fusion
    Runtime --> Fusion
    Aer --> Fusion

    Fusion --> Granite["IBM Granite"]

    Granite --> Dashboard["Engineer & Fan Dashboards"]

    Fusion --> Audit["Strategy Audit Store"]
```

---

# Research Vision

VeritasPen aims to combine four emerging technologies into a single
motorsport intelligence platform:

1. Real-time telemetry analytics
2. Explainable artificial intelligence
3. Historical race simulation
4. Quantum optimization research

By leveraging Qiskit and the IBM Quantum ecosystem, VeritasPen establishes a
future-ready architecture capable of exploring advanced race-strategy
optimization problems while maintaining the transparency, explainability, and
auditability required in high-performance motorsport environments.

## Requirements

### Docker Setup

Recommended:

- Docker Desktop or Docker Engine
- Docker Compose
- At least 8 GB RAM for the backend image build because Docling and CPU-only
  PyTorch are installed

### Local Development

Required:

- Python 3.12+
- Node.js 20+
- npm
- PostgreSQL 16, unless database fallback behavior is sufficient
- Redis 7, unless in-memory fallback behavior is sufficient

## Environment Configuration

Copy the root template:

```bash
cd Veritasppen
cp .env.example .env
```

The template intentionally leaves deployment-specific values blank. Do not
commit `.env` files.

### Required For IBM Granite Narration

Set these values in `.env`:

```text
WATSONX_URL=
WATSONX_PROJECT_ID=
WATSONX_API_KEY=
WATSONX_MODEL_ID=
```

Create the watsonx.ai project and access credentials in IBM Cloud before
running AI-backed narration. If these values are not configured, the backend
reports the missing AI requirements instead of embedding credentials in code.

### Required For Firebase Authentication

Set these values when Firebase login and realtime database sync are enabled:

```text
FIREBASE_PROJECT_ID=
FIREBASE_DATABASE_URL=
FIREBASE_WEB_API_KEY=
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_DATABASE_URL=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
VITE_FIREBASE_WEB_API_KEY=
```

The `VITE_*` entries are browser configuration values. Firebase security rules
and domain restrictions must still be configured in the Firebase and Google
Cloud consoles.

### Required For Production Persistence

Set these values for PostgreSQL and Redis:

```text
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
REDIS_PASSWORD=
REDIS_URL=
```

The development Docker Compose file can use local defaults. Production
deployments should always provide deployment-specific passwords and URLs.

### Optional Integrations

These values are optional:

```text
LANGFLOW_API_URL=
LANGFLOW_FLOW_ID=
LANGFLOW_API_KEY=
HF_API_TOKEN=
HF_MODEL_ID=
REPLICATE_API_TOKEN=
REPLICATE_MODEL_OWNER=
REPLICATE_MODEL_NAME=
GOOGLE_MAPS_API_KEY=
VITE_GOOGLE_MAPS_API_KEY=
VITE_GA_MEASUREMENT_ID=
```

## Run With Docker

Start the main application:

```bash
docker compose up --build
```

Open:

```text
Application: http://localhost:8080
Backend API: http://localhost:8001
API docs:    http://localhost:8001/docs
```

The Nginx frontend proxies `/api` and WebSocket upgrades to the backend, so
browser builds do not need Docker-internal hostnames.

## Run Locally

Backend:

```bash
cd Veritasppen/backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```bash
cd Veritasppen/frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

For local frontend development, set:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_WS_URL=ws://127.0.0.1:8000/api/v1/stream/telemetry
```

## Historical Replay Workflow

Launch the integrated interactive session loader:

```powershell
cd Veritasppen
.\scripts\run-replay.ps1
```

Or run the replay CLI directly:

```bash
cd Veritasppen/backend
python -m open_pit_wall
```

To broadcast an existing replay file:

```bash
python -m open_pit_wall replay \
  --data-file /path/to/replay.json \
  --host 127.0.0.1 \
  --port 8765 \
  --speed 1.0 \
  --autoplay
```

To run the optional Docker replay service, ensure the selected replay JSON file
exists in the shared replay volume and start:

```bash
docker compose --profile replay up --build
```

The standalone replay WebSocket server listens on:

```text
ws://localhost:8765
```

Example subscription:

```json
{
  "action": "subscribe",
  "channels": ["telemetry.drivers", "leaderboard", "race_control"]
}
```

## Testing

Backend:

```bash
cd Veritasppen/backend
python -m pytest tests -q
```

Frontend:

```bash
cd Veritasppen/frontend
npm install
npm test
```

## Repository Notes

- Replay files are JSON, not pickle, to avoid unsafe deserialization.
- Generated FastF1 cache and replay data are ignored by Git.
- Real credentials belong in `.env` or a deployment secret manager.
- The integrated replay utility retains its required MIT notice in
  `THIRD_PARTY_NOTICES.md`.
