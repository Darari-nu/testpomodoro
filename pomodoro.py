#!/usr/bin/env python3
"""Simple CLI Pomodoro timer.

Usage
-----
$ python pomodoro.py            # 25-min work / 5-min break, infinite cycles
$ python pomodoro.py -w 50 -b 10 -c 4  # custom durations and cycle count

Press Ctrl-C at any time to quit early.
"""
import argparse
import signal
import sys
import time
from datetime import timedelta


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def format_duration(seconds: int) -> str:
    """Return a HH:MM:SS string for given seconds."""
    return str(timedelta(seconds=seconds))


def create_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Create a visual progress bar."""
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {progress:.1%}"


def countdown(label: str, seconds: int) -> None:
    """Run a countdown printing remaining time every second."""
    is_work = label.lower() == "work"
    color = Colors.GREEN if is_work else Colors.CYAN
    
    print(f"\n{color}{Colors.BOLD}== {label.upper()} {format_duration(seconds)} =={Colors.RESET}")
    
    try:
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            elapsed = seconds - remaining
            progress_bar = create_progress_bar(elapsed, seconds)
            
            time_display = f"{mins:02d}:{secs:02d}"
            print(f"\r{color}{label}: {time_display} {Colors.RESET}{progress_bar} ", end="", flush=True)
            time.sleep(1)
        
        completion_msg = f"{label.upper()} COMPLETE! "
        print(f"\r{color}{Colors.BOLD}{completion_msg}{Colors.RESET}{' ' * 50}")
        
        # Add a visual separator
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Interrupted. Exiting…{Colors.RESET}")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Pomodoro timer (CLI)")
    parser.add_argument("-w", "--work", type=int, default=25, help="work duration in minutes (default: 25)")
    parser.add_argument("-b", "--break_", type=int, default=5, help="break duration in minutes (default: 5)")
    parser.add_argument("-c", "--cycles", type=int, default=0, help="number of Pomodoro cycles (0 = infinite)")
    args = parser.parse_args()

    work_sec = args.work * 60
    break_sec = args.break_ * 60
    cycles = args.cycles

    # Graceful Ctrl-C handling
    def _signal_handler(sig, frame):
        print(f"\n{Colors.RED}Interrupted. Goodbye!{Colors.RESET}")
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    print(f"{Colors.MAGENTA}{Colors.BOLD}")
    print("🍅 POMODORO TIMER STARTED 🍅")
    print(f"Work: {args.work} min | Break: {args.break_} min")
    if cycles:
        print(f"Cycles: {cycles}")
    else:
        print("Cycles: Infinite")
    print(f"{Colors.RESET}")

    count = 0
    while True:
        count += 1
        if cycles and count > cycles:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 All cycles completed. Well done! 🎉{Colors.RESET}")
            break
            
        cycle_info = f"{count}" if cycles == 0 else f"{count}/{cycles}"
        print(f"\n{Colors.BLUE}{Colors.BOLD}===== CYCLE {cycle_info} ====={Colors.RESET}")
        
        countdown("Work", work_sec)
        countdown("Break", break_sec)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Additional fallback (in case countdown handler didn't catch)
        pass
