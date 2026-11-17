"""Statistics used by the app: intervals, convergence, validation, head-to-head."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from core.ratings import Ratings
from core.simulate import STAGES, SimulationResult


@dataclass(frozen=True)
class ChiSquareResult:
    statistic: float
    dof: int
    p_value: float
    n_observations: int
    mean_goals: float
    labels: tuple[str, ...]
    observed: tuple[float, ...]
    expected: tuple[float, ...]

    @property
    def reject_null(self) -> bool:
        return bool(self.p_value < 0.05)

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "gol": self.labels,
                "observasi": self.observed,
                "harapan_poisson": self.expected,
            }
        )


@dataclass(frozen=True)
class BrierResult:
    score: float
    baseline: float
    home: float
    draw: float
    away: float
    n_matches: int

    @property
    def beats_baseline(self) -> bool:
        return self.score < self.baseline


@dataclass(frozen=True)
class HeadToHeadResult:
    team_a: str
    team_b: str
    neutral: bool
    matrix: np.ndarray
    p_a: float
    p_draw: float
    p_b: float
    exp_goals_a: float
    exp_goals_b: float
    most_likely_score: tuple[int, int]

    @property
    def outcome_total(self) -> float:
        return self.p_a + self.p_draw + self.p_b


def wilson_interval(successes: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n <= 0:
        return 0.0, 0.0
    p = float(successes) / n
    denominator = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denominator
    margin = (
        z * np.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denominator
    )
    return float(max(0.0, centre - margin)), float(min(1.0, centre + margin))


def probability_table(result: SimulationResult) -> pd.DataFrame:
    """Full 36-team probability table, values in percent, sorted by title odds."""
    champion = result.probability("champion")
    rows = []
    for index, team in enumerate(result.teams):
        low, high = wilson_interval(int(result.counts["champion"][index]), result.n_sims)
        row = {
            "team": team,
            "champion": champion[index] * 100.0,
            "ci_low": low * 100.0,
            "ci_high": high * 100.0,
            "final": result.probability("final")[index] * 100.0,
            "semi": result.probability("semi")[index] * 100.0,
            "quarter": result.probability("quarter")[index] * 100.0,
            "r16": result.probability("r16")[index] * 100.0,
            "top8": result.probability("top8")[index] * 100.0,
            "top24": result.probability("top24")[index] * 100.0,
            "avg_points": float(result.avg_points[index]),
            "avg_position": float(result.avg_position[index]),
        }
        rows.append(row)
    return (
        pd.DataFrame(rows)
        .sort_values(["champion", "final", "avg_points"], ascending=False)
        .reset_index(drop=True)
    )


def stage_matrix(result: SimulationResult) -> np.ndarray:
    """Stage probabilities as an (teams x stages) array, in percent."""
    return np.column_stack([result.probability(stage) for stage in STAGES]) * 100.0


def convergence_checkpoints(n_sims: int) -> list[int]:
    candidates = [100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]
    points = [value for value in candidates if value < n_sims]
    points.append(n_sims)
    return sorted(set(points))


def convergence_curve(
    result: SimulationResult, team_index: int, z: float = 1.96
) -> pd.DataFrame:
    """Cumulative title probability and Wilson band over the simulation run."""
    hits = (result.champion_ids == team_index).astype(np.int64)
    cumulative = np.cumsum(hits)
    rows = []
    for n in convergence_checkpoints(result.n_sims):
        successes = int(cumulative[n - 1])
        low, high = wilson_interval(successes, n, z=z)
        rows.append(
            {
                "simulasi": n,
                "peluang": successes / n * 100.0,
                "batas_bawah": low * 100.0,
                "batas_atas": high * 100.0,
            }
        )
    return pd.DataFrame(rows)


def poisson_chi_square(goals: pd.Series | np.ndarray) -> ChiSquareResult:
    """Goodness-of-fit test of goals against a Poisson distribution."""
    values = np.asarray(goals, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 10:
        raise ValueError("Butuh minimal 10 gol untuk uji Chi-square")

    mean = float(values.mean())
    threshold = 5
    upper = min(5, int(np.max(values)))
    labels = [str(goals_count) for goals_count in range(upper)]
    observed = [float(np.sum(values == goals_count)) for goals_count in range(upper)]

    tail_probability = 1.0 - scipy_stats.poisson.cdf(upper - 1, mean)
    expected = [
        float(values.size * scipy_stats.poisson.pmf(goals_count, mean))
        for goals_count in range(upper)
    ]
    expected.append(float(values.size * tail_probability))
    observed.append(float(np.sum(values >= upper)))
    labels.append(f"{upper}+")

    while len(expected) > 2 and (expected[-1] < 5 or expected[-2] < 5):
        expected[-2] += expected[-1]
        observed[-2] += observed[-1]
        labels[-2] = f"{labels[-2]}+"
        expected.pop()
        observed.pop()
        labels.pop()

    while len(expected) > 2 and expected[0] < 5:
        expected[1] += expected[0]
        observed[1] += observed[0]
        labels[1] = f"0-{labels[1]}"
        expected.pop(0)
        observed.pop(0)
        labels.pop(0)

    statistic = float(
        np.sum((np.asarray(observed) - np.asarray(expected)) ** 2 / np.asarray(expected))
    )
    dof = max(len(expected) - 2, 1)
    p_value = float(scipy_stats.chi2.sf(statistic, dof))
    return ChiSquareResult(
        statistic=statistic,
        dof=dof,
        p_value=p_value,
        n_observations=int(values.size),
        mean_goals=mean,
        labels=tuple(labels),
        observed=tuple(observed),
        expected=tuple(expected),
    )


def _poisson_pmf(lam: float, max_goals: int) -> np.ndarray:
    goals = np.arange(max_goals + 1)
    return scipy_stats.poisson.pmf(goals, max(lam, 1e-9))


def score_matrix(
    lambda_a: float, lambda_b: float, max_goals: int = 10
) -> np.ndarray:
    return np.outer(_poisson_pmf(lambda_a, max_goals), _poisson_pmf(lambda_b, max_goals))


def _lambdas(
    ratings: Ratings, team_a: str, team_b: str, neutral: bool
) -> tuple[float, float]:
    index_a = ratings.index(team_a)
    index_b = ratings.index(team_b)
    home_factor = 1.0 if neutral else ratings.home_advantage
    lambda_a = (
        ratings.mu * home_factor * ratings.attack[index_a] * ratings.defence[index_b]
    )
    lambda_b = ratings.mu * ratings.attack[index_b] * ratings.defence[index_a]
    return float(lambda_a), float(lambda_b)


def head_to_head(
    ratings: Ratings,
    team_a: str,
    team_b: str,
    neutral: bool = False,
    max_goals: int = 8,
) -> HeadToHeadResult:
    lambda_a, lambda_b = _lambdas(ratings, team_a, team_b, neutral)
    matrix = score_matrix(lambda_a, lambda_b, max_goals=max_goals)
    total = float(matrix.sum())
    matrix = matrix / total

    p_a = float(np.tril(matrix, -1).sum())
    p_draw = float(np.trace(matrix))
    p_b = float(np.triu(matrix, 1).sum())
    best = np.unravel_index(int(np.argmax(matrix)), matrix.shape)

    return HeadToHeadResult(
        team_a=team_a,
        team_b=team_b,
        neutral=neutral,
        matrix=matrix,
        p_a=p_a,
        p_draw=p_draw,
        p_b=p_b,
        exp_goals_a=lambda_a,
        exp_goals_b=lambda_b,
        most_likely_score=(int(best[0]), int(best[1])),
    )


def _difference_pmf(lambda_a: float, lambda_b: float, max_goals: int) -> np.ndarray:
    matrix = score_matrix(lambda_a, lambda_b, max_goals=max_goals)
    difference = np.zeros(2 * max_goals + 1)
    for goals_a in range(max_goals + 1):
        for goals_b in range(max_goals + 1):
            difference[max_goals + goals_a - goals_b] += matrix[goals_a, goals_b]
    return difference


def two_leg_qualification(
    ratings: Ratings, team_a: str, team_b: str, max_goals: int = 10
) -> dict[str, float]:
    """Probability of advancing over two legs; aggregate draw is a 50:50 coin flip."""
    first_a, first_b = _lambdas(ratings, team_a, team_b, neutral=False)
    second_a, second_b = _lambdas(ratings, team_b, team_a, neutral=False)

    first_difference = _difference_pmf(first_a, first_b, max_goals)
    second_difference = _difference_pmf(second_a, second_b, max_goals)
    aggregate = np.convolve(first_difference, second_difference, mode="full")

    offsets = np.arange(-(2 * max_goals), 2 * max_goals + 1)
    p_a = float(aggregate[offsets > 0].sum() + 0.5 * aggregate[offsets == 0].sum())
    p_draw = float(aggregate[offsets == 0].sum())
    return {
        "a": p_a,
        "b": 1.0 - p_a,
        "aggregate_draw": p_draw,
        "exp_goals_a": first_a + second_a,
        "exp_goals_b": first_b + second_b,
    }


def brier_score(matches: pd.DataFrame, ratings: Ratings) -> BrierResult:
    """Multiclass (1X2) Brier score on played matches, in-sample."""
    played = matches.dropna(subset=["home_goals", "away_goals"])
    if played.empty:
        raise ValueError("Tidak ada laga untuk dihitung Brier score")

    components = np.zeros(3)
    index = {team: i for i, team in enumerate(ratings.teams)}
    count = 0
    for row in played.itertuples(index=False):
        home = row.home
        away = row.away
        if home not in index or away not in index:
            continue
        lambda_home, lambda_away = _lambdas(ratings, home, away, neutral=False)
        matrix = score_matrix(lambda_home, lambda_away, max_goals=10)
        p_home = float(np.tril(matrix, -1).sum())
        p_draw = float(np.trace(matrix))
        p_away = float(np.triu(matrix, 1).sum())
        probabilities = np.array([p_home, p_draw, p_away])
        probabilities /= probabilities.sum()

        home_goals = int(row.home_goals)
        away_goals = int(row.away_goals)
        outcome = 0 if home_goals > away_goals else (1 if home_goals == away_goals else 2)
        target = np.zeros(3)
        target[outcome] = 1.0
        components += (probabilities - target) ** 2
        count += 1

    if count == 0:
        raise ValueError("Tidak ada laga dengan tim yang memiliki rating")
    components /= count
    return BrierResult(
        score=float(components.sum()),
        baseline=2.0 / 3.0,
        home=float(components[0]),
        draw=float(components[1]),
        away=float(components[2]),
        n_matches=count,
    )
