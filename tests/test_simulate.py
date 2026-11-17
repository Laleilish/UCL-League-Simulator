from __future__ import annotations

import numpy as np
import pytest

from core.pipeline import Settings, run_pipeline


def test_acceptance_sums(model):
    result = model.result
    assert result.probability("champion").sum() == pytest.approx(1.0)
    assert result.probability("top8").sum() == pytest.approx(8.0)
    assert result.probability("top24").sum() == pytest.approx(24.0)


def test_stage_probabilities_are_monotonic(model):
    counts = model.result.counts
    assert (counts["champion"] <= counts["final"]).all()
    assert (counts["final"] <= counts["semi"]).all()
    assert (counts["semi"] <= counts["quarter"]).all()
    assert (counts["quarter"] <= counts["r16"]).all()
    assert (counts["r16"] <= counts["top24"]).all()


def test_average_position_is_in_range(model):
    positions = model.result.avg_position
    assert positions.min() >= 1.0
    assert positions.max() <= 36.0
    assert np.isfinite(model.result.avg_points).all()


def test_same_seed_is_identical(matches):
    first = run_pipeline(matches, Settings(n_sims=300, seed=99))
    second = run_pipeline(matches, Settings(n_sims=300, seed=99))
    assert first.table.equals(second.table)
    assert first.result.champion_ids.tolist() == second.result.champion_ids.tolist()


def test_different_seed_changes_results(matches):
    first = run_pipeline(matches, Settings(n_sims=300, seed=1))
    second = run_pipeline(matches, Settings(n_sims=300, seed=2))
    assert not np.array_equal(first.result.counts["champion"], second.result.counts["champion"])


def test_manual_home_advantage_is_used(matches):
    model = run_pipeline(
        matches,
        Settings(n_sims=200, seed=5, home_advantage_mode="manual", home_advantage=1.4),
    )
    assert model.result.home_advantage == pytest.approx(1.4)
