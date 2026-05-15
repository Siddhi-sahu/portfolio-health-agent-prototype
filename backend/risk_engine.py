from activity_logger import log_activity


def analyze_loan(loan, autonomy_level=1):

    risk_score = 0

    explanations = []

    # DELINQUENCY SCORING

    if loan.daysLate > 60:

        risk_score += 50

        explanations.append(
            "Loan overdue by more than 60 days"
        )

    elif loan.daysLate > 30:

        risk_score += 35

        explanations.append(
            "Loan overdue by more than 30 days"
        )

    elif loan.daysLate > 10:

        risk_score += 20

        explanations.append(
            "Loan overdue by more than 10 days"
        )

    else:

        explanations.append(
            "Loan repayment is mostly on time"
        )

    # ARREARS SCORING

    if loan.inArrears:

        risk_score += 20

        explanations.append(
            "Account is currently in arrears"
        )

    # NPA SCORING

    if loan.isNPA:

        risk_score += 40

        explanations.append(
            "Loan classified as Non-Performing Asset"
        )

    # DELINQUENT AMOUNT

    if loan.delinquentAmount > 50000:

        risk_score += 30

        explanations.append(
            "Very high delinquent amount detected"
        )

    elif loan.delinquentAmount > 10000:

        risk_score += 15

        explanations.append(
            "Moderate delinquent amount detected"
        )

    # -------------------------
    # LOAN EXPOSURE
    # -------------------------

    if loan.loanAmount > 500000:

        risk_score += 20

        explanations.append(
            "High portfolio exposure from loan amount"
        )

    elif loan.loanAmount > 100000:

        risk_score += 10

        explanations.append(
            "Elevated loan exposure detected"
        )

    # -------------------------
    # MISSED PAYMENTS
    # -------------------------

    if loan.missedPayments >= 3:

        risk_score += 20

        explanations.append(
            "Multiple missed payments detected"
        )

    elif loan.missedPayments >= 1:

        risk_score += 10

        explanations.append(
            "Recent missed payments observed"
        )

    # -------------------------
    # FINAL CLASSIFICATION
    # -------------------------

    if risk_score >= 80:

        risk = "HIGH"

        action = "ESCALATE_TO_OFFICER"

    elif risk_score >= 40:

        risk = "MEDIUM"

        action = "SCHEDULE_FOLLOW_UP"

    else:

        risk = "LOW"

        action = "SEND_REMINDER"

    # -------------------------
    # AUTONOMY LOGIC
    # -------------------------

    automated = False

    if autonomy_level == 2 and risk == "LOW":

        automated = True

    elif autonomy_level == 3 and risk in ["LOW", "MEDIUM"]:

        automated = True

    # -------------------------
    # ACTIVITY LOGGING
    # -------------------------

    log = log_activity(
        client=loan.clientName,
        action=action,
        risk_level=risk,
    )

    return {

        "client": loan.clientName,

        "riskScore": risk_score,

        "riskLevel": risk,

        "suggestedAction": action,

        "automatedDecision": automated,

        "autonomyLevel": autonomy_level,

        "explanation": explanations,

        "activityLog": log,
    }