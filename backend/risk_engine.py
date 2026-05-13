from activity_logger import log_activity


def analyze_loan(loan, autonomy_level=1):
    explanations = []

    if loan.daysLate > 30:
        risk = "HIGH"
        explanations.append("Loan overdue by more than 30 days")

    elif loan.daysLate > 10:
        risk = "MEDIUM"
        explanations.append("Loan overdue by more than 10 days")

    else:
        risk = "LOW"
        explanations.append("Loan repayment is mostly on time")

    if loan.missedPayments >= 3:
        explanations.append("Multiple missed payments detected")

    if loan.loanAmount > 50000:
        explanations.append("High outstanding loan amount")

    if risk == "HIGH":
        action = "ESCALATE_TO_OFFICER"

    elif risk == "MEDIUM":
        action = "SCHEDULE_FOLLOW_UP"

    else:
        action = "SEND_REMINDER"

    automated = False

    if autonomy_level == 2 and risk == "LOW":
        automated = True

    if autonomy_level == 3 and risk in ["LOW", "HIGH"]:
        automated = True

    log = log_activity(
        client=loan.clientName,
        action=action,
        risk_level=risk,
    )

    return {
        "client": loan.clientName,
        "riskLevel": risk,
        "suggestedAction": action,
        "automatedDecision": automated,
        "autonomyLevel": autonomy_level,
        "explanation": explanations,
        "activityLog": log,
    }