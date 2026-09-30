# InterlockGuard

Ransomware Behavior Detection Tool — Defensive Educational Prototype.

InterlockGuard demonstrates behavior-based monitoring inspired by the Interlock ransomware case study.

## Features
- Download Monitor
- Process Monitor
- File Activity Monitor
- Risk Engine
- Alert generation
- Report generation
- Harmless dummy-file simulator
- Tkinter GUI

## Architecture

Download Monitor + Process Monitor + File Activity Monitor -> Risk Engine -> Alert / Report

## Demo

```bash
python3 interlockguard_gui.py
```

Then click **START MONITORING** and **GENERATE REPORT**.

## CLI

```bash
python3 main.py
```

## Harmless Simulator

```bash
python3 simulator/ransomware_simulator.py
```

The simulator only uses files in `test_data/`. It does not encrypt, delete, or execute malware.

## Ubuntu setup

```bash
sudo apt update
sudo apt install -y python3-tk
pip install -r requirements.txt
```

## Safety

This is a defensive educational prototype. No real ransomware is included or executed.

## Authors

Tanvi Rakshe  
Riddhi Shah

## WhatsAppShield-style desktop prototype UI

The project includes an updated Tkinter desktop interface in `interlockguard_gui.py` designed as a simple analysis application:

- **SCAN TEST DATA** runs the harmless ransomware-behavior demonstration.
- **SAVE REPORT** saves the calculated risk results to `reports/`.
- **QUARANTINE DEMO** copies one dummy test file into `quarantine/` without deleting or encrypting the original.
- The main **ANALYSIS REPORT** panel shows download, process, file-activity findings, total risk score, risk level, and recommended action.

The interface is a prototype for the case study. It does not execute ransomware or encrypt real files.

### Run the GUI

```bash
python3 interlockguard_gui.py
```

On Ubuntu/Kali Linux, if Tkinter is missing:

```bash
sudo apt update
sudo apt install -y python3-tk
```
