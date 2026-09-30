from datetime import datetime

def generate_alert(total_score, risk_level):
    return f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ALERT: {risk_level} activity detected (risk score: {total_score})."
