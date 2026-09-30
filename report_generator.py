from datetime import datetime
from config import REPORTS_DIR


def generate_report(download_risk, process_risk, file_risk, total_score, risk_level):
    REPORTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now()
    path = REPORTS_DIR / f"interlockguard_report_{stamp:%Y%m%d_%H%M%S}.txt"
    text = f'''INTERLOCKGUARD ANALYSIS REPORT
==============================

Generated: {stamp:%Y-%m-%d %H:%M:%S}

MONITOR RESULTS
---------------
Download Activity Risk : {download_risk} [WARNING]
Process Activity Risk  : {process_risk} [SUSPICIOUS]
File Activity Risk     : {file_risk} [HIGH]

RISK ENGINE
-----------
TOTAL RISK SCORE       : {total_score} / 100
RISK LEVEL             : {risk_level}

OBSERVATIONS
------------
- Suspicious downloads
- Unusual process activity
- Rapid file modifications
- Unusual file renames
- Unusual file extensions
- Large-scale file activity

RECOMMENDED ACTION
------------------
Review suspicious activity and affected test files.
Use this report as a defensive demonstration record.

SAFETY
------
This is a defensive prototype. The demonstration uses simulated
activity and dummy files only. No real ransomware is executed and
no real files are encrypted.
'''
    path.write_text(text, encoding="utf-8")
    return path
