from __future__ import annotations

import pandas as pd
import pytest

from core.pipeline import (
    DataValidationError,
    Settings,
    dataset_summary,
    load_matches,
    validate_matches,
)


def test_bundled_data_is_valid(matches):
    summary = dataset_summary(matches)
    assert summary["teams"] == 36
    assert summary["competitions"] == 11
    assert summary["domestic"] > 1_000
    assert summary["ucl"] == 144
    assert summary["ucl_remaining"] > 0
    assert summary["ucl_played"] == summary["ucl"] - summary["ucl_remaining"]


def test_missing_column_is_rejected(matches):
    broken = matches.drop(columns=["date"])
    with pytest.raises(DataValidationError) as exc:
        validate_matches(broken)
    assert "date" in str(exc.value)


def test_one_sided_goals_are_rejected(matches):
    broken = matches.copy()
    index = broken.dropna(subset=["home_goals"]).index[0]
    broken.loc[index, "away_goals"] = None
    with pytest.raises(DataValidationError) as exc:
        validate_matches(broken)
    assert "keduanya" in str(exc.value)


def test_non_numeric_goals_are_rejected(matches):
    broken = matches.copy()
    index = broken.dropna(subset=["home_goals"]).index[0]
    broken["home_goals"] = broken["home_goals"].astype(object)
    broken.loc[index, "home_goals"] = "banyak"
    with pytest.raises(DataValidationError) as exc:
        validate_matches(broken)
    assert "bukan angka" in str(exc.value)


def test_wrong_ucl_team_count_is_rejected(matches):
    ucl = matches[matches["competition"] == "UCL"].head(10)
    domestic = matches[matches["competition"] != "UCL"]
    broken = pd.concat([domestic, ucl], ignore_index=True)
    with pytest.raises(DataValidationError) as exc:
        validate_matches(broken)
    assert "36 tim" in str(exc.value)


def test_same_team_is_rejected(matches):
    broken = matches.copy()
    broken.loc[0, "away"] = broken.loc[0, "home"]
    with pytest.raises(DataValidationError) as exc:
        validate_matches(broken)
    assert "tim yang sama" in str(exc.value)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_sims": 0},
        {"n_sims": 200_001},
        {"half_life_days": 10},
        {"domestic_weight": 2.0},
        {"home_advantage_mode": "sesukanya"},
    ],
)
def test_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        Settings(**kwargs)


def test_load_from_buffer(matches):
    buffer = matches.to_csv(index=False).encode("utf-8")
    import io

    loaded = load_matches(io.BytesIO(buffer))
    assert len(loaded) == len(matches)
    assert loaded["competition"].eq("UCL").sum() == 144
