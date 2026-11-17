"""Vectorised Monte Carlo engine and knockout bracket.

The league phase is simulated from the remaining UCL fixtures, then the
playoff (9th-24th), round of 16, quarter-final, semi-final and final are
played per simulation. All randomness comes from one seeded generator so a
run with the same seed and settings is reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from core.ratings import Ratings

STAGES = ("top24", "top8", "r16", "quarter", "semi", "final", "champion")

STAGE_LABELS = {
    "top24": "Top 24",
    "top8": "Top 8",
    "r16": "16 Besar",
    "quarter": "Perempat Final",
    "semi": "Semifinal",
    "final": "Final",
    "champion": "Juara",
}


@dataclass
class SimulationResult:
    teams: tuple[str, ...]
    n_sims: int
    seed: int
    counts: dict[str, np.ndarray]
    avg_points: np.ndarray
    avg_position: np.ndarray
    champion_ids: np.ndarray = field(repr=False)
    n_remaining: int = 0
    n_played: int = 0
    home_advantage: float = 1.0

    def probability(self, stage: str) -> np.ndarray:
        stage = stage.lower()
        if stage not in self.counts:
            raise KeyError(f"Tahap tidak dikenal: {stage}")
        return self.counts[stage] / self.n_sims

    def expected_counts(self, stage: str) -> float:
        return float(self.counts[stage.lower()].sum()) / self.n_sims

    def champion_team(self) -> str:
        return self.teams[int(np.argmax(self.counts["champion"]))]


def _ucl_matches(matches: pd.DataFrame) -> pd.DataFrame:
    is_ucl = matches["competition"].astype(str).str.strip().str.upper().eq("UCL")
    return matches[is_ucl].copy()


def _base_table(
    played: pd.DataFrame, team_index: dict[str, int], n_teams: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    points = np.zeros(n_teams, dtype=float)
    goals_for = np.zeros(n_teams, dtype=float)
    goals_against = np.zeros(n_teams, dtype=float)

    for row in played.itertuples(index=False):
        home = team_index[row.home]
        away = team_index[row.away]
        home_goals = int(row.home_goals)
        away_goals = int(row.away_goals)
        goals_for[home] += home_goals
        goals_for[away] += away_goals
        goals_against[home] += away_goals
        goals_against[away] += home_goals
        if home_goals > away_goals:
            points[home] += 3
        elif home_goals < away_goals:
            points[away] += 3
        else:
            points[home] += 1
            points[away] += 1

    return points, goals_for, goals_against


def simulate_season(
    matches: pd.DataFrame,
    ratings: Ratings,
    n_sims: int = 10_000,
    seed: int = 42,
    home_advantage: float | None = None,
    chunk_size: int = 25_000,
) -> SimulationResult:
    """Run the remaining UCL season ``n_sims`` times."""
    if n_sims < 1:
        raise ValueError("n_sims minimal 1")
    if chunk_size < 1:
        raise ValueError("chunk_size minimal 1")

    ucl = _ucl_matches(matches)
    if ucl.empty:
        raise ValueError("Dataset tidak memuat laga UCL")

    played = ucl.dropna(subset=["home_goals", "away_goals"]).copy()
    remaining = ucl[ucl["home_goals"].isna() & ucl["away_goals"].isna()].copy()

    teams = tuple(ratings.teams)
    team_index = {team: i for i, team in enumerate(teams)}
    unknown = (set(ucl["home"]) | set(ucl["away"])) - set(team_index)
    if unknown:
        raise ValueError(f"Laga UCL memuat tim tanpa rating: {', '.join(sorted(unknown))}")

    n_teams = len(teams)
    base_points, base_for, base_against = _base_table(played, team_index, n_teams)

    home_idx = remaining["home"].map(team_index).to_numpy(dtype=np.int64)
    away_idx = remaining["away"].map(team_index).to_numpy(dtype=np.int64)

    attack = ratings.attack
    defence = ratings.defence
    mu = ratings.mu
    advantage = float(home_advantage if home_advantage is not None else ratings.home_advantage)
    lambda_home = mu * advantage * attack[home_idx] * defence[away_idx]
    lambda_away = mu * attack[away_idx] * defence[home_idx]

    rng = np.random.default_rng(seed)
    counts = {stage: np.zeros(n_teams, dtype=np.int64) for stage in STAGES}
    avg_points = np.zeros(n_teams, dtype=float)
    avg_position = np.zeros(n_teams, dtype=float)
    champion_ids = np.empty(n_sims, dtype=np.int64)

    def add_count(stage: str, ids: np.ndarray) -> None:
        counts[stage] += np.bincount(ids.ravel(), minlength=n_teams)

    def two_legs(first_home: np.ndarray, second_home: np.ndarray) -> np.ndarray:
        first_home = np.asarray(first_home, dtype=np.int64)
        second_home = np.asarray(second_home, dtype=np.int64)
        first_away = second_home
        second_away = first_home

        leg_one_home = rng.poisson(
            mu * advantage * attack[first_home] * defence[first_away]
        )
        leg_one_away = rng.poisson(mu * attack[first_away] * defence[first_home])
        leg_two_home = rng.poisson(
            mu * advantage * attack[second_home] * defence[second_away]
        )
        leg_two_away = rng.poisson(mu * attack[second_away] * defence[second_home])

        aggregate_first = leg_one_home + leg_two_away
        aggregate_second = leg_one_away + leg_two_home
        coin_flip = rng.random(aggregate_first.shape) < 0.5
        return np.where(
            aggregate_first > aggregate_second,
            first_home,
            np.where(
                aggregate_second > aggregate_first,
                second_home,
                np.where(coin_flip, first_home, second_home),
            ),
        )

    def neutral_match(first: np.ndarray, second: np.ndarray) -> np.ndarray:
        first = np.asarray(first, dtype=np.int64)
        second = np.asarray(second, dtype=np.int64)
        goals_first = rng.poisson(mu * attack[first] * defence[second])
        goals_second = rng.poisson(mu * attack[second] * defence[first])
        coin_flip = rng.random(goals_first.shape) < 0.5
        return np.where(
            goals_first > goals_second,
            first,
            np.where(goals_second > goals_first, second, np.where(coin_flip, first, second)),
        )

    for start in range(0, n_sims, chunk_size):
        size = min(chunk_size, n_sims - start)

        points = np.tile(base_points, (size, 1))
        goal_difference = np.tile(base_for - base_against, (size, 1))
        goals_for = np.tile(base_for, (size, 1))

        for fixture in range(len(home_idx)):
            home = int(home_idx[fixture])
            away = int(away_idx[fixture])
            simulated_home = rng.poisson(lambda_home[fixture], size=size)
            simulated_away = rng.poisson(lambda_away[fixture], size=size)

            points[:, home] += np.where(
                simulated_home > simulated_away,
                3,
                np.where(simulated_home == simulated_away, 1, 0),
            )
            points[:, away] += np.where(
                simulated_away > simulated_home,
                3,
                np.where(simulated_home == simulated_away, 1, 0),
            )
            difference = simulated_home - simulated_away
            goal_difference[:, home] += difference
            goal_difference[:, away] -= difference
            goals_for[:, home] += simulated_home
            goals_for[:, away] += simulated_away

        random_tiebreak = rng.random((size, n_teams))
        score = (
            points * 1e8
            + (goal_difference + 200.0) * 1e5
            + goals_for * 1e2
            + random_tiebreak
        )
        order = np.argsort(-score, axis=1, kind="stable")

        position = np.empty_like(order)
        np.put_along_axis(position, order, np.arange(n_teams, dtype=np.int64), axis=1)

        avg_points += points.sum(axis=0)
        avg_position += (position + 1).sum(axis=0)
        add_count("top24", order[:, :24])
        add_count("top8", order[:, :8])

        direct = order[:, :8]
        playoff = order[:, 8:24]
        higher_seed = playoff[:, :8]
        lower_seed = playoff[:, 15:7:-1]
        playoff_winners = two_legs(lower_seed, higher_seed)
        add_count("r16", np.concatenate((direct, playoff_winners), axis=1))

        round_of_16 = two_legs(playoff_winners[:, ::-1], direct)
        add_count("quarter", round_of_16)

        quarter_winners = two_legs(round_of_16[:, 0::2], round_of_16[:, 1::2])
        add_count("semi", quarter_winners)

        semi_winners = two_legs(quarter_winners[:, 0::2], quarter_winners[:, 1::2])
        add_count("final", semi_winners)

        champion = neutral_match(semi_winners[:, 0], semi_winners[:, 1])
        add_count("champion", champion)
        champion_ids[start : start + size] = champion

    return SimulationResult(
        teams=teams,
        n_sims=n_sims,
        seed=seed,
        counts=counts,
        avg_points=avg_points / n_sims,
        avg_position=avg_position / n_sims,
        champion_ids=champion_ids,
        n_remaining=int(len(remaining)),
        n_played=int(len(played)),
        home_advantage=advantage,
    )
