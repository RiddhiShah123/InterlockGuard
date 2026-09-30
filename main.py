from config import TEST_DATA_DIR, DOWNLOAD_RISK, PROCESS_RISK, FILE_ACTIVITY_RISK
from risk_engine import calculate_risk
from alert_manager import generate_alert
from report_generator import generate_report
from monitors.process_monitor import ProcessMonitor
from monitors.file_monitor import FileActivityMonitor

def main():
    print("=" * 55)
    print("INTERLOCKGUARD - RANSOMWARE BEHAVIOR DETECTION")
    print("=" * 55)

    process = ProcessMonitor().scan()
    file_result = FileActivityMonitor(TEST_DATA_DIR).scan()

    download_risk = DOWNLOAD_RISK
    process_risk = PROCESS_RISK if process["events"] else 0
    file_risk = FILE_ACTIVITY_RISK if file_result["events"] else 0

    total, level = calculate_risk(download_risk, process_risk, file_risk)

    print(f"\nDownload Risk : {download_risk}")
    print(f"Process Risk  : {process_risk}")
    print(f"File Risk     : {file_risk}")
    print(f"TOTAL RISK SCORE : {total}")
    print(f"RISK LEVEL       : {level}")
    print(generate_alert(total, level))

    report = generate_report(download_risk, process_risk, file_risk, total, level)
    print(f"Report generated: {report}")

if __name__ == "__main__":
    main()
