from pathlib import Path

class DownloadMonitor:
    def __init__(self, download_dir=None):
        self.download_dir = Path(download_dir) if download_dir else None

    def scan(self):
        if not self.download_dir or not self.download_dir.exists():
            return {"risk": 0, "status": "NORMAL", "events": []}
        events = [p.name for p in self.download_dir.iterdir() if p.is_file()]
        return {"risk": 10 if events else 0,
                "status": "WARNING" if events else "NORMAL",
                "events": events}
