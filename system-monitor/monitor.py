#!/usr/bin/env python3
"""
System Monitor (Mini Edition)
- Terminal mode: prints CPU, memory, temperature (if available) periodically.
- GUI mode: Matplotlib live chart of overall CPU percentage; prints memory/temps to console once per second.
- Optional GIF recording for a short demo.
"""
import argparse
import time
import sys
import psutil
import math
from typing import Dict, List, Optional

def format_bytes(num):
    # Human-readable bytes
    step = 1024.0
    for unit in ['B','KB','MB','GB','TB','PB']:
        if num < step:
            return f"{num:3.1f} {unit}"
        num /= step
    return f"{num:.1f} PB"

def read_temperatures() -> Dict[str, List[psutil._common.sdiskusage]]:
    try:
        temps = psutil.sensors_temperatures()
        return temps or {}
    except Exception:
        return {}

def print_header():
    print("-"*72)
    print(f"{'Time':<8} {'CPU% (avg)':<12} {'CPU per-core%':<24} {'Mem Used/Total':<22} {'Temp(C)':<8}")
    print("-"*72)

def terminal_mode(interval: float, duration: float):
    print_header()
    start = time.time()
    last_temp_print = 0.0
    while time.time() - start < duration:
        cpu_overall = psutil.cpu_percent(interval=None)
        cpu_percpu = psutil.cpu_percent(interval=None, percpu=True)
        vm = psutil.virtual_memory()
        temps = read_temperatures()

        # Extract a representative CPU temp if present
        cpu_temp = None
        for name, entries in temps.items():
            for entry in entries:
                # heuristic: look for a label that resembles "cpu" or "package"
                label = (getattr(entry, 'label', '') or '').lower()
                if 'cpu' in label or 'package' in label or not label:
                    cpu_temp = getattr(entry, 'current', None)
                    if cpu_temp is not None:
                        break
            if cpu_temp is not None:
                break

        now = time.strftime("%H:%M:%S")
        percpu_str = "[" + ", ".join(f"{c:>4.0f}" for c in cpu_percpu[:8]) + (" ...]" if len(cpu_percpu) > 8 else "]")
        mem_str = f"{format_bytes(vm.used)}/{format_bytes(vm.total)}"
        temp_str = f"{cpu_temp:.1f}" if cpu_temp is not None else "--"

        print(f"{now:<8} {cpu_overall:>8.1f}%    {percpu_str:<24} {mem_str:<22} {temp_str:<8}")
        time.sleep(interval)

def gui_mode(interval: float, duration: float, save_gif: Optional[str] = None):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter

    xs = []
    ys = []  # overall CPU%

    fig, ax = plt.subplots()
    ax.set_title("CPU Utilization (%) — Mini Monitor")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CPU %")
    ax.set_ylim(0, 100)
    line, = ax.plot([], [], lw=2)

    start = time.time()
    def update(frame):
        t = time.time() - start
        cpu = psutil.cpu_percent(interval=None)
        xs.append(t)
        ys.append(cpu)
        # keep last N points for clarity (e.g., 200)
        N = 200
        xs_trim = xs[-N:]
        ys_trim = ys[-N:]
        line.set_data(xs_trim, ys_trim)
        ax.set_xlim(max(0, t- max(10, duration)), max(10, t))
        return (line,)

    anim = FuncAnimation(fig, update, interval=max(50, int(interval*1000)), blit=True)
    if save_gif:
        # Save at the end of runtime
        print(f"[info] Recording GIF to: {save_gif}")
        # We run a blocking loop to reach the duration; the animation callback still fires
        end_time = time.time() + duration
        while time.time() < end_time:
            plt.pause(0.05)
        try:
            writer = PillowWriter(fps=max(5, int(1/interval)))
            anim.save(save_gif, writer=writer)
            print(f"[ok] Saved {save_gif}")
        except Exception as e:
            print(f"[warn] Failed to save GIF: {e}")
    else:
        plt.show(block=True)

def main():
    parser = argparse.ArgumentParser(description="Mini System Monitor (terminal or Matplotlib).")
    parser.add_argument("--interval", type=float, default=0.5, help="Sampling interval in seconds (default 0.5).")
    parser.add_argument("--duration", type=float, default=10, help="Run duration in seconds (default 10).")
    parser.add_argument("--no-gui", action="store_true", help="Terminal mode (no GUI).")
    parser.add_argument("--save-gif", type=str, default=None, help="Path to save a short demo GIF (GUI mode only).")
    args = parser.parse_args()

    if args.no_gui:
        terminal_mode(args.interval, args.duration)
    else:
        gui_mode(args.interval, args.duration, args.save_gif)

if __name__ == "__main__":
    main()
