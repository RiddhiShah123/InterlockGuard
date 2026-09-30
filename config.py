from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR = BASE_DIR / "test_data"
REPORTS_DIR = BASE_DIR / "reports"

DOWNLOAD_RISK = 10
PROCESS_RISK = 25
FILE_ACTIVITY_RISK = 35
HIGH_RISK_THRESHOLD = 60
CRITICAL_RISK_THRESHOLD = 90

TEST_DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
