from auto_upgrade_ai import AutoUpgradeAI


def test_upgrade_creates_state_file(tmp_path):
    state = tmp_path / "state.json"
    ai = AutoUpgradeAI(state_file=str(state), seed=1)

    report = ai.upgrade_once(candidates=10)

    assert state.exists()
    assert report["new_score"] >= report["old_score"]


def test_run_returns_requested_cycles(tmp_path):
    state = tmp_path / "state.json"
    ai = AutoUpgradeAI(state_file=str(state), seed=2)

    reports = ai.run(cycles=3)

    assert len(reports) == 3
