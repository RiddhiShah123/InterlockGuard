from pathlib import Path

class FileActivityMonitor:
    def __init__(self, directory):
        self.directory = Path(directory)

    def scan(self):
        if not self.directory.exists():
            return {"risk": 0, "status": "NORMAL", "events": []}
        unusual = [p.name for p in self.directory.iterdir()
                   if p.is_file() and p.suffix.lower() not in {".txt", ".md", ".log"}]
        return {"risk": 35 if unusual else 0,
                "status": "HIGH" if unusual else "NORMAL",
                "events": unusual}
