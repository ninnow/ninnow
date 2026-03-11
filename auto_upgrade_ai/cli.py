from __future__ import annotations

import argparse
import json

from .engine import AutoUpgradeAI


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AutoUpgrade AI")
    parser.add_argument("--cycles", type=int, default=5, help="Upgrade cycles")
    parser.add_argument("--state", type=str, default="state.json", help="State file path")
    args = parser.parse_args()

    ai = AutoUpgradeAI(state_file=args.state)
    report = ai.run(cycles=args.cycles)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
