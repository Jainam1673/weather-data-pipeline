"""
Processor pipeline wrapper to satisfy the project script entry point.
This provides a graceful fallback when Mojo is not installed.
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    mojo_file = project_root / "src" / "processors" / "weather_processor.mojo"

    try:
        result = subprocess.run(["which", "mojo"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print("⚠️ Mojo not found. Skipping Mojo execution.")
            print("Info: Install Mojo or run 'python main.py process' on a machine with Mojo.")
            return 0

        return subprocess.call(["mojo", str(mojo_file)])
    except Exception as exc:
        print(f"❌ Failed to run processor: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

