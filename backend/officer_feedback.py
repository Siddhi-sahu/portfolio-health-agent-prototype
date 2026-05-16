from datetime import datetime


officer_feedback = []


def record_officer_feedback(feedback):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "client": feedback.client,
        "decision": feedback.decision,
        "notes": feedback.notes,
    }

    officer_feedback.append(entry)

    return entry
