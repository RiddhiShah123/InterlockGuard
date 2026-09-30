import shutil
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

from config import BASE_DIR, TEST_DATA_DIR
from report_generator import generate_report
from risk_engine import calculate_risk


# InterlockGuard - defensive prototype GUI
# This interface intentionally uses harmless simulated activity and dummy files.

BG = "#f6f1f6"
PANEL = "#ffffff"
TEXT = "#1f2937"
MUTED = "#6b7280"
BORDER = "#d1d5db"
ACCENT = "#7c3aed"
ACCENT_DARK = "#5b21b6"
DANGER = "#dc2626"
WARNING = "#d97706"
SAFE = "#15803d"
DARK = "#111827"


class InterlockGuardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InterlockGuard - Ransomware Behavior Analyzer")
        self.root.geometry("1050x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)

        self.download_risk = 0
        self.process_risk = 0
        self.file_risk = 0
        self.total_risk = 0
        self.risk_level = "LOW"
        self.monitoring = False
        self.last_report = None
        self.quarantine_dir = BASE_DIR / "quarantine"

        self.build()
        self.reset_view()

    def make_button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            fg="white" if primary else TEXT,
            bg=ACCENT if primary else PANEL,
            activeforeground="white" if primary else TEXT,
            activebackground=ACCENT_DARK if primary else "#eeeef2",
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
            cursor="hand2",
        )

    def build(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=34, pady=(24, 8))

        tk.Label(
            header,
            text="INTERLOCKGUARD",
            font=("Arial", 28, "bold"),
            fg=DARK,
            bg=BG,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Ransomware Behavior Detection & Risk Analyzer",
            font=("Arial", 12),
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(2, 0))

        # Main action buttons - WhatsAppShield-style
        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill="x", padx=34, pady=(14, 10))

        self.scan_btn = self.make_button(actions, "SCAN TEST DATA", self.start_monitoring, True)
        self.scan_btn.pack(side="left", padx=(0, 10))

        self.save_btn = self.make_button(actions, "SAVE REPORT", self.generate_report)
        self.save_btn.pack(side="left", padx=10)

        self.quarantine_btn = self.make_button(actions, "QUARANTINE DEMO", self.quarantine_demo)
        self.quarantine_btn.pack(side="left", padx=10)

        # Scan target line
        target = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        target.pack(fill="x", padx=34, pady=(0, 12))
        self.target_label = tk.Label(
            target,
            text="Monitored: test_data/ (dummy files only)",
            font=("Arial", 10, "bold"),
            fg=TEXT,
            bg=PANEL,
            anchor="w",
        )
        self.target_label.pack(fill="x", padx=14, pady=10)

        # Report panel
        report_card = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        report_card.pack(fill="both", expand=True, padx=34, pady=(0, 12))

        tk.Label(
            report_card,
            text="ANALYSIS REPORT",
            font=("Arial", 11, "bold"),
            fg=TEXT,
            bg=PANEL,
        ).pack(anchor="w", padx=16, pady=(14, 7))

        self.report = tk.Text(
            report_card,
            bg="#fbfbfc",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
            font=("Courier New", 10),
            wrap="word",
            padx=14,
            pady=12,
        )
        self.report.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.report.configure(state="disabled")

        # Bottom status area
        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill="x", padx=34, pady=(0, 12))

        status_card = tk.Frame(bottom, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        status_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(
            status_card,
            text="RISK STATUS",
            font=("Arial", 10, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", padx=14, pady=(12, 2))

        self.risk_status = tk.Label(
            status_card,
            text="LOW",
            font=("Arial", 23, "bold"),
            fg=SAFE,
            bg=PANEL,
        )
        self.risk_status.pack(anchor="w", padx=14, pady=(0, 12))

        score_card = tk.Frame(bottom, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        score_card.pack(side="right", fill="both", expand=True, padx=(8, 0))

        tk.Label(
            score_card,
            text="RISK SCORE",
            font=("Arial", 10, "bold"),
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", padx=14, pady=(12, 2))

        self.score_label = tk.Label(
            score_card,
            text="0 / 100",
            font=("Arial", 23, "bold"),
            fg=TEXT,
            bg=PANEL,
        )
        self.score_label.pack(anchor="w", padx=14, pady=(0, 12))

        tk.Label(
            self.root,
            text="Defensive prototype • Harmless simulation • Dummy files only",
            font=("Arial", 9),
            fg=MUTED,
            bg=BG,
        ).pack(pady=(0, 10))

    def set_report(self, text):
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")
        self.report.insert("1.0", text)
        self.report.configure(state="disabled")

    def reset_view(self):
        self.set_report(
            "INTERLOCKGUARD ANALYSIS\n"
            "========================\n\n"
            "Status: READY\n"
            "Target : test_data/\n\n"
            "Download Activity   : NOT SCANNED\n"
            "Process Activity    : NOT SCANNED\n"
            "File Activity       : NOT SCANNED\n\n"
            "Risk Score           : 0 / 100\n"
            "Risk Level           : LOW\n\n"
            "Click SCAN TEST DATA to run the harmless demonstration.\n"
            "The demo uses dummy files and simulated ransomware-like events."
        )

    def start_monitoring(self):
        if self.monitoring:
            return
        self.monitoring = True
        self.scan_btn.config(text="SCANNING...", state="disabled")
        threading.Thread(target=self.demo_scan, daemon=True).start()

    def demo_scan(self):
        self.download_risk = 10
        self.process_risk = 25
        self.file_risk = 35

        self.update_report(
            "SCAN STARTED\n"
            "------------------------\n"
            "Target: test_data/\n\n"
            "[1/3] Download Monitor\n"
            "Status : WARNING\n"
            "Observation: suspicious download activity detected.\n\n"
        )
        time.sleep(0.7)

        self.update_report(
            "SCAN STARTED\n"
            "------------------------\n"
            "Target: test_data/\n\n"
            "[1/3] Download Monitor\n"
            "Status : WARNING\n"
            "Observation: suspicious download activity detected.\n\n"
            "[2/3] Process Monitor\n"
            "Status : SUSPICIOUS\n"
            "Observation: unusual process activity detected.\n\n"
        )
        time.sleep(0.7)

        self.update_report(
            "SCAN STARTED\n"
            "------------------------\n"
            "Target: test_data/\n\n"
            "[1/3] Download Monitor\n"
            "Status : WARNING\n"
            "Observation: suspicious download activity detected.\n\n"
            "[2/3] Process Monitor\n"
            "Status : SUSPICIOUS\n"
            "Observation: unusual process activity detected.\n\n"
            "[3/3] File Activity Monitor\n"
            "Status : HIGH\n"
            "Observation: rapid file modifications and unusual renames detected.\n\n"
        )
        time.sleep(0.8)

        self.total_risk, self.risk_level = calculate_risk(
            self.download_risk, self.process_risk, self.file_risk
        )

        final = (
            "INTERLOCKGUARD ANALYSIS REPORT\n"
            "==============================\n\n"
            f"Scanned: {TEST_DATA_DIR.name}/\n"
            f"Time   : {datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
            "MONITOR RESULTS\n"
            "------------------------------\n"
            f"Download Activity Risk : {self.download_risk}  [WARNING]\n"
            f"Process Activity Risk  : {self.process_risk}  [SUSPICIOUS]\n"
            f"File Activity Risk     : {self.file_risk}  [HIGH]\n\n"
            "RISK ENGINE\n"
            "------------------------------\n"
            f"Total Risk Score       : {self.total_risk} / 100\n"
            f"Risk Level             : {self.risk_level}\n\n"
            "RECOMMENDED ACTION\n"
            "------------------------------\n"
            "Review suspicious activity and affected test files.\n"
            "Use the report option to save the analysis.\n\n"
            "SAFETY NOTE\n"
            "------------------------------\n"
            "This is a defensive prototype. The demonstration uses\n"
            "dummy files and simulated activity only. No real\n"
            "ransomware is executed and no real files are encrypted."
        )
        self.root.after(0, lambda: self.set_report(final))
        self.root.after(0, self.update_status)
        self.root.after(0, self.finish_scan)

    def update_report(self, text):
        self.root.after(0, lambda: self.set_report(text))

    def update_status(self):
        self.score_label.config(text=f"{self.total_risk} / 100")
        self.risk_status.config(text=self.risk_level, fg=self.level_color())

    def level_color(self):
        if self.risk_level == "CRITICAL":
            return DANGER
        if self.risk_level == "HIGH":
            return DANGER
        if self.risk_level == "MEDIUM":
            return WARNING
        return SAFE

    def finish_scan(self):
        self.monitoring = False
        self.scan_btn.config(text="SCAN TEST DATA", state="normal")
        self.target_label.config(
            text=f"Scanned: {TEST_DATA_DIR.name}/ • Result: {self.risk_level} risk • Dummy files only"
        )

    def generate_report(self):
        if self.total_risk == 0:
            messagebox.showinfo("InterlockGuard", "Run SCAN TEST DATA first.")
            return
        path = generate_report(
            self.download_risk,
            self.process_risk,
            self.file_risk,
            self.total_risk,
            self.risk_level,
        )
        self.last_report = path
        messagebox.showinfo("Report Saved", f"Report saved successfully:\n{path}")

    def quarantine_demo(self):
        """Safely copy one dummy test file to a local quarantine folder."""
        try:
            TEST_DATA_DIR.mkdir(exist_ok=True)
            self.quarantine_dir.mkdir(exist_ok=True)
            candidates = sorted(TEST_DATA_DIR.glob("*.txt"))
            if not candidates:
                messagebox.showinfo("Quarantine Demo", "No dummy test file is available.")
                return

            source = candidates[0]
            destination = self.quarantine_dir / source.name
            shutil.copy2(source, destination)
            self.target_label.config(text=f"Demo quarantine copy: {source.name} → quarantine/")
            messagebox.showinfo(
                "Quarantine Demo",
                "A COPY of a dummy test file was placed in the quarantine folder.\n\n"
                "The original dummy file was not deleted or encrypted.",
            )
        except Exception as exc:
            messagebox.showerror("Quarantine Demo", f"Could not complete demo quarantine:\n{exc}")


if __name__ == "__main__":
    root = tk.Tk()
    InterlockGuardGUI(root)
    root.mainloop()
