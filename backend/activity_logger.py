from datetime import datetime

# in-memory storage. for now
activity_logs = []


def log_activity(client, action, risk_level):
    log = {
        "timestamp": datetime.now().isoformat(),
        "client": client,
        "riskLevel": risk_level,
        "action": action,
        "status": "PENDING_APPROVAL",
    }

    activity_logs.append(log)

    return log