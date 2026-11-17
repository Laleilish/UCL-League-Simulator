from __future__ import annotations

import numpy as np
import pytest

from core.stats import (
    brier_score,
    convergence_curve,
    head_to_head,
    poisson_chi_square,
    two_leg_qualification,
    wilson_interval,
)


def test_wilson_interval_reasonable():
    low, high = wilson_interval(50, 100)
    assert low == pytest.approx(0.4038, abs=1e-3)
    assert high == pytest.approx(0.5962, abs=1e-3)

    low, high = wilson_interval(0, 100)
    assert low == 0.0
    assert 0.0 < high < 0.05

    low, high = wilson_interval(100, 100)
    assert high == pytest.approx(1.0)
    assert 0.95 < low < 1.0


def test_wilson_band_narrows_with_more_simulations():
    small = wilson_interval(50, 100)
    large = wilson_interval(500, 1_000)
    assert (large[1] - large[0]) < (small[1] - small[0])


def test_head_to_head_is_a_distribution(model):
    result = head_to_head(model.ratings, "Bayern Munich", "Arsenal")
    assert result.outcome_total == pytest.approx(1.0)
    assert result.matrix.sum() == pytest.approx(1.0)
    assert result.exp_goals_a > 0
    assert result.exp_goals_b > 0
    assert result.most_likely_score[0] >= 0
    assert result.most_likely_score[1] >= 0


def test_home_side_has_an_advantage(model):
    home = head_to_head(model.ratings, "Bayern Munich", "Arsenal", neutral=False)
    neutral = head_to_head(model.ratings, "Bayern Munich", "Arsenal", neutral=True)
    assert home.p_a > neutral.p_a
    assert home.exp_goals_a > neutral.exp_goals_a


def test_two_leg_probabilities_sum_to_one(model):
    result = two_leg_qualification(model.ratings, "Bayern Munich", "Arsenal")
    assert result["a"] + result["b"] == pytest.approx(1.0)
    assert 0 < result["aggregate_draw"] < 1
    assert result["exp_goals_a"] > 0
    assert result["exp_goals_b"] > 0


def test_chi_square_structure(matches):
    played = matches.dropna(subset=["home_goals", "away_goals"])
    goals = np.concatenate(
        [played["home_goals"].to_numpy(float), played["away_goals"].to_numpy(float)]
    )
    result = poisson_chi_square(goals)
    assert result.statistic >= 0
    assert result.dof >= 1
    assert 0 <= result.p_value <= 1
    assert sum(result.observed) == pytest.approx(len(goals))
    assert sum(result.expected) == pytest.approx(len(goals), abs=1e-6)
    assert len(result.labels) == len(result.observed) == len(result.expected)


def test_brier_score_components(model):
    result = brier_score(model.matches, model.ratings)
    assert result.home + result.draw + result.away == pytest.approx(result.score)
    assert 0 < result.score < 2
    assert result.n_matches == int(
        model.matches.dropna(subset=["home_goals", "away_goals"])
        .loc[
            lambda frame: frame["home"].isin(model.ratings.teams)
            & frame["away"].isin(model.ratings.teams)
        ]
        .shape[0]
    )


def test_convergence_curve_narrows(model):
    curve = convergence_curve(model.result, 0)
    assert curve["simulasi"].iloc[-1] == model.n_sims
    widths = curve["batas_atas"] - curve["batas_bawah"]
    assert widths.iloc[-1] <= widths.iloc[0]
    assert (curve["batas_bawah"] <= curve["peluang"]).all()
    assert (curve["peluang"] <= curve["batas_atas"]).all()
