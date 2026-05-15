from datetime import datetime

ai_logs = []

def log_ai_activity(prompt, response):

    entry = {
        "timestamp": str(datetime.utcnow()),
        "prompt": prompt,
        "response": response
    }

    ai_logs.append(entry)

    return entry