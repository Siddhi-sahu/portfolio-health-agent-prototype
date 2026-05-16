Mifos Data/API
      ↓
FastAPI Backend
      ↓
Risk Analysis Logic
      ↓
Explainability Layer
      ↓
Agent Decision System
      ↓
LangChain + LLM
      ↓
Frontend Dashboard


portfolio-health-agent/
│
├── backend/
│   ├── main.py
│   ├── risk_engine.py
│   ├── models.py
│   └── mock_data.py
│
└── frontend/

first steps:

Input loan data → analyze risk → return explanation + action

GET /mifos-portfolio-analysis

flow:
Mifos API
   ↓
Fetch loans
   ↓
Transform data
   ↓
Analyze risk
   ↓
Return portfolio analysis


logs:

POST /analyze-loan
       ↓
risk_engine.analyze_loan()
       ↓
log_activity()
       ↓
activity_logs.append(log)
       ↓
GET /activity-logs shows accumulated logs


# mifos api integration

Mifos JSON
   ↓
Transformation Layer
   ↓
Your Internal Loan Model
   ↓
Risk Engine

# next

a REAL portfolio monitoring prototype.
Mifos → Transform → Risk Engine → FastAPI Endpoint

full working pipeline now:
Mifos API
   ↓
Fetch real loans
   ↓
Transform data
   ↓
Run deterministic risk engine
   ↓
Generate explainable analysis
   ↓
Create audit/activity logs
   ↓
Return portfolio-wide analysis

what langchain is doing:
structured portfolio data
↓
prompt template
↓
LangChain chain
↓
Ollama local LLM
↓
natural language summary


# React dashboard

The prototype includes a React dashboard in `frontend/` for proposal demos and officer review workflows.

Run the backend:

```bash
cd backend
venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev -- --port 5173
```

Open:

```text
http://127.0.0.1:5173/
```

The dashboard connects to `http://127.0.0.1:8000` by default. To point it at another backend URL, set `VITE_API_BASE_URL` before running the frontend.

Dashboard features:

- portfolio risk queue
- autonomy level control
- deterministic confidence score
- machine-readable decision factors
- approval status and autonomy policy display
- officer feedback form
- activity and governance records
