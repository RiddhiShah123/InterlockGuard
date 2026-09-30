import psutil

class ProcessMonitor:
    def scan(self):
        suspicious = {"powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe"}
        matches = []
        for p in psutil.process_iter(["pid", "name"]):
            try:
                name = (p.info.get("name") or "").lower()
                if name in suspicious:
                    matches.append(f"PID {p.info['pid']}: {p.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {"risk": 25 if matches else 0,
                "status": "SUSPICIOUS" if matches else "NORMAL",
                "events": matches}
