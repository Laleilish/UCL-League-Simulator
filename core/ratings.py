"""Team strength estimation for the SiKupingBesar Poisson model.

Goals are modelled as

    lambda_home = mu * H * attack[home] * defence[away]
    lambda_away = mu * attack[away] * defence[home]

where a larger ``defence`` value means a weaker defence. Parameters are fitted
with a weighted iterative maximum-likelihood scheme and shrunk towards 1 so
teams with only a handful of matches do not get extreme ratings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("date", "home", "away", "home_goals", "away_goals", "competition")


@dataclass(frozen=True)
class RatingConfig:
    half_life_days: float = 365.0
    domestic_weight: float = 0.6
    shrinkage: float = 6.0
    max_iter: int = 80
    tolerance: float = 1e-7
    home_advantage: float | None = None
    reference_date: date | None = None

    def __post_init__(self) -> None:
        if self.half_life_days <= 0:
            raise ValueError("half_life_days harus lebih besar dari 0")
        if self.domestic_weight <= 0:
            raise ValueError("domestic_weight harus lebih besar dari 0")
        if self.shrinkage < 0:
            raise ValueError("shrinkage tidak boleh negatif")


@dataclass
class Ratings:
    teams: tuple[str, ...]
    attack: np.ndarray
    defence: np.ndarray
    mu: float
    home_advantage: float
    n_matches: np.ndarray
    reference_date: date | None
    config: RatingConfig = field(repr=False)
    matches_used: int = 0

    def index(self, team: str) -> int:
        try:
            return self.teams.index(team)
        except ValueError as exc:
            raise KeyError(f"Tim tidak dikenal: {team}") from exc

    def attack_of(self, team: str) -> float:
        return float(self.attack[self.index(team)])

    def defence_of(self, team: str) -> float:
        return float(self.defence[self.index(team)])

    def subset(self, teams: list[str] | tuple[str, ...]) -> "Ratings":
        """Keep a subset of teams while preserving the fitted parameters."""
        indices = [self.index(team) for team in teams]
        return Ratings(
            teams=tuple(teams),
            attack=self.attack[indices],
            defence=self.defence[indices],
            mu=self.mu,
            home_advantage=self.home_advantage,
            n_matches=self.n_matches[indices],
            reference_date=self.reference_date,
            config=self.config,
            matches_used=self.matches_used,
        )

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "team": self.teams,
                "attack": self.attack,
                "defence": self.defence,
                "matches": self.n_matches,
            }
        ).sort_values("attack", ascending=False, ignore_index=True)


def _check_columns(matches: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in matches.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(missing)}")


def _played(matches: pd.DataFrame) -> pd.DataFrame:
    _check_columns(matches)
    goals = matches.dropna(subset=["home_goals", "away_goals"]).copy()
    if goals.empty:
        raise ValueError("Tidak ada laga yang sudah dimainkan pada dataset")
    goals["home_goals"] = goals["home_goals"].astype(float)
    goals["away_goals"] = goals["away_goals"].astype(float)
    return goals


def estimate_ratings(
    matches: pd.DataFrame,
    teams: list[str] | tuple[str, ...] | None = None,
    config: RatingConfig | None = None,
) -> Ratings:
    """Fit attack, defence, mu, and home advantage from played matches."""
    config = config or RatingConfig()
    played = _played(matches)
    if teams is None:
        teams = tuple(sorted(set(played["home"]) | set(played["away"])))
    else:
        teams = tuple(teams)

    team_index = {team: i for i, team in enumerate(teams)}
    unknown = (set(played["home"]) | set(played["away"])) - set(team_index)
    if unknown:
        raise ValueError(f"Tim tanpa rating: {', '.join(sorted(unknown))}")

    home_idx = played["home"].map(team_index).to_numpy(dtype=np.int64)
    away_idx = played["away"].map(team_index).to_numpy(dtype=np.int64)
    home_goals = played["home_goals"].to_numpy(dtype=np.float64)
    away_goals = played["away_goals"].to_numpy(dtype=np.float64)

    dates = pd.to_datetime(played["date"]).dt.date
    reference_date = config.reference_date or dates.max()
    age_days = np.array([max((reference_date - day).days, 0) for day in dates], dtype=float)
    decay = np.power(0.5, age_days / config.half_life_days)
    competition = played["competition"].astype(str).str.strip().str.upper()
    is_ucl = competition.str.startswith("UCL")
    competition_weight = np.where(is_ucl, 1.0, config.domestic_weight)
    weights = decay * competition_weight

    if not np.isfinite(weights).all() or weights.sum() <= 0:
        raise ValueError("Bobot laga tidak valid; periksa tanggal dan competition")

    n_teams = len(teams)
    attack = np.ones(n_teams)
    defence = np.ones(n_teams)
    total_goals = float(np.sum(weights * (home_goals + away_goals)))
    mu = max(total_goals / float(np.sum(weights) * 2.0), 0.2)
    fixed_home = config.home_advantage
    home_advantage = float(fixed_home) if fixed_home is not None else 1.1
    shrinkage = float(config.shrinkage)

    team_weight = np.bincount(home_idx, weights=weights, minlength=n_teams)
    team_weight += np.bincount(away_idx, weights=weights, minlength=n_teams)
    denominator_weight = np.where(team_weight > 0, team_weight, 1.0)
    match_count = np.bincount(home_idx, minlength=n_teams)
    match_count += np.bincount(away_idx, minlength=n_teams)

    for _ in range(config.max_iter):
        home_exposure = mu * home_advantage * attack[home_idx] * defence[away_idx]
        away_exposure = mu * attack[away_idx] * defence[home_idx]

        scored = np.bincount(home_idx, weights=weights * home_goals, minlength=n_teams)
        scored += np.bincount(away_idx, weights=weights * away_goals, minlength=n_teams)
        scored_exposure = np.bincount(
            home_idx,
            weights=weights * mu * home_advantage * defence[away_idx],
            minlength=n_teams,
        )
        scored_exposure += np.bincount(
            away_idx,
            weights=weights * mu * defence[home_idx],
            minlength=n_teams,
        )

        conceded = np.bincount(home_idx, weights=weights * away_goals, minlength=n_teams)
        conceded += np.bincount(away_idx, weights=weights * home_goals, minlength=n_teams)
        conceded_exposure = np.bincount(
            home_idx,
            weights=weights * mu * attack[away_idx],
            minlength=n_teams,
        )
        conceded_exposure += np.bincount(
            away_idx,
            weights=weights * mu * home_advantage * attack[home_idx],
            minlength=n_teams,
        )

        new_attack = (scored + shrinkage) / (scored_exposure + shrinkage)
        new_defence = (conceded + shrinkage) / (conceded_exposure + shrinkage)

        new_attack = np.where(team_weight > 0, new_attack, 1.0)
        new_defence = np.where(team_weight > 0, new_defence, 1.0)
        new_attack /= float(np.average(new_attack, weights=denominator_weight))
        new_defence /= float(np.average(new_defence, weights=denominator_weight))

        new_mu = total_goals / float(
            np.sum(
                weights
                * (
                    home_advantage * new_attack[home_idx] * new_defence[away_idx]
                    + new_attack[away_idx] * new_defence[home_idx]
                )
            )
        )

        if fixed_home is None:
            home_expectation = np.sum(
                weights * new_mu * new_attack[home_idx] * new_defence[away_idx]
            )
            new_home = float(np.sum(weights * home_goals) / max(home_expectation, 1e-9))
            new_home = float(np.clip(new_home, 0.75, 2.0))
        else:
            new_home = float(fixed_home)

        delta = max(
            float(np.max(np.abs(new_attack - attack))),
            float(np.max(np.abs(new_defence - defence))),
            abs(new_mu - mu) / max(mu, 1e-9),
            abs(new_home - home_advantage),
        )
        attack, defence, mu, home_advantage = new_attack, new_defence, new_mu, new_home
        if delta < config.tolerance:
            break

    return Ratings(
        teams=teams,
        attack=np.asarray(attack, dtype=float),
        defence=np.asarray(defence, dtype=float),
        mu=float(mu),
        home_advantage=float(home_advantage),
        n_matches=match_count,
        reference_date=reference_date,
        config=config,
        matches_used=int(len(played)),
    )
