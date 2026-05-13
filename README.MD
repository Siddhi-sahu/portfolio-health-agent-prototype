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