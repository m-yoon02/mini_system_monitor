 **system-monitor/** — Python system metrics viewer (CPU, memory, temperatures if available). 
  - Terminal and Matplotlib modes, optional **GIF recording** for demos.
  - Includes a tiny **unittest**.


```bash
cd system-monitor
# (Recommended) Create venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Terminal mode (no GUI)
python monitor.py --interval 0.5 --duration 10 --no-gui
# Live chart (Matplotlib)
python monitor.py --interval 0.5 --duration 10
# Save a demo GIF (headless ok if pillow/writers available)
python monitor.py --interval 0.2 --duration 8 --save-gif demo.gif
# Run tests
python -m unittest -v
```
