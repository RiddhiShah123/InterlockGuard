from config import HIGH_RISK_THRESHOLD, CRITICAL_RISK_THRESHOLD

def calculate_risk(download_risk, process_risk, file_risk):
    total = download_risk + process_risk + file_risk
    if total >= CRITICAL_RISK_THRESHOLD:
        level = "CRITICAL"
    elif total >= HIGH_RISK_THRESHOLD:
        level = "HIGH"
    elif total >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"
    return total, level
