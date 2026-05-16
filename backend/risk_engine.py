from activity_logger import log_activity


AUTONOMY_POLICY = {
    "LOW": "AUTO_HANDLE",
    "MEDIUM": "REVIEW_REQUIRED",
    "HIGH": "ESCALATE",
}

AUTONOMY_LEVEL_POLICIES = {
    1: {
        "LOW": "REVIEW_REQUIRED",
        "MEDIUM": "REVIEW_REQUIRED",
        "HIGH": "ESCALATE",
    },
    2: {
        "LOW": "AUTO_HANDLE",
        "MEDIUM": "REVIEW_REQUIRED",
        "HIGH": "ESCALATE",
    },
    3: {
        "LOW": "AUTO_HANDLE",
        "MEDIUM": "AUTO_HANDLE",
        "HIGH": "ESCALATE",
    },
}

APPROVAL_STATUS_BY_RISK = {
    "HIGH": "REQUIRES_OFFICER_REVIEW",
    "MEDIUM": "PENDING_REVIEW",
    "LOW": "AUTO_APPROVED",
}


def add_decision_factor(decision_factors, factor, value, impact):
    decision_factors.append({
        "factor": factor,
        "value": value,
        "impact": impact,
    })


def analyze_loan(loan, autonomy_level=1):

    risk_score = 0

    explanations = []

    decision_factors = []

    # DELINQUENCY SCORING

    if loan.daysLate > 60:

        risk_score += 50

        add_decision_factor(
            decision_factors,
            "daysLate",
            loan.daysLate,
            50,
        )

        explanations.append(
            "Loan overdue by more than 60 days"
        )

    elif loan.daysLate > 30:

        risk_score += 35

        add_decision_factor(
            decision_factors,
            "daysLate",
            loan.daysLate,
            35,
        )

        explanations.append(
            "Loan overdue by more than 30 days"
        )

    elif loan.daysLate > 10:

        risk_score += 20

        add_decision_factor(
            decision_factors,
            "daysLate",
            loan.daysLate,
            20,
        )

        explanations.append(
            "Loan overdue by more than 10 days"
        )

    else:

        add_decision_factor(
            decision_factors,
            "daysLate",
            loan.daysLate,
            0,
        )

        explanations.append(
            "Loan repayment is mostly on time"
        )

    # ARREARS SCORING

    if loan.inArrears:

        risk_score += 20

        add_decision_factor(
            decision_factors,
            "inArrears",
            loan.inArrears,
            20,
        )

        explanations.append(
            "Account is currently in arrears"
        )

    else:

        add_decision_factor(
            decision_factors,
            "inArrears",
            loan.inArrears,
            0,
        )

    # NPA SCORING

    if loan.isNPA:

        risk_score += 40

        add_decision_factor(
            decision_factors,
            "isNPA",
            loan.isNPA,
            40,
        )

        explanations.append(
            "Loan classified as Non-Performing Asset"
        )

    else:

        add_decision_factor(
            decision_factors,
            "isNPA",
            loan.isNPA,
            0,
        )

    # DELINQUENT AMOUNT

    if loan.delinquentAmount > 50000:

        risk_score += 30

        add_decision_factor(
            decision_factors,
            "delinquentAmount",
            loan.delinquentAmount,
            30,
        )

        explanations.append(
            "Very high delinquent amount detected"
        )

    elif loan.delinquentAmount > 10000:

        risk_score += 15

        add_decision_factor(
            decision_factors,
            "delinquentAmount",
            loan.delinquentAmount,
            15,
        )

        explanations.append(
            "Moderate delinquent amount detected"
        )

    else:

        add_decision_factor(
            decision_factors,
            "delinquentAmount",
            loan.delinquentAmount,
            0,
        )

    # -------------------------
    # LOAN EXPOSURE
    # -------------------------

    if loan.loanAmount > 500000:

        risk_score += 20

        add_decision_factor(
            decision_factors,
            "loanAmount",
            loan.loanAmount,
            20,
        )

        explanations.append(
            "High portfolio exposure from loan amount"
        )

    elif loan.loanAmount > 100000:

        risk_score += 10

        add_decision_factor(
            decision_factors,
            "loanAmount",
            loan.loanAmount,
            10,
        )

        explanations.append(
            "Elevated loan exposure detected"
        )

    else:

        add_decision_factor(
            decision_factors,
            "loanAmount",
            loan.loanAmount,
            0,
        )

    # -------------------------
    # MISSED PAYMENTS
    # -------------------------

    if loan.missedPayments >= 3:

        risk_score += 20

        add_decision_factor(
            decision_factors,
            "missedPayments",
            loan.missedPayments,
            20,
        )

        explanations.append(
            "Multiple missed payments detected"
        )

    elif loan.missedPayments >= 1:

        risk_score += 10

        add_decision_factor(
            decision_factors,
            "missedPayments",
            loan.missedPayments,
            10,
        )

        explanations.append(
            "Recent missed payments observed"
        )

    else:

        add_decision_factor(
            decision_factors,
            "missedPayments",
            loan.missedPayments,
            0,
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

    approval_status = APPROVAL_STATUS_BY_RISK[risk]

    confidence_score = min(risk_score / 100, 1.0)

    # -------------------------
    # AUTONOMY POLICY
    # -------------------------

    policy = AUTONOMY_LEVEL_POLICIES.get(
        autonomy_level,
        AUTONOMY_POLICY,
    )

    autonomy_policy = policy[risk]

    automated = autonomy_policy == "AUTO_HANDLE"


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

        "confidenceScore": confidence_score,

        "suggestedAction": action,

        "automatedDecision": automated,

        "autonomyLevel": autonomy_level,

        "autonomyPolicy": autonomy_policy,

        "approvalStatus": approval_status,

        "decisionFactors": decision_factors,

        "explanation": explanations,

        "activityLog": log,
    }
