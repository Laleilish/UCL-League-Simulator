"""Build the app dataset from the domestic and UCL source CSVs.

Sources in ``data/``:

- 11 domestic league files from football-data.co.uk (``E0.csv`` ... ``SC0.csv``)
  with 2026/27 results,
- ``ucl_2025_26.csv`` with the complete 2025/26 UCL (used as history for the
  rating model),
- ``ucl_2026_27_teams.csv`` with the 36 clubs in the 2026/27 UCL.

The script maps club names to one spelling, attaches the historical UCL
results, and generates the 2026/27 UCL league phase for the new 36-team field.
Those 144 fixtures are left without goals, so the app forecasts the whole
league phase. The combined dataset is written to ``data/matches.csv``.

Usage:
    python build_dataset.py
    python build_dataset.py --out data/matches.csv --seed 20262027
"""

from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from core.pipeline import dataset_summary, validate_matches
from generate_sample_data import balance_home_games, circle_rounds

LEAGUES: dict[str, str] = {
    "E0": "Premier League",
    "SP1": "La Liga",
    "D1": "Bundesliga",
    "I1": "Serie A",
    "F1": "Ligue 1",
    "N1": "Eredivisie",
    "B1": "Pro League",
    "P1": "Primeira Liga",
    "T1": "Super Lig",
    "G1": "Super League Greece",
    "SC0": "Scottish Premiership",
}

# One spelling per club across the domestic files, the UCL history, and the
# 2026/27 participant list.
ALIASES: dict[str, str] = {
    "AEK": "AEK Athens",
    "Ath Madrid": "Atletico Madrid",
    "Ath Bilbao": "Athletic Club",
    "Atleti": "Atletico Madrid",
    "Atlético de Madrid": "Atletico Madrid",
    "B. Dortmund": "Borussia Dortmund",
    "Bayern München": "Bayern Munich",
    "Betis": "Real Betis",
    "Bodø/Glimt": "Bodo/Glimt",
    "Copenhagen": "FC Copenhagen",
    "Dortmund": "Borussia Dortmund",
    "Ein Frankfurt": "Eintracht Frankfurt",
    "Fenerbahçe": "Fenerbahce",
    "Frankfurt": "Eintracht Frankfurt",
    "Leipzig": "RB Leipzig",
    "Leverkusen": "Bayer Leverkusen",
    "Man City": "Manchester City",
    "Man United": "Manchester United",
    "Newcastle": "Newcastle United",
    "Nott'm Forest": "Nottingham Forest",
    "Olympiakos": "Olympiacos",
    "Paris": "Paris Saint-Germain",
    "Paris SG": "Paris Saint-Germain",
    "PSV Eindhoven": "PSV",
    "Sp Braga": "Braga",
    "Sp Lisbon": "Sporting CP",
    "Stuttgart": "VfB Stuttgart",
    "Tottenham": "Tottenham Hotspur",
    "Union SG": "Union Saint-Gilloise",
}

UCL_HISTORY = "UCL 2025/26"
UCL_HISTORY_FILE = "ucl_2025_26.csv"
UCL_TEAMS_FILE = "ucl_2026_27_teams.csv"
UCL_TEAM_COUNT = 36

UCL_MATCHDAYS = [
    date(2026, 9, 16),
    date(2026, 9, 30),
    date(2026, 10, 21),
    date(2026, 11, 4),
    date(2026, 11, 25),
    date(2026, 12, 9),
    date(2027, 1, 20),
    date(2027, 1, 28),
]

SOURCE_COLUMNS = ("Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG")
OUTPUT_COLUMNS = ["date", "home", "away", "home_goals", "away_goals", "competition"]


def _names(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().replace(ALIASES)


def load_league(path: Path, competition: str) -> pd.DataFrame:
    frame = pd.read_csv(path, encoding="utf-8-sig", usecols=list(SOURCE_COLUMNS))
    frame = frame.rename(
        columns={
            "Date": "date",
            "HomeTeam": "home",
            "AwayTeam": "away",
            "FTHG": "home_goals",
            "FTAG": "away_goals",
        }
    )
    frame["date"] = pd.to_datetime(frame["date"], format="%d/%m/%Y")
    frame["home"] = _names(frame["home"])
    frame["away"] = _names(frame["away"])
    frame["home_goals"] = frame["home_goals"].astype("Int64")
    frame["away_goals"] = frame["away_goals"].astype("Int64")
    frame["competition"] = competition
    return frame[OUTPUT_COLUMNS]


def load_ucl_history(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, encoding="utf-8-sig")
    frame.columns = [str(column).strip() for column in frame.columns]
    frame = frame.rename(
        columns={
            "Date": "date",
            "Home Team": "home",
            "Away Team": "away",
            "Result": "result",
        }
    )
    frame["date"] = pd.to_datetime(frame["date"], format="%d/%m/%Y %H:%M")
    score = frame["result"].astype(str).str.extract(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
    frame["home_goals"] = pd.to_numeric(score[0], errors="coerce").astype("Int64")
    frame["away_goals"] = pd.to_numeric(score[1], errors="coerce").astype("Int64")
    bad = frame[["home_goals", "away_goals"]].isna().any(axis=1)
    if bad.any():
        raise SystemExit(f"{int(bad.sum())} hasil UCL tidak bisa dibaca di {path}")
    frame["home"] = _names(frame["home"])
    frame["away"] = _names(frame["away"])
    frame["competition"] = UCL_HISTORY
    return frame[OUTPUT_COLUMNS]


def load_ucl_teams(path: Path) -> list[str]:
    frame = pd.read_csv(path, encoding="utf-8-sig")
    teams = sorted(set(_names(frame["team_name"])))
    if len(teams) != UCL_TEAM_COUNT:
        raise SystemExit(
            f"Daftar tim UCL berisi {len(teams)} klub, seharusnya {UCL_TEAM_COUNT}"
        )
    return teams


def build_ucl_schedule(teams: list[str], seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rounds = balance_home_games(circle_rounds(teams, len(UCL_MATCHDAYS)), rng)

    rows: list[dict[str, object]] = []
    for matchday, pairs in zip(UCL_MATCHDAYS, rounds):
        for home, away in pairs:
            rows.append(
                {
                    "date": pd.Timestamp(matchday),
                    "home": home,
                    "away": away,
                    "home_goals": pd.NA,
                    "away_goals": pd.NA,
                    "competition": "UCL",
                }
            )

    frame = pd.DataFrame(rows)
    frame["home_goals"] = frame["home_goals"].astype("Int64")
    frame["away_goals"] = frame["away_goals"].astype("Int64")
    return frame[OUTPUT_COLUMNS]


def build(data_dir: Path, seed: int) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for code, competition in LEAGUES.items():
        path = data_dir / f"{code}.csv"
        if not path.exists():
            raise SystemExit(f"File liga tidak ditemukan: {path}")
        frames.append(load_league(path, competition))

    history_path = data_dir / UCL_HISTORY_FILE
    teams_path = data_dir / UCL_TEAMS_FILE
    if not history_path.exists():
        raise SystemExit(f"File histori UCL tidak ditemukan: {history_path}")
    if not teams_path.exists():
        raise SystemExit(f"Daftar tim UCL tidak ditemukan: {teams_path}")

    frames.append(load_ucl_history(history_path))
    frames.append(build_ucl_schedule(load_ucl_teams(teams_path), seed))

    matches = pd.concat(frames, ignore_index=True)
    return matches.sort_values(
        ["date", "competition", "home"], ignore_index=True
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data", help="Folder dataset")
    parser.add_argument("--out", default="data/matches.csv", help="Output CSV")
    parser.add_argument("--seed", type=int, default=20262027, help="Seed jadwal UCL")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out = Path(args.out)
    backup = data_dir / "matches_sample.csv"

    if out.exists() and not backup.exists():
        shutil.copy2(out, backup)
        print(f"Menyimpan dataset contoh ke {backup}")

    matches = validate_matches(build(data_dir, args.seed))

    out.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(out, index=False, na_rep="")

    summary = dataset_summary(matches)
    print(f"Wrote {len(matches)} matches to {out}")
    print(
        f"  domestik: {summary['domestic']} | UCL 2026/27: {summary['ucl']} "
        f"({summary['ucl_played']} dimainkan, {summary['ucl_remaining']} sisa) "
        f"| histori UCL: {summary['ucl_history']}"
    )
    print(
        f"  tim UCL: {summary['teams']} | liga domestik: {summary['competitions']} "
        f"| laga dimainkan: {summary['played']}"
    )
    print(f"  data terakhir: {summary['last_played']}")

    domestic = matches[matches["competition"].isin(LEAGUES.values())]
    appearances = pd.concat([domestic["home"], domestic["away"]]).value_counts()
    ucl = matches[matches["competition"].eq("UCL")]
    ucl_teams = sorted(set(ucl["home"]) | set(ucl["away"]))
    without_domestic = [team for team in ucl_teams if appearances.get(team, 0) == 0]
    if without_domestic:
        print(f"  tanpa data domestik ({len(without_domestic)}): "
              + ", ".join(without_domestic))

    played_teams = set(
        matches.dropna(subset=["home_goals", "away_goals"])["home"]
    ) | set(matches.dropna(subset=["home_goals", "away_goals"])["away"])
    without_any = [team for team in ucl_teams if team not in played_teams]
    if without_any:
        print(
            f"  tanpa satu pun laga ({len(without_any)}): "
            + ", ".join(without_any)
            + " - rating memakai shrinkage"
        )


if __name__ == "__main__":
    main()
