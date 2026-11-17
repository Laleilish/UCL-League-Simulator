from __future__ import annotations

import numpy as np
import pytest

from core.ratings import RatingConfig, estimate_ratings


def test_ratings_are_normalised_and_finite(matches):
    teams = sorted(set(matches["home"]) | set(matches["away"]))
    ratings = estimate_ratings(matches, teams=teams)

    played = matches.dropna(subset=["home_goals", "away_goals"])
    expected = set(played["home"]) | set(played["away"])
    assert expected <= set(ratings.teams)

    ucl = matches[matches["competition"] == "UCL"]
    ucl_teams = sorted(set(ucl["home"]) | set(ucl["away"]))
    assert len(ucl_teams) == 36
    assert len(ratings.subset(ucl_teams).teams) == 36
    assert np.isfinite(ratings.attack).all()
    assert np.isfinite(ratings.defence).all()
    assert (ratings.attack > 0).all()
    assert (ratings.defence > 0).all()
    assert 0.75 <= ratings.home_advantage <= 2.0
    assert ratings.mu > 0
    assert ratings.n_matches.sum() == 2 * ratings.matches_used


def test_strong_teams_rate_higher(matches):
    ratings = estimate_ratings(matches)

    def strength(team: str) -> float:
        return ratings.attack_of(team) / ratings.defence_of(team)

    assert strength("Real Madrid") > strength("Slavia Praha")
    assert strength("Bayern Munich") > strength("FC Copenhagen")
    assert strength("Arsenal") > strength("Qarabag")


def test_manual_home_advantage_is_kept(matches):
    ratings = estimate_ratings(
        matches, config=RatingConfig(home_advantage=1.30)
    )
    assert ratings.home_advantage == pytest.approx(1.30)


def test_half_life_changes_ratings(matches):
    long_memory = estimate_ratings(
        matches, config=RatingConfig(half_life_days=1_095)
    )
    short_memory = estimate_ratings(
        matches, config=RatingConfig(half_life_days=90)
    )
    assert not np.allclose(long_memory.attack, short_memory.attack)


def test_domestic_weight_changes_ratings(matches):
    heavy = estimate_ratings(matches, config=RatingConfig(domestic_weight=1.0))
    light = estimate_ratings(matches, config=RatingConfig(domestic_weight=0.1))
    assert not np.allclose(heavy.attack, light.attack)


def test_subset_keeps_parameters(matches):
    ratings = estimate_ratings(matches)
    teams = list(ratings.teams[:5])
    subset = ratings.subset(teams)
    assert subset.teams == tuple(teams)
    np.testing.assert_allclose(subset.attack, ratings.attack[:5])
    np.testing.assert_allclose(subset.n_matches, ratings.n_matches[:5])
