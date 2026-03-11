from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from random import Random
from typing import Iterable, List


@dataclass
class BrainConfig:
    """Simple tunable parameters that represent the AI's "brain"."""

    creativity: float = 0.5
    caution: float = 0.5
    learning_rate: float = 0.3


class AutoUpgradeAI:
    """
    A tiny self-upgrading AI simulation.

    It evaluates its current configuration, mutates it to create candidate
    versions, and adopts the best-performing one.
    """

    def __init__(self, state_file: str = "state.json", seed: int = 42) -> None:
        self.state_path = Path(state_file)
        self.rng = Random(seed)
        self.config = self._load_state()

    def _load_state(self) -> BrainConfig:
        if not self.state_path.exists():
            return BrainConfig()

        data = json.loads(self.state_path.read_text())
        return BrainConfig(**data)

    def _save_state(self) -> None:
        self.state_path.write_text(json.dumps(asdict(self.config), indent=2))

    def score(self, dataset: Iterable[dict]) -> float:
        """Score quality on a fake benchmark dataset."""
        total = 0.0
        count = 0

        for sample in dataset:
            target_risk = sample["target_risk"]
            target_style = sample["target_style"]

            predicted_risk = 1.0 - self.config.caution
            predicted_style = self.config.creativity

            risk_penalty = abs(target_risk - predicted_risk)
            style_penalty = abs(target_style - predicted_style)

            sample_score = max(0.0, 1.0 - (0.6 * risk_penalty + 0.4 * style_penalty))
            total += sample_score
            count += 1

        return total / max(count, 1)

    def _mutate(self, base: BrainConfig) -> BrainConfig:
        def clamp(value: float) -> float:
            return max(0.0, min(1.0, value))

        return BrainConfig(
            creativity=clamp(base.creativity + self.rng.uniform(-0.2, 0.2)),
            caution=clamp(base.caution + self.rng.uniform(-0.2, 0.2)),
            learning_rate=clamp(base.learning_rate + self.rng.uniform(-0.1, 0.1)),
        )

    def _benchmark(self) -> List[dict]:
        return [
            {"target_risk": 0.1, "target_style": 0.8},
            {"target_risk": 0.3, "target_style": 0.6},
            {"target_risk": 0.2, "target_style": 0.7},
            {"target_risk": 0.4, "target_style": 0.5},
        ]

    def upgrade_once(self, candidates: int = 6) -> dict:
        dataset = self._benchmark()
        best_config = self.config
        best_score = self.score(dataset)

        for _ in range(candidates):
            candidate = self._mutate(best_config)
            old = self.config
            self.config = candidate
            candidate_score = self.score(dataset)
            self.config = old

            if candidate_score > best_score:
                best_config = candidate
                best_score = candidate_score

        improved = best_config != self.config
        old_score = self.score(dataset)
        self.config = best_config
        self._save_state()

        return {
            "improved": improved,
            "old_score": round(old_score, 4),
            "new_score": round(best_score, 4),
            "config": asdict(self.config),
        }

    def run(self, cycles: int = 5) -> list[dict]:
        reports = []
        for _ in range(cycles):
            reports.append(self.upgrade_once())
        return reports
