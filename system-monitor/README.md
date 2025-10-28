# system-monitor
A tiny system metrics viewer using **Python + psutil** with both terminal and **Matplotlib** display modes.

## Features
- CPU % (overall + per-core), memory, and temperatures (if `psutil.sensors_temperatures` is supported on your OS).
- Terminal mode (no GUI) or live chart via Matplotlib.
- Optional **GIF recording** for a short demo (`--save-gif demo.gif`).
- Minimal **unittest**.

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
# Terminal (no GUI):
python monitor.py --interval 0.5 --duration 10 --no-gui

# Live chart:
python monitor.py --interval 0.5 --duration 10

# Save GIF (headless-friendly if Pillow writer is available):
python monitor.py --interval 0.2 --duration 8 --save-gif demo.gif
```

## Test
```bash
python -m unittest -v
```
