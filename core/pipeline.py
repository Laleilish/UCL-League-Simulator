"""Data validation and the Streamlit-free pipeline: data -> ratings -> simulation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from time import perf_counter
from typing import IO

import pandas as pd

from core.ratings import RatingConfig, Ratings, estimate_ratings
from core.simulate import SimulationResult, simulate_season
from core.stats import probability_table

REQUIRED_COLUMNS = ("date", "home", "away", "home_goals", "away_goals", "competition")
TEAM_COUNT = 36


class DataValidationError(ValueError):
    def __init__(self, issues: list[str]):
        self.issues = issues
        super().__init__(" ".join(issues))


@dataclass(frozen=True)
class Settings:
    n_sims: int = 10_000
    seed: int = 42
    half_life_days: float = 365.0
    domestic_weight: float = 0.6
    shrinkage: float = 6.0
    home_advantage_mode: str = "auto"
    home_advantage: float = 1.12

    def __post_init__(self) -> None:
        if not 1 <= self.n_sims <= 200_000:
            raise ValueError("Jumlah simulasi harus antara 1 dan 200.000")
        if self.seed < 0:
            raise ValueError("Seed tidak boleh negatif")
        if not 30 <= self.half_life_days <= 3_650:
            raise ValueError("Half-life harus antara 30 dan 3.650 hari")
        if not 0.05 <= self.domestic_weight <= 1.5:
            raise ValueError("Bobot liga domestik harus antara 0,05 dan 1,5")
        if not 0 <= self.shrinkage <= 50:
            raise ValueError("Shrinkage harus antara 0 dan 50")
        if self.home_advantage_mode not in {"auto", "manual"}:
            raise ValueError("Mode home advantage harus 'auto' atau 'manual'")
        if not 0.5 <= self.home_advantage <= 2.5:
            raise ValueError("Home advantage manual harus antara 0,5 dan 2,5")

    def rating_config(self) -> RatingConfig:
        return RatingConfig(
            half_life_days=self.half_life_days,
            domestic_weight=self.domestic_weight,
            shrinkage=self.shrinkage,
            home_advantage=(
                self.home_advantage if self.home_advantage_mode == "manual" else None
            ),
        )


@dataclass
class ModelRun:
    matches: pd.DataFrame
    teams: tuple[str, ...]
    ratings: Ratings
    result: SimulationResult
    settings: Settings
    table: pd.DataFrame
    duration_seconds: float
    latest_played: date | None
    n_played: int
    n_remaining: int

    @property
    def n_domestic(self) -> int:
        competition = self.matches["competition"].astype(str).str.upper()
        return int((~competition.str.startswith("UCL")).sum())

    @property
    def n_sims(self) -> int:
        return int(self.result.n_sims)

    def team_row(self, team: str) -> pd.Series:
        rows = self.table[self.table["team"] == team]
        if rows.empty:
            raise KeyError(f"Tim tidak dikenal: {team}")
        return rows.iloc[0]


def _read_csv(source: str | Path | IO[bytes]) -> pd.DataFrame:
    try:
        if isinstance(source, (str, Path)):
            return pd.read_csv(source)
        return pd.read_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise DataValidationError(["File CSV kosong."]) from exc
    except UnicodeDecodeError:
        if isinstance(source, (str, Path)):
            return pd.read_csv(source, encoding="latin-1")
        raise DataValidationError(["File CSV tidak bisa dibaca sebagai teks UTF-8."])
    except Exception as exc:
        raise DataValidationError([f"File CSV tidak bisa dibaca: {exc}"]) from exc


def load_matches(source: str | Path | IO[bytes]) -> pd.DataFrame:
    """Read and validate a CSV from a path or an uploaded file object."""
    return validate_matches(_read_csv(source))


def validate_matches(matches: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy or raise DataValidationError with readable issues."""
    issues: list[str] = []
    frame = matches.copy()
    frame.columns = [str(column).strip().lower() for column in frame.columns]

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise DataValidationError(
            [f"Kolom wajib tidak ditemukan: {', '.join(missing)}."]
        )
    if frame.empty:
        raise DataValidationError(["Dataset tidak memuat satu baris pun."])

    frame = frame[list(REQUIRED_COLUMNS)]

    frame["home"] = frame["home"].astype("string").str.strip()
    frame["away"] = frame["away"].astype("string").str.strip()
    frame["competition"] = frame["competition"].astype("string").str.strip()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")

    bad_dates = int(frame["date"].isna().sum())
    if bad_dates:
        issues.append(f"{bad_dates} baris punya tanggal yang tidak valid.")

    empty_home = frame["home"].isna() | frame["home"].eq("")
    empty_away = frame["away"].isna() | frame["away"].eq("")
    if empty_home.any() or empty_away.any():
        issues.append("Ada baris tanpa nama tim kandang atau tandang.")

    same_team = frame["home"] == frame["away"]
    if same_team.any():
        issues.append(f"{int(same_team.sum())} laga mempertemukan tim yang sama.")

    empty_competition = (
        frame["competition"].isna() | frame["competition"].eq("")
    )
    if empty_competition.any():
        issues.append("Ada baris tanpa nama kompetisi.")

    raw_home = frame["home_goals"]
    raw_away = frame["away_goals"]
    frame["home_goals"] = pd.to_numeric(raw_home, errors="coerce")
    frame["away_goals"] = pd.to_numeric(raw_away, errors="coerce")

    def _bad_numeric(raw: pd.Series, parsed: pd.Series) -> pd.Series:
        text = raw.astype("string").str.strip()
        return parsed.isna() & text.notna() & text.ne("")

    bad_goals = _bad_numeric(raw_home, frame["home_goals"]) | _bad_numeric(
        raw_away, frame["away_goals"]
    )
    if bad_goals.any():
        issues.append(f"{int(bad_goals.sum())} baris punya gol yang bukan angka.")

    one_sided = frame["home_goals"].isna() != frame["away_goals"].isna()
    if one_sided.any():
        issues.append(
            "Gol kandang dan tandang harus diisi keduanya atau dikosongkan keduanya."
        )

    played_mask = frame["home_goals"].notna() & frame["away_goals"].notna()
    played_goals = frame.loc[played_mask, ["home_goals", "away_goals"]]
    if (played_goals < 0).any().any():
        issues.append("Gol tidak boleh negatif.")
    fractional = (played_goals % 1).abs() > 1e-9
    if fractional.any().any():
        issues.append("Gol harus berupa bilangan bulat.")

    frame["competition"] = frame["competition"].astype(str).str.strip()
    frame["competition"] = frame["competition"].where(
        frame["competition"].str.upper() != "UCL", "UCL"
    )

    normalized_competition = frame["competition"].str.upper()
    ucl_mask = normalized_competition.eq("UCL")
    if not ucl_mask.any():
        raise DataValidationError(["Dataset harus memuat laga UCL."])

    ucl_teams = set(frame.loc[ucl_mask, "home"]) | set(frame.loc[ucl_mask, "away"])
    ucl_teams.discard(None)
    if len(ucl_teams) != TEAM_COUNT:
        issues.append(
            f"Laga UCL harus memuat tepat {TEAM_COUNT} tim, ditemukan {len(ucl_teams)}."
        )

    if issues:
        raise DataValidationError(issues)

    frame = frame.dropna(subset=["date"])
    frame = frame.sort_values(
        ["date", "competition", "home"], ignore_index=True
    )
    return frame


def dataset_summary(matches: pd.DataFrame) -> dict[str, object]:
    competition = matches["competition"].astype(str).str.upper()
    is_ucl = competition.eq("UCL")
    is_history = competition.str.startswith("UCL") & ~is_ucl
    is_domestic = ~competition.str.startswith("UCL")

    ucl = matches[is_ucl]
    played = matches.dropna(subset=["home_goals", "away_goals"])
    ucl_played = ucl.dropna(subset=["home_goals", "away_goals"])
    return {
        "matches": len(matches),
        "domestic": int(is_domestic.sum()),
        "ucl": len(ucl),
        "ucl_history": int(is_history.sum()),
        "played": len(played),
        "ucl_played": len(ucl_played),
        "ucl_remaining": len(ucl) - len(ucl_played),
        "teams": len(set(ucl["home"]) | set(ucl["away"])),
        "competitions": int(matches.loc[is_domestic, "competition"].nunique()),
        "first_date": matches["date"].min().date(),
        "last_played": played["date"].max().date(),
        "last_date": matches["date"].max().date(),
    }


def _to_date(value: object) -> date | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return pd.Timestamp(value).date()


def run_pipeline(matches: pd.DataFrame, settings: Settings | None = None) -> ModelRun:
    """Estimate ratings and simulate the season. No Streamlit imports here."""
    settings = settings or Settings()
    started = perf_counter()
    clean = validate_matches(matches)

    ucl = clean[clean["competition"].eq("UCL")]
    teams = tuple(sorted(set(ucl["home"]) | set(ucl["away"])))

    all_teams = tuple(
        sorted(set(clean["home"]) | set(clean["away"]))
    )
    fitted = estimate_ratings(clean, teams=all_teams, config=settings.rating_config())
    ratings = fitted.subset(teams)

    played = clean.dropna(subset=["home_goals", "away_goals"])
    latest = _to_date(played["date"].max())
    result = simulate_season(
        clean,
        ratings,
        n_sims=settings.n_sims,
        seed=settings.seed,
        home_advantage=(
            settings.home_advantage
            if settings.home_advantage_mode == "manual"
            else ratings.home_advantage
        ),
    )

    return ModelRun(
        matches=clean,
        teams=teams,
        ratings=ratings,
        result=result,
        settings=settings,
        table=probability_table(result),
        duration_seconds=perf_counter() - started,
        latest_played=latest,
        n_played=result.n_played,
        n_remaining=result.n_remaining,
    )
