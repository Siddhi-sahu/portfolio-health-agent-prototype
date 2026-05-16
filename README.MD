# Portfolio Health Agent Prototype

An exploratory prototype for the Mifos DMP 2026 project: **Agentic AI for Proactive Portfolio Management with Explainable Autonomy**.

This project is not the final DMP implementation. I built it to understand the project space better before selection: how Mifos X loan data can be fetched, transformed, scored for risk, explained to loan officers, and shown in a dashboard with configurable autonomy and human oversight.

## What This Prototype Does

- Fetches loan records from the Mifos demo API.
- Transforms Mifos loan JSON into an internal loan model.
- Runs deterministic risk scoring on each loan.
- Returns human-readable explanations for every decision.
- Returns machine-readable decision factors for explainability UI and future charts.
- Supports configurable autonomy levels.
- Adds approval statuses such as `AUTO_APPROVED`, `PENDING_REVIEW`, and `REQUIRES_OFFICER_REVIEW`.
- Captures officer feedback through an API endpoint.
- Creates activity/governance logs for agent actions.
- Uses LangChain with Ollama for AI-generated portfolio summaries.
- Provides a React dashboard for portfolio review and proposal demos.

## Architecture

```text
Mifos X / Fineract Demo API
        |
        v
Loan Fetching + Transformation Layer
        |
        v
Deterministic Risk Engine
        |
        v
Explainability + Autonomy Policy Layer
        |
        v
FastAPI Backend
        |
        v
React Officer Dashboard
```

The backend keeps the risk decisions transparent and reproducible. LangChain/Ollama is used for portfolio summary support, not as the source of truth for financial decisions.

## Repository Structure

```text
portfolio-health-agent/
|
|-- backend/
|   |-- main.py                  # FastAPI routes
|   |-- mifos_service.py         # Mifos API fetch + transformation
|   |-- risk_engine.py           # Risk scoring, explanations, autonomy policy
|   |-- models.py                # Pydantic request models
|   |-- officer_feedback.py      # In-memory officer feedback storage
|   |-- activity_logger.py       # In-memory activity logs
|   |-- mock_data.py             # Fallback/demo loan data
|   |-- ai/
|   |   |-- chains.py            # LangChain chain
|   |   |-- prompts.py           # Portfolio summary prompt
|   |   |-- llm_service.py       # Ollama model configuration
|   |   |-- summary_service.py   # AI summary wrapper
|   |   `-- ai_activity_logger.py
|   `-- requirements.txt
|
`-- frontend/
    |-- src/
    |   |-- App.jsx              # React dashboard
    |   |-- main.jsx
    |   `-- styles.css
    |-- package.json
    `-- index.html
```

## Backend Setup

From the repository root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the FastAPI backend:

```bash
venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Frontend Setup

From the repository root, in a separate terminal:

```bash
cd frontend
npm install
npm run dev -- --port 5173
```

Open the dashboard:

```text
http://127.0.0.1:5173/
```

By default, the frontend connects to:

```text
http://127.0.0.1:8000
```

To use another backend URL, set `VITE_API_BASE_URL` before starting the frontend.

## Optional AI Summary Setup

The AI portfolio summary uses LangChain with Ollama.

Install and run Ollama locally, then pull the configured model:

```bash
ollama pull llama3:8b
```

The configured model is defined in `backend/ai/llm_service.py`.

If Ollama is not running, the core risk analysis endpoints still work. Only the AI summary feature may be unavailable.

## API Reference

### `GET /`

Health check endpoint.

Returns:

```json
{
  "message": "Portfolio Health Agent API running"
}
```

### `POST /analyze-loan`

Analyzes a single loan payload and returns the risk decision.

Query parameter:

- `autonomy_level`: optional integer, defaults to `1`

Returns fields such as:

- `riskScore`
- `riskLevel`
- `confidenceScore`
- `suggestedAction`
- `automatedDecision`
- `autonomyPolicy`
- `approvalStatus`
- `decisionFactors`
- `explanation`
- `activityLog`

### `GET /portfolio-analysis`

Fetches loans from Mifos, transforms them, analyzes each loan, and returns portfolio-level analysis.

Query parameter:

- `autonomy_level`: optional integer, defaults to `1`

### `GET /mifos-portfolio-analysis`

Returns portfolio analysis using transformed Mifos loan records.

### `GET /portfolio-summary`

Returns structured portfolio metrics such as:

- total loans
- high-risk loans
- medium-risk loans
- low-risk loans
- total portfolio exposure
- total delinquent amount
- NPA accounts
- portfolio health

### `GET /ai-portfolio-summary`

Returns structured portfolio analysis plus an AI-generated summary using LangChain and Ollama.

### `GET /ai-logs`

Returns in-memory logs for AI summary activity during the current backend session.

### `GET /activity-logs`

Returns in-memory activity logs created when loan analysis runs.

### `POST /officer-feedback`

Stores officer feedback in memory.

Example request:

```json
{
  "client": "Ravi",
  "decision": "APPROVED",
  "notes": "Escalation justified"
}
```

### `GET /officer-feedback`

Returns all officer feedback captured during the current backend session.

## How The Risk Engine Works

The risk engine is deterministic and rule-based. It evaluates each loan using factors such as:

- days late
- arrears status
- NPA status
- delinquent amount
- loan amount
- missed payments

Each factor can add to the final `riskScore`. The score is then mapped to a risk level:

- `LOW`
- `MEDIUM`
- `HIGH`

For explainability, the backend returns two kinds of reasoning:

1. `explanation`: human-readable text for loan officers.
2. `decisionFactors`: structured metadata showing factor, value, and impact.

Example:

```json
{
  "factor": "daysLate",
  "value": 45,
  "impact": 35
}
```

The backend also returns:

- `confidenceScore`: deterministic confidence derived from the risk score.
- `approvalStatus`: whether the case is auto-approved, pending review, or requires officer review.
- `autonomyPolicy`: whether the agent should auto-handle, require review, or escalate.

## Autonomy Levels

The prototype supports three autonomy levels:

```text
Level 1: conservative review mode
Level 2: low-risk loans can be auto-handled
Level 3: low and medium-risk loans can be auto-handled
```

High-risk loans remain escalated to officers.

This is meant to show the idea of explainable autonomy: the agent can act within clear policy boundaries, while sensitive cases stay under human review.

## Frontend Dashboard

The React dashboard shows:

- total loans
- high-risk loans
- loans needing review
- auto-handled loans
- total exposure
- delinquent amount
- loan decision queue
- selected loan explainability panel
- decision factor impact bars
- autonomy level controls
- officer feedback form
- recent governance/activity records

The dashboard calls the FastAPI backend directly and refreshes portfolio analysis whenever the autonomy level changes.

## Notes On Mifos Demo Data

The Mifos demo API may return repeated client names, such as the same borrower appearing multiple times. This dashboard displays loan records, not unique clients.

In a fuller implementation, the UI could show loan account IDs, group loans by client, or provide filters to make this clearer for officers.

## Prototype Limitations

- This is an exploratory prototype, not a production-ready Mifos X integration.
- Officer feedback is stored in memory and disappears when the backend restarts.
- Activity logs are also in-memory.
- Risk scoring rules are intentionally simple and deterministic.
- The Mifos demo API data can be repetitive and may not show many high-risk examples.
- LangChain/Ollama is used for summarization support, not final financial decision-making.
- Authentication, role-based access, persistent storage, production audit logs, and deeper Mifos X Web App integration are future work.

## Future Work

With mentor guidance, this prototype could be extended into a stronger DMP implementation by adding:

- deeper Apache Fineract/Mifos X data integration
- persistent database storage for decisions, logs, and feedback
- role-based officer workflows
- better loan/client identifiers in the UI
- configurable risk policies
- mentor-approved action execution rules
- richer explainability charts
- stronger audit trails
- integration into the Mifos X Web App
- a user study to evaluate officer trust and usability

## Why This Prototype Exists

I built this project to explore the DMP problem before selection and to understand the technical shape of the work: Mifos API integration, backend risk scoring, explainability, autonomy policies, LangChain/Ollama summaries, and an officer-facing dashboard.

The main goal is to show initiative and provide a practical starting point for discussion, not to replace the final implementation that would be designed with mentors during the internship.
