from fastapi import FastAPI
from models import Loan
from risk_engine import analyze_loan
from mock_data import mock_loans
from activity_logger import activity_logs
from mifos_service import get_transformed_loans

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Portfolio Health Agent API running"}

@app.get("/portfolio-analysis")
def portfolio_analysis(autonomy_level: int = 1):
    analyzed_loans = []

    for loan_data in mock_loans:
        loan = Loan(**loan_data)

        result = analyze_loan(loan, autonomy_level)

        analyzed_loans.append(result)

    return {
        "totalLoans": len(analyzed_loans),
        "portfolioAnalysis": analyzed_loans,
    }
    
@app.post("/analyze-loan")
def analyze(loan: Loan, autonomy_level: int = 1):
    result = analyze_loan(loan, autonomy_level)
    return result

@app.get("/mifos-portfolio-analysis")
def mifos_portfolio_analysis():

    loans = get_transformed_loans()

    analyzed_portfolio = []

    for loan in loans:
        loan_model = Loan(**loan)
        analysis = analyze_loan(loan_model)

        analyzed_portfolio.append({
            "loan": loan,
            "analysis": analysis
        })

    return {
        "totalLoans": len(analyzed_portfolio),
        "portfolioAnalysis": analyzed_portfolio
    }
    
@app.get("/activity-logs")
def get_logs():
    return {
        "totalLogs": len(activity_logs),
        "logs": activity_logs,
    }