from fastapi import FastAPI
from models import Loan
from risk_engine import analyze_loan
from mock_data import mock_loans
from activity_logger import activity_logs
from mifos_service import get_transformed_loans
from ai.summary_service import generate_portfolio_summary
from ai.ai_activity_logger import ai_logs

app = FastAPI()

def generate_portfolio_analysis_data(autonomy_level=1):

    loans = get_transformed_loans()

    analyzed_loans = []

    for loan_data in loans:

        loan = Loan(**loan_data)

        result = analyze_loan(
            loan,
            autonomy_level
        )

        analyzed_loans.append({
            "loan": loan_data,
            "analysis": result
        })

    return {
        "totalLoans": len(analyzed_loans),
        "portfolioAnalysis": analyzed_loans,
    }

@app.get("/")
def home():
    return {"message": "Portfolio Health Agent API running"}

    
@app.get("/portfolio-analysis")
def portfolio_analysis(autonomy_level: int = 1):

    return generate_portfolio_analysis_data(
        autonomy_level
    )
    
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
    
@app.get("/portfolio-summary")
def portfolio_summary():

    loans = get_transformed_loans()

    analyses = []

    for loan in loans:
        loan_model = Loan(**loan)

        analysis = analyze_loan(loan_model)

        analyses.append({
            "loan": loan,
            "analysis": analysis
        })

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    total_exposure = 0
    total_delinquent = 0

    npa_accounts = 0
    
    # ANALYTICS

    for item in analyses:

        loan = item["loan"]

        analysis = item["analysis"]

        total_exposure += loan["loanAmount"]

        total_delinquent += loan["delinquentAmount"]

        if loan["isNPA"]:

            npa_accounts += 1

        if analysis["riskLevel"] == "HIGH":

            high_risk += 1

        elif analysis["riskLevel"] == "MEDIUM":

            medium_risk += 1

        else:

            low_risk += 1

    # PORTFOLIO HEALTH

    if high_risk >= 2:

        portfolio_health = "HIGH_RISK"

    elif medium_risk >= 2:

        portfolio_health = "MODERATE_RISK"

    else:

        portfolio_health = "STABLE"

    return {

        "totalLoans": len(loans),

        "highRiskLoans": high_risk,

        "mediumRiskLoans": medium_risk,

        "lowRiskLoans": low_risk,

        "totalPortfolioExposure": total_exposure,

        "totalDelinquentAmount": total_delinquent,

        "npaAccounts": npa_accounts,

        "portfolioHealth": portfolio_health
    }
    
@app.get("/ai-portfolio-summary")
def ai_portfolio_summary():

    portfolio_results = generate_portfolio_analysis_data()

    try:
        summary = generate_portfolio_summary(
        portfolio_results
        )
    except Exception:
        summary = "AI summary unavailable"
        

    return {
        "structuredData": portfolio_results,
        "aiSummary": summary
    }
    
@app.get("/ai-logs")
def get_ai_logs():

    return {
        "totalLogs": len(ai_logs),
        "logs": ai_logs
    }